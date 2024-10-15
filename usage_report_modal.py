import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from collections import defaultdict


# Helper function to calculate usage statistics
def calculate_usage(supplies, suppliers):
    usage_by_type = defaultdict(int)
    usage_by_name = defaultdict(int)
    usage_by_supplier = defaultdict(int)
    usage_by_month = defaultdict(int)
    usage_by_day = defaultdict(int)

    today = datetime.now()
    last_month = today - timedelta(days=30)
    last_3_months = today - timedelta(days=90)

    for supply_id, details in supplies.items():
        supply_name = details["name"]
        supply_type = details.get("type", "Unknown")
        supplier_id = details["supplier"]
        supplier_name = suppliers.get(supplier_id, "Unknown")
        quantity = details["quantity"]

        # Convert the 'created_at' field to a datetime object
        supply_date = datetime.strptime(details["created_at"], "%Y-%m-%d %H:%M:%S")

        # Usage by type
        usage_by_type[supply_type] += quantity

        # Usage by name
        usage_by_name[supply_name] += quantity

        # Usage by supplier
        usage_by_supplier[supplier_name] += quantity

        # Usage by day (last month)
        if supply_date >= last_month:
            day_key = supply_date.strftime("%Y-%m-%d")
            usage_by_day[day_key] += quantity

        # Usage by month (last 3 months)
        if supply_date >= last_3_months:
            month_key = supply_date.strftime("%Y-%m")
            usage_by_month[month_key] += quantity

    # Sorting by most recent date for month and day
    usage_by_month = sorted(
        usage_by_month.items(),
        key=lambda x: datetime.strptime(x[0], "%Y-%m"),
        reverse=True,
    )
    usage_by_day = sorted(
        usage_by_day.items(),
        key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"),
        reverse=True,
    )

    return (
        sorted(usage_by_type.items(), key=lambda x: x[1], reverse=True),
        sorted(usage_by_name.items(), key=lambda x: x[1], reverse=True),
        sorted(usage_by_supplier.items(), key=lambda x: x[1], reverse=True),
        usage_by_month,
        usage_by_day,
    )


# Function to create and show the modal for usage report
def show_usage_report_modal(supplies, suppliers):
    # Calculate usage statistics
    usage_by_type, usage_by_name, usage_by_supplier, usage_by_month, usage_by_day = (
        calculate_usage(supplies, suppliers)
    )

    # Create a modal window to show the report
    modal = tk.Toplevel()
    modal.title("Usage Report")

    # Add description
    description = (
        "This report shows the usage data for supplies based on different categories.\n"
        "The data is sorted from most used to least used."
    )
    tk.Label(modal, text=description, wraplength=500, justify="left").pack(pady=10)

    # Create notebook (tabs) to organize report sections
    notebook = ttk.Notebook(modal)
    notebook.pack(pady=10, fill="both", expand=True)

    # Helper function to populate tables
    def create_table(tab, data, columns):
        tree = ttk.Treeview(tab, columns=columns, show="headings")

        # Configure columns with center alignment
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center")  # Center the data in each column

        for item in data:
            tree.insert("", tk.END, values=item)
        tree.pack(fill="both", expand=True)

    # Usage by type tab
    tab_type = ttk.Frame(notebook)
    notebook.add(tab_type, text="Usage by Type")
    create_table(tab_type, usage_by_type, ("Type", "Total Used"))

    # Usage by name tab
    tab_name = ttk.Frame(notebook)
    notebook.add(tab_name, text="Usage by Supply")
    create_table(tab_name, usage_by_name, ("Supply Name", "Total Used"))

    # Usage by supplier tab
    tab_supplier = ttk.Frame(notebook)
    notebook.add(tab_supplier, text="Usage by Supplier")
    create_table(tab_supplier, usage_by_supplier, ("Supplier Name", "Total Used"))

    # Usage by month tab
    tab_month = ttk.Frame(notebook)
    notebook.add(tab_month, text="Usage by Month")
    create_table(tab_month, usage_by_month, ("Month", "Total Used"))

    # Usage by day tab (last month)
    tab_day = ttk.Frame(notebook)
    notebook.add(tab_day, text="Usage by Day (Last Month)")
    create_table(tab_day, usage_by_day, ("Day", "Total Used"))

    # Close button
    tk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)
