# Stacks Ranking Priorities

Task thread tracking and prioritization system with multi-system sync.

## Components

- **orchestration/** - Sync scripts for calendar, GitHub, and GDrive integration
- **skills/** - Operational runbooks and workflow documentation
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

## Payment Verification Helper

The `orchestration/find_recurring_payment.py` script scans CSV exports from bank accounts to verify recurring payments:

```bash
python3 orchestration/find_recurring_payment.py transactions.csv \
  --amount 169 \
  --query IRS --query TREAS \
  --target-date 2025-11-15 \
  --target-date 2025-12-15
```

Features:
- Scan single CSV files or entire directories
- Search by amount and description keywords
- Check transactions near target dates (±5 day window)
- Multiple date format support (YYYY-MM-DD, MM/DD/YYYY, etc.)
- Handles positive/negative amounts and various CSV formats

See `skills/irs-payment-verification/SKILL.md` for detailed usage examples.

## Skills Documentation

The `skills/` directory contains operational runbooks for common workflows:
- **inter-company-loan/** - Mercury transfers and QBO journal entries for intercompany loans
- **irs-payment-verification/** - Verifying IRS installment payments in Mercury and QuickBooks

## Related

- [Equabot workspace](https://github.com/ShawnOwen/equabot)
- Thread system: `/equabot/threads/`
