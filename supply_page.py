import tkinter as tk
from tkinter import ttk, messagebox
from common import (
    get_current_timestamp,
    import_data_from_json,
    export_data_to_json,
    generate_unique_id,
    refresh_table,
)
from predict_usage_modal import show_predict_usage_modal
from usage_report_modal import show_usage_report_modal
from database import fetch_suppliers, fetch_supplies, save_supplies


# Initial data for supplies and suppliers
supplies = {}
suppliers = {}

# CSV file for supplies and suppliers
SUPPLY_CSV_FILE = "supplies.csv"
SUPPLIER_CSV_FILE = "suppliers.csv"

# Predefined supply names for each type
SUPPLY_TYPES = {
    "Fertilizers": [
        "Ammonium Nitrate",
        "Monoammonium Phosphate (MAP)",
        "Urea",
        "Potassium Sulfate",
        "Organic Fertilizers",
    ],
    "Seeds": [
        "Soybean Seeds",
        "Hybrid Corn Seeds",
        "Cotton Seeds",
        "Wheat Seeds",
        "Barley Seeds",
    ],
}


# Function to load suppliers from the database
def load_suppliers_from_db():
    global suppliers
    supplier_rows = fetch_suppliers()
    suppliers = {row["id"]: row["name"] for row in supplier_rows}


# Function to load supplies from the database
def load_supplies_from_db(tree_supplies):
    supply_rows = fetch_supplies()
    supplies.clear()
    for row in supply_rows:
        supply_id = row["id"]
        supplies[supply_id] = {
            "name": row["name"],
            "quantity": row["quantity"],
            "supplier": row["supplier_id"],
            "type": row["type"],
            "created_at": row["created_at"],
        }
    refresh_supply_table(tree_supplies)


# Function to refresh suppliers in the combobox and show success message
def refresh_suppliers_combobox(combobox_supplier, show_message=False):
    load_suppliers_from_db()
    combobox_supplier["values"] = [
        supplier_name for supplier_name in suppliers.values()
    ]

    if show_message:
        messagebox.showinfo("Success", "Suppliers list refreshed successfully!")


# Function to get supplier ID by name
def get_supplier_id_by_name(supplier_name):
    for supplier_id, name in suppliers.items():
        if name == supplier_name:
            return supplier_id
    return None


# Function to get supplier name by ID
def get_supplier_name_by_id(supplier_id):
    return suppliers.get(supplier_id, "Unknown")


# Function to save supplies to the database with error handling
def save_supplies_to_db(tree_supplies):
    try:
        # Call the function to save supplies to the database
        save_supplies(supplies)
        refresh_supply_table(tree_supplies)
    except Exception:
        # If an error occurs, show an error message with the exception
        messagebox.showerror(
            "Error", "An error occurred while saving supplies, please restart the app."
        )


# Function to register a new supply
def add_supply(supply_name, quantity, supplier_id, supply_type, tree_supplies):
    supplies[generate_unique_id()] = {
        "name": supply_name,
        "quantity": quantity,
        "supplier": supplier_id,
        "type": supply_type,
        "created_at": get_current_timestamp(),
    }
    save_supplies_to_db(tree_supplies)


# Function to export data when the button is clicked
def export_data():
    export_data_to_json(supplies, "supplies")
    messagebox.showinfo("Success", "Data exported successfully!")


# Function to handle the import action
def import_data(tree_supplies):
    try:
        data = import_data_from_json()

        if data:
            for supply_id, details in data.items():
                supplies[supply_id] = {
                    "name": details["name"],
                    "quantity": details["quantity"],
                    "supplier": details["supplier"],
                    "type": details["type"],
                    "created_at": details.get("created_at", get_current_timestamp()),
                }

            # Update the CSV file with the new data
            save_supplies_to_db(tree_supplies)

            messagebox.showinfo("Success", "Data imported successfully!")
    except FileNotFoundError:
        messagebox.showwarning("No File Selected", "Please select a JSON file.")
    except ValueError as ve:
        messagebox.showerror("Invalid JSON", str(ve))
    except RuntimeError as re:
        messagebox.showerror("Error", str(re))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")


# Function to refresh the supply table in the GUI (show supplier name and type)
def refresh_supply_table(tree_supplies):
    table_dict = {}

    for supply_id, details in supplies.items():
        table_dict[supply_id] = {
            "name": details["name"],
            "quantity": details["quantity"],
            "supplier": get_supplier_name_by_id(details["supplier"]),
            "type": details["type"],
            "created_at": details.get("created_at", get_current_timestamp()),
        }

    refresh_table(tree_supplies, table_dict)


# Function to update supply names based on the selected type
def update_supply_names_by_type(combobox_name, combobox_type):
    supply_type = combobox_type.get()
    if supply_type in SUPPLY_TYPES:
        combobox_name["values"] = SUPPLY_TYPES[supply_type]
    else:
        combobox_name["values"] = []


# Function to add a new supply via GUI
def add_supply_gui(
    entry_supply_name, entry_quantity, combobox_supplier, combobox_type, tree_supplies
):
    supply_name = entry_supply_name.get()
    quantity = entry_quantity.get()
    supplier_name = combobox_supplier.get()  # Get supplier name
    supply_type = combobox_type.get()  # Get supply type

    supplier_id = get_supplier_id_by_name(supplier_name)  # Get supplier ID by name

    # Validate if all fields are filled
    if not supply_name or not quantity or not supplier_id or not supply_type:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    add_supply(supply_name, int(quantity), supplier_id, supply_type, tree_supplies)
    clear_supply_fields(
        entry_supply_name, entry_quantity, combobox_supplier, combobox_type
    )


# Function to clear input fields for supplies
def clear_supply_fields(
    entry_supply_name, entry_quantity, combobox_supplier, combobox_type
):
    entry_supply_name.set("")  # Clear combobox for supply names
    entry_quantity.delete(0, tk.END)
    combobox_supplier.set("")  # Clear combobox for suppliers
    combobox_type.set("")  # Clear combobox for types


# Function to validate that only numbers are allowed in the quantity field
def validate_quantity_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False


# Function to create the supply page
def create_supply_page(root):
    frame_supplies = tk.Frame(root)

    # Load suppliers whenever entering the supply page
    load_suppliers_from_db()

    # Title and description
    tk.Label(frame_supplies, text="Supply Management", font=("Arial", 18)).pack(pady=10)
    tk.Label(
        frame_supplies, text="Manage your supplies and track their quantities."
    ).pack(pady=5)

    # Frame for adding new supplies
    frame_add_supplies = tk.Frame(frame_supplies)
    frame_add_supplies.pack(pady=10)

    tk.Label(frame_add_supplies, text="Type:").grid(row=0, column=0)
    combobox_type = ttk.Combobox(
        frame_add_supplies, state="readonly", values=["Fertilizers", "Seeds"]
    )
    combobox_type.grid(row=0, column=1)

    tk.Label(frame_add_supplies, text="Supply Name:").grid(row=1, column=0)
    combobox_name = ttk.Combobox(frame_add_supplies, state="readonly")
    combobox_name.grid(row=1, column=1)

    combobox_type.bind(
        "<<ComboboxSelected>>",
        lambda event: update_supply_names_by_type(combobox_name, combobox_type),
    )

    tk.Label(frame_add_supplies, text="Quantity:").grid(row=2, column=0)
    validate_quantity = root.register(validate_quantity_input)
    entry_quantity = tk.Entry(
        frame_add_supplies, validate="key", validatecommand=(validate_quantity, "%P")
    )
    entry_quantity.grid(row=2, column=1)

    tk.Label(frame_add_supplies, text="Supplier:").grid(row=3, column=0)
    combobox_supplier = ttk.Combobox(frame_add_supplies, state="readonly")
    combobox_supplier.grid(row=3, column=1)

    # Button to refresh the supplier combobox
    btn_refresh_suppliers = tk.Button(
        frame_add_supplies,
        text="Refresh Suppliers",
        command=lambda: refresh_suppliers_combobox(combobox_supplier, True),
    )
    btn_refresh_suppliers.grid(row=3, column=2)

    # Button to add supply
    btn_add_supply = tk.Button(
        frame_add_supplies,
        text="Add Supply",
        command=lambda: add_supply_gui(
            combobox_name,
            entry_quantity,
            combobox_supplier,
            combobox_type,
            tree_supplies,
        ),
    )
    btn_add_supply.grid(row=4, columnspan=2, pady=10)

    # Table for supplies (after the form)
    frame_table_supplies = tk.Frame(frame_supplies)
    frame_table_supplies.pack(pady=10)

    columns_supplies = ("ID", "Name", "Quantity", "Supplier", "Type", "Created At")
    tree_supplies = ttk.Treeview(
        frame_table_supplies, columns=columns_supplies, show="headings"
    )
    tree_supplies.pack()

    for col in columns_supplies:
        tree_supplies.heading(col, text=col)

    # Frame for adding new supplies
    frame_footer_buttons = tk.Frame(frame_table_supplies)
    frame_footer_buttons.pack(pady=10)

    # Button to export data
    btn_export_data = tk.Button(
        frame_footer_buttons,
        text="Export Data (JSON)",
        command=export_data,
    )
    btn_export_data.grid(row=1, column=1, sticky="ew")

    # Button to import data
    btn_import_data = tk.Button(
        frame_footer_buttons,
        text="Import Data (JSON)",
        command=lambda: import_data(tree_supplies),
    )
    btn_import_data.grid(row=1, column=2, sticky="ew")

    # Button to predict supply usage
    btn_predict_usage = tk.Button(
        frame_footer_buttons,
        text="Predict Supply Usage",
        command=lambda: show_predict_usage_modal(supplies),
    )
    btn_predict_usage.grid(row=1, column=3, sticky="ew")

    # Button to generate usage report
    btn_generate_report = tk.Button(
        frame_footer_buttons,
        text="Generate Usage Report",
        command=lambda: show_usage_report_modal(supplies, suppliers),
    )
    btn_generate_report.grid(row=2, column=1, sticky="ew")

    # Load existing supplies from DB
    load_supplies_from_db(tree_supplies)

    # Load the suppliers into the combobox
    refresh_suppliers_combobox(combobox_supplier)

    return frame_supplies
