#!/usr/bin/env python3
"""
Mapper untuk analisis distribusi transaksi berdasarkan waktu
Output: 
  - MONTHLY:Year-Month \t Quantity \t TotalPrice \t 1
  - WEEKLY:Year-Week \t Quantity \t TotalPrice \t 1
  - DAYTYPE:Weekday/Weekend \t Quantity \t TotalPrice \t 1
"""
import sys
from datetime import datetime

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
            quantity = int(fields[3])
            invoice_date = fields[4]
            unit_price = float(fields[5])
            
            # Skip invalid data
            if quantity <= 0:
                continue
            
            # Parse date (format: 12/1/2010 8:26)
            date_obj = datetime.strptime(invoice_date.split()[0], '%m/%d/%Y')
            
            total_price = quantity * unit_price
            
            # 1. Monthly Analysis: Year-Month
            year_month = date_obj.strftime('%Y-%m')
            print("MONTHLY:{}\t{}\t{:.2f}\t1".format(year_month, quantity, total_price))
            
            # 2. Weekly Analysis: Year-Week (ISO week number)
            year_week = date_obj.strftime('%Y-W%U')
            print("WEEKLY:{}\t{}\t{:.2f}\t1".format(year_week, quantity, total_price))
            
            # 3. Day Type Analysis: Weekday (Mon-Fri) vs Weekend (Sat-Sun)
            day_of_week = date_obj.weekday()  # 0=Monday, 6=Sunday
            day_type = "Weekday" if day_of_week < 5 else "Weekend"
            print("DAYTYPE:{}\t{}\t{:.2f}\t1".format(day_type, quantity, total_price))
            
    except (ValueError, IndexError) as e:
        # Skip malformed lines
        continue
