#!/usr/bin/env python3
"""
Reducer untuk analisis produk terlaris
Input: StockCode-Description \t Quantity \t 1
Output: StockCode \t Description \t TotalQuantity \t TransactionCount
"""
import sys

current_product = None
total_quantity = 0
transaction_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
        
    try:
        parts = line.split('\t')
        product_key = parts[0]
        quantity = int(parts[1])
        count = int(parts[2])
        
        if product_key == current_product:
            total_quantity += quantity
            transaction_count += count
        else:
            if current_product:
                stock_code, description = current_product.split('|', 1)
                print("{}\t{}\t{}\t{}".format(stock_code, description, total_quantity, transaction_count))
            current_product = product_key
            total_quantity = quantity
            transaction_count = count
    except (ValueError, IndexError):
        continue

# Output last product
if current_product:
    stock_code, description = current_product.split('|', 1)
    print("{}\t{}\t{}\t{}".format(stock_code, description, total_quantity, transaction_count))
