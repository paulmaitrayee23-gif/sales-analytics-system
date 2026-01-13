#3.1: Fetch Product Details

import requests

# 3.1 Fetch products from API
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # SAFETY CHECK (this fixes your error)
        if isinstance(data, dict):
            products = data.get("products", [])
        elif isinstance(data, list):
            products = data
        else:
            products = []

        print(f"Products fetched successfully: {len(products)}")
        return products

    except Exception as e:
        print("Failed to fetch products:", e)
        return []


# 3.1 Create product mapping
def create_product_mapping(api_products):
    product_map = {}

    for product in api_products:
        product_id = product.get("id")

        if product_id is None:
            continue

        product_map[product_id] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_map


# 3.2 Enrich Sales Data
def enrich_sales_data(transactions, product_mapping):
    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        product_id_str = txn.get("ProductID", "")
        numeric_id = None

        if isinstance(product_id_str, str) and product_id_str.startswith("P"):
            try:
                numeric_id = int(product_id_str[1:])
            except ValueError:
                numeric_id = None

        product_info = product_mapping.get(numeric_id)

        if product_info:
            enriched_txn["API_Category"] = product_info.get("category")
            enriched_txn["API_Brand"] = product_info.get("brand")
            enriched_txn["API_Rating"] = product_info.get("rating")
            enriched_txn["API_Match"] = True
        else:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    return enriched_transactions


# 3.3 Save Enriched Data
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    if not enriched_transactions:
        print("No enriched data to save.")
        return

    headers = enriched_transactions[0].keys()

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for txn in enriched_transactions:
            row = []
            for header in headers:
                value = txn.get(header)
                row.append("" if value is None else str(value))
            file.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")