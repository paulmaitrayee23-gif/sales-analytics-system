import pandas as pd

def read_sales_data(filename):
    """
    Reads sales data from a file while handling encoding issues.
    Returns a list of raw data lines (strings).
    """
    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            raise FileNotFoundError("Sales data file not found.")
    else:
        raise UnicodeDecodeError("Unable to decode file with supported encodings.")

    # Remove header and empty lines
    cleaned_lines = []
    for line in lines[1:]:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines


def parse_transactions(raw_lines):
    """
    Parses raw sales data lines into a list of cleaned dictionaries.
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        if len(parts) != 8:
            continue

        try:
            transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

            quantity = int(quantity.replace(",", ""))
            unit_price = float(unit_price.replace(",", ""))

            transaction = {
                "TransactionID": transaction_id,
                "Date": date,
                "ProductID": product_id,
                "ProductName": product_name,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "CustomerID": customer_id,
                "Region": region
            }

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns valid transactions, invalid count, and summary.
    """
    valid_transactions = []
    invalid_count = 0

    filtered_by_region = 0
    filtered_by_amount = 0

    for txn in transactions:
        try:
            if (
                txn["Quantity"] <= 0
                or txn["UnitPrice"] <= 0
                or not txn["TransactionID"].startswith("T")
                or not txn["ProductID"].startswith("P")
                or not txn["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            amount = txn["Quantity"] * txn["UnitPrice"]

            if region and txn["Region"] != region:
                filtered_by_region += 1
                continue

            if min_amount and amount < min_amount:
                filtered_by_amount += 1
                continue

            if max_amount and amount > max_amount:
                filtered_by_amount += 1
                continue

            valid_transactions.append(txn)

        except KeyError:
            invalid_count += 1

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }
    print(f"Total records parsed: {len(transactions)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")


    return valid_transactions, invalid_count, summary




                