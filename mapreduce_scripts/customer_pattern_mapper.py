#!/usr/bin/env python3
"""
Mapper untuk analisis pola pembelian pelanggan
Output: CustomerID \t Quantity \t UnitPrice \t Country
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
        if len(fields) >= 8:
            quantity = int(fields[3])
            unit_price = float(fields[5])
            customer_id = fields[6]
            country = fields[7]
            
            # Skip invalid data
            if quantity <= 0 or not customer_id or customer_id == '':
                continue
            
            total_price = quantity * unit_price
            # Output: customer_id \t quantity \t total_price \t country \t 1
            print("{}\t{}\t{:.2f}\t{}\t1".format(customer_id, quantity, total_price, country))
    except (ValueError, IndexError) as e:
        # Skip malformed lines
        continue
