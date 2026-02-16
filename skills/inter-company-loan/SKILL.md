# Inter-Company Loan: Mercury Transfer + QBO Journal Entry

## Overview
When an entity (e.g., Hills & Hollows) has insufficient funds to cover scheduled vendor payments, transfer funds from a sister entity (e.g., Sugarloaf Valley Farms) via Mercury and record as a short-term intercompany loan in QuickBooks Online.

## Trigger
- Vendor bill payments are scheduled/approved but the paying entity's Mercury checking balance is insufficient to cover them.
- Example: H&H Checking ••5310 balance $964.01, but $2,626.56 in invoices scheduled for Feb 17.

## Entities & Accounts

| Entity | Mercury Account | QBO Account |
|--------|----------------|-------------|
| Sugarloaf Valley Farms (SVF) | Checking ••8444 (source) | — |
| Hills & Hollows (H&H) | Checking ••5310 (destination) | Mercury Checking *5310 |

## Workflow Steps

### Step 1: Identify Shortfall
1. Check the paying entity's Mercury balance.
2. Sum all scheduled/approved vendor payments.
3. Calculate shortfall: `Scheduled Payments - Current Balance = Shortfall`.
4. Determine transfer amount (round up for buffer).

### Step 2: Execute Mercury Transfer

**CRITICAL: Initiate from the RECEIVING entity's dashboard (H&H), not the sending entity (SVF).**

This is because SVF's "Send Money > Transfer" dropdown may not list H&H ••5310 as a destination, but H&H's dashboard WILL show SVF ••8444 as an available funding source.

#### Steps in Mercury:
1. Log into Mercury → Switch to **Hills & Hollows** dashboard.
2. Navigate to **Send Money** (left sidebar).
3. Click the **Transfer** tab (internal transfers between linked accounts).
4. Set **From:** SVF Mercury Checking ••8444.
5. Set **To:** H&H Mercury Checking ••5310.
6. Enter **Amount** (e.g., $5,000.00).
7. Add **Internal note:** `SVF to HH short-term loan - [Purpose, e.g., Cover shortfall for High Noon Tacos payments scheduled Feb 17]`
8. Click **Review details** → Verify all fields → **Submit transfer**.
9. Note the estimated arrival window (typically 2-4 business days for ACH, same-day for internal).

### Step 3: Record Journal Entry in QBO

Record the transfer as an intercompany loan in the RECEIVING entity's QBO.

#### Steps in QBO (H&H books):
1. Navigate to **+ New** → **Journal Entry** (or go to `/app/journal`).
2. Set **Journal date** to the transfer date.
3. Set **Journal no.** following the block numbering convention (e.g., `BLK-1-12/30/31`).
4. **Line 1 (Debit):**
   - Account: `Mercury Checking *5310` (or the appropriate bank account)
   - Debit: Transfer amount (e.g., $5,000.00)
5. **Line 2 (Credit):**
   - Account: `Loan SVF to HH (LOC)` (intercompany loan liability account)
   - Credit: Transfer amount (e.g., $5,000.00)
6. **Memo:** `SVF to HH short-term loan - [Purpose]. Transfer via Mercury [date].`
7. Click **Save and close**.

### Step 4: Document in GitHub Issue

Post a comment on the relevant GitHub issue with:
- Transfer details (from, to, amount, date, estimated arrival)
- Internal note text
- QBO Journal Entry reference number
- Projected balance after transfer + scheduled payments clear

## QBO Account Setup (if needed)

If `Loan SVF to HH (LOC)` doesn't exist:
1. **Chart of Accounts** → **New**
2. Type: **Other Current Liabilities**
3. Detail Type: **Line of Credit**
4. Name: `Loan SVF to HH (LOC)`

## Reversal / Repayment

When H&H repays SVF:
1. Execute Mercury transfer: H&H ••5310 → SVF ••8444.
2. QBO Journal Entry (reverse):
   - Debit: `Loan SVF to HH (LOC)`
   - Credit: `Mercury Checking *5310`
3. Memo: `Repayment of SVF to HH short-term loan - [reference original JE#]`

## Gotchas & Lessons Learned

- **Transfer direction matters in Mercury UI.** SVF dashboard may NOT show H&H as a transfer destination. Always initiate from the receiving entity's (H&H) dashboard where the source entity appears in the "From" dropdown.
- **Verify balance covers transfer.** SVF must have sufficient funds for the outgoing transfer.
- **QBO dropdown behavior.** When selecting accounts in Journal Entry lines, the dropdown may require clicking directly on the Account field, clearing any pre-filled text, and typing to search. Use precise clicks if the dropdown doesn't respond.
- **Timing.** Schedule the transfer with enough lead time for funds to arrive before vendor payment dates. Mercury internal transfers between linked accounts may settle faster than standard ACH.

## Example: Issue #277 (Feb 15, 2026)

| Field | Value |
|-------|-------|
| Trigger | H&H balance $964.01, invoices #17 + #18 = $2,626.56 due Feb 17 |
| Transfer | $5,000 SVF ••8444 → H&H ••5310 |
| Mercury initiated from | H&H dashboard |
| Arrival | Feb 17-19, 2026 |
| QBO JE | #BLK-1-12/30/31 (02/15/2026) |
| QBO Debit | Mercury Checking *5310 $5,000 |
| QBO Credit | Loan SVF to HH (LOC) $5,000 |
| Projected H&H balance | ~$2,337.45 after transfer + invoice payments |
