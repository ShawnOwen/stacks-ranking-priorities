#!/usr/bin/env python3
"""
Calendar Sync Module for Universal Task Thread Tracking
Syncs task threads to Google Calendar events with links to all systems.

Part of Issue #273: Universal Task Thread Tracking - Calendar Sync Integration

Features:
- Auto-create calendar events for active threads
- Extract deadlines from labels, meta.json, or issue descriptions
- Update events when priority changes
- Clean up events when issues are closed
- Track sync status with detailed state
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# Configuration
THREADS_DIR = Path("/Users/shawnowen/equabot/threads")
CALENDAR_SCRIPT = Path("/Users/shawnowen/equabot/scripts/google-workspace/google_calendar.py")
STATE_FILE = Path("/Users/shawnowen/equabot/orchestration/calendar-sync-state.json")
GITHUB_REPO = "ShawnOwen/stacks-ranking-priorities"
DEFAULT_DEADLINE_DAYS = 7

# Calendar colors by priority (Google Calendar color IDs)
PRIORITY_COLORS = {
    "P1": "11",  # Red
    "P2": "6",   # Orange
    "P3": "5",   # Yellow
    "P4": "8",   # Gray
}


def log(msg: str, level: str = "INFO"):
    """Log with timestamp and level."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARN": "⚠️", "SYNC": "📅"}.get(level, "")
    print(f"[{ts}] {prefix} {msg}")


def load_state() -> Dict:
    """Load sync state (thread_id -> calendar_event_id mapping)."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "synced_threads": {},
        "last_sync": None,
        "sync_stats": {
            "created": 0,
            "updated": 0,
            "deleted": 0,
            "errors": 0
        }
    }


def save_state(state: Dict):
    """Save sync state."""
    state["last_sync"] = datetime.utcnow().isoformat() + "Z"
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_priority_emoji(priority: str) -> str:
    """Return emoji for priority level."""
    priority_map = {
        "P1": "🔴", "1": "🔴", "priority-1": "🔴",
        "P2": "🟠", "2": "🟠", "priority-2": "🟠",
        "P3": "🟡", "3": "🟡", "priority-3": "🟡",
        "P4": "⚪", "4": "⚪", "priority-4": "⚪",
    }
    return priority_map.get(str(priority), "⚪")


def normalize_priority(priority: Any) -> str:
    """Normalize priority to P1-P4 format."""
    if priority is None:
        return "P4"
    p = str(priority).upper()
    if p in ["P1", "1", "PRIORITY-1"]:
        return "P1"
    elif p in ["P2", "2", "PRIORITY-2"]:
        return "P2"
    elif p in ["P3", "3", "PRIORITY-3"]:
        return "P3"
    return "P4"


def extract_deadline_from_text(text: str) -> Optional[datetime]:
    """Extract deadline from text using common patterns."""
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Pattern: "deadline: YYYY-MM-DD" or "due: YYYY-MM-DD"
    date_match = re.search(r'(?:deadline|due)[:\s]+(\d{4}-\d{2}-\d{2})', text_lower)
    if date_match:
        try:
            return datetime.strptime(date_match.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    
    # Pattern: "by March 15" or "due March 15, 2026"
    month_match = re.search(
        r'(?:by|due|before)\s+(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{1,2})(?:[,\s]+(\d{4}))?',
        text_lower
    )
    if month_match:
        month_names = {
            'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
            'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
            'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
            'nov': 11, 'november': 11, 'dec': 12, 'december': 12
        }
        try:
            month = month_names.get(month_match.group(1))
            day = int(month_match.group(2))
            year = int(month_match.group(3)) if month_match.group(3) else datetime.now().year
            return datetime(year, month, day)
        except (ValueError, KeyError):
            pass
    
    # Pattern: "in X days/weeks"
    relative_match = re.search(r'in\s+(\d+)\s+(day|week|month)s?', text_lower)
    if relative_match:
        num = int(relative_match.group(1))
        unit = relative_match.group(2)
        if unit == 'day':
            return datetime.now() + timedelta(days=num)
        elif unit == 'week':
            return datetime.now() + timedelta(weeks=num)
        elif unit == 'month':
            return datetime.now() + timedelta(days=num * 30)
    
    return None


def extract_deadline_from_labels(labels: list) -> Optional[datetime]:
    """Extract deadline from GitHub-style labels."""
    if not labels:
        return None
    
    for label in labels:
        label_str = str(label).lower()
        
        # Pattern: "deadline:2026-02-20"
        if label_str.startswith("deadline:"):
            try:
                return datetime.strptime(label_str.split(":")[1], "%Y-%m-%d")
            except ValueError:
                pass
        
        # Pattern: "due-2026-02-20"
        if label_str.startswith("due-"):
            try:
                return datetime.strptime(label_str[4:], "%Y-%m-%d")
            except ValueError:
                pass
        
        # Pattern: "this-week", "next-week"
        if label_str == "this-week":
            return datetime.now() + timedelta(days=(7 - datetime.now().weekday()))
        if label_str == "next-week":
            return datetime.now() + timedelta(days=(14 - datetime.now().weekday()))
    
    return None


def get_deadline(meta: Dict, default_days: int = DEFAULT_DEADLINE_DAYS) -> datetime:
    """Extract deadline from meta.json with multiple fallback strategies."""
    
    # 1. Check explicit deadline field
    if "deadline" in meta:
        try:
            return datetime.fromisoformat(meta["deadline"].replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            deadline = extract_deadline_from_text(str(meta["deadline"]))
            if deadline:
                return deadline
    
    # 2. Check due_date field
    if "due_date" in meta:
        try:
            return datetime.strptime(meta["due_date"], "%Y-%m-%d")
        except ValueError:
            pass
    
    # 3. Check labels
    labels = meta.get("labels", [])
    label_deadline = extract_deadline_from_labels(labels)
    if label_deadline:
        return label_deadline
    
    # 4. Check description for deadline mentions
    description = meta.get("description", "")
    desc_deadline = extract_deadline_from_text(description)
    if desc_deadline:
        return desc_deadline
    
    # 5. Check notes field
    notes = meta.get("notes", "")
    notes_deadline = extract_deadline_from_text(notes)
    if notes_deadline:
        return notes_deadline
    
    # 6. Priority-based default (P1 = 3 days, P2 = 7 days, P3 = 14 days)
    priority = normalize_priority(meta.get("priority"))
    priority_days = {"P1": 3, "P2": 7, "P3": 14, "P4": 30}
    return datetime.now() + timedelta(days=priority_days.get(priority, default_days))


def build_event_title(thread_id: str, meta: Dict) -> str:
    """Build calendar event title with priority and issue number."""
    name = meta.get("name", thread_id)
    priority = normalize_priority(meta.get("priority"))
    emoji = get_priority_emoji(priority)
    
    issue_num = meta.get("sync", {}).get("github_issue_number")
    if issue_num:
        return f"{emoji} {priority}: #{issue_num} - {name}"
    return f"{emoji} {priority}: {name}"


def build_event_description(thread_id: str, meta: Dict) -> str:
    """Build rich calendar event description with all links."""
    name = meta.get("name", thread_id)
    sync = meta.get("sync", {})
    issue_num = sync.get("github_issue_number")
    
    parts = [
        f"📋 Task Thread: {name}",
        f"Priority: {normalize_priority(meta.get('priority'))}",
        "",
        "🔗 Links:",
    ]
    
    if issue_num:
        parts.append(f"• GitHub: https://github.com/{GITHUB_REPO}/issues/{issue_num}")
    
    gdrive_url = sync.get("gdrive_folder_url")
    if gdrive_url:
        parts.append(f"• GDrive: {gdrive_url}")
    
    parts.append(f"• Thread: /equabot/threads/{thread_id}/")
    parts.append(f"• Session: agent:main:task-thread:{issue_num or thread_id}")
    
    # Add deadline info if extracted
    deadline = get_deadline(meta)
    parts.append("")
    parts.append(f"📅 Deadline: {deadline.strftime('%Y-%m-%d')}")
    
    # Add status
    status = meta.get("status", "active")
    parts.append(f"📊 Status: {status}")
    
    return "\n".join(parts)


def run_calendar_command(args: list) -> Tuple[bool, str]:
    """Run calendar script command and return (success, output)."""
    cmd = ["python3", str(CALENDAR_SCRIPT)] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(CALENDAR_SCRIPT.parent)
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def create_calendar_event(thread_id: str, meta: Dict) -> Optional[str]:
    """Create a calendar event for a thread. Returns event ID or None."""
    title = build_event_title(thread_id, meta)
    description = build_event_description(thread_id, meta)
    deadline = get_deadline(meta)
    
    start_str = deadline.strftime("%Y-%m-%dT09:00:00")
    end_str = deadline.strftime("%Y-%m-%dT10:00:00")
    
    priority = normalize_priority(meta.get("priority"))
    color_id = PRIORITY_COLORS.get(priority, "8")
    
    success, output = run_calendar_command([
        "create", title,
        "--start", start_str,
        "--end", end_str,
        "--description", description,
        "--color", color_id
    ])
    
    if success:
        # Try to extract event ID from output
        try:
            # Look for JSON response with ID
            if "{" in output:
                json_start = output.find("{")
                event_data = json.loads(output[json_start:])
                event_id = event_data.get("id")
                if event_id:
                    log(f"Created event: {title} (ID: {event_id[:20]}...)", "SUCCESS")
                    return event_id
        except json.JSONDecodeError:
            pass
        
        log(f"Created event: {title} (ID extraction failed)", "SUCCESS")
        return "created_no_id"
    else:
        log(f"Failed to create event: {output[:100]}", "ERROR")
        return None


def update_calendar_event(event_id: str, thread_id: str, meta: Dict) -> bool:
    """Update an existing calendar event. Returns success."""
    title = build_event_title(thread_id, meta)
    description = build_event_description(thread_id, meta)
    deadline = get_deadline(meta)
    
    start_str = deadline.strftime("%Y-%m-%dT09:00:00")
    end_str = deadline.strftime("%Y-%m-%dT10:00:00")
    
    priority = normalize_priority(meta.get("priority"))
    color_id = PRIORITY_COLORS.get(priority, "8")
    
    success, output = run_calendar_command([
        "update", event_id,
        "--title", title,
        "--start", start_str,
        "--end", end_str,
        "--description", description,
        "--color", color_id
    ])
    
    if success:
        log(f"Updated event: {title}", "SUCCESS")
        return True
    else:
        log(f"Failed to update event: {output[:100]}", "WARN")
        return False


def delete_calendar_event(event_id: str, thread_name: str) -> bool:
    """Delete a calendar event. Returns success."""
    success, output = run_calendar_command(["delete", event_id])
    
    if success:
        log(f"Deleted event for closed thread: {thread_name}", "SUCCESS")
        return True
    else:
        log(f"Failed to delete event: {output[:100]}", "WARN")
        return False


def get_thread_hash(meta: Dict) -> str:
    """Generate a hash to detect if thread needs updating."""
    key_fields = {
        "name": meta.get("name"),
        "priority": normalize_priority(meta.get("priority")),
        "status": meta.get("status"),
        "deadline": meta.get("deadline"),
        "labels": sorted(meta.get("labels", [])),
    }
    return json.dumps(key_fields, sort_keys=True)


def sync_thread_to_calendar(thread_id: str, state: Dict) -> str:
    """
    Sync a single thread to calendar.
    Returns: 'created', 'updated', 'deleted', 'skipped', or 'error'
    """
    meta_file = THREADS_DIR / thread_id / "meta.json"
    if not meta_file.exists():
        return "skipped"
    
    try:
        meta = json.loads(meta_file.read_text())
    except json.JSONDecodeError:
        log(f"Invalid JSON in {thread_id}/meta.json", "ERROR")
        return "error"
    
    status = meta.get("status", "active")
    synced_info = state["synced_threads"].get(thread_id)
    
    # Handle closed/completed threads
    if status in ["done", "closed", "completed"]:
        if synced_info and synced_info.get("event_id"):
            event_id = synced_info["event_id"]
            if event_id != "created_no_id":
                delete_calendar_event(event_id, meta.get("name", thread_id))
            del state["synced_threads"][thread_id]
            return "deleted"
        return "skipped"
    
    # Calculate current hash for change detection
    current_hash = get_thread_hash(meta)
    
    # Check if needs update (already synced but changed)
    if synced_info:
        if synced_info.get("hash") == current_hash:
            return "skipped"  # No changes
        
        # Thread changed - update event
        event_id = synced_info.get("event_id")
        if event_id and event_id != "created_no_id":
            log(f"Thread changed, updating: {meta.get('name', thread_id)}", "SYNC")
            if update_calendar_event(event_id, thread_id, meta):
                synced_info["hash"] = current_hash
                synced_info["updated_at"] = datetime.utcnow().isoformat() + "Z"
                return "updated"
            return "error"
        else:
            # No valid event ID, create new
            pass
    
    # Create new event
    log(f"Creating event: {meta.get('name', thread_id)}", "SYNC")
    event_id = create_calendar_event(thread_id, meta)
    
    if event_id:
        state["synced_threads"][thread_id] = {
            "event_id": event_id,
            "synced_at": datetime.utcnow().isoformat() + "Z",
            "issue_number": meta.get("sync", {}).get("github_issue_number"),
            "hash": current_hash,
            "priority": normalize_priority(meta.get("priority")),
        }
        
        # Update meta.json with calendar event ID
        meta.setdefault("sync", {})
        meta["sync"]["calendar_event_id"] = event_id
        meta["sync"]["calendar_synced_at"] = datetime.utcnow().isoformat() + "Z"
        meta_file.write_text(json.dumps(meta, indent=2))
        
        return "created"
    
    return "error"


def cleanup_orphaned_events(state: Dict) -> int:
    """Remove state entries for threads that no longer exist."""
    orphaned = []
    
    for thread_id in list(state["synced_threads"].keys()):
        thread_dir = THREADS_DIR / thread_id
        if not thread_dir.exists() or not (thread_dir / "meta.json").exists():
            orphaned.append(thread_id)
    
    for thread_id in orphaned:
        synced_info = state["synced_threads"][thread_id]
        event_id = synced_info.get("event_id")
        if event_id and event_id != "created_no_id":
            delete_calendar_event(event_id, thread_id)
        del state["synced_threads"][thread_id]
        log(f"Cleaned up orphaned thread: {thread_id}", "WARN")
    
    return len(orphaned)


def print_sync_summary(stats: Dict, state: Dict):
    """Print detailed sync summary."""
    print("\n" + "=" * 60)
    print("📊 CALENDAR SYNC SUMMARY")
    print("=" * 60)
    print(f"   Created:  {stats['created']}")
    print(f"   Updated:  {stats['updated']}")
    print(f"   Deleted:  {stats['deleted']}")
    print(f"   Skipped:  {stats['skipped']}")
    print(f"   Errors:   {stats['errors']}")
    print("-" * 60)
    print(f"   Total tracked events: {len(state['synced_threads'])}")
    print(f"   Last sync: {state.get('last_sync', 'Never')}")
    print("=" * 60)
    
    # Show active events by priority
    if state["synced_threads"]:
        print("\n📅 Active Calendar Events:")
        by_priority = {"P1": [], "P2": [], "P3": [], "P4": []}
        for tid, info in state["synced_threads"].items():
            p = info.get("priority", "P4")
            by_priority[p].append(tid)
        
        for p in ["P1", "P2", "P3", "P4"]:
            if by_priority[p]:
                emoji = get_priority_emoji(p)
                print(f"   {emoji} {p}: {len(by_priority[p])} events")


def main():
    """Main sync function."""
    log("=" * 60)
    log("📅 Calendar Sync Starting", "SYNC")
    
    state = load_state()
    
    # Initialize sync stats
    stats = {"created": 0, "updated": 0, "deleted": 0, "skipped": 0, "errors": 0}
    
    # Clean up orphaned events first
    orphaned = cleanup_orphaned_events(state)
    if orphaned:
        stats["deleted"] += orphaned
    
    # Get all threads
    threads = [d.name for d in THREADS_DIR.iterdir() 
               if d.is_dir() and (d / "meta.json").exists()]
    log(f"Found {len(threads)} threads to process")
    
    # Process each thread
    for thread_id in sorted(threads):
        result = sync_thread_to_calendar(thread_id, state)
        stats[result] = stats.get(result, 0) + 1
    
    # Update cumulative stats
    state.setdefault("sync_stats", {"created": 0, "updated": 0, "deleted": 0, "errors": 0})
    for key in ["created", "updated", "deleted", "errors"]:
        state["sync_stats"][key] = state["sync_stats"].get(key, 0) + stats.get(key, 0)
    
    save_state(state)
    print_sync_summary(stats, state)
    
    # Return non-zero if any errors
    return 1 if stats["errors"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
