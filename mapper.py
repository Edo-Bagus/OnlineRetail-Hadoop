#!/usr/bin/env python
import sys

for line in sys.stdin:
    data = line.strip().split(",")
    try:
        stock_code = data[1]
        quantity = int(data[3])
        print("{}\t{}".format(stock_code, quantity))
    except:
        pass
