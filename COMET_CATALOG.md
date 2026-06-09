# Comet Catalog

This document catalogs the Comet skills and comet-mcp tools extracted from the source Claude session transcript, then records the recommended primary tool selected by Task 1 for future reference.

Source transcript: `/Users/shawnowen/.claude/projects/-Users-shawnowen-dev-equa-tools-stacks-ranking-priorities/7d60ab60-7484-46a0-8428-d6b0a99d527c/subagents/workflows/wf_b8bed0a9-4f8/agent-aa77dfb78eb51c28f.jsonl`

## Catalog

Total entries: 56 (31 Comet skills, 25 MCP tools).

| Type | Name | Description |
|---|---|---|
| Comet skill | `15-comet-review` | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. |
| Comet skill | `15.1-comet-pr-review` | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. |
| Comet skill | `comet-agent` | General Comet Browser agentic browsing skill |
| Comet skill | `comet-assistant` | Sidecar interactions with active pages |
| Comet skill | `comet-auto` | Full browser automation orchestrator - combine browse, scrape, interact, and network capabilities into multi-step workflows with the Comet b |
| Comet skill | `comet-browse` | Browse a URL using Comet browser in an isolated tab group on the top display. Opens a new session, navigates to the URL, and reports what it |
| Comet skill | `comet-browser` | Core Comet Browser automation skill — CDP connection management, Perplexity AI integration, page interaction patterns, screenshot capture, a |
| Comet skill | `comet-browser-control-toolkit` | Master routing skill for the complete Perplexity Comet Browser Control Toolkit in Codex. Use for any Comet browser automation, Perplexity br |
| Comet skill | `comet-connect` | Initialize an isolated Comet browser session with its own tab group on the top display. Use before any browser work. Accepts optional agent |
| Comet skill | `comet-delegate` | Delegate a browser task to the Comet orchestration system. Creates an isolated tab group, registers lifecycle tracking, and dispatches the t |
| Comet skill | `comet-dispatch` | Route Comet browser task dispatch, Query Shortcut planning, sidecar instructions, and multi-agent browser work coordination through the Come |
| Comet skill | `comet-interact` | Interact with web pages - fill forms, click buttons, type text, navigate, scroll, upload files, and perform multi-step browser automation wo |
| Comet skill | `comet-keepalive` | Prevent browser session timeouts during Comet automation. Monitors authenticated sessions and sends periodic activity to keep them alive. |
| Comet skill | `comet-labs` | Analytics, visualizations, and coding in Comet browser |
| Comet skill | `comet-monitor` | Monitor web pages for changes - detect content updates, capture diffs, send macOS notifications, with continuous or one-shot modes. |
| Comet skill | `comet-network` | Capture and analyze network traffic - HAR files, API responses, request interception, URL blocking, response mocking. |
| Comet skill | `comet-orphan-tab-management` | Manage orphaned browser tabs in Comet Browser — scan for ungrouped tabs, analyze their context (draft messages, page content), and move them |
| Comet skill | `comet-pdf` | Generate PDFs from web pages with customizable format, margins, headers, footers, and print-optimized rendering. |
| Comet skill | `comet-read` | Extract content from a URL as clean text or accessibility tree through a visible top-display windowed full-display Comet session. Opens the |
| Comet skill | `comet-research` | Deep research using Comet/Perplexity AI research mode. Asks Perplexity in research mode for comprehensive analysis with sources. Use for inv |
| Comet skill | `comet-scrape` | Extract structured data from web pages - tables, JSON-LD, lists, specific elements by CSS selector, with auto-scroll for lazy-loaded content |
| Comet skill | `comet-screenshot` | Advanced screenshot capture - full page, element-specific, multiple viewports, dark mode, clipping regions, and element hiding. |
| Comet skill | `comet-search` | Basic web search mode |
| Comet skill | `comet-session` | Manage Comet browser CDP sessions - check status, list pages, diagnose issues. For starting browser work, prefer /comet-connect which create |
| Comet skill | `comet-shortcuts` | Manage and execute Comet shortcuts |
| Comet skill | `comet-skill-inventory` | Perplexity Comet browser skill inventory registry. Use when routing Comet browser work, selecting browser automation skills, checking availa |
| Comet skill | `comet-task-threads` | Inventory, map, and reason about Comet browser task threads, tab groups, active browser sessions, ownership, group status, and workspace rou |
| Comet skill | `comet-workflows` | Browser workflow reproducibility and documentation skill for Comet Browser Control. Use when asked to document, replay, reproduce, audit, or |
| Comet skill | `comet-workspace` | Organize tabs into intelligent workspaces |
| Comet skill | `spequa-15-1-comet-pr-review` | Use when the user asks to run the Spequa plugin command spequa:15.1-comet-pr-review or execute the full Comet PR review gates. |
| Comet skill | `spequa-15-comet-review` | Use when the user asks to run the Spequa plugin command spequa:15-comet-review or delegate a PR review to Comet. |
| MCP tool | `comet_connect` | Open or reuse a Comet session bound to this caller; required before any other comet_* call. |
| MCP tool | `comet_ask` | Send a prompt to Perplexity inside Comet and start waiting for a response. |
| MCP tool | `comet_poll` | Check whether the last Perplexity ask has finished and return its result. |
| MCP tool | `comet_stop` | Cancel an in-flight Perplexity ask without closing the session. |
| MCP tool | `comet_screenshot` | Capture a screenshot of the active Comet tab (full page, element, viewport options). |
| MCP tool | `comet_mode` | Switch the Comet/Perplexity surface between search, research, labs, and agentic modes. |
| MCP tool | `comet_tab_groups` | Create, update, list, archive, or restore Chromium tab groups in Comet (title, color, collapsed). |
| MCP tool | `comet_shortcut` | Execute a configured Comet keyboard shortcut by name. |
| MCP tool | `comet_read_page` | Extract clean text / accessibility-tree content from the current tab — no UI interaction. |
| MCP tool | `comet_interact` | Fill forms, click, type, scroll, navigate, upload — multi-step page interaction. |
| MCP tool | `comet_navigate` | Navigate the current Comet tab to a URL (back/forward/reload variants). |
| MCP tool | `comet_wait_for_idle` | Block until the active tab's network and DOM settle (used between interactions). |
| MCP tool | `comet_lifecycle_start` | Mark the start of a tracked browser task lifecycle bound to this caller. |
| MCP tool | `comet_lifecycle_complete` | Mark the bound browser task lifecycle complete + record outcome. |
| MCP tool | `comet_lifecycle_abort` | Abort the bound browser task lifecycle (e.g. user cancelled). |
| MCP tool | `comet_lifecycle_update` | Push a status update into the bound browser task lifecycle. |
| MCP tool | `comet_task_status` | Read the current status of one or more tracked browser tasks. |
| MCP tool | `comet_delegate` | Hand a browser task to another bound agent / tab group via the orchestrator. |
| MCP tool | `comet_observe` | Attach a passive observer to a tab/group (read-only event stream). |
| MCP tool | `comet_peek` | Read another agent's tab/group state without taking ownership (requires authorization). |
| MCP tool | `comet_pdf` | Render the active page to PDF with margin / header / footer / print options. |
| MCP tool | `comet_scrape` | Structured extraction (tables, JSON-LD, lists, CSS selectors) with auto-scroll for lazy content. |
| MCP tool | `comet_network` | Capture / analyze network traffic — HAR, API responses, request interception, URL blocking, mocking. |
| MCP tool | `comet_automate` | Combine browse + scrape + interact + network into a multi-step end-to-end workflow. |
| MCP tool | `comet_domain` | Cross-tab/session domain helpers (e.g. open QBO, Mercury, GitHub, Google Workspace, SALT Tax with auth checks). |

## Recommended Primary Tool

Task 1 selected `comet-read` as the recommended primary Comet tool. The recommendation JSON is cited below:

```json
{
  "recommended_tool": "comet-read",
  "rationale": "The source transcript is an AI conversation/design-surface tab whose next action is to review or capture the generated Site Survey.html artifact. Among the cataloged Comet skills and MCP tools, comet-read is the best primary tool for read-only extraction from a URL or active browser surface as clean text or an accessibility tree. It is lower-risk than full automation, broadly useful for transcript/design review, and can be paired with capture or automation tools when visual evidence or interaction is required.",
  "alternatives": [
    "comet-screenshot",
    "comet-browser",
    "comet-auto"
  ]
}
```

### Rationale

- `comet-read` best matches the observed task context: a Claude design surface at `claude.ai/design/...` where the next action is to review or capture a generated `Site Survey.html` artifact.
- It provides low-risk, read-only extraction of page content as clean text or an accessibility tree, which makes it a strong default before deciding whether visual capture or browser interaction is necessary.
- It has broad capability coverage for AI-conversation surfaces, static pages, Gmail/Shortwave-style reading, and many documentation-review workflows without taking ownership of a page or mutating state.

### Alternatives

| Alternative | When to use it instead |
|---|---|
| `comet-screenshot` | Use when the important output is visual state, layout, rendered design fidelity, or evidence that must be captured as an image. |
| `comet-browser` | Use when lower-level browser session management, CDP diagnostics, or mixed read/screenshot/page-interaction patterns are needed. |
| `comet-auto` | Use when the work requires a multi-step workflow that combines browsing, scraping, interaction, and network capabilities. |
