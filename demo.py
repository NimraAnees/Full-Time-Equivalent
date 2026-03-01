#!/usr/bin/env python3
"""
Quick demo - Run this and drop a file in Inbox to see it work!
"""
import sys
import time
import threading
from pathlib import Path

sys.path.insert(0, 'scripts')

from filesystem_watcher import FilesystemWatcher
from orchestrator import Orchestrator

def main():
    vault_path = 'AI_Employee_Vault'
    
    print("=" * 60)
    print("AI Employee Bronze Tier - Live Demo")
    print("=" * 60)
    print()
    print(f"Watching: {Path(vault_path).absolute()}")
    print()
    print("INSTRUCTIONS:")
    print("1. Drop any file in: AI_Employee_Vault/Inbox/")
    print("2. Watcher will create an action file in Needs_Action/")
    print("3. Press Ctrl+C to stop")
    print()
    
    # Start watcher in a thread
    watcher = FilesystemWatcher(vault_path)
    watcher_thread = threading.Thread(target=watcher.run, daemon=True)
    watcher_thread.start()
    
    # Wait for keyboard interrupt
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping...")

if __name__ == '__main__':
    main()
