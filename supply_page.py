import tkinter as tk
from tkinter import ttk, messagebox
from common import (
    get_current_timestamp,
    export_data_to_json,
    generate_unique_id,
    load_from_csv,
    save_to_csv,
)

# Initial data for supplies and suppliers
supplies = {}
suppliers = {}

# CSV file for supplies and suppliers
SUPPLY_CSV_FILE = "supplies.csv"
SUPPLIER_CSV_FILE = "suppliers.csv"


# Function to load suppliers from CSV
def load_suppliers():
    global suppliers
    rows = load_from_csv(SUPPLIER_CSV_FILE)
    suppliers = {row["ID"]: row["Name"] for row in rows}


# Function to refresh suppliers in the combobox and show success message
def refresh_suppliers_combobox(combobox_supplier, show_message=False):
    load_suppliers()
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


# Function to load supplies from CSV
def load_supplies_from_csv(tree_supplies):
    rows = load_from_csv(SUPPLY_CSV_FILE)
    for row in rows:
        supply_id = row["ID"]  # Load UUID as ID
        supplies[supply_id] = {
            "name": row["Name"],
            "quantity": int(row["Quantity"]),
            "supplier": row["Supplier"],  # Save the supplier ID
            "created_at": row["Created At"],
        }
    refresh_supply_table(tree_supplies)


# Function to register a new supply
def add_supply(supply_name, quantity, supplier_id):
    supply_id = generate_unique_id()  # Generate a UUID as ID
    created_at = get_current_timestamp()  # Get current timestamp
    supplies[supply_id] = {
        "name": supply_name,
        "quantity": quantity,
        "supplier": supplier_id,  # Save supplier ID
        "created_at": created_at,
    }
    save_supplies_to_csv()


# Function to save supplies to CSV (save supplier ID)
def save_supplies_to_csv():
    headers = ["ID", "Name", "Quantity", "Supplier", "Created At"]
    data = [
        [
            supply_id,
            details["name"],
            details["quantity"],
            details["supplier"],  # Save supplier ID to CSV
            details["created_at"],
        ]
        for supply_id, details in supplies.items()
    ]
    save_to_csv(SUPPLY_CSV_FILE, headers, data)


# Function to export data when the button is clicked
def export_data():
    export_data_to_json(supplies, "supplies")
    messagebox.showinfo("Success", "Data exported successfully!")


# Function to refresh the supply table in the GUI (show supplier name)
def refresh_supply_table(tree_supplies):
    for row in tree_supplies.get_children():
        tree_supplies.delete(row)
    for supply_id, details in supplies.items():
        supplier_name = get_supplier_name_by_id(
            details["supplier"]
        )  # Get supplier name by ID
        tree_supplies.insert(
            "",
            tk.END,
            values=(
                supply_id,
                details["name"],
                details["quantity"],
                supplier_name,  # Display supplier name
                details["created_at"],
            ),
        )


# Function to add a new supply via GUI
def add_supply_gui(
    entry_supply_name,
    entry_quantity,
    combobox_supplier,
    tree_supplies,
):
    supply_name = entry_supply_name.get()
    quantity = entry_quantity.get()
    supplier_name = combobox_supplier.get()  # Get supplier name

    supplier_id = get_supplier_id_by_name(supplier_name)  # Get supplier ID by name

    # Validate if all fields are filled
    if not supply_name or not quantity or not supplier_id:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    add_supply(supply_name, int(quantity), supplier_id)
    refresh_supply_table(tree_supplies)
    clear_supply_fields(entry_supply_name, entry_quantity, combobox_supplier)


# Function to clear input fields for supplies
def clear_supply_fields(entry_supply_name, entry_quantity, combobox_supplier):
    entry_supply_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    combobox_supplier.set("")  # Clear combobox


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
    load_suppliers()

    # Title and description
    tk.Label(frame_supplies, text="Supply Management", font=("Arial", 18)).pack(pady=10)
    tk.Label(
        frame_supplies, text="Manage your supplies and track their quantities."
    ).pack(pady=5)

    # Frame for adding new supplies
    frame_add_supplies = tk.Frame(frame_supplies)
    frame_add_supplies.pack(pady=10)

    tk.Label(frame_add_supplies, text="Supply Name:").grid(row=0, column=0)
    entry_supply_name = tk.Entry(frame_add_supplies)
    entry_supply_name.grid(row=0, column=1)

    tk.Label(frame_add_supplies, text="Quantity:").grid(row=1, column=0)

    # Validation for the quantity field to accept only numbers
    validate_quantity = root.register(validate_quantity_input)
    entry_quantity = tk.Entry(
        frame_add_supplies, validate="key", validatecommand=(validate_quantity, "%P")
    )
    entry_quantity.grid(row=1, column=1)

    tk.Label(frame_add_supplies, text="Supplier:").grid(row=2, column=0)

    # Create a combobox for selecting suppliers (only showing names)
    combobox_supplier = ttk.Combobox(frame_add_supplies, state="readonly")
    combobox_supplier.grid(row=2, column=1)

    # Button to refresh the supplier combobox
    btn_refresh_suppliers = tk.Button(
        frame_add_supplies,
        text="Refresh Suppliers",
        command=lambda: refresh_suppliers_combobox(combobox_supplier, True),
    )
    btn_refresh_suppliers.grid(row=2, column=2)

    # Button to add supply
    btn_add_supply = tk.Button(
        frame_add_supplies,
        text="Add Supply",
        command=lambda: add_supply_gui(
            entry_supply_name,
            entry_quantity,
            combobox_supplier,
            tree_supplies,
        ),
    )
    btn_add_supply.grid(row=3, columnspan=2, pady=10)

    # Table for supplies (after the form)
    frame_table_supplies = tk.Frame(frame_supplies)
    frame_table_supplies.pack(pady=10)

    columns_supplies = ("ID", "Name", "Quantity", "Supplier", "Created At")
    tree_supplies = ttk.Treeview(
        frame_table_supplies, columns=columns_supplies, show="headings"
    )
    tree_supplies.pack()

    for col in columns_supplies:
        tree_supplies.heading(col, text=col)

    # Button to export data
    btn_export_data = tk.Button(
        frame_supplies,
        text="Export Data (JSON)",
        command=export_data,
    )
    btn_export_data.pack(pady=10)

    # Load existing supplies from CSV
    load_supplies_from_csv(tree_supplies)

    # Load the suppliers into the combobox
    refresh_suppliers_combobox(combobox_supplier)

    return frame_supplies
