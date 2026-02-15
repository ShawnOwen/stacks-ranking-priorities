# Stacks Ranking Priorities

Task thread tracking and prioritization system with multi-system sync.

## Components

- **orchestration/** - Sync scripts for calendar, GitHub, and GDrive integration
- **Issues** - Task tracking via GitHub Issues

## Calendar Sync

The `orchestration/calendar-sync.py` script syncs task threads to Google Calendar:

```bash
python3 orchestration/calendar-sync.py
```

Features:
- Auto-create calendar events for active threads
- Extract deadlines from labels, meta fields, or descriptions
- Update events when priority changes
- Delete events when threads close
- Color-coded by priority (P1=red, P2=orange, P3=yellow)

## Related

- [Equabot workspace](https://github.com/ShawnOwen/equabot)
- Thread system: `/equabot/threads/`
