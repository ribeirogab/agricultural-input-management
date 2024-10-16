import tkinter as tk
from tkinter import ttk, messagebox
from common import (
    get_current_timestamp,
    import_data_from_json,
    export_data_to_json,
    generate_unique_id,
    is_valid_email,
    refresh_table,
)
from database import fetch_suppliers, save_suppliers

# Initial data for suppliers
suppliers = {}


# Function to load suppliers from DB
def load_suppliers_from_db(tree_suppliers):
    supplier_rows = fetch_suppliers()
    suppliers.clear()
    for row in supplier_rows:
        supplier_id = row["id"]
        suppliers[supplier_id] = {
            "name": row["name"],
            "email": row["email"],
            "created_at": row["created_at"],
        }
    refresh_table(tree_suppliers, suppliers)


# Function to save suppliers to the database with error handling
def save_suppliers_to_db(tree_suppliers):
    try:
        # Call the function to save suppliers to the database
        save_suppliers(suppliers)
        refresh_table(tree_suppliers, suppliers)
    except Exception:
        # If an error occurs, show an error message with the exception
        messagebox.showerror(
            "Error", "An error occurred while saving suppliers, please restart the app."
        )


# Function to register a new supplier
def add_supplier(supplier_name, email, tree_suppliers):
    suppliers[generate_unique_id()] = {
        "name": supplier_name,
        "email": email,
        "created_at": get_current_timestamp(),
    }
    save_suppliers_to_db(tree_suppliers)


# Function to export data when the button is clicked
def export_data():
    export_data_to_json(suppliers, "suppliers")
    messagebox.showinfo("Success", "Data exported successfully!")


# Function to handle the import action
def import_data(tree_suppliers):
    try:
        data = import_data_from_json()

        if data:
            for supplier_id, details in data.items():
                suppliers[supplier_id] = {
                    "name": details["name"],
                    "email": details["email"],
                    "created_at": details.get("created_at", get_current_timestamp()),
                }

            # Update the DB with the new data
            save_suppliers_to_db(tree_suppliers)

            messagebox.showinfo("Success", "Data imported successfully!")
    except FileNotFoundError:
        messagebox.showwarning("No File Selected", "Please select a JSON file.")
    except ValueError as ve:
        messagebox.showerror("Invalid JSON", str(ve))
    except RuntimeError as re:
        messagebox.showerror("Error", str(re))
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")


# Function to add a new supplier via GUI
def add_supplier_gui(entry_supplier_name, entry_supplier_email, tree_suppliers):
    supplier_name = entry_supplier_name.get()
    supplier_email = entry_supplier_email.get()

    # Validate if email is valid
    if not is_valid_email(supplier_email):
        messagebox.showerror("Error", "Invalid email address!")
        return

    if not supplier_name or not supplier_email:
        messagebox.showerror("Error", "All fields must be filled!")
        return

    add_supplier(supplier_name, supplier_email, tree_suppliers)
    clear_supplier_fields(entry_supplier_name, entry_supplier_email)


# Function to clear input fields for suppliers
def clear_supplier_fields(entry_supplier_name, entry_supplier_email):
    entry_supplier_name.delete(0, tk.END)
    entry_supplier_email.delete(0, tk.END)


# Function to create the supplier page
def create_supplier_page(root):
    frame_suppliers = tk.Frame(root)

    # Title and Description
    tk.Label(frame_suppliers, text="Supplier Management", font=("Arial", 18)).pack(
        pady=10
    )
    tk.Label(
        frame_suppliers,
        text="Add and manage your suppliers below.",
    ).pack(pady=5)

    # Frame for adding new suppliers
    frame_add_suppliers = tk.Frame(frame_suppliers)
    frame_add_suppliers.pack(pady=10)

    tk.Label(frame_add_suppliers, text="Supplier Name:").grid(row=0, column=0)
    entry_supplier_name = tk.Entry(frame_add_suppliers)
    entry_supplier_name.grid(row=0, column=1)

    tk.Label(frame_add_suppliers, text="Email:").grid(row=1, column=0)
    entry_supplier_email = tk.Entry(frame_add_suppliers)
    entry_supplier_email.grid(row=1, column=1)

    # Button to add supplier
    btn_add_supplier = tk.Button(
        frame_add_suppliers,
        text="Add Supplier",
        command=lambda: add_supplier_gui(
            entry_supplier_name, entry_supplier_email, tree_suppliers
        ),
    )
    btn_add_supplier.grid(row=2, columnspan=2, pady=10)

    # Table for suppliers (after the form)
    frame_table_suppliers = tk.Frame(frame_suppliers)
    frame_table_suppliers.pack(pady=10)

    columns_suppliers = ("ID", "Name", "Email", "Created At")
    tree_suppliers = ttk.Treeview(
        frame_table_suppliers, columns=columns_suppliers, show="headings"
    )
    tree_suppliers.pack()

    for col in columns_suppliers:
        tree_suppliers.heading(col, text=col)

    # Frame for adding new supplies
    frame_footer_buttons = tk.Frame(frame_table_suppliers)
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
        command=lambda: import_data(tree_suppliers),
    )
    btn_import_data.grid(row=1, column=2, sticky="ew")

    # Load existing suppliers from DB
    load_suppliers_from_db(tree_suppliers)

    return frame_suppliers
