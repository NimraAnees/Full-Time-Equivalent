#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator - Master process for AI Employee.

The orchestrator:
1. Monitors the Needs_Action folder for new items
2. Triggers Claude Code to process pending items
3. Manages the approval workflow
4. Updates the Dashboard.md with activity summaries
5. Logs all actions for audit purposes

Usage:
    python orchestrator.py /path/to/AI_Employee_Vault
"""

import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Coordinates between watchers, Claude Code, and human approval workflows.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: How often to check for work (in seconds)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.logger = logging.getLogger('Orchestrator')
        
        # Folder references
        self.needs_action = self.vault_path / 'Needs_Action'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.rejected = self.vault_path / 'Rejected'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure all folders exist
        for folder in [self.needs_action, self.plans, self.pending_approval, 
                       self.approved, self.rejected, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f'Orchestrator initialized for vault: {self.vault_path}')
    
    def get_pending_items(self) -> List[Path]:
        """Get all .md files in Needs_Action folder."""
        if not self.needs_action.exists():
            return []
        return sorted(self.needs_action.glob('*.md'))
    
    def get_approved_items(self) -> List[Path]:
        """Get all .md files in Approved folder."""
        if not self.approved.exists():
            return []
        return sorted(self.approved.glob('*.md'))
    
    def log_action(self, action_type: str, details: dict, status: str = 'success'):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action (e.g., 'file_processed', 'approval_requested')
            details: Dictionary of action details
            status: success, error, pending, etc.
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'orchestrator',
            'status': status,
            **details
        }
        
        # Read existing logs or create new
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except json.JSONDecodeError:
                logs = []
        else:
            logs = []
        
        logs.append(log_entry)
        log_file.write_text(json.dumps(logs, indent=2))
        self.logger.info(f'Logged action: {action_type} - {status}')
    
    def update_dashboard(self, needs_action_count: int, pending_approval_count: int, 
                         completed_today: int):
        """
        Update the Dashboard.md with current status.
        
        Args:
            needs_action_count: Number of items in Needs_Action
            pending_approval_count: Number of items pending approval
            completed_today: Number of items completed today
        """
        if not self.dashboard.exists():
            self.logger.warning('Dashboard.md not found')
            return

        # Use UTF-8 encoding to handle emoji characters on Windows
        content = self.dashboard.read_text(encoding='utf-8')

        # Update timestamp
        content = content.replace(
            'last_updated: 2026-03-01T00:00:00Z',
            f'last_updated: {datetime.now().isoformat()}Z'
        )

        # Update status table
        old_status = '| **Needs Action** | 0 items |'
        new_status = f'| **Needs Action** | {needs_action_count} items |'
        content = content.replace(old_status, new_status)

        old_pending = '| **Pending Approval** | 0 items |'
        new_pending = f'| **Pending Approval** | {pending_approval_count} items |'
        content = content.replace(old_pending, new_pending)

        old_completed = '| **Completed Today** | 0 tasks |'
        new_completed = f'| **Completed Today** | {completed_today} tasks |'
        content = content.replace(old_completed, new_completed)

        self.dashboard.write_text(content, encoding='utf-8')
        self.logger.debug('Dashboard updated')
    
    def trigger_qwen(self, prompt: str) -> bool:
        """
        Trigger Qwen Code to process a prompt.
        
        Creates _QWEN_INSTRUCTION.md file for manual Qwen Code execution.

        Args:
            prompt: The prompt to send to Qwen

        Returns:
            True if instruction file was created successfully
        """
        try:
            # For Bronze tier, we create a state file for Qwen to process
            # The user will run 'qwen' manually in the vault directory

            self.logger.info('Creating Qwen Code instruction file...')
            self.logger.info(f'Prompt ready: {prompt[:50]}...')

            # Create a processing instruction file
            instruction_file = self.vault_path / '_QWEN_INSTRUCTION.md'
            instruction_file.write_text(f'''---
created: {datetime.now().isoformat()}
status: ready
---

# Qwen Code Instruction

{prompt}

---

## Next Steps

1. Read all files in `/Needs_Action/`
2. Review `Company_Handbook.md` for rules
3. Review `Business_Goals.md` for context
4. Create plans in `/Plans/`
5. Request approval for sensitive actions
6. Move completed items to `/Done/`

**To execute:** Run `qwen` in the vault directory and reference this file.
''')

            self.log_action('qwen_triggered', {'prompt': prompt[:200]}, 'success')
            self.logger.info(f'Created: {instruction_file.name}')
            return True

        except Exception as e:
            self.logger.error(f'Error creating instruction file: {e}')
            return False
    
    def process_needs_action(self):
        """Process all items in Needs_Action folder."""
        pending_items = self.get_pending_items()

        if not pending_items:
            self.logger.debug('No items in Needs_Action')
            return

        self.logger.info(f'Found {len(pending_items)} items to process')

        # Create summary of items
        item_names = [item.name for item in pending_items]
        prompt = f'''Process {len(pending_items)} pending item(s) in /Needs_Action/:

{chr(10).join(f'- {name}' for name in item_names)}

Follow the Company_Handbook.md rules and Business_Goals.md context.
For each item:
1. Read and understand the request
2. Create a plan in /Plans/
3. Take action or request approval
4. Move to /Done/ when complete'''

        self.trigger_qwen(prompt)
    
    def process_approved_items(self):
        """Process items that have been approved by human."""
        approved_items = self.get_approved_items()
        
        if not approved_items:
            return
        
        self.logger.info(f'Found {len(approved_items)} approved items to execute')
        
        for item in approved_items:
            # Read the approval file to understand what action to take
            content = item.read_text()
            
            # Log the approval execution
            self.log_action('execute_approved', {
                'file': item.name,
                'content_preview': content[:200]
            }, 'executed')
            
            # Move to Done after "execution"
            # In Bronze tier, we just log and move
            dest = self.done / item.name
            item.rename(dest)
            self.logger.info(f'Moved approved item to Done: {item.name}')
    
    def count_completed_today(self) -> int:
        """Count items completed today."""
        if not self.done.exists():
            return 0
        
        today = datetime.now().strftime('%Y-%m-%d')
        count = 0
        
        for item in self.done.glob('*.md'):
            # Try to read the file modification time
            try:
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if mtime.strftime('%Y-%m-%d') == today:
                    count += 1
            except Exception:
                pass
        
        return count
    
    def run(self):
        """Main orchestrator loop."""
        self.logger.info('Starting Orchestrator')
        self.logger.info(f'Check interval: {self.check_interval}s')
        
        try:
            while True:
                # Process pending items
                self.process_needs_action()
                
                # Process approved items
                self.process_approved_items()
                
                # Update dashboard
                needs_action_count = len(self.get_pending_items())
                pending_approval_count = len(list(self.pending_approval.glob('*.md')))
                completed_today = self.count_completed_today()
                
                self.update_dashboard(
                    needs_action_count,
                    pending_approval_count,
                    completed_today
                )
                
                # Wait for next cycle
                import time
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Orchestrator error: {e}', exc_info=True)
            raise


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <vault_path> [check_interval]")
        print("\nExample:")
        print("  python orchestrator.py /path/to/AI_Employee_Vault")
        print("  python orchestrator.py /path/to/AI_Employee_Vault 30")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    check_interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    # Validate vault path
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create and run orchestrator
    orchestrator = Orchestrator(vault_path, check_interval)
    orchestrator.run()


if __name__ == '__main__':
    main()
