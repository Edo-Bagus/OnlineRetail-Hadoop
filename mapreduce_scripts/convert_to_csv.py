#!/usr/bin/env python3
"""
Script untuk mengkonversi hasil MapReduce menjadi format CSV yang lebih mudah dibaca
"""
import csv
import sys

def convert_product_sales(input_file, output_file):
    """Convert product sales results to CSV with header"""
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        writer.writerow(['StockCode', 'Description', 'TotalQuantity', 'TransactionCount'])
        
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 4:
                writer.writerow(parts[:4])
    
    print("[OK] Product Sales CSV created: {}".format(output_file))

def convert_customer_patterns(input_file, output_file):
    """Convert customer patterns results to CSV with header"""
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        writer.writerow(['CustomerID', 'TotalQuantity', 'TotalSpending', 'Country', 'TransactionCount'])
        
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 5:
                writer.writerow(parts[:5])
    
    print("[OK] Customer Patterns CSV created: {}".format(output_file))

def convert_time_distribution(input_file, output_file):
    """Convert time distribution results to CSV with header"""
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        writer = csv.writer(outfile)
        writer.writerow(['AnalysisType', 'Period', 'TotalQuantity', 'TotalRevenue', 'TransactionCount', 'AvgTransactionValue'])
        
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) >= 5:
                # Split TYPE:Period menjadi dua kolom
                type_period = parts[0].split(':', 1)
                if len(type_period) == 2:
                    row = [type_period[0], type_period[1]] + parts[1:5]
                    writer.writerow(row)
    
    print("[OK] Time Distribution CSV created: {}".format(output_file))

if __name__ == '__main__':
    print("\n========================================")
    print("Converting MapReduce Results to CSV")
    print("========================================\n")
    
    # Convert all three analyses
    convert_product_sales('product_sales_result.txt', 'product_sales_result.csv')
    convert_customer_patterns('customer_patterns_result.txt', 'customer_patterns_result.csv')
    convert_time_distribution('time_distribution_result.txt', 'time_distribution_result.csv')
    
    print("\n[SUCCESS] All conversions completed!")
    print("\nCSV Files created:")
    print("  - product_sales_result.csv")
    print("  - customer_patterns_result.csv")
    print("  - time_distribution_result.csv")
    print()
