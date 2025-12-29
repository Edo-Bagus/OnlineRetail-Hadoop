#!/usr/bin/env python3
"""
Reducer untuk analisis pola pembelian pelanggan
Input: CustomerID \t Quantity \t TotalPrice \t Country \t 1
Output: CustomerID \t TotalQuantity \t TotalSpending \t Country \t TransactionCount
"""
import sys

current_customer = None
total_quantity = 0
total_spending = 0.0
transaction_count = 0
country = ""

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        parts = line.split('\t')
        customer_id = parts[0]
        quantity = int(parts[1])
        price = float(parts[2])
        cust_country = parts[3]
        count = int(parts[4])
        
        if customer_id == current_customer:
            total_quantity += quantity
            total_spending += price
            transaction_count += count
        else:
            if current_customer:
                print("{}\t{}\t{:.2f}\t{}\t{}".format(current_customer, total_quantity, total_spending, country, transaction_count))
            current_customer = customer_id
            total_quantity = quantity
            total_spending = price
            transaction_count = count
            country = cust_country
    except (ValueError, IndexError):
        continue

# Output last customer
if current_customer:
    print("{}\t{}\t{:.2f}\t{}\t{}".format(current_customer, total_quantity, total_spending, country, transaction_count))
