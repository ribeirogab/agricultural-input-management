import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Default growth rate
DEFAULT_GROWTH_RATE = 10


# Function to allow only numbers (integers or floats) in Entry fields
def validate_float_input(new_value):
    if new_value == "":
        return True  # Allow empty input
    try:
        float(new_value)  # Try converting the value to a float
        return True
    except ValueError:
        return False  # If conversion fails, disallow the input


# Function to filter supplies within the last 30 days and calculate daily usage
def filter_recent_supplies(supplies):
    filtered_supplies = {}
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)

    for supply_id, details in supplies.items():
        # Convert the 'created_at' field to a datetime object
        supply_date = datetime.strptime(details["created_at"], "%Y-%m-%d %H:%M:%S")

        # If the supply was created within the last 30 days, include it
        if supply_date >= thirty_days_ago:
            filtered_supplies[supply_id] = details

    return filtered_supplies


# Function to calculate predicted usage based on actual usage over the past 30 days
def calculate_predicted_usage(supplies, growth_rate, waste_rate):
    predictions = {}
    for supply_id, details in supplies.items():
        # Assuming 'quantity' is the total amount used in the last 30 days
        total_used = details["quantity"]

        # Calculate daily usage as the total used divided by 30 days
        daily_usage = total_used / 30 if total_used else 0

        # Apply growth rate to future usage
        future_usage = (daily_usage * 30) * (1 + growth_rate / 100)

        # Add waste rate to future usage
        future_usage = future_usage * (1 + waste_rate / 100)

        predictions[details["name"]] = {
            "Total Used (last 30 days)": total_used,
            "Daily Usage (avg)": round(daily_usage, 2),
            "Predicted Usage (next 30 days)": round(future_usage, 2),
        }

    return predictions


# Function to create and show the modal for supply usage prediction
def show_predict_usage_modal(supplies):
    # Create a modal window to show predictions
    modal = tk.Toplevel()
    modal.title("Predicted Supply Usage")

    # Add title
    tk.Label(modal, text="Predicted Supply Usage", font=("Arial", 18)).pack(pady=10)

    # Add description
    description = (
        "This modal shows the predicted usage of supplies based on the last 30 days.\n"
        "You can adjust the growth rate and waste rate to predict the usage for the next 30 days."
    )
    tk.Label(modal, text=description, wraplength=400, justify="left").pack(pady=10)

    # Labels and Entry for growth rate and waste rate
    tk.Label(modal, text="Growth Rate (%)").pack()
    validate_float = modal.register(validate_float_input)
    entry_growth_rate = tk.Entry(
        modal, validate="key", validatecommand=(validate_float, "%P")
    )
    entry_growth_rate.insert(0, str(DEFAULT_GROWTH_RATE))  # Default growth rate
    entry_growth_rate.pack()

    tk.Label(modal, text="Waste Rate (%)").pack()
    entry_waste_rate = tk.Entry(
        modal, validate="key", validatecommand=(validate_float, "%P")
    )
    entry_waste_rate.insert(0, "0")  # Default waste rate of 0%
    entry_waste_rate.pack()

    # Create a table inside the modal
    tree = ttk.Treeview(
        modal,
        columns=("Name", "Total Used", "Daily Usage", "Predicted Usage"),
        show="headings",
    )
    tree.heading("Name", text="Supply Name")
    tree.heading("Total Used", text="Total Used (last 30 days)")
    tree.heading("Daily Usage", text="Daily Usage (avg)")
    tree.heading("Predicted Usage", text="Predicted Usage (next 30 days)")

    tree.pack(pady=10)

    # Function to update predictions when button is clicked
    def update_predictions():
        try:
            # Get growth and waste rates from inputs
            growth_rate = float(entry_growth_rate.get())
            waste_rate = float(entry_waste_rate.get())

            # Filter supplies to consider only those within the last 30 days
            recent_supplies = filter_recent_supplies(supplies)

            # Calculate predicted usage for filtered supplies
            predictions = calculate_predicted_usage(
                recent_supplies, growth_rate, waste_rate
            )

            # Clear previous rows in the table
            for row in tree.get_children():
                tree.delete(row)

            # Insert new predictions into the table
            for supply_name, data in predictions.items():
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        supply_name,
                        data["Total Used (last 30 days)"],
                        data["Daily Usage (avg)"],
                        data["Predicted Usage (next 30 days)"],
                    ),
                )

        except ValueError:
            tk.messagebox.showerror(
                "Error", "Please enter valid numbers for the rates."
            )

    # Button to update predictions
    tk.Button(modal, text="Update Predictions", command=update_predictions).pack(
        pady=10
    )

    tk.Button(modal, text="Close", command=modal.destroy).pack(pady=10)

    # Call update_predictions initially to populate the table with default values
    update_predictions()
