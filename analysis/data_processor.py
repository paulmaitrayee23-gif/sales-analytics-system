#2.1: Sales Summary Calculator
# a)Calculate total revenue

def calculate_total_revenue(transactions):
    total_revenue = 0.0
    for txn in transactions:
        total_revenue += txn["Quantity"]*txn["UnitPrice"]
    return total_revenue


# b) Region wise Sales Analysis

def region_wise_sales(transactions):
    region_data = {}
    grand_total = 0.0

    for txn in transactions:
        region = txn["Region"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        grand_total += amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += amount
        region_data[region]["transaction_count"] += 1

    # add percentage
    for region in region_data:
        percentage =(region_data[region]["total_sales"] / grand_total) * 100
        region_data[region]["percentage"] = round(percentage,2)
        

    # sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_regions

# c) Top Selling Products

def top_selling_products(transactions, n=5):
    product_data = {}

    # Step 1: Aggregate by ProductName
    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    # Step 2: Convert to list of tuples
    product_list = []
    for product, data in product_data.items():
        product_tuple = (product, data["quantity"], data["revenue"])
        product_list.append(product_tuple)
        

    # Step 3: Sort by total quantity sold (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Step 4: Top n products returned
    return product_list[:n]



# d) Customer Purchase Analysis

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns dictionary of customer statistics.
    """

    customer_data = {}

    # Step 1: Aggregate data per customer
    for txn in transactions:
        customer = txn["CustomerID"]
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer]["total_spent"] += quantity * unit_price
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(product)

    # Step 2: Calculate average order value
    for customer, data in customer_data.items():
        data["avg_order_value"] = round(
            data["total_spent"] / data["purchase_count"], 2
        )
        data["products_bought"] = list(data["products_bought"])

    # Step 3: Sort by total_spent (descending)
    customer_data = dict(
        sorted(
            customer_data.items(),
            key=lambda x: x[1]["total_spent"],
            reverse=True
        )
    )

    return customer_data


#2.2: Date Based Analysis
# a) Daily Sales Trend

def daily_sales_trend(transactions):
    daily_data = {}

    for txn in transactions:
        date = txn["Date"]
        customer = txn["CustomerID"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # convert customers set → count
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": daily_data[date]["revenue"],
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result


# b) Find Peak Sales Day

def find_peak_sales_day(transactions):
    daily_sales = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0.0

    for date, data in daily_sales.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date

    return (
        peak_date,
        daily_sales[peak_date]["revenue"],
        daily_sales[peak_date]["transaction_count"]
    )

#2.3: Product Performance
# a) Low performing products

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales.

    Returns:
    List of tuples (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    # Step 1: Aggregate quantity and revenue per product
    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        unit_price = txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += quantity * unit_price

    # Step 2: Filter low performing products
    low_products = []

    for product, data in product_data.items():
        if data["quantity"] < threshold:
            low_products.append(
                (product, data["quantity"], data["revenue"])
            )

    # Step 3: Sort by total quantity (ascending)
    low_products.sort(key=lambda x: x[1])

    return low_products


def perform_all_analysis(transactions, enriched_transactions):
    """
    Runs all analytics and returns a dictionary of results
    """

    results = {}

    # Example placeholders (you can expand later)
    results["total_transactions"] = len(transactions)
    results["total_enriched"] = len(enriched_transactions)

    return results

