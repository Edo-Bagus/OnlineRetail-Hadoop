#!/usr/bin/env python3
"""
Reducer untuk analisis distribusi transaksi berdasarkan waktu
Input: TYPE:Period \t Quantity \t TotalPrice \t 1
Output: TYPE:Period \t TotalQuantity \t TotalRevenue \t TransactionCount \t AvgTransactionValue
"""
import sys

current_period = None
total_quantity = 0
total_revenue = 0.0
transaction_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        parts = line.split('\t')
        period = parts[0]  # Format: TYPE:period (e.g., MONTHLY:2010-12)
        quantity = int(parts[1])
        price = float(parts[2])
        count = int(parts[3])
        
        if period == current_period:
            total_quantity += quantity
            total_revenue += price
            transaction_count += count
        else:
            if current_period:
                avg_transaction_value = total_revenue / transaction_count if transaction_count > 0 else 0
                print("{}\t{}\t{:.2f}\t{}\t{:.2f}".format(current_period, total_quantity, total_revenue, transaction_count, avg_transaction_value))
            current_period = period
            total_quantity = quantity
            total_revenue = price
            transaction_count = count
    except (ValueError, IndexError):
        continue

# Output last period
if current_period:
    avg_transaction_value = total_revenue / transaction_count if transaction_count > 0 else 0
    print("{}\t{}\t{:.2f}\t{}\t{:.2f}".format(current_period, total_quantity, total_revenue, transaction_count, avg_transaction_value))
