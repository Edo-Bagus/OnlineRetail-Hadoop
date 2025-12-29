# Online Retail Analysis - Hadoop MapReduce

Analisis data transaksi retail menggunakan Hadoop MapReduce di Docker untuk mengidentifikasi:
1. **Produk terlaris** berdasarkan quantity dan jumlah transaksi
2. **Pola pembelian pelanggan** berdasarkan spending dan frekuensi
3. **Distribusi transaksi** per periode waktu (bulanan, mingguan, weekday vs weekend)

---

## Dataset

**File**: `Online-Retail.csv`
**Total Records**: 541,910 transaksi
**Periode**: December 2010 - December 2011

**Kolom Data**:
- InvoiceNo: Nomor invoice transaksi
- StockCode: Kode produk
- Description: Deskripsi produk
- Quantity: Jumlah item
- InvoiceDate: Tanggal transaksi (format: M/D/YYYY H:MM)
- UnitPrice: Harga per unit
- CustomerID: ID pelanggan
- Country: Negara transaksi

---

## Arsitektur Sistem

```
Docker Container (Hadoop Cluster)
├── Namenode (HDFS Master)
├── Datanode (HDFS Worker)
└── YARN (Resource Manager)

MapReduce Jobs:
├── Analisis 1: Product Sales
│   ├── product_sales_mapper.py
│   └── product_sales_reducer.py
├── Analisis 2: Customer Patterns
│   ├── customer_pattern_mapper.py
│   └── customer_pattern_reducer.py
└── Analisis 3: Time Distribution
    ├── time_distribution_mapper.py
    └── time_distribution_reducer.py
```

---

## Quick Start

### Option 1: Automated Scripts (Recommended)

**Quick Re-run** (if cluster is already running):
```powershell
.\rerun.ps1
```

**Full Restart** (restart cluster + run all analyses):
```powershell
.\full-restart.ps1
```

### Option 2: Manual Setup

### 1. Setup Hadoop Cluster
```powershell
# Build dan start container
docker-compose build
docker-compose up -d

# Tunggu 30 detik untuk inisialisasi
Start-Sleep -Seconds 30

# Verifikasi cluster
docker exec namenode hdfs dfsadmin -report
```

### 2. Persiapan Data dan Scripts
```powershell
# Copy file ke container
docker cp Online-Retail.csv namenode:/tmp/
docker cp mapreduce_scripts/product_sales_mapper.py namenode:/tmp/
docker cp mapreduce_scripts/product_sales_reducer.py namenode:/tmp/
docker cp mapreduce_scripts/customer_pattern_mapper.py namenode:/tmp/
docker cp mapreduce_scripts/customer_pattern_reducer.py namenode:/tmp/
docker cp mapreduce_scripts/time_distribution_mapper.py namenode:/tmp/
docker cp mapreduce_scripts/time_distribution_reducer.py namenode:/tmp/

# Fix line endings dan permissions
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/*.py"
docker exec namenode bash -c "chmod +x /tmp/*.py"

# Upload CSV ke HDFS
docker exec namenode hdfs dfs -mkdir -p /input
docker exec namenode hdfs dfs -put /tmp/Online-Retail.csv /input/
```

### 3. Jalankan Analisis

#### Analisis 1: Produk Terlaris
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/product_sales_mapper.py,/tmp/product_sales_reducer.py -mapper 'python3 /tmp/product_sales_mapper.py' -reducer 'python3 /tmp/product_sales_reducer.py' -input /input/Online-Retail.csv -output /output/product_sales"

# Lihat TOP 20 produk by quantity
docker exec namenode bash -c "hdfs dfs -cat /output/product_sales/part-* | sort -t\$'\t' -k3 -nr | head -20"
```

#### Analisis 2: Pola Pelanggan
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/customer_pattern_mapper.py,/tmp/customer_pattern_reducer.py -mapper 'python3 /tmp/customer_pattern_mapper.py' -reducer 'python3 /tmp/customer_pattern_reducer.py' -input /input/Online-Retail.csv -output /output/customer_patterns"

# Lihat TOP 20 customers by spending
docker exec namenode bash -c "hdfs dfs -cat /output/customer_patterns/part-* | sort -t\$'\t' -k3 -nr | head -20"
```

#### Analisis 3: Distribusi Waktu (Bulanan, Mingguan, Weekday/Weekend)
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/time_distribution_mapper.py,/tmp/time_distribution_reducer.py -mapper 'python3 /tmp/time_distribution_mapper.py' -reducer 'python3 /tmp/time_distribution_reducer.py' -input /input/Online-Retail.csv -output /output/time_distribution"

# Lihat distribusi per bulan
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'MONTHLY:' | sort"

# Lihat distribusi per minggu (top 10)
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'WEEKLY:' | sort -t\$'\t' -k3 -nr | head -10"

# Lihat weekday vs weekend
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'DAYTYPE:'"
```

---

## Output Format

### 1. Product Sales Analysis
```
StockCode | Description | TotalQuantity | TransactionCount
85123A | WHITE HANGING HEART T-LIGHT HOLDER | 15000 | 500
```

### 2. Customer Patterns Analysis
```
CustomerID | TotalQuantity | TotalSpending | Country | TransactionCount
17850 | 5000 | 25000.50 | United Kingdom | 150
```

### 3. Time Distribution Analysis (Multi-Level)
```
# Monthly Analysis
MONTHLY:2010-12 | 50000 | 150000.00 | 2000 | 75.00

# Weekly Analysis
WEEKLY:2010-W49 | 12000 | 35000.00 | 500 | 70.00

# Weekday vs Weekend
DAYTYPE:Weekday | 400000 | 1200000.00 | 15000 | 80.00
DAYTYPE:Weekend | 100000 | 300000.00 | 4000 | 75.00
```

**Format**: TYPE:Period | TotalQuantity | TotalRevenue | TransactionCount | AvgTransactionValue

---

## Business Insights

### Produk Terlaris
- **Metrik**: Total quantity terjual dan jumlah transaksi
- **Insight**: Produk mana yang paling populer dan sering dibeli
- **Action**: Optimasi inventory, fokus marketing, product bundling

### Pola Pelanggan
- **Metrik**: Total spending, frekuensi transaksi, dan lokasi
- **Insight**: Segmentasi customer (VIP vs loyal vs casual)
- **Action**: Customer retention program, targeted marketing

### Distribusi Waktu (Multi-Level)
- **Metrik**: Transaksi dan revenue per bulan, minggu, dan day-type
- **Insight**: 
  - **Monthly**: Peak season, trend pertumbuhan, pola musiman
  - **Weekly**: Minggu dengan performa terbaik, volatilitas penjualan
  - **Day Type**: Perbedaan perilaku weekday vs weekend
- **Action**: 
  - Inventory planning: stock up sebelum peak periods
  - Staffing optimization: adjust workforce berdasarkan patterns
  - Promotional timing: campaign di slow periods untuk boost sales

---

## Web UI Monitoring

- **HDFS Namenode**: http://localhost:9870
- **YARN Resource Manager**: http://localhost:8088
- **DataNode**: http://localhost:9864

---

## Cleanup

```powershell
# Hapus output di HDFS
docker exec namenode hdfs dfs -rm -r /output/*

# Stop cluster
docker-compose down

# Hapus semua (termasuk volumes)
docker-compose down -v
```

---

## Technical Details

**Hadoop Version**: 3.2.1  
**Python Version**: 3.x  
**MapReduce Framework**: Hadoop Streaming  
**Docker Memory**: Minimum 4GB recommended  

**Performance**:
- Per analisis: 10-20 detik
- Total (3 analisis): ~1-2 menit

---

## Troubleshooting

**Output directory exists**:
```powershell
docker exec namenode hdfs dfs -rm -r /output/product_sales
```

**Line ending errors**:
```powershell
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/*.py"
```

**Check job status**:
```powershell
docker exec namenode yarn application -list
```

---

## File Structure

```
OnlineRetail-Hadoop/
├── README.md                           # This file
├── docker-compose.yml                  # Docker orchestration
├── Dockerfile                          # Hadoop image definition
├── Online-Retail.csv                   # Input dataset (541K records)
│
├── mapreduce_scripts/                  # MapReduce analysis scripts
│   ├── product_sales_mapper.py         # Mapper for product analysis
│   ├── product_sales_reducer.py        # Reducer for product analysis
│   ├── customer_pattern_mapper.py      # Mapper for customer analysis
│   ├── customer_pattern_reducer.py     # Reducer for customer analysis
│   ├── time_distribution_mapper.py     # Mapper for time analysis
│   ├── time_distribution_reducer.py    # Reducer for time analysis
│   ├── run_all_analysis.sh             # Automation script
│   └── convert_to_csv.py               # Convert results to CSV
│
├── results/                            # Analysis output (CSV format)
│   ├── product_sales_result.csv        # Product analysis results
│   ├── customer_patterns_result.csv    # Customer analysis results
│   └── time_distribution_result.csv    # Time distribution results
│
└── docs/                               # Documentation
    ├── COMMANDS.md                     # Detailed command reference
    ├── ANALYSIS_REPORT.md              # Executive summary & insights
    └── CSV_GUIDE.md                    # CSV analysis guide
```

---

## Author & License

**Project**: Online Retail Analysis with Hadoop MapReduce  
**Dataset**: UCI Machine Learning Repository - Online Retail Dataset  
**License**: Educational purposes

---

For detailed commands and step-by-step instructions, see [docs/COMMANDS.md](docs/COMMANDS.md)

For business insights and analysis report, see [docs/ANALYSIS_REPORT.md](docs/ANALYSIS_REPORT.md)

For CSV analysis guide, see [docs/CSV_GUIDE.md](docs/CSV_GUIDE.md)
