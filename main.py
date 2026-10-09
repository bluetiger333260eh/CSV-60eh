#!/usr/bin/env python3
"""
CSV profiling script: prints row count, column names, missing values, and basic data type info.
"""

import csv
import argparse
import sys
from collections import Counter, defaultdict

def profile_csv(path, sample=5, max_unique=10):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        stats = {h: Counter() for h in headers}
        missing = defaultdict(int)
        total_rows = 0
        for row in reader:
            total_rows += 1
            for h in headers:
                val = row.get(h, '')
                if val == '':
                    missing[h] += 1
                else:
                    stats[h][val] += 1
        print(f"Rows: {total_rows}")
        print(f"Columns: {len(headers)}")
        for h in headers:
            uniq_vals = list(stats[h].keys())
            types = set()
            for val in uniq_vals[:sample]:
                try:
                    float(val)
                    types.add('numeric')
                except ValueError:
                    types.add('text')
            uniq_count = len(uniq_vals)
            uniq_display = uniq_vals[:max_unique]
            print(f"\nColumn: {h}")
            print(f"  Missing: {missing[h]}")
            print(f"  Types: {', '.join(sorted(types))}")
            print(f"  Unique values ({uniq_count}): {uniq_display}")

def main():
    parser = argparse.ArgumentParser(description="Profile a CSV file.")
    parser.add_argument("filepath", help="Path to the CSV file")
    args = parser.parse_args()
    try:
        profile_csv(args.filepath)
    except FileNotFoundError:
        sys.exit(f"Error: file '{args.filepath}' not found.")
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()