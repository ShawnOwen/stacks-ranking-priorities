# IRS Payment Verification: Balancing Rock $169 Monthly Installment

## Overview
Verify monthly IRS installment payments for **Balancing Rock LLC** ($169 due on the 15th of each month) by checking Mercury bank transactions and QuickBooks Online records.

## Payment Details

| Field | Value |
|-------|-------|
| Entity | Balancing Rock LLC |
| Amount | $169.00 |
| Due Date | 15th of each month |
| Payment Method | IRS Direct Pay / ACH |
| Tax Type | Form 1065 (Partnership) Installment Plan |
| Tax Years | 2020 + 2021 |

## Trigger
- Payment marked as past due on IRS portal
- Missing verification of recent payments (e.g., Nov, Dec, Jan, Feb)
- Monthly reconciliation of tax obligations

## Verification Methods

### Method A: Mercury UI (Fastest)

#### Steps:
1. Log into **Mercury** → Navigate to **Accounts → Checking**
2. Set date range to cover the verification period (e.g., Oct 2025 → Feb 2026)
3. Use search filters:
   - Keywords: `IRS`, `TREAS`, `TREASURY`, `US TREASURY`, `INTERNAL REVENUE`, `IRS DIRECT PAY`
   - Amount: `$169` or `-$169` (depending on debit display format)
4. For each target due date (±5 days window):
   - **2025-11-15**
   - **2025-12-15**
   - **2026-01-15**
   - **2026-02-15**
5. Click transaction details to capture:
   - Posted date
   - Amount
   - Description/descriptor
   - Trace/confirmation number
   - Payment method (ACH/DirectPay/etc.)

#### Expected Results:
- **Found**: Payment processed, note confirmation number
- **Not found**: Payment may be missing (investigate further or make payment)

### Method B: QuickBooks Online

#### Steps:
1. Navigate to **Banking → Transactions** (for bank feed) or **Expenses**
2. Filter by:
   - Bank account: Mercury Checking
   - Date range: Oct 2025 → Feb 2026
   - Amount: $169
3. Search for vendor/description keywords: `IRS`, `TREASURY`, `IRS DIRECT PAY`
4. Verify the same target dates (±5 days)

**Note:** If transaction appears in Mercury but not in QBO, it may be an uncategorized bank feed item that needs to be matched or categorized.

### Method C: Automated CSV Scan (Recommended for Bulk Verification)

Use the `find_recurring_payment.py` helper script to scan exported Mercury transactions:

#### Prerequisites:
1. Export Mercury transactions to CSV:
   - Mercury → Accounts → Checking → Export
   - Date range: Oct 2025 → Feb 2026
   - Save to local directory (e.g., `~/Downloads/mercury-transactions.csv`)

#### Run Script:
```bash
python3 orchestration/find_recurring_payment.py \
  ~/Downloads/mercury-transactions.csv \
  --amount 169 \
  --query IRS --query TREAS --query TREASURY \
  --target-date 2025-11-15 \
  --target-date 2025-12-15 \
  --target-date 2026-01-15 \
  --target-date 2026-02-15
```

#### Script Output:
The script will display matching transactions near target dates:
```
Target: 2025-11-15
  2025-11-13 | -$169.00 | IRS DIRECT PAY - TAX PMT | mercury-transactions.csv:45

Target: 2025-12-15
  Not found within ±5 days

Target: 2026-01-15
  2026-01-16 | -$169.00 | US TREASURY IRS | mercury-transactions.csv:102
```

#### Directory Mode:
If you have multiple CSV exports:
```bash
python3 orchestration/find_recurring_payment.py \
  ~/Downloads/exports/ \
  --amount 169 \
  --query IRS
```

## Documenting Results

### In GitHub Issue:
Post a verification comment with:
```markdown
### IRS Payment Verification Results (YYYY-MM-DD)

**Verification period:** Oct 2025 → Feb 2026  
**Payment amount:** $169  
**Entity:** Balancing Rock LLC

| Due Date | Status | Posted Date | Confirmation | Notes |
|----------|--------|-------------|--------------|-------|
| 2025-11-15 | ✅ Verified | 2025-11-13 | ACH-xxxxx | Mercury transaction |
| 2025-12-15 | ✅ Verified | 2025-12-15 | ACH-xxxxx | Mercury transaction |
| 2026-01-15 | ❌ Missing | - | - | No matching transaction found |
| 2026-02-15 | ❌ Missing | - | - | Past due - needs payment |

**Action needed:** Missing payments for Jan 15 and Feb 15 require immediate attention.
```

### In Task Thread:
Update the associated task thread (e.g., `tt-275-irs-payment-balancing-rock`) with:
- Verification results
- Missing payments requiring action
- Next steps (e.g., make payment, investigate with IRS, request abatement)

## Making Missing Payments (If Needed)

**⚠️ IMPORTANT:** This runbook is for **verification only**. Do not make payments without explicit approval.

If verification confirms missing payments:
1. Confirm with stakeholders that payment should be made
2. Calculate any late penalties or interest
3. Use IRS Direct Pay: https://www.irs.gov/payments/direct-pay
4. Record payment details in GitHub issue and task thread

## QBO Categorization (After Verification)

If payments exist in Mercury but are uncategorized in QBO:
1. **Banking → Transactions** (bank feed)
2. Find the $169 IRS payment
3. Click **Categorize**:
   - Category: `Taxes & Licenses` or `Business Taxes`
   - Payee: `Internal Revenue Service`
   - Memo: `Form 1065 installment - Tax Years 2020+2021`
4. Click **Save**

## Related Resources

- **IRS Portal:** https://www.irs.gov/account
- **IRS Direct Pay:** https://www.irs.gov/payments/direct-pay
- **Task Thread:** `tt-275-irs-payment-balancing-rock`
- **GitHub Issue:** #299
- **Helper Script:** `orchestration/find_recurring_payment.py`

## Gotchas & Lessons Learned

- **Search multiple descriptors:** IRS payments may appear as "IRS", "US TREASURY", "TREAS", "IRS DIRECT PAY", or other variations
- **Date window:** Payments may post 1-3 days before or after the due date (always check ±5 days)
- **Negative amounts:** Mercury may display debits as negative values (e.g., `-$169.00`)
- **Bank feed delay:** Mercury transactions may take 1-2 business days to appear in QBO bank feed
- **IRS portal delay:** IRS website may show payments as "pending" for several days after they clear the bank
- **Manual vs. automated:** For one-off checks, Mercury UI is fastest. For bulk verification (4+ dates), use the script to save time.
