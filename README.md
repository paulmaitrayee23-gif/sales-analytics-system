# Sales Analytics System

## Overview
This project simulates a Sales Analytics System for an e-commerce company.  
It reads raw sales data from a file, cleans and validates the records, performs multiple sales analyses, enriches the data using an external API, and finally generates a comprehensive sales report.

The project is modular, easy to understand, and follows proper Python project structure.

---

##  Project Structure

```text
sales-analytics-system/
│
├── analysis/
│   ├── data_processor.py        # Data cleaning, validation & analysis
│   ├── reporting.py             # Report generation logic
│   └── _init_.py
│
├── data/
│   ├── sales_data.txt           # Raw sales data (provided)
│   ├── enriched_sales_data.txt  # API-enriched sales data (generated)
│   ├── api_handler.py           # DummyJSON API integration
│   └── _init_.py
│
├── utils/
│   ├── file_handler.py          # File read/write utilities
│   └── _init_.py
│
├── output/
│   └── sales_report.txt         # Final analytics report
│
├── main.py                      # Main execution script
├── requirements.txt             # External dependencies
└── README.md
```
---

##  Features Implemented

### 1. Data Cleaning & Validation
- Removes empty lines
- Cleans numeric fields with commas (e.g., 1,500 → 1500)
- Validates required fields
- Tracks valid and invalid records
- Prints validation summary as required

### 2. Sales Analysis
- Total revenue calculation
- Region-wise sales performance
- Top-selling products
- Customer purchase analysis
- Daily sales trend
- Peak sales day identification
- Low-performing products detection

### 3. API Integration
- Integrates DummyJSON API
- Fetches product details
- Enriches sales data with API information
- Tracks successful and failed product enrichments

### 4. Report Generation
- Generates a structured sales report
- Includes overall summary, trends, top products, customers, and API enrichment summary
- Saves report to output/sales_report.txt

---

## 5. How to Run the Project

1. Make sure Python 3.10+ is installed
2. Navigate to the project root directory
3. Run the main script:

python main.py

---

##  Output Files

- data/enriched_sales_data.txt → Cleaned & API-enriched sales data
- output/sales_report.txt → Final analytics report

---

##  Dependencies

Only standard libraries and one external library are used:

requests

Install it using:

pip install requests

---


