# 📁 Repository Index - Quick Navigation

## 🚀 Getting Started

1. **First Time Setup**: Read [README.md](README.md)
2. **Run Analysis**: Follow [docs/COMMANDS.md](docs/COMMANDS.md)
3. **View Results**: Check [results/](results/) folder

---

## 📊 Analysis Results (CSV Format)

All results are in CSV format for easy analysis in Excel/Google Sheets:

- [results/product_sales_result.csv](results/product_sales_result.csv) - Top selling products
- [results/customer_patterns_result.csv](results/customer_patterns_result.csv) - Customer behavior
- [results/time_distribution_result.csv](results/time_distribution_result.csv) - Time patterns

**How to use**: See [docs/CSV_GUIDE.md](docs/CSV_GUIDE.md)

---

## 📖 Documentation

### For Users:
- [README.md](README.md) - Project overview & quick start
- [docs/ANALYSIS_REPORT.md](docs/ANALYSIS_REPORT.md) - Executive summary with business insights
- [docs/CSV_GUIDE.md](docs/CSV_GUIDE.md) - How to analyze CSV files

### For Developers:
- [docs/COMMANDS.md](docs/COMMANDS.md) - Complete Hadoop command reference
- [mapreduce_scripts/](mapreduce_scripts/) - MapReduce source code
- [Dockerfile](Dockerfile) - Hadoop container configuration
- [docker-compose.yml](docker-compose.yml) - Cluster orchestration

---

## 🔧 MapReduce Scripts

Location: [mapreduce_scripts/](mapreduce_scripts/)

**Product Analysis:**
- `product_sales_mapper.py` - Extract product data
- `product_sales_reducer.py` - Aggregate product sales

**Customer Analysis:**
- `customer_pattern_mapper.py` - Extract customer data
- `customer_pattern_reducer.py` - Aggregate customer patterns

**Time Distribution:**
- `time_distribution_mapper.py` - Extract time patterns
- `time_distribution_reducer.py` - Aggregate by monthly/weekly/daytype

**Utilities:**
- `run_all_analysis.sh` - Run all analyses at once
- `convert_to_csv.py` - Convert results to CSV format

---

## 🎯 Quick Commands

### Run Single Analysis
```powershell
# Product Sales
docker exec namenode bash -c "hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /tmp/product_sales_mapper.py,/tmp/product_sales_reducer.py -mapper 'python3 /tmp/product_sales_mapper.py' -reducer 'python3 /tmp/product_sales_reducer.py' -input /input/Online-Retail.csv -output /output/product_sales"
```

### View Results
```powershell
# View in terminal
docker exec namenode bash -c "hdfs dfs -cat /output/product_sales/part-* | head -20"

# Download to local
docker exec namenode hdfs dfs -get /output/product_sales/part-00000 /tmp/product_sales.txt
docker cp namenode:/tmp/product_sales.txt ./results/
```

### Convert to CSV
```powershell
python mapreduce_scripts/convert_to_csv.py
```

---

## 📂 Project Structure

```
OnlineRetail-Hadoop/
├── 📄 README.md                    ← Start here
├── 📄 INDEX.md                     ← This file
├── 🐳 docker-compose.yml
├── 🐳 Dockerfile
├── 📊 Online-Retail.csv            ← Input data (541K records)
│
├── 📁 mapreduce_scripts/           ← Analysis code
│   ├── *_mapper.py
│   ├── *_reducer.py
│   ├── run_all_analysis.sh
│   └── convert_to_csv.py
│
├── 📁 results/                     ← Output CSV files
│   ├── product_sales_result.csv
│   ├── customer_patterns_result.csv
│   └── time_distribution_result.csv
│
└── 📁 docs/                        ← Documentation
    ├── COMMANDS.md                 ← Detailed commands
    ├── ANALYSIS_REPORT.md          ← Business insights
    └── CSV_GUIDE.md                ← CSV analysis guide
```

---

## 🆘 Troubleshooting

**Problem**: Container won't start
- **Solution**: Check [docs/COMMANDS.md](docs/COMMANDS.md) - Troubleshooting section

**Problem**: Output directory exists
- **Solution**: `docker exec namenode hdfs dfs -rm -r /output/product_sales`

**Problem**: Need to re-run analysis
- **Solution**: Delete output folder first, then re-run

**Problem**: Can't open CSV
- **Solution**: Try opening with Excel/Google Sheets, see [docs/CSV_GUIDE.md](docs/CSV_GUIDE.md)

---

## 📞 Need Help?

1. Check [docs/COMMANDS.md](docs/COMMANDS.md) for complete command reference
2. Read [docs/CSV_GUIDE.md](docs/CSV_GUIDE.md) for analysis tips
3. Review [docs/ANALYSIS_REPORT.md](docs/ANALYSIS_REPORT.md) for insights examples

---

## 📊 Key Metrics at a Glance

From the analysis results:

- **541,910** total transactions analyzed
- **4,740** unique products
- **4,339** unique customers
- **13 months** of data (Dec 2010 - Dec 2011)
- **Peak season**: November 2011 (£1.5M revenue)
- **Best week**: Week 49 of 2011 (£529K revenue)
- **Weekday dominance**: 91.7% of revenue from Mon-Fri

See full report: [docs/ANALYSIS_REPORT.md](docs/ANALYSIS_REPORT.md)

---

*Last updated: December 29, 2025*
