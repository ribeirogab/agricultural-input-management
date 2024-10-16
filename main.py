import tkinter as tk
from supply_page import create_supply_page
from supplier_page import create_supplier_page

# GUI Setup
root = tk.Tk()
root.title("Management Dashboard")

# Menu to switch between pages
menu = tk.Menu(root)
root.config(menu=menu)
main_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Menu", menu=main_menu)

# Create frames for pages
frame_supplies = create_supply_page(root)
frame_suppliers = create_supplier_page(root)

frame_supplies.grid(row=0, column=0, sticky="nsew")
frame_suppliers.grid(row=0, column=0, sticky="nsew")

# Add menu commands to switch pages
main_menu.add_command(label="Supply", command=lambda: frame_supplies.tkraise())
main_menu.add_command(label="Supplier", command=lambda: frame_suppliers.tkraise())

# Show supplies page by default
frame_supplies.tkraise()

# Start the GUI
root.mainloop()
