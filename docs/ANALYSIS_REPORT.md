# Online Retail Analysis - Executive Summary Report

## Dataset Overview
- **Period**: December 2010 - December 2011
- **Total Transactions**: 541,910 records
- **Date Generated**: December 29, 2025

---

## 1. Product Sales Analysis

### Top 10 Best Selling Products (by Quantity)

| Rank | Stock Code | Description | Total Quantity | Transaction Count |
|------|------------|-------------|----------------|-------------------|
| 1 | 23843 | PAPER CRAFT , LITTLE BIRDIE | 80,995 | 1 |
| 2 | 23166 | MEDIUM CERAMIC TOP STORAGE JAR | 78,033 | 250 |
| 3 | 84077 | WORLD WAR 2 GLIDERS ASSTD DESIGNS | 55,047 | 537 |
| 4 | 85099B | JUMBO BAG RED RETROSPOT | 48,478 | 2,115 |
| 5 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 37,603 | 2,260 |
| 6 | 22197 | POPCORN HOLDER | 36,761 | 829 |
| 7 | 84879 | ASSORTED COLOUR BIRD ORNAMENT | 36,461 | 1,489 |
| 8 | 21212 | PACK OF 72 RETROSPOT CAKE CASES | 36,419 | 1,370 |
| 9 | 23084 | RABBIT NIGHT LIGHT | 30,788 | 1,036 |
| 10 | 22492 | MINI PAINT SET VINTAGE | 26,633 | 380 |

**Key Insights:**
- Product #23843 (PAPER CRAFT) sold 80,995 units but only in 1 transaction (likely a bulk order)
- Product #85123A (WHITE HANGING HEART T-LIGHT HOLDER) has highest frequency with 2,260 transactions
- Products with high transaction counts are more consistent sellers

**Data File**: `product_sales_result.csv` (4,740 unique products)

---

## 2. Customer Behavior Analysis

### Top 10 Customers by Total Spending

| Rank | Customer ID | Total Quantity | Total Spending (£) | Country | Transaction Count |
|------|-------------|----------------|-------------------|---------|-------------------|
| 1 | 14646 | 197,491 | 280,206.02 | Netherlands | 2,080 |
| 2 | 18102 | 64,124 | 259,657.30 | United Kingdom | 431 |
| 3 | 17450 | 69,993 | 194,550.79 | United Kingdom | 337 |
| 4 | 16446 | 80,997 | 168,472.50 | United Kingdom | 3 |
| 5 | 14911 | 80,515 | 143,825.06 | EIRE | 5,677 |
| 6 | 12415 | 77,670 | 124,914.53 | Australia | 716 |
| 7 | 14156 | 57,885 | 117,379.63 | EIRE | 1,400 |
| 8 | 17511 | 64,549 | 91,062.38 | United Kingdom | 963 |
| 9 | 16029 | 40,208 | 81,024.84 | United Kingdom | 242 |
| 10 | 12346 | 74,215 | 77,183.60 | United Kingdom | 1 |

**Key Insights:**
- Top customer (ID: 14646) from Netherlands spent £280,206 across 2,080 transactions
- Customer #14911 from EIRE has highest loyalty with 5,677 transactions
- Customer #16446 spent £168,472 in only 3 transactions (£56,157 per transaction - likely B2B)
- UK customers dominate the top spenders list

**Customer Segmentation:**
- **VIP Customers**: Top 1% by spending (£100K+) - require premium service
- **Loyal Customers**: High transaction count (1000+) - target for loyalty programs
- **Bulk Buyers**: High spending, low frequency - B2B opportunities

**Data File**: `customer_patterns_result.csv` (4,339 unique customers)

---

## 3. Time Distribution Analysis

### 3.1 Monthly Sales Performance

| Month | Total Quantity | Total Revenue (£) | Transactions | Avg Transaction (£) |
|-------|----------------|-------------------|--------------|---------------------|
| 2010-12 | 362,316 | 823,746.14 | 41,683 | 19.76 |
| 2011-01 | 397,716 | 691,364.56 | 34,350 | 20.13 |
| 2011-02 | 286,695 | 523,631.89 | 27,184 | 19.26 |
| 2011-03 | 384,950 | 717,639.36 | 35,915 | 19.98 |
| 2011-04 | 312,176 | 537,808.62 | 29,171 | 18.44 |
| 2011-05 | 399,425 | 770,536.02 | 36,292 | 21.23 |
| 2011-06 | 394,337 | 761,739.90 | 36,056 | 21.13 |
| 2011-07 | 407,539 | 719,221.19 | 38,716 | 18.58 |
| 2011-08 | 425,016 | 737,014.26 | 34,566 | 21.32 |
| 2011-09 | 575,416 | 1,058,590.17 | 49,323 | 21.46 |
| 2011-10 | 628,745 | 1,154,979.30 | 59,396 | 19.45 |
| **2011-11** | **771,598** | **1,509,496.33** | **83,498** | **18.08** |
| 2011-12 | 315,052 | 638,792.68 | 25,135 | 25.41 |

**Peak Season:** November 2011
- Revenue: £1,509,496 (highest)
- Transactions: 83,498 (highest)
- Items sold: 771,598 (highest)

**Low Season:** February 2011
- Revenue: £523,632 (lowest)
- Transactions: 27,184 (lowest)

### 3.2 Weekday vs Weekend Analysis

| Day Type | Total Quantity | Total Revenue (£) | Transactions | Avg Transaction (£) | % of Total |
|----------|----------------|-------------------|--------------|---------------------|------------|
| **Weekday** | 5,189,972 | 9,830,732.81 | 467,375 | 21.03 | **91.7%** |
| Weekend | 471,009 | 813,827.61 | 63,910 | 12.73 | 8.3% |

**Key Insights:**
- Weekdays account for 91.7% of total revenue
- Weekday average transaction value is 65% higher (£21.03 vs £12.73)
- Suggests B2B business model or office-hour shopping preference
- Weekend shoppers are more casual/leisure buyers

### 3.3 Weekly Performance (Top 5 Weeks)

| Week | Revenue (£) | Transactions | Avg Transaction (£) |
|------|-------------|--------------|---------------------|
| 2011-W49 | 528,931.36 | 19,490 | 27.14 |
| 2011-W46 | 387,633.79 | 20,481 | 18.93 |
| 2011-W45 | 378,921.39 | 19,420 | 19.51 |
| 2010-W49 | 344,382.69 | 17,510 | 19.67 |
| 2011-W47 | 330,859.65 | 20,474 | 16.16 |

**Data File**: `time_distribution_result.csv` (68 time periods analyzed)

---

## Business Recommendations

### 1. Inventory Management
- **Action**: Increase stock for top 20 products (especially #85123A with 2,260 transactions)
- **Timing**: Build inventory in Q3 (Aug-Sep) for Q4 peak season
- **Priority**: November is peak month - prepare 2-3 months in advance

### 2. Customer Relationship Management
- **VIP Program**: Focus on top 50 customers (£50K+ spending) - personalized service
- **Loyalty Rewards**: Target customers with 500+ transactions
- **B2B Opportunities**: Identify and nurture bulk buyers (high value, low frequency)

### 3. Marketing Strategy
- **Peak Season Campaigns**: Run major campaigns in September-October to maximize November sales
- **Off-Peak Promotions**: Boost February-April sales with targeted promotions
- **Weekday Focus**: Allocate 90% of marketing budget to weekday campaigns
- **Weekend Special**: Create weekend-specific offers to boost casual shopping

### 4. Operational Planning
- **Staffing**: Increase workforce in Q4, especially November
- **Warehouse**: Expand capacity before peak season
- **Working Hours**: Optimize for weekday operations (consider extended hours Mon-Fri)

### 5. Revenue Optimization
- **Cross-selling**: Bundle frequently bought products
- **Premium Products**: Focus on items with high transaction value
- **International Expansion**: Netherlands and EIRE show high spending - explore expansion

---

## Technical Details

**Analysis Method**: Hadoop MapReduce (Distributed Computing)
**Cluster**: Docker-based Hadoop 3.2.1
**Processing Time**: ~1-2 minutes for 541K records
**Output Format**: CSV with headers for easy analysis

**Generated Files:**
1. `product_sales_result.csv` - Product performance data
2. `customer_patterns_result.csv` - Customer behavior data
3. `time_distribution_result.csv` - Time-based patterns

---

## Data Quality Notes

- Records processed: 541,910 transactions
- Valid transactions: ~530K (98% data quality)
- Unique products: 4,740
- Unique customers: 4,339
- Time period: 13 months (Dec 2010 - Dec 2011)

---

*Report generated by Hadoop MapReduce Analysis*  
*Date: December 29, 2025*
