from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from analysis.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from data.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from analysis.reporting import generate_sales_report


def main():
    try:
        print("=" * 50)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 50)

        # 1. Read sales data
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")

        # 2. Parse transactions
        print("[2/10] Parsing transactions...")
        transactions = parse_transactions(raw_data)

        # 3. Validate transactions
        print("[3/10] Validating transactions...")
        valid_transactions, invalid_count, validation_summary = validate_and_filter(transactions)

        # 4. Perform analysis
        print("[4/10] Performing sales analysis...")

        total_revenue = calculate_total_revenue(valid_transactions)
        region_sales = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions)
        customer_stats = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions)

        # 5. Fetch API products
        print("[5/10] Fetching product data from API...")
        products = fetch_all_products()
        product_mapping = create_product_mapping(products)

        # 6. Enrich sales data
        print("[6/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        # 7. Save enriched data
        print("[7/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)

        # 8. Generate report
        print("[8/10] Generating report...")
        generate_sales_report(
            valid_transactions,
            enriched_transactions
        )

        print("[10/10] Process Complete!")
        print("=" * 50)

    except Exception as e:
        print("An error occurred:")
        print(e)


if __name__ == "__main__":
    main()