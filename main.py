import json
from datetime import datetime, timedelta

# Initial data
supplies = {}
usage_records = []
suppliers = {}


# Function to register a new supply
def add_supply(supply_name, supply_type, quantity, supplier, expiration_date):
    supplies[supply_name] = {
        "type": supply_type,
        "quantity": quantity,
        "supplier": supplier,
        "expiration_date": expiration_date,
    }


# Function to register the usage of a supply
def register_usage(supply_name, quantity_used, area, date):
    if supply_name in supplies and supplies[supply_name]["quantity"] >= quantity_used:
        supplies[supply_name]["quantity"] -= quantity_used
        usage_records.append(
            {
                "supply": supply_name,
                "quantity_used": quantity_used,
                "area": area,
                "date": date,
            }
        )
    else:
        print("Not enough supply or supply not found.")


# Function to predict future consumption based on past usage
def predict_supply_usage(supply_name, area):
    total_usage = sum(
        [
            record["quantity_used"]
            for record in usage_records
            if record["supply"] == supply_name and record["area"] == area
        ]
    )
    usage_count = len(
        [
            record
            for record in usage_records
            if record["supply"] == supply_name and record["area"] == area
        ]
    )
    if usage_count > 0:
        avg_usage = total_usage / usage_count
        print(f"Predicted usage for {supply_name} in {area}: {avg_usage:.2f} units.")
    else:
        print(f"No data available to predict usage for {supply_name} in {area}.")


# Function to check supply levels
def check_stock_levels(minimum_level):
    for supply, details in supplies.items():
        if details["quantity"] <= minimum_level:
            print(
                f"Low stock alert for {supply}. Current quantity: {details['quantity']}."
            )


# Function to generate a report of supply usage
def generate_usage_report(start_date, end_date):
    report = [
        record for record in usage_records if start_date <= record["date"] <= end_date
    ]
    if report:
        for entry in report:
            print(
                f"Supply: {entry['supply']}, Quantity used: {entry['quantity_used']}, Area: {entry['area']}, Date: {entry['date']}"
            )
    else:
        print("No records found for the specified period.")


# Function to export data to a JSON file
def export_data(filename):
    data = {
        "supplies": supplies,
        "usage_records": usage_records,
        "suppliers": suppliers,
    }
    with open(filename, "w") as file:
        json.dump(data, file)
    print(f"Data exported to {filename}.")


# Function to import data from a JSON file
def import_data(filename):
    global supplies, usage_records, suppliers
    with open(filename, "r") as file:
        data = json.load(file)
        supplies = data["supplies"]
        usage_records = data["usage_records"]
        suppliers = data["suppliers"]
    print(f"Data imported from {filename}.")


# Function to check the usage history of a supply in a specific area
def check_usage_history(area):
    history = [record for record in usage_records if record["area"] == area]
    if history:
        for entry in history:
            print(
                f"Supply: {entry['supply']}, Quantity used: {entry['quantity_used']}, Date: {entry['date']}"
            )
    else:
        print(f"No usage history for area {area}.")


# Function to add a supplier
def add_supplier(name, contact, supplied_items):
    suppliers[name] = {"contact": contact, "supplied_items": supplied_items}


# Function to alert if a supply is near expiration
def check_expiration_alert(days_before_expiration):
    today = datetime.now().date()
    for supply, details in supplies.items():
        expiration_date = datetime.strptime(
            details["expiration_date"], "%Y-%m-%d"
        ).date()
        if expiration_date <= (today + timedelta(days=days_before_expiration)):
            print(
                f"Expiration alert for {supply}. Expiration date: {details['expiration_date']}."
            )


# Function to show a general dashboard of the system
def show_dashboard():
    print("Supplies in stock:")
    for supply, details in supplies.items():
        print(
            f"Supply: {supply}, Quantity: {details['quantity']}, Expiration: {details['expiration_date']}"
        )

    print("\nLow stock alerts:")
    check_stock_levels(50)

    print("\nExpiration alerts:")
    check_expiration_alert(30)
