# Coffee-Shop-Sales-Analysis

A comprehensive data cleaning, analysis, and reporting pipeline for coffee shop sales data.  
This project processes raw sales records, cleans them, analyzes profitability, and generates a detailed business performance report.

---

##  Project Structure

├── coffee_shop_analysis_complete.py # End-to-end analysis pipeline
├── clean_data.py # Standalone cleaning script
├── coffee_shop_sales_cleaned.csv # Example cleaned dataset
├── coffee_shop_analysis_report.txt # Example analysis report
├── requirements.txt # Python dependencies


---

##  Features

### 🔹 Data Cleaning
- Handles missing/invalid dates, times, and numeric values  
- Removes duplicates & outliers  
- Calculates additional features (revenue, profit, time-based fields)  

### 🔹 Profitability Analysis
- Product, category, and store performance metrics  
- Cost estimation using industry-standard ratios  
- Identification of top/bottom performers  

### 🔹 Temporal Analysis
- Monthly trends  
- Daily and hourly performance patterns  
- Peak sales times  

### 🔹 Comprehensive Report
- Executive summary  
- Financial, product, category, and store performance  
- Key insights & recommendations  
- Data quality summary  

---

### **Financial Performance**
| Metric | Value |
|--------|-------|
| Total Revenue | `$658,332.83` |
| Total Estimated Profit | `$408,637.51` |
| Overall Profit Margin | `62.1%` |
| Total Transactions | `147,584` |
| Average Transaction Value | `$4.46` |
| Average Transaction Profit | `$2.77` |

---

### **Top 5 Products by Profit**
| Rank | Product | Profit | Profit Margin |
|------|---------|--------|---------------|
| 1 | Sustainably Grown Organic Lg | $12,691 | 60.0% |
| 2 | Dark chocolate Lg | $12,604 | 60.0% |
| 3 | Latte Rg | $12,423 | 65.0% |
| 4 | Morning Sunrise Chai Lg | $12,169 | 70.0% |
| 5 | Cappuccino Lg | $11,467 | 65.0% |

---

### **Category Performance**
| Category | Revenue | Profit | Margin |
|----------|---------|--------|--------|
| Coffee | $269,952.45 | $175,469.09 | 65.0% |
| Tea | $196,405.95 | $137,484.16 | 70.0% |
| Bakery | $82,315.64 | $32,926.26 | 40.0% |
| Drinking Chocolate | $72,416.00 | $43,449.60 | 60.0% |
| Loose Tea | $11,213.60 | $5,606.80 | 50.0% |

---

### **Store Performance**
| Store | Revenue | Profit | Margin |
|-------|---------|--------|--------|
| Astoria | $220,580.96 | $137,333.66 | 62.3% |
| Hell's Kitchen | $219,666.07 | $136,541.82 | 62.2% |
| Lower Manhattan | $218,085.80 | $134,762.03 | 61.8% |

---

### **Key Insights**
1. Strong profitability with >50% profit margin  
2. Top 3 profit generators: **Sustainably Grown Organic Lg**, **Dark chocolate Lg**, **Latte Rg**  
3. Most profitable category: **Coffee**  
4. Best performing store: **Astoria**  
5. Peak performance: **June**, **Thursdays**, **6:00 AM**  

---
