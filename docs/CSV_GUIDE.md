# Quick Start Guide - CSV Results

## 📊 File CSV yang Dihasilkan

### 1. product_sales_result.csv
**Kolom:**
- `StockCode` - Kode produk
- `Description` - Deskripsi produk
- `TotalQuantity` - Total unit terjual
- `TransactionCount` - Jumlah transaksi

**Cara Analisis:**
- Sort by `TotalQuantity` DESC → Produk paling laku by volume
- Sort by `TransactionCount` DESC → Produk paling sering dibeli
- Filter high quantity + low transaction → Bulk orders
- Filter high transaction + low quantity → Consistent sellers

---

### 2. customer_patterns_result.csv
**Kolom:**
- `CustomerID` - ID pelanggan
- `TotalQuantity` - Total item dibeli
- `TotalSpending` - Total belanja (£)
- `Country` - Negara pelanggan
- `TransactionCount` - Jumlah transaksi

**Cara Analisis:**
- Sort by `TotalSpending` DESC → VIP customers
- Sort by `TransactionCount` DESC → Loyal customers
- Calculate AvgPerTransaction = TotalSpending / TransactionCount
- Group by `Country` → Geographic analysis

**Customer Segmentation:**
- VIP: TotalSpending > £100,000
- Loyal: TransactionCount > 1,000
- Bulk Buyer: High spending, low transaction count
- Casual: Low spending, low frequency

---

### 3. time_distribution_result.csv
**Kolom:**
- `AnalysisType` - Tipe analisis (MONTHLY/WEEKLY/DAYTYPE)
- `Period` - Periode waktu
- `TotalQuantity` - Total item terjual
- `TotalRevenue` - Total pendapatan (£)
- `TransactionCount` - Jumlah transaksi
- `AvgTransactionValue` - Rata-rata nilai transaksi (£)

**Cara Analisis:**
- Filter `AnalysisType = "MONTHLY"` → Trend bulanan
- Filter `AnalysisType = "WEEKLY"` → Analisis mingguan
- Filter `AnalysisType = "DAYTYPE"` → Weekday vs Weekend

**Insights:**
- MONTHLY: Identifikasi peak season & low season
- WEEKLY: Best performing weeks untuk campaign planning
- DAYTYPE: Staffing & operational optimization

---

## 🚀 Cara Membuka di Excel/Google Sheets

### Microsoft Excel:
1. Double-click file `.csv`
2. Atau: File → Open → Browse → Pilih file CSV
3. Data akan otomatis terpisah per kolom

### Google Sheets:
1. File → Import → Upload
2. Pilih file CSV
3. Separator: Comma
4. Click "Import data"

### PowerBI/Tableau:
1. Get Data → Text/CSV
2. Pilih file yang diinginkan
3. Load untuk visualisasi

---

## 📈 Quick Analysis Tips

### Excel Pivot Table:
1. Select data range
2. Insert → PivotTable
3. Drag fields untuk analisis:
   - Rows: Category/Period
   - Values: Sum of Quantity/Revenue
   - Filters: Country/Month

### Excel Charts:
- **Product Sales**: Bar chart (Top 10 products)
- **Monthly Trend**: Line chart (Revenue by month)
- **Country Distribution**: Pie chart (Revenue by country)
- **Weekday vs Weekend**: Column chart comparison

### Filter & Sort:
- Click header → Sort Largest to Smallest
- Use AutoFilter untuk quick filtering
- Conditional formatting untuk highlight values

---

## 🎯 Key Metrics to Track

### Product Performance:
- Top 10 products by quantity
- Top 10 products by transaction count
- Products with single large orders vs frequent small orders

### Customer Analysis:
- Top 20 customers by spending
- Top 20 customers by frequency
- Customer lifetime value (CLV)
- Geographic distribution

### Time Patterns:
- Monthly growth rate
- Peak season identification
- Best performing weeks
- Weekday efficiency vs weekend

---

## 💡 Advanced Analysis Ideas

### 1. Cohort Analysis
Analyze customer retention by first purchase month

### 2. RFM Analysis
- Recency: Last transaction date
- Frequency: Transaction count
- Monetary: Total spending

### 3. Product Association
Which products are often bought together?

### 4. Seasonality Index
Calculate seasonal multipliers for forecasting

### 5. Customer Segmentation
Create customer personas based on behavior

---

## 📝 Sample Excel Formulas

### Average Transaction Value:
```excel
=TotalSpending/TransactionCount
```

### Month-over-Month Growth:
```excel
=(CurrentMonth-PreviousMonth)/PreviousMonth
```

### Rank Products:
```excel
=RANK(TotalQuantity, $Range$, 0)
```

### Conditional Formatting for Top 10:
```excel
=RANK(A2,$A$2:$A$100)<=10
```

---

## 🔍 Data Validation Checks

Before analysis, verify:
- ✓ No empty rows in middle of data
- ✓ Headers are in first row
- ✓ Numbers are formatted as numbers (not text)
- ✓ Dates are in consistent format
- ✓ No duplicate headers

---

## 📞 Need Help?

Refer to:
- `ANALYSIS_REPORT.md` - Executive summary with insights
- `COMMANDS.md` - Hadoop commands reference
- `README.md` - Project overview

---

*Files generated from Hadoop MapReduce analysis*  
*Dataset: 541,910 transactions (Dec 2010 - Dec 2011)*
