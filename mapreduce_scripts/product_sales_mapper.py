#!/usr/bin/env python3
"""
Mapper untuk analisis produk terlaris
Output: StockCode-Description \t Quantity
"""
import sys

def parse_line(line):
    """Parse CSV line with proper handling of commas in description"""
    fields = []
    current_field = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(current_field.strip())
            current_field = ""
        else:
            current_field += char
    fields.append(current_field.strip())
    return fields

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('InvoiceNo'):
        continue
        
    try:
        fields = parse_line(line)
        if len(fields) >= 7:
            invoice_no = fields[0]
            stock_code = fields[1]
            description = fields[2]
            quantity = int(fields[3])
            
            # Skip invalid data
            if quantity <= 0 or not stock_code or stock_code == 'POST':
                continue
            
            # Output: product_key \t quantity \t 1 (untuk menghitung jumlah transaksi)
            product_key = "{}|{}".format(stock_code, description)
            print("{}\t{}\t1".format(product_key, quantity))
    except (ValueError, IndexError) as e:
        # Skip malformed lines
        continue
