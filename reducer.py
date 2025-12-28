#!/usr/bin/env python
import sys

current_product = None
total = 0

for line in sys.stdin:
    product, quantity = line.strip().split("\t")
    quantity = int(quantity)

    if product == current_product:
        total += quantity
    else:
        if current_product:
            print("{}\t{}".format(current_product, total))
        current_product = product
        total = quantity

if current_product:
    print("{}\t{}".format(current_product, total))
