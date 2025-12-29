# Perintah Lengkap MapReduce dengan Hadoop di Docker

## ANALISIS RETAIL DATA - 3 ANALISIS UTAMA
1. **Produk Terlaris** - Identifikasi produk dengan penjualan tertinggi
2. **Pola Pembelian Pelanggan** - Analisis perilaku customer
3. **Distribusi Transaksi Waktu** - Analisis penjualan per periode

---

## Langkah-langkah dari Awal (Fresh Start)

### 1. Build Docker Image dengan Python
```powershell
docker-compose build
```

### 2. Start Hadoop Cluster (Namenode + Datanode)
```powershell
docker-compose up -d
```

### 3. Tunggu Cluster Siap (30 detik)
```powershell
Start-Sleep -Seconds 30
docker ps
```

### 4. Verifikasi Datanode Terhubung
```powershell
docker exec namenode hdfs dfsadmin -report
```

### 5. Copy File CSV ke Namenode Container
```powershell
docker cp Online-Retail.csv namenode:/tmp/
```

### 6. Copy Semua Mapper & Reducer Scripts ke Container
```powershell
# Original scripts
docker cp mapper.py namenode:/tmp/
docker cp reducer.py namenode:/tmp/

# Analisis Produk Terlaris
docker cp product_sales_mapper.py namenode:/tmp/
docker cp product_sales_reducer.py namenode:/tmp/

# Analisis Pola Pelanggan
docker cp customer_pattern_mapper.py namenode:/tmp/
docker cp customer_pattern_reducer.py namenode:/tmp/

# Analisis Distribusi Waktu
docker cp time_distribution_mapper.py namenode:/tmp/
docker cp time_distribution_reducer.py namenode:/tmp/
```

### 7. Fix Line Ending (Windows ke Unix)
```powershell
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/*.py"
```

### 8. Buat Scripts Executable
```powershell
docker exec namenode bash -c "chmod +x /tmp/*.py"
```

### 9. Buat Direktori Input di HDFS
```powershell
docker exec namenode hdfs dfs -mkdir -p /input
```

### 10. Upload File CSV ke HDFS
```powershell
docker exec namenode hdfs dfs -put /tmp/Online-Retail.csv /input/
```

### 11. Verifikasi File di HDFS
```powershell
docker exec namenode hdfs dfs -ls /input/
```

---

## ANALISIS 1: PRODUK TERLARIS

### 12a. Jalankan MapReduce - Produk Terlaris
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/product_sales_mapper.py,/tmp/product_sales_reducer.py -mapper 'python3 /tmp/product_sales_mapper.py' -reducer 'python3 /tmp/product_sales_reducer.py' -input /input/Online-Retail.csv -output /output/product_sales"
```

### 13a. Lihat TOP 20 Produk Berdasarkan Total Quantity
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/product_sales/part-* | sort -t\$'\t' -k3 -nr | head -20"
```

### 14a. Lihat TOP 20 Produk Berdasarkan Jumlah Transaksi
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/product_sales/part-* | sort -t\$'\t' -k4 -nr | head -20"
```

### 15a. Download Hasil Produk Terlaris
```powershell
docker exec namenode hdfs dfs -get /output/product_sales/part-00000 /tmp/product_sales.txt
docker cp namenode:/tmp/product_sales.txt ./product_sales_result.txt
```

---

## ANALISIS 2: POLA PEMBELIAN PELANGGAN

### 12b. Jalankan MapReduce - Pola Pelanggan
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/customer_pattern_mapper.py,/tmp/customer_pattern_reducer.py -mapper 'python3 /tmp/customer_pattern_mapper.py' -reducer 'python3 /tmp/customer_pattern_reducer.py' -input /input/Online-Retail.csv -output /output/customer_patterns"
```

### 13b. Lihat TOP 20 Pelanggan Berdasarkan Total Spending
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/customer_patterns/part-* | sort -t\$'\t' -k3 -nr | head -20"
```

### 14b. Lihat TOP 20 Pelanggan Berdasarkan Jumlah Transaksi
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/customer_patterns/part-* | sort -t\$'\t' -k5 -nr | head -20"
```

### 15b. Download Hasil Pola Pelanggan
```powershell
docker exec namenode hdfs dfs -get /output/customer_patterns/part-00000 /tmp/customer_patterns.txt
docker cp namenode:/tmp/customer_patterns.txt ./customer_patterns_result.txt
```

---

## ANALISIS 3: DISTRIBUSI TRANSAKSI PER PERIODE (Bulanan, Mingguan, Weekday/Weekend)

### 12c. Jalankan MapReduce - Distribusi Waktu
```powershell
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/time_distribution_mapper.py,/tmp/time_distribution_reducer.py -mapper 'python3 /tmp/time_distribution_mapper.py' -reducer 'python3 /tmp/time_distribution_reducer.py' -input /input/Online-Retail.csv -output /output/time_distribution"
```

### 13c.1. Lihat Distribusi Transaksi Per Bulan
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'MONTHLY:' | sort -t\$'\\t' -k1"
```

### 13c.2. Lihat Distribusi Transaksi Per Minggu
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'WEEKLY:' | sort -t\$'\\t' -k1"
```

### 13c.3. Lihat Perbandingan Weekday vs Weekend
```powershell
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'DAYTYPE:'"
```

### 14c. Download Hasil Distribusi Waktu
```powershell
docker exec namenode hdfs dfs -get /output/time_distribution/part-00000 /tmp/time_distribution.txt
docker cp namenode:/tmp/time_distribution.txt ./time_distribution_result.txt
```

### 14c.1. Extract dan Analisis Spesifik
```powershell
# Extract monthly patterns saja
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'MONTHLY:'" > monthly_analysis.txt

# Extract weekly patterns saja
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'WEEKLY:'" > weekly_analysis.txt

# Extract weekday vs weekend saja
docker exec namenode bash -c "hdfs dfs -cat /output/time_distribution/part-* | grep 'DAYTYPE:'" > daytype_analysis.txt
```

---

## SHORTCUT: Jalankan Semua Analisis Sekaligus

### Option 1: Jalankan Satu per Satu (Manual)
Jalankan perintah 12a-15a, 12b-15b, dan 12c-14c di atas secara berurutan.

### Option 2: Menggunakan Script Otomatis
```powershell
# Copy script ke container
docker cp run_all_analysis.sh namenode:/tmp/
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/run_all_analysis.sh"
docker exec namenode bash -c "chmod +x /tmp/run_all_analysis.sh"

# Jalankan semua analisis
docker exec namenode bash -c "cd /tmp && ./run_all_analysis.sh"

# Download semua hasil
docker cp namenode:/tmp/product_sales.txt ./product_sales_result.txt
docker cp namenode:/tmp/customer_patterns.txt ./customer_patterns_result.txt
docker cp namenode:/tmp/time_distribution.txt ./time_distribution_result.txt
```

---

## Cleanup HDFS Output (Untuk Menjalankan Ulang)

```powershell
# Hapus output analisis produk
docker exec namenode hdfs dfs -rm -r /output/product_sales

# Hapus output analisis pelanggan
docker exec namenode hdfs dfs -rm -r /output/customer_patterns

# Hapus output analisis waktu
docker exec namenode hdfs dfs -rm -r /output/time_distribution

# Hapus semua output sekaligus
docker exec namenode hdfs dfs -rm -r /output/*
```

---

## Command Cleanup (Untuk Mengulang dari Awal)

### Stop dan Hapus Semua Container + Volumes
```powershell
docker-compose down -v
```

### Verifikasi Tidak Ada Container
```powershell
docker ps -a
```

---

## Ringkasan Hasil

### Analisis 1: Produk Terlaris
- **Output**: StockCode | Description | TotalQuantity | TransactionCount
- **Contoh**: `85123A | WHITE HANGING HEART T-LIGHT HOLDER | 15000 | 500`
- **Insight**: Produk mana yang paling banyak terjual dan sering dibeli

### Analisis 2: Pola Pembelian Pelanggan
- **Output**: CustomerID | TotalQuantity | TotalSpending | Country | TransactionCount
- **Contoh**: `17850 | 5000 | 25000.50 | United Kingdom | 150`
- **Insight**: Pelanggan dengan spending tertinggi dan frekuensi pembelian

### Analisis 3: Distribusi Transaksi Waktu (Enhanced)
- **Output Format**: TYPE:Period | TotalQuantity | TotalRevenue | TransactionCount | AvgTransactionValue

**3.1 Analisis Bulanan (Monthly)**
- **Contoh**: `MONTHLY:2010-12 | 50000 | 150000.00 | 2000 | 75.00`
- **Insight**: Tren penjualan per bulan, pertumbuhan month-over-month, identifikasi peak season

**3.2 Analisis Mingguan (Weekly)**
- **Contoh**: `WEEKLY:2010-W49 | 12000 | 35000.00 | 500 | 70.00`
- **Insight**: Pola mingguan, identifikasi minggu dengan performa terbaik, volatilitas penjualan

**3.3 Analisis Weekday vs Weekend**
- **Contoh**: 
  - `DAYTYPE:Weekday | 400000 | 1200000.00 | 15000 | 80.00`
  - `DAYTYPE:Weekend | 100000 | 300000.00 | 4000 | 75.00`
- **Insight**: Perbandingan perilaku pembelian hari kerja vs akhir pekan, staffing optimization

---

## Format Data CSV Input

```
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,12/1/2010 8:26,2.55,17850,United Kingdom
```

**Total Records**: 541,910 transaksi

---

## Ringkasan Files

### Input Files
- `Online-Retail.csv` - Dataset transaksi retail (541K records)

### Analisis 1: Produk Terlaris
- `product_sales_mapper.py` - Extract StockCode, Description, Quantity
- `product_sales_reducer.py` - Aggregate quantity dan hitung transaksi
- **Output**: `product_sales_result.txt`

### Analisis 2: Pola Pelanggan
- `customer_pattern_mapper.py` - Extract CustomerID, spending, country
- `customer_pattern_reducer.py` - Aggregate per customer
- **Output**: `customer_patterns_result.txt`

### Analisis 3: Distribusi Waktu
- `time_distribution_mapper.py` - Extract year-month dari invoice date
- `time_distribution_reducer.py` - Aggregate per periode
- **Output**: `time_distribution_result.txt`

### Legacy Files (Original)
- `mapper.py` - Simple quantity mapper
- `reducer.py` - Simple aggregation reducer

### Infrastructure
- `Dockerfile` - Custom Hadoop image dengan Python 3
- `docker-compose.yml` - Orchestration namenode + datanode
- `run_all_analysis.sh` - Script untuk menjalankan semua analisis

---

## Troubleshooting

### Jika Datanode Tidak Terhubung
Cek environment variable di docker-compose.yml:
```yaml
environment:
  - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
```

### Jika Error "python\r: No such file"
Jalankan command fix line ending:
```powershell
docker exec namenode bash -c "sed -i 's/\r$//' /tmp/*.py"
```

### Jika Output Directory Already Exists
```powershell
# Hapus output directory yang sudah ada
docker exec namenode hdfs dfs -rm -r /output/product_sales
docker exec namenode hdfs dfs -rm -r /output/customer_patterns
docker exec namenode hdfs dfs -rm -r /output/time_distribution
```

### Jika Error Parsing CSV
- Pastikan file CSV menggunakan encoding UTF-8
- Mapper sudah menangani comma dalam description dengan proper parsing

### Debugging MapReduce Job
```powershell
# Cek log aplikasi
docker exec namenode yarn logs -applicationId <application_id>

# Monitor job progress
docker exec namenode yarn application -list

# Cek HDFS health
docker exec namenode hdfs dfsadmin -report
```

---

## Akses Web UI

- **Namenode UI**: http://localhost:9870 - Monitor HDFS
- **Resource Manager**: http://localhost:8088 - Monitor MapReduce jobs
- **DataNode**: http://localhost:9864 - Monitor datanode

---

## Interpretasi Hasil

### 1. Produk Terlaris
**Kolom Output**: StockCode | Description | TotalQuantity | TransactionCount

**Analisis**:
- Produk dengan TotalQuantity tertinggi = best seller by volume
- Produk dengan TransactionCount tertinggi = paling sering dibeli
- Perbedaan keduanya menunjukkan: bulk buyers vs frequent buyers

**Business Value**:
- Inventory management: stock lebih banyak untuk produk populer
- Marketing focus: promosikan produk dengan transaksi tinggi
- Product bundling: gabungkan produk yang sering dibeli

### 2. Pola Pembelian Pelanggan
**Kolom Output**: CustomerID | TotalQuantity | TotalSpending | Country | TransactionCount

**Analisis**:
- High spending customers = VIP/premium customers
- High transaction count = loyal customers
- Average spending per transaction = TotalSpending / TransactionCount

**Business Value**:
- Customer segmentation: VIP program untuk high spenders
- Loyalty program: rewards untuk frequent buyers
- Geographic insights: fokus marketing berdasarkan country

### 3. Distribusi Transaksi Waktu (Multi-Level Analysis)
**Kolom Output**: TYPE:Period | TotalQuantity | TotalRevenue | TransactionCount | AvgTransactionValue

**3.1 Analisis Bulanan (MONTHLY)**
- Identifikasi peak season dan low season
- Trend analysis: pertumbuhan month-over-month
- Seasonality patterns: pola musiman dalam penjualan
- Proyeksi penjualan untuk periode berikutnya

**3.2 Analisis Mingguan (WEEKLY)**
- Identifikasi minggu dengan performa terbaik/terburuk
- Volatilitas penjualan: minggu stabil vs fluktuatif
- Event-driven analysis: pengaruh holiday/special events
- Optimal timing untuk campaign dan promosi

**3.3 Analisis Weekday vs Weekend (DAYTYPE)**
- Perbandingan volume transaksi hari kerja vs akhir pekan
- Perbedaan average transaction value
- Pattern pembelian yang berbeda (bulk buying vs casual shopping)
- Insight untuk staffing dan inventory allocation

**Business Value**:
- Inventory planning: stock up sebelum peak season dan peak weeks
- Staffing optimization: adjust workforce berdasarkan weekday/weekend patterns
- Promotional timing: jalankan campaign di slow months atau low-performing weeks
- Budget allocation: fokus marketing spend di periode high-ROI
- Customer experience: prepare untuk peak times dengan adequate resources

---

## Performance Metrics

**Dataset Size**: 541,910 transaksi
**Estimated MapReduce Time**: 
- Per analisis: 10-20 detik
- Total (3 analisis): 30-60 detik

**Resource Usage**:
- Docker Memory: ~4GB recommended
- Disk Space: ~500MB untuk HDFS blocks
- CPU: 2+ cores recommended

---

## Files yang Dibutuhkan

### Core Infrastructure
1. `Dockerfile` - Custom Hadoop image dengan Python 3
2. `docker-compose.yml` - Orchestration namenode + datanode

### Data
3. `Online-Retail.csv` - Input dataset (541K records)

### Analisis 1: Produk Terlaris
4. `product_sales_mapper.py` - Map phase untuk produk
5. `product_sales_reducer.py` - Reduce phase untuk produk

### Analisis 2: Pola Pelanggan
6. `customer_pattern_mapper.py` - Map phase untuk customer
7. `customer_pattern_reducer.py` - Reduce phase untuk customer

### Analisis 3: Distribusi Waktu
8. `time_distribution_mapper.py` - Map phase untuk waktu
9. `time_distribution_reducer.py` - Reduce phase untuk waktu

### Automation
10. `run_all_analysis.sh` - Bash script untuk menjalankan semua analisis

### Legacy (Optional)
11. `mapper.py` - Simple mapper original
12. `reducer.py` - Simple reducer original

---

**Total Waktu Setup**: ~5 menit (pertama kali)
**Total Waktu Eksekusi**: ~1-2 menit (semua analisis)
