#!/bin/bash
# Script untuk menjalankan semua analisis MapReduce di Hadoop

echo "====================================================="
echo "ANALISIS 1: PRODUK TERLARIS"
echo "====================================================="

# Clean up previous outputs
hadoop fs -rm -r /output/product_sales 2>/dev/null

# Run MapReduce job
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files product_sales_mapper.py,product_sales_reducer.py \
    -mapper "python3 product_sales_mapper.py" \
    -reducer "python3 product_sales_reducer.py" \
    -input /input/Online-Retail.csv \
    -output /output/product_sales

# Get top 20 products by quantity
echo -e "\n>>> TOP 20 PRODUK BERDASARKAN TOTAL QUANTITY <<<"
hadoop fs -cat /output/product_sales/part-* | sort -t$'\t' -k3 -nr | head -20

# Get top 20 products by transaction count
echo -e "\n>>> TOP 20 PRODUK BERDASARKAN JUMLAH TRANSAKSI <<<"
hadoop fs -cat /output/product_sales/part-* | sort -t$'\t' -k4 -nr | head -20

echo -e "\n====================================================="
echo "ANALISIS 2: POLA PEMBELIAN PELANGGAN"
echo "====================================================="

# Clean up previous outputs
hadoop fs -rm -r /output/customer_patterns 2>/dev/null

# Run MapReduce job
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files customer_pattern_mapper.py,customer_pattern_reducer.py \
    -mapper "python3 customer_pattern_mapper.py" \
    -reducer "python3 customer_pattern_reducer.py" \
    -input /input/Online-Retail.csv \
    -output /output/customer_patterns

# Get top 20 customers by spending
echo -e "\n>>> TOP 20 PELANGGAN BERDASARKAN TOTAL SPENDING <<<"
hadoop fs -cat /output/customer_patterns/part-* | sort -t$'\t' -k3 -nr | head -20

# Get top 20 customers by transaction count
echo -e "\n>>> TOP 20 PELANGGAN BERDASARKAN JUMLAH TRANSAKSI <<<"
hadoop fs -cat /output/customer_patterns/part-* | sort -t$'\t' -k5 -nr | head -20

echo -e "\n====================================================="
echo "ANALISIS 3: DISTRIBUSI TRANSAKSI PER PERIODE"
echo "====================================================="

# Clean up previous outputs
hadoop fs -rm -r /output/time_distribution 2>/dev/null

# Run MapReduce job
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files time_distribution_mapper.py,time_distribution_reducer.py \
    -mapper "python3 time_distribution_mapper.py" \
    -reducer "python3 time_distribution_reducer.py" \
    -input /input/Online-Retail.csv \
    -output /output/time_distribution

# Get monthly analysis
echo -e "\n>>> DISTRIBUSI TRANSAKSI PER BULAN <<<"
hadoop fs -cat /output/time_distribution/part-* | grep 'MONTHLY:' | sort -t$'\t' -k1

# Get weekly analysis - show top 10 and bottom 10 weeks
echo -e "\n>>> TOP 10 MINGGU DENGAN REVENUE TERTINGGI <<<"
hadoop fs -cat /output/time_distribution/part-* | grep 'WEEKLY:' | sort -t$'\t' -k3 -nr | head -10

echo -e "\n>>> TOP 10 MINGGU DENGAN TRANSAKSI TERBANYAK <<<"
hadoop fs -cat /output/time_distribution/part-* | grep 'WEEKLY:' | sort -t$'\t' -k4 -nr | head -10

# Get weekday vs weekend comparison
echo -e "\n>>> PERBANDINGAN WEEKDAY VS WEEKEND <<<"
hadoop fs -cat /output/time_distribution/part-* | grep 'DAYTYPE:'

echo -e "\n====================================================="
echo "SEMUA ANALISIS SELESAI!"
echo "====================================================="
