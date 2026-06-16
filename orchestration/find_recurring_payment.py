#!/usr/bin/env python3
"""
find_recurring_payment.py - Scan CSV exports for recurring payments near target dates

Usage:
    # Scan a single CSV file
    python3 find_recurring_payment.py transactions.csv --amount 169 --query IRS --target-date 2025-11-15

    # Scan a directory of CSV files
    python3 find_recurring_payment.py ~/Downloads/exports/ --amount 169 --query TREAS

    # Multiple search terms and target dates
    python3 find_recurring_payment.py data.csv \\
        --amount 169 \\
        --query IRS --query TREAS --query TREASURY \\
        --target-date 2025-11-15 \\
        --target-date 2025-12-15 \\
        --target-date 2026-01-15 \\
        --target-date 2026-02-15
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Tuple


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string in various formats."""
    formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%b %d, %Y',
        '%B %d, %Y',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def parse_amount(amount_str: str) -> Optional[float]:
    """Parse amount string, handling various formats."""
    if not amount_str:
        return None
    
    # Remove currency symbols, whitespace, and commas
    cleaned = amount_str.replace('$', '').replace(',', '').replace(' ', '').strip()
    
    # Handle parentheses notation for negative numbers
    if cleaned.startswith('(') and cleaned.endswith(')'):
        cleaned = '-' + cleaned[1:-1]
    
    try:
        return float(cleaned)
    except ValueError:
        return None


def find_date_column(headers: List[str]) -> Optional[int]:
    """Find the date column index."""
    date_keywords = ['date', 'transaction date', 'posted date', 'post date', 'trans date']
    headers_lower = [h.lower() for h in headers]
    
    for keyword in date_keywords:
        for i, header in enumerate(headers_lower):
            if keyword in header:
                return i
    return None


def find_amount_column(headers: List[str]) -> Optional[int]:
    """Find the amount column index."""
    amount_keywords = ['amount', 'debit', 'payment', 'withdrawal', 'transaction amount']
    headers_lower = [h.lower() for h in headers]
    
    for keyword in amount_keywords:
        for i, header in enumerate(headers_lower):
            if keyword in header and 'balance' not in header:
                return i
    return None


def find_description_column(headers: List[str]) -> Optional[int]:
    """Find the description column index."""
    desc_keywords = ['description', 'memo', 'note', 'details', 'payee', 'counterparty']
    headers_lower = [h.lower() for h in headers]
    
    for keyword in desc_keywords:
        for i, header in enumerate(headers_lower):
            if keyword in header:
                return i
    return None


def matches_query(text: str, queries: List[str]) -> bool:
    """Check if text matches any of the query strings (case-insensitive)."""
    if not queries:
        return True
    text_lower = text.lower()
    return any(query.lower() in text_lower for query in queries)


def scan_csv_file(
    filepath: Path,
    target_amount: float,
    queries: List[str],
    target_dates: List[datetime],
    date_window: int = 5
) -> List[Tuple[datetime, str, float, str, str, int]]:
    """
    Scan a single CSV file for matching transactions.
    
    Returns list of tuples: (target_date, transaction_date, amount, description, filename, row_number)
    """
    results = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # Find column indices
            date_col = find_date_column(headers)
            amount_col = find_amount_column(headers)
            desc_col = find_description_column(headers)
            
            if date_col is None:
                print(f"Warning: Could not find date column in {filepath.name}", file=sys.stderr)
                return results
            
            if amount_col is None:
                print(f"Warning: Could not find amount column in {filepath.name}", file=sys.stderr)
                return results
            
            # Scan rows
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (1 for header)
                if len(row) <= max(date_col, amount_col, desc_col or 0):
                    continue
                
                # Parse transaction date
                trans_date = parse_date(row[date_col])
                if not trans_date:
                    continue
                
                # Parse amount
                amount = parse_amount(row[amount_col])
                if amount is None:
                    continue
                
                # Check if amount matches (handle positive/negative)
                amount_abs = abs(amount)
                if abs(amount_abs - target_amount) > 0.01:  # Allow small floating point differences
                    continue
                
                # Check description if queries provided
                description = row[desc_col] if desc_col is not None else ''
                if queries and not matches_query(description, queries):
                    continue
                
                # Check if transaction is near any target date
                if target_dates:
                    for target_date in target_dates:
                        delta = abs((trans_date - target_date).days)
                        if delta <= date_window:
                            results.append((
                                target_date,
                                trans_date.strftime('%Y-%m-%d'),
                                amount,
                                description[:60],  # Truncate long descriptions
                                filepath.name,
                                row_num
                            ))
                            break  # Don't double-count if multiple targets match
                else:
                    # No target dates - include all matching transactions
                    results.append((
                        trans_date,  # Use transaction date as "target"
                        trans_date.strftime('%Y-%m-%d'),
                        amount,
                        description[:60],
                        filepath.name,
                        row_num
                    ))
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    
    return results


def scan_directory(
    directory: Path,
    target_amount: float,
    queries: List[str],
    target_dates: List[datetime],
    date_window: int = 5
) -> List[Tuple[datetime, str, float, str, str, int]]:
    """Scan all CSV files in a directory."""
    all_results = []
    csv_files = list(directory.glob('*.csv'))
    
    if not csv_files:
        print(f"Warning: No CSV files found in {directory}", file=sys.stderr)
        return all_results
    
    for csv_file in csv_files:
        results = scan_csv_file(csv_file, target_amount, queries, target_dates, date_window)
        all_results.extend(results)
    
    return all_results


def main():
    parser = argparse.ArgumentParser(
        description='Scan CSV exports for recurring payments near target dates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'path',
        type=Path,
        help='CSV file or directory containing CSV files'
    )
    
    parser.add_argument(
        '--amount',
        type=float,
        required=True,
        help='Target payment amount (e.g., 169 for $169.00)'
    )
    
    parser.add_argument(
        '--query',
        action='append',
        dest='queries',
        help='Search term(s) to filter descriptions (case-insensitive, can be specified multiple times)'
    )
    
    parser.add_argument(
        '--target-date',
        action='append',
        dest='target_dates',
        help='Target date(s) to check (YYYY-MM-DD format, can be specified multiple times)'
    )
    
    parser.add_argument(
        '--window',
        type=int,
        default=5,
        help='Number of days before/after target date to search (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not args.path.exists():
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Parse target dates
    target_dates = []
    if args.target_dates:
        for date_str in args.target_dates:
            date = parse_date(date_str)
            if date is None:
                print(f"Error: Could not parse date '{date_str}'", file=sys.stderr)
                sys.exit(1)
            target_dates.append(date)
    else:
        # If no target dates provided, show all matching transactions
        print("Note: No target dates specified, showing all matching transactions")
    
    # Scan files
    if args.path.is_file():
        results = scan_csv_file(args.path, args.amount, args.queries or [], target_dates, args.window)
    elif args.path.is_dir():
        results = scan_directory(args.path, args.amount, args.queries or [], target_dates, args.window)
    else:
        print(f"Error: '{args.path}' is neither a file nor a directory", file=sys.stderr)
        sys.exit(1)
    
    # Display results
    if not results:
        print(f"\nNo matching transactions found for amount ${args.amount:.2f}")
        if args.queries:
            print(f"Search terms: {', '.join(args.queries)}")
        sys.exit(0)
    
    # Sort results by target date, then transaction date
    results.sort(key=lambda x: (x[0], x[1]))
    
    # Group by target date
    if target_dates:
        print(f"\n{'='*80}")
        print(f"Recurring Payment Search Results: ${args.amount:.2f}")
        print(f"Date window: ±{args.window} days")
        if args.queries:
            print(f"Search terms: {', '.join(args.queries)}")
        print(f"{'='*80}\n")
        
        for target_date in target_dates:
            target_str = target_date.strftime('%Y-%m-%d')
            print(f"Target: {target_str}")
            
            matches = [r for r in results if r[0] == target_date]
            if matches:
                for _, trans_date, amount, desc, filename, row_num in matches:
                    amount_str = f"${amount:.2f}" if amount >= 0 else f"-${abs(amount):.2f}"
                    print(f"  {trans_date} | {amount_str:>10} | {desc} | {filename}:{row_num}")
            else:
                print(f"  Not found within ±{args.window} days")
            print()
    else:
        # No target dates - show all matches
        print(f"\nAll matching transactions for ${args.amount:.2f}:")
        print(f"{'='*80}\n")
        for _, trans_date, amount, desc, filename, row_num in results:
            amount_str = f"${amount:.2f}" if amount >= 0 else f"-${abs(amount):.2f}"
            print(f"{trans_date} | {amount_str:>10} | {desc} | {filename}:{row_num}")
        print()


if __name__ == '__main__':
    main()
