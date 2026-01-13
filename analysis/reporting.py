#4.1: Generate Comprehensive Text Report

from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    # ---------- BASIC METRICS ----------
    total_revenue = 0
    total_transactions = len(transactions)
    dates = []

    for txn in enriched_transactions:
        total_revenue += txn["Quantity"] * txn["UnitPrice"]
        dates.append(txn["Date"])

    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # ---------- REGION WISE ----------
    region_data = defaultdict(lambda: {"sales": 0, "transactions": 0})

    for txn in enriched_transactions:
        revenue = txn["Quantity"] * txn["UnitPrice"]
        region = txn["Region"]
        region_data[region]["sales"] += revenue
        region_data[region]["transactions"] += 1

    # ---------- PRODUCT PERFORMANCE ----------
    product_data = defaultdict(lambda: {"quantity": 0, "revenue": 0})

    for txn in enriched_transactions:
        product = txn["ProductName"]
        qty = txn["Quantity"]
        revenue = qty * txn["UnitPrice"]
        product_data[product]["quantity"] += qty
        product_data[product]["revenue"] += revenue

    top_products = sorted(
        product_data.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:5]

    # ---------- CUSTOMER PERFORMANCE ----------
    customer_data = defaultdict(lambda: {"spent": 0, "orders": 0})

    for txn in enriched_transactions:
        customer = txn["CustomerID"]
        revenue = txn["Quantity"] * txn["UnitPrice"]
        customer_data[customer]["spent"] += revenue
        customer_data[customer]["orders"] += 1

    top_customers = sorted(
        customer_data.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY SALES ----------
    daily_data = defaultdict(lambda: {"revenue": 0, "transactions": 0, "customers": set()})

    for txn in enriched_transactions:
        date = txn["Date"]
        revenue = txn["Quantity"] * txn["UnitPrice"]
        daily_data[date]["revenue"] += revenue
        daily_data[date]["transactions"] += 1
        daily_data[date]["customers"].add(txn["CustomerID"])

    # ---------- API ENRICHMENT ----------
    enriched_count = sum(1 for t in enriched_transactions if t["API_Match"])
    failed_products = list({t["ProductID"] for t in enriched_transactions if not t["API_Match"]})
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("SALES ANALYTICS REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 40 + "\n")
        for region, data in region_data.items():
            percent = (data["sales"] / total_revenue) * 100 if total_revenue else 0
            f.write(f"{region:<10} ₹{data['sales']:,.0f}   {percent:.2f}%   {data['transactions']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 40 + "\n")
        for i, (product, data) in enumerate(top_products, 1):
            f.write(f"{i}. {product} | Qty: {data['quantity']} | Revenue: ₹{data['revenue']:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 40 + "\n")
        for i, (cust, data) in enumerate(top_customers, 1):
            f.write(f"{i}. {cust} | Spent: ₹{data['spent']:,.2f} | Orders: {data['orders']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 40 + "\n")
        for date, data in sorted(daily_data.items()):
            f.write(f"{date} | ₹{data['revenue']:,.2f} | {data['transactions']} | {len(data['customers'])}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write(f"Products Failed: {failed_products}\n")