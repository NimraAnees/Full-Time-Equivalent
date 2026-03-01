#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Simple polling version for Windows.

Watches the Inbox folder and creates action files when new files appear.

Usage:
    python filesystem_watcher.py AI_Employee_Vault
"""

import sys
import hashlib
import time
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class FilesystemWatcher:
    """
    Simple polling-based filesystem watcher.
    
    Checks the Inbox folder every second for new files.
    """
    
    def __init__(self, vault_path: str):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logger = logging.getLogger('FilesystemWatcher')
        
        # Ensure folders exist
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        # Track processed files
        self.processed_files = set()
        
        self.logger.info(f'Watching folder: {self.inbox}')
    
    def _calculate_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file."""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f'Error hashing {filepath.name}: {e}')
            return str(time.time())
    
    def _format_size(self, size: int) -> str:
        """Format file size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def create_action_file(self, filepath: Path) -> Path:
        """Create action file for dropped file."""
        stat = filepath.stat()
        file_size = stat.st_size
        created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
        
        content = f'''---
type: file_drop
original_name: {filepath.name}
size: {file_size}
received: {created_time}
status: pending
---

# File Dropped for Processing

**Original File:** `{filepath.name}`

**Size:** {self._format_size(file_size)}

**Received:** {created_time}

---

## Suggested Actions

- [ ] Review file contents
- [ ] Categorize the file
- [ ] Take necessary action
- [ ] Move to appropriate folder

---

## Processing Notes

<!-- Add your notes here -->

'''
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = filepath.stem.replace(' ', '_')[:30]
        action_filename = f'FILE_DROP_{safe_name}_{timestamp}.md'
        
        action_file = self.needs_action / action_filename
        action_file.write_text(content, encoding='utf-8')
        
        return action_file
    
    def check_inbox(self):
        """Check inbox for new files."""
        try:
            files = [f for f in self.inbox.iterdir() if f.is_file() and not f.name.startswith('.')]
            
            for filepath in files:
                file_hash = self._calculate_hash(filepath)
                
                if file_hash in self.processed_files:
                    continue
                
                self.logger.info(f'New file detected: {filepath.name}')
                
                # Create action file
                action_file = self.create_action_file(filepath)
                self.logger.info(f'Created: {action_file.name}')
                
                # Mark as processed
                self.processed_files.add(file_hash)
                
        except Exception as e:
            self.logger.error(f'Error checking inbox: {e}')
    
    def run(self):
        """Main run loop."""
        self.logger.info('Starting FilesystemWatcher')
        self.logger.info(f'Inbox folder: {self.inbox}')
        self.logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                self.check_inbox()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Stopping...')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python filesystem_watcher.py <vault_path>")
        print("Example: python filesystem_watcher.py AI_Employee_Vault")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    
    if not Path(vault_path).exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    watcher = FilesystemWatcher(vault_path)
    watcher.run()
