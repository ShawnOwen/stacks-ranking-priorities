# Comet Skills Catalog

This catalog summarizes the available Comet browser skills and comet-mcp tools extracted from the browser-orchestration runtime catalog. Entries are sorted alphabetically by Skill ID and include a concise suggested use case for routing future Comet work.

| Skill ID | Type | Description | Suggested Use Case |
| --- | --- | --- | --- |
| `15-comet-review` | Comet skill | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. |
| `15.1-comet-pr-review` | Comet skill | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. |
| `comet-agent` | Comet skill | General Comet Browser agentic browsing skill | General Comet Browser agentic browsing skill |
| `comet-assistant` | Comet skill | Sidecar interactions with active pages | Sidecar interactions with active pages |
| `comet-auto` | Comet skill | Full browser automation orchestrator - combine browse, scrape, interact, and network capabilities into multi-step workflows with the Comet b | Full browser automation orchestrator - combine browse, scrape, interact, and network capabilities into multi-step workflows with the Comet b |
| `comet-browse` | Comet skill | Browse a URL using Comet browser in an isolated tab group on the top display. Opens a new session, navigates to the URL, and reports what it | Browse a URL using Comet browser in an isolated tab group on the top display. Opens a new session, navigates to the URL, and reports what it |
| `comet-browser` | Comet skill | Core Comet Browser automation skill — CDP connection management, Perplexity AI integration, page interaction patterns, screenshot capture, a | Core Comet Browser automation skill — CDP connection management, Perplexity AI integration, page interaction patterns, screenshot capture, a |
| `comet-browser-control-toolkit` | Comet skill | Master routing skill for the complete Perplexity Comet Browser Control Toolkit in Codex. Use for any Comet browser automation, Perplexity br | Master routing skill for the complete Perplexity Comet Browser Control Toolkit in Codex. Use for any Comet browser automation, Perplexity br |
| `comet-connect` | Comet skill | Initialize an isolated Comet browser session with its own tab group on the top display. Use before any browser work. Accepts optional agent | Initialize an isolated Comet browser session with its own tab group on the top display. Use before any browser work. Accepts optional agent |
| `comet-delegate` | Comet skill | Delegate a browser task to the Comet orchestration system. Creates an isolated tab group, registers lifecycle tracking, and dispatches the t | Delegate a browser task to the Comet orchestration system. Creates an isolated tab group, registers lifecycle tracking, and dispatches the t |
| `comet-dispatch` | Comet skill | Route Comet browser task dispatch, Query Shortcut planning, sidecar instructions, and multi-agent browser work coordination through the Come | Route Comet browser task dispatch, Query Shortcut planning, sidecar instructions, and multi-agent browser work coordination through the Come |
| `comet-interact` | Comet skill | Interact with web pages - fill forms, click buttons, type text, navigate, scroll, upload files, and perform multi-step browser automation wo | Interact with web pages - fill forms, click buttons, type text, navigate, scroll, upload files, and perform multi-step browser automation wo |
| `comet-keepalive` | Comet skill | Prevent browser session timeouts during Comet automation. Monitors authenticated sessions and sends periodic activity to keep them alive. | Prevent browser session timeouts during Comet automation. Monitors authenticated sessions and sends periodic activity to keep them alive. |
| `comet-labs` | Comet skill | Analytics, visualizations, and coding in Comet browser | Analytics, visualizations, and coding in Comet browser |
| `comet-monitor` | Comet skill | Monitor web pages for changes - detect content updates, capture diffs, send macOS notifications, with continuous or one-shot modes. | Monitor web pages for changes - detect content updates, capture diffs, send macOS notifications, with continuous or one-shot modes. |
| `comet-network` | Comet skill | Capture and analyze network traffic - HAR files, API responses, request interception, URL blocking, response mocking. | Capture and analyze network traffic - HAR files, API responses, request interception, URL blocking, response mocking. |
| `comet-orphan-tab-management` | Comet skill | Manage orphaned browser tabs in Comet Browser — scan for ungrouped tabs, analyze their context (draft messages, page content), and move them | Manage orphaned browser tabs in Comet Browser — scan for ungrouped tabs, analyze their context (draft messages, page content), and move them |
| `comet-pdf` | Comet skill | Generate PDFs from web pages with customizable format, margins, headers, footers, and print-optimized rendering. | Generate PDFs from web pages with customizable format, margins, headers, footers, and print-optimized rendering. |
| `comet-read` | Comet skill | Extract content from a URL as clean text or accessibility tree through a visible top-display windowed full-display Comet session. Opens the | Extract content from a URL as clean text or accessibility tree through a visible top-display windowed full-display Comet session. Opens the |
| `comet-research` | Comet skill | Deep research using Comet/Perplexity AI research mode. Asks Perplexity in research mode for comprehensive analysis with sources. Use for inv | Deep research using Comet/Perplexity AI research mode. Asks Perplexity in research mode for comprehensive analysis with sources. Use for inv |
| `comet-scrape` | Comet skill | Extract structured data from web pages - tables, JSON-LD, lists, specific elements by CSS selector, with auto-scroll for lazy-loaded content | Extract structured data from web pages - tables, JSON-LD, lists, specific elements by CSS selector, with auto-scroll for lazy-loaded content |
| `comet-screenshot` | Comet skill | Advanced screenshot capture - full page, element-specific, multiple viewports, dark mode, clipping regions, and element hiding. | Advanced screenshot capture - full page, element-specific, multiple viewports, dark mode, clipping regions, and element hiding. |
| `comet-search` | Comet skill | Basic web search mode | Basic web search mode |
| `comet-session` | Comet skill | Manage Comet browser CDP sessions - check status, list pages, diagnose issues. For starting browser work, prefer /comet-connect which create | Manage Comet browser CDP sessions - check status, list pages, diagnose issues. For starting browser work, prefer /comet-connect which create |
| `comet-shortcuts` | Comet skill | Manage and execute Comet shortcuts | Manage and execute Comet shortcuts |
| `comet-skill-inventory` | Comet skill | Perplexity Comet browser skill inventory registry. Use when routing Comet browser work, selecting browser automation skills, checking availa | Perplexity Comet browser skill inventory registry. Use when routing Comet browser work, selecting browser automation skills, checking availa |
| `comet-task-threads` | Comet skill | Inventory, map, and reason about Comet browser task threads, tab groups, active browser sessions, ownership, group status, and workspace rou | Inventory, map, and reason about Comet browser task threads, tab groups, active browser sessions, ownership, group status, and workspace rou |
| `comet-workflows` | Comet skill | Browser workflow reproducibility and documentation skill for Comet Browser Control. Use when asked to document, replay, reproduce, audit, or | Browser workflow reproducibility and documentation skill for Comet Browser Control. Use when asked to document, replay, reproduce, audit, or |
| `comet-workspace` | Comet skill | Organize tabs into intelligent workspaces | Organize tabs into intelligent workspaces |
| `comet_ask` | comet-mcp tool | Send a prompt to Perplexity inside Comet and start waiting for a response. | Send a prompt to Perplexity inside Comet and start waiting for a response. |
| `comet_automate` | comet-mcp tool | Combine browse + scrape + interact + network into a multi-step end-to-end workflow. | Combine browse + scrape + interact + network into a multi-step end-to-end workflow. |
| `comet_connect` | comet-mcp tool | Open or reuse a Comet session bound to this caller; required before any other comet_* call. | Open or reuse a Comet session bound to this caller; required before any other comet_* call. |
| `comet_delegate` | comet-mcp tool | Hand a browser task to another bound agent / tab group via the orchestrator. | Hand a browser task to another bound agent / tab group via the orchestrator. |
| `comet_domain` | comet-mcp tool | Cross-tab/session domain helpers (e.g. open QBO, Mercury, GitHub, Google Workspace, SALT Tax with auth checks). | Cross-tab/session domain helpers (e.g. open QBO, Mercury, GitHub, Google Workspace, SALT Tax with auth checks). |
| `comet_interact` | comet-mcp tool | Fill forms, click, type, scroll, navigate, upload — multi-step page interaction. | Fill forms, click, type, scroll, navigate, upload — multi-step page interaction. |
| `comet_lifecycle_abort` | comet-mcp tool | Abort the bound browser task lifecycle (e.g. user cancelled). | Abort the bound browser task lifecycle (e.g. user cancelled). |
| `comet_lifecycle_complete` | comet-mcp tool | Mark the bound browser task lifecycle complete + record outcome. | Mark the bound browser task lifecycle complete + record outcome. |
| `comet_lifecycle_start` | comet-mcp tool | Mark the start of a tracked browser task lifecycle bound to this caller. | Mark the start of a tracked browser task lifecycle bound to this caller. |
| `comet_lifecycle_update` | comet-mcp tool | Push a status update into the bound browser task lifecycle. | Push a status update into the bound browser task lifecycle. |
| `comet_mode` | comet-mcp tool | Switch the Comet/Perplexity surface between search, research, labs, and agentic modes. | Switch the Comet/Perplexity surface between search, research, labs, and agentic modes. |
| `comet_navigate` | comet-mcp tool | Navigate the current Comet tab to a URL (back/forward/reload variants). | Navigate the current Comet tab to a URL (back/forward/reload variants). |
| `comet_network` | comet-mcp tool | Capture / analyze network traffic — HAR, API responses, request interception, URL blocking, mocking. | Capture / analyze network traffic — HAR, API responses, request interception, URL blocking, mocking. |
| `comet_observe` | comet-mcp tool | Attach a passive observer to a tab/group (read-only event stream). | Attach a passive observer to a tab/group (read-only event stream). |
| `comet_pdf` | comet-mcp tool | Render the active page to PDF with margin / header / footer / print options. | Render the active page to PDF with margin / header / footer / print options. |
| `comet_peek` | comet-mcp tool | Read another agent's tab/group state without taking ownership (requires authorization). | Read another agent's tab/group state without taking ownership (requires authorization). |
| `comet_poll` | comet-mcp tool | Check whether the last Perplexity ask has finished and return its result. | Check whether the last Perplexity ask has finished and return its result. |
| `comet_read_page` | comet-mcp tool | Extract clean text / accessibility-tree content from the current tab — no UI interaction. | Extract clean text / accessibility-tree content from the current tab — no UI interaction. |
| `comet_scrape` | comet-mcp tool | Structured extraction (tables, JSON-LD, lists, CSS selectors) with auto-scroll for lazy content. | Structured extraction (tables, JSON-LD, lists, CSS selectors) with auto-scroll for lazy content. |
| `comet_screenshot` | comet-mcp tool | Capture a screenshot of the active Comet tab (full page, element, viewport options). | Capture a screenshot of the active Comet tab (full page, element, viewport options). |
| `comet_shortcut` | comet-mcp tool | Execute a configured Comet keyboard shortcut by name. | Execute a configured Comet keyboard shortcut by name. |
| `comet_stop` | comet-mcp tool | Cancel an in-flight Perplexity ask without closing the session. | Cancel an in-flight Perplexity ask without closing the session. |
| `comet_tab_groups` | comet-mcp tool | Create, update, list, archive, or restore Chromium tab groups in Comet (title, color, collapsed). | Create, update, list, archive, or restore Chromium tab groups in Comet (title, color, collapsed). |
| `comet_task_status` | comet-mcp tool | Read the current status of one or more tracked browser tasks. | Read the current status of one or more tracked browser tasks. |
| `comet_wait_for_idle` | comet-mcp tool | Block until the active tab's network and DOM settle (used between interactions). | Block until the active tab's network and DOM settle (used between interactions). |
| `spequa-15-1-comet-pr-review` | Comet skill | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. |
| `spequa-15-comet-review` | Comet skill | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. |

## Recommended Comet Tool

```json
{
  "recommended_comet_tool": {
    "justification": "No extracted skill descriptions contained primary/default; selected the first catalog entry alphabetically by Skill ID.",
    "primary": "15-comet-review",
    "selection_method": "alphabetical_by_skill_id"
  }
}
```
