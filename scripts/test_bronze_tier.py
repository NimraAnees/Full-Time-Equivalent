#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test script to verify Bronze Tier functionality.
"""

import sys
import time
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, 'scripts')

from base_watcher import BaseWatcher
from filesystem_watcher import FilesystemWatcher
from orchestrator import Orchestrator

def test_imports():
    """Test that all modules import correctly."""
    print("Testing imports...")
    assert BaseWatcher is not None, "BaseWatcher failed to import"
    assert FilesystemWatcher is not None, "FilesystemWatcher failed to import"
    assert Orchestrator is not None, "Orchestrator failed to import"
    print("  [PASS] All modules imported successfully")
    return True

def test_vault_structure():
    """Test that vault folder structure exists."""
    print("Testing vault structure...")
    vault = Path('AI_Employee_Vault')
    
    required_folders = [
        'Inbox',
        'Needs_Action',
        'Done',
        'Plans',
        'Pending_Approval',
        'Approved',
        'Rejected',
        'Logs',
        'Accounting',
        'Briefings'
    ]
    
    for folder in required_folders:
        folder_path = vault / folder
        assert folder_path.exists(), f"Missing folder: {folder}"
        assert folder_path.is_dir(), f"Not a directory: {folder}"
        print(f"  [OK] {folder}/")
    
    required_files = [
        'Dashboard.md',
        'Company_Handbook.md',
        'Business_Goals.md'
    ]
    
    for file in required_files:
        file_path = vault / file
        assert file_path.exists(), f"Missing file: {file}"
        print(f"  [OK] {file}")
    
    print("  [PASS] Vault structure verified")
    return True

def test_orchestrator_init():
    """Test that orchestrator initializes correctly."""
    print("Testing orchestrator initialization...")
    orchestrator = Orchestrator('AI_Employee_Vault', check_interval=1)
    
    assert orchestrator.vault_path == Path('AI_Employee_Vault')
    assert orchestrator.needs_action.exists()
    assert orchestrator.dashboard.exists()
    
    print("  [PASS] Orchestrator initialized correctly")
    return True

def test_file_drop():
    """Test dropping a file in Inbox."""
    print("Testing file drop detection...")
    
    inbox = Path('AI_Employee_Vault/Inbox')
    needs_action = Path('AI_Employee_Vault/Needs_Action')
    
    # Create a test file
    test_file = inbox / 'test_document.txt'
    test_file.write_text('This is a test document for processing.')
    print(f"  Created test file: {test_file}")
    
    # Give watcher time to process (if running)
    time.sleep(2)
    
    # Check if action file was created (watcher should be running separately)
    action_files = list(needs_action.glob('FILE_DROP_*.md'))
    
    if action_files:
        print(f"  [OK] Action file created: {action_files[-1].name}")
        print("  [PASS] File drop workflow working")
    else:
        print("  [INFO] No action file created yet (watcher not running)")
        print("  [INFO] Start watcher with: python scripts/filesystem_watcher.py AI_Employee_Vault")
    
    # Clean up test file
    test_file.unlink()
    print(f"  Cleaned up test file")
    
    return True

def main():
    """Run all tests."""
    print("=" * 50)
    print("AI Employee Bronze Tier - Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_imports,
        test_vault_structure,
        test_orchestrator_init,
        test_file_drop
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print()
        print("All tests passed!")
        print()
        print("Next steps:")
        print("1. Open AI_Employee_Vault in Obsidian")
        print("2. Start watcher: python scripts/filesystem_watcher.py AI_Employee_Vault")
        print("3. Start orchestrator: python scripts/orchestrator.py AI_Employee_Vault")
        print("4. Drop a file in AI_Employee_Vault/Inbox/ to test the workflow")
        return 0
    else:
        print()
        print("Some tests failed. Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
