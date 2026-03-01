# Full-Time-Equivalent (FTE) Project

## Project Overview

This is a **Personal AI Employee Hackathon** project focused on building autonomous "Digital FTEs" (Full-Time Equivalents) — AI agents that work 24/7 to manage personal and business affairs. The project uses a local-first, agent-driven architecture with human-in-the-loop oversight.

**Core Concept:** Transform Claude Code from a reactive chatbot into a proactive business partner that autonomously handles email, WhatsApp, banking, social media, and task management.

**Key Innovation:** The "Monday Morning CEO Briefing" — where the AI audits bank transactions and tasks to report revenue and bottlenecks without being asked.

## Architecture

### The Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **The Brain** | Claude Code | Reasoning engine with Ralph Wiggum persistence loop |
| **The Memory/GUI** | Obsidian (Markdown) | Local dashboard and knowledge base |
| **The Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems |
| **The Hands** | MCP Servers | Model Context Protocol for external actions |
| **Browser Automation** | Playwright MCP | Web interaction and form filling |

### Core Patterns

1. **Watcher Architecture:** Lightweight Python scripts run continuously, monitoring inputs and creating `.md` files in `/Needs_Action` folders
2. **Ralph Wiggum Loop:** A Stop hook pattern that keeps Claude iterating until multi-step tasks are complete
3. **Human-in-the-Loop:** Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
4. **File-Based Orchestration:** Agents communicate by writing/reading Markdown files (vault sync compatible)

## Directory Structure

```
Full-Time-Equivalent/
├── .qwen/skills/           # Qwen skill configurations
│   └── browsing-with-playwright/
│       ├── SKILL.md        # Skill documentation
│       ├── references/     # Tool reference docs
│       └── scripts/        # MCP client and server helpers
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main blueprint
├── skills-lock.json        # Skill version tracking
└── QWEN.md                 # This file
```

## Available Skills

### browsing-with-playwright

Browser automation via Playwright MCP server for web scraping, form submission, and UI testing.

**Server Management:**
```bash
# Start server (keeps browser context alive)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Stop server (closes browser cleanly)
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh

# Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

**Key Tools Available:**
- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Capture accessibility snapshot (preferred over screenshots)
- `browser_click`, `browser_type`, `browser_fill_form` - Element interaction
- `browser_evaluate` - Execute JavaScript
- `browser_run_code` - Run multi-step Playwright code
- `browser_take_screenshot` - Capture screenshots

**Example Usage:**
```bash
# Call a tool via MCP client
python .qwen/skills/browsing-with-playwright/scripts/mcp-client.py call \
  -u http://localhost:8808 \
  -t browser_navigate \
  -p '{"url": "https://example.com"}'
```

See `.qwen/skills/browsing-with-playwright/` for complete documentation.

## Hackathon Tiers

### Bronze Tier (Foundation)
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script
- Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`

### Silver Tier (Functional Assistant)
- Multiple Watcher scripts (Gmail + WhatsApp + LinkedIn)
- Automated LinkedIn posting
- MCP server for external actions
- Human-in-the-loop approval workflow

### Gold Tier (Autonomous Employee)
- Full cross-domain integration
- Odoo accounting integration via MCP
- Facebook/Instagram/Twitter integration
- Weekly Business Audit with CEO Briefing
- Ralph Wiggum loop for autonomous completion

### Platinum Tier (Production)
- Cloud deployment (24/7 always-on)
- Work-Zone specialization (Cloud drafts, Local approves)
- Delegated sync via Git/Syncthing
- Odoo on Cloud VM with HTTPS

## Key Templates

### Watcher Script Pattern

```python
from base_watcher import BaseWatcher

class MyWatcher(BaseWatcher):
    def check_for_updates(self) -> list:
        # Return list of new items to process
        pass

    def create_action_file(self, item) -> Path:
        # Create .md file in Needs_Action folder
        pass
```

### Approval Request Template

```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
status: pending
---

## Payment Details
- Amount: $500.00
- To: Client A

## To Approve
Move this file to /Approved folder.
```

## Development Practices

- **Local-First:** All data stored locally in Obsidian vault (Markdown)
- **Privacy:** Secrets never sync (`.env`, tokens, banking credentials excluded)
- **Audit Logging:** All actions logged to Markdown files for traceability
- **Graceful Degradation:** Error recovery built into watchers

## Resources

- **Main Blueprint:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Ralph Wiggum Pattern:** [GitHub Reference](https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum)
- **MCP Servers:** [Model Context Protocol Docs](https://platform.claude.com/docs/en/agents-and-tools/mcp)
- **Agent Skills:** [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Weekly Research Meeting

- **When:** Wednesdays at 10:00 PM
- **Zoom:** [Join Meeting](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- **YouTube:** [Panaversity Channel](https://www.youtube.com/@panaversity)
