# AI Employee - Bronze Tier

> **Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.**

This is a **Personal AI Employee** implementation using Qwen Code and Obsidian. The Bronze Tier provides the foundational layer for autonomous task processing.

## What This Does

The AI Employee:
- **Watches** for new files dropped in the Inbox folder
- **Creates action items** automatically in Needs_Action
- **Triggers Qwen Code** to process pending items
- **Manages approvals** for sensitive actions
- **Logs everything** for audit purposes
- **Updates Dashboard.md** with real-time status

## Quick Start (Windows)

### Option 1: Double-click to Start

1. **Start the system:** Double-click `start.bat`
   - Opens two terminal windows automatically
   - Window 1: Filesystem Watcher
   - Window 2: Orchestrator

2. **Test it:** Drop any file in `AI_Employee_Vault\Inbox\`
   - Watcher creates an action file in `Needs_Action\`
   - Orchestrator triggers Claude to process it

3. **Stop the system:** Double-click `stop.bat`

### Option 2: Manual Commands

**Terminal 1 - Start Watcher:**
```bash
cd "C:\Users\T L S\Documents\bronze\Full-Time-Equivalent"
python scripts/filesystem_watcher.py AI_Employee_Vault
```

**Terminal 2 - Start Orchestrator:**
```bash
cd "C:\Users\T L S\Documents\bronze\Full-Time-Equivalent"
python scripts/orchestrator.py AI_Employee_Vault
```

**Stop:** Press `Ctrl+C` in each terminal

---

## Project Structure

```
Full-Time-Equivalent/
├── AI_Employee_Vault/       # Obsidian vault (your data)
│   ├── Dashboard.md         # Real-time status dashboard
│   ├── Company_Handbook.md  # Rules of engagement
│   ├── Business_Goals.md    # Your objectives
│   ├── Inbox/               # Drop zone for files
│   ├── Needs_Action/        # Items requiring AI attention
│   ├── Plans/               # AI-generated plans
│   ├── Pending_Approval/    # Awaiting your decision
│   ├── Approved/            # Approved actions
│   ├── Rejected/            # Declined actions
│   ├── Done/                # Completed items
│   ├── Logs/                # Audit logs
│   ├── Accounting/          # Financial records
│   └── Briefings/           # CEO briefings
│
├── scripts/
│   ├── base_watcher.py      # Base class for watchers
│   ├── filesystem_watcher.py # File system watcher
│   ├── orchestrator.py      # Main orchestrator
│   └── requirements.txt     # Python dependencies
│
├── start.bat                # Start both services
├── stop.bat                 # Stop both services
└── README.md                # This file
```

---

## How It Works

### Workflow Example

**Step 1: You drop a file**
```
Copy: invoice.pdf → AI_Employee_Vault\Inbox\
```

**Step 2: Watcher detects and creates action file**
```
Filesystem Watcher sees: invoice.pdf
Creates: Needs_Action\FILE_DROP_invoice_20260301_120000.md
```

**Step 3: Orchestrator triggers Qwen**
```
Orchestrator detects: 1 item in Needs_Action\
Creates: _QWEN_INSTRUCTION.md
Triggers: qwen (in vault directory)
```

**Step 4: Qwen processes the file**
```
Qwen reads:
  - Needs_Action\FILE_DROP_*.md
  - Company_Handbook.md (for rules)
  - Business_Goals.md (for context)

Qwen creates:
  - Plans\PLAN_process_file.md
  - Updates Dashboard.md
```

**Step 5: Qwen moves to Done**
```
Moves: Needs_Action\FILE_DROP_*.md → Done\
Updates: Dashboard.md with activity
Logs: Logs\2026-03-01.json
```

---

## Installation

### Prerequisites

1. **Python 3.13+** - [Download](https://www.python.org/downloads/)
2. **Qwen Code** - Run manually when `_QWEN_INSTRUCTION.md` appears
3. **Obsidian** (optional) - [Download](https://obsidian.md/download)

### Setup

```bash
# Install Python dependencies
cd "C:\Users\T L S\Documents\bronze\Full-Time-Equivalent"
pip install -r scripts/requirements.txt
```

### How It Works

1. **Start the services** (watcher + orchestrator)
2. **Drop a file** in `AI_Employee_Vault\Inbox\`
3. **Orchestrator creates** `_QWEN_INSTRUCTION.md`
4. **Run Qwen Code** manually:
   ```bash
   cd AI_Employee_Vault
   qwen
   ```
5. **Qwen processes** the instruction and handles items in `Needs_Action/`

---

## Configuration

### Watcher Settings

Edit `scripts/filesystem_watcher.py`:
```python
# Change check interval (default: 1 second)
time.sleep(1)  # in run() method
```

### Orchestrator Settings

Edit `scripts/orchestrator.py`:
```python
# Change check interval (default: 60 seconds)
check_interval = 60  # in __init__
```

---

## Bronze Tier Deliverables

**Completed:**
- [x] Obsidian vault with Dashboard.md, Company_Handbook.md, Business_Goals.md
- [x] Filesystem Watcher script (monitors drop folder)
- [x] Orchestrator script (triggers Claude, manages workflow)
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] Logging system for audit trails
- [x] UTF-8 encoding support for Windows

**Next Tier (Silver):**
- [ ] Gmail Watcher integration
- [ ] WhatsApp Watcher integration
- [ ] MCP server for sending emails
- [ ] Human-in-the-loop approval workflow execution
- [ ] Scheduled operations (cron/Task Scheduler)

---

## Troubleshooting

### Qwen Code not running
```bash
# When _QWEN_INSTRUCTION.md appears, run:
cd AI_Employee_Vault
qwen
```

### Watcher not detecting files
- Ensure the Inbox folder exists
- Check file permissions
- Verify Python is running: `tasklist | findstr python`

### Orchestrator not creating _QWEN_INSTRUCTION.md
- Check logs in `Logs\` folder for errors
- Ensure vault path is correct
- Orchestrator checks every 60 seconds by default

### Encoding errors on Windows
- All files now use UTF-8 encoding explicitly
- If you see encoding errors, re-save files as UTF-8

---

## Usage Examples

### Example 1: Process an Invoice

1. Save invoice PDF to `AI_Employee_Vault\Inbox\invoice_march.pdf`
2. Watcher creates action file in `Needs_Action\`
3. Qwen reads invoice, categorizes expense
4. Updates `Accounting\Current_Month.md`
5. Moves to `Done\` when complete

### Example 2: Request Approval

1. Qwen detects a payment > $500
2. Creates approval request in `Pending_Approval\`
3. You review and move to `Approved\`
4. Orchestrator logs the approval
5. Action is executed (or queued)

---

## Security Notes

- **Never commit** `.env` files with credentials
- **Never store** API keys in vault files
- **Always review** approval requests before approving
- **Regular audit** of `Logs\` folder recommended

---

## Support

- **Documentation:** See `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Weekly Meeting:** Wednesdays 10:00 PM on Zoom
- **YouTube:** [Panaversity Channel](https://www.youtube.com/@panaversity)

---

*Built with ❤️ by the Panaversity Community*
*Version: 0.1 (Bronze Tier) - Tested on Windows*
