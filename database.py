import oracledb
from common import generate_unique_id, get_current_timestamp

# Database connection settings
username = "dbuser"
password = "dbpass"
dsn = "localhost:1521/EIS"

# Connect to the Oracle database
connection = oracledb.connect(
    user=username, password=password, dsn=dsn, mode=oracledb.DEFAULT_AUTH
)


# Function to fetch all suppliers from the database
def fetch_suppliers():
    cursor = connection.cursor()
    query = "SELECT id, name, email, created_at FROM supplier"
    cursor.execute(query)
    suppliers = []
    for row in cursor:
        suppliers.append(
            {"id": row[0], "name": row[1], "email": row[2], "created_at": row[3]}
        )
    cursor.close()
    return suppliers


# Function to fetch all supplies from the database
def fetch_supplies():
    cursor = connection.cursor()
    query = "SELECT id, name, quantity, supplier_id, type, created_at FROM supply"
    cursor.execute(query)
    supplies = []
    for row in cursor:
        supplies.append(
            {
                "id": row[0],
                "name": row[1],
                "quantity": row[2],
                "supplier_id": row[3],
                "type": row[4],
                "created_at": row[5],
            }
        )
    cursor.close()
    return supplies


# Function to upsert many supplies in the database with rollback on error
def save_supplies(supplies):
    cursor = connection.cursor()

    try:
        # For each supply in the dictionary, perform the UPSERT operation
        for supply_id, details in supplies.items():
            # Ensure created_at is in the correct format (assume it's already a string in 'YYYY-MM-DD HH24:MI:SS' format)
            created_at = details.get("created_at", get_current_timestamp())

            query = """
                MERGE INTO supply s
                USING (SELECT :1 AS id, :2 AS name, :3 AS quantity, :4 AS supplier_id, :5 AS type, TO_DATE(:6, 'YYYY-MM-DD HH24:MI:SS') AS created_at FROM dual) incoming
                ON (s.id = incoming.id)
                WHEN MATCHED THEN
                    UPDATE SET s.name = incoming.name, s.quantity = incoming.quantity, s.supplier_id = incoming.supplier_id, s.type = incoming.type, s.created_at = incoming.created_at
                WHEN NOT MATCHED THEN
                    INSERT (s.id, s.name, s.quantity, s.supplier_id, s.type, s.created_at)
                    VALUES (incoming.id, incoming.name, incoming.quantity, incoming.supplier_id, incoming.type, incoming.created_at)
            """

            cursor.execute(
                query,
                [
                    supply_id,
                    details["name"],
                    details["quantity"],
                    details["supplier"],
                    details["type"],
                    created_at,
                ],
            )

        # Commit all changes to the database if no errors occur
        connection.commit()

    except Exception as e:
        # If an error occurs, rollback the transaction
        connection.rollback()
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception to propagate it up the stack

    finally:
        # Close the cursor after the operation is complete
        cursor.close()


# Function to upsert many suppliers in the database with rollback on error
def save_suppliers(suppliers):
    cursor = connection.cursor()

    try:
        # For each supplier in the dictionary, perform the INSERT or UPDATE operation
        for supplier_id, details in suppliers.items():
            created_at = details.get("created_at", get_current_timestamp())

            # UPSERT supplier (Insert if not exists, otherwise update)
            query = """
                MERGE INTO supplier s
                USING (SELECT :1 AS id, :2 AS name, :3 AS email, TO_DATE(:4, 'YYYY-MM-DD HH24:MI:SS') AS created_at FROM dual) incoming
                ON (s.id = incoming.id)
                WHEN MATCHED THEN
                    UPDATE SET s.name = incoming.name, s.email = incoming.email, s.created_at = incoming.created_at
                WHEN NOT MATCHED THEN
                    INSERT (s.id, s.name, s.email, s.created_at)
                    VALUES (incoming.id, incoming.name, incoming.email, incoming.created_at)
            """

            cursor.execute(
                query,
                [
                    supplier_id,
                    details["name"],
                    details["email"],
                    created_at,
                ],
            )

        # Commit all changes to the database if no errors occur
        connection.commit()

    except Exception as e:
        # Rollback if any error occurs
        connection.rollback()
        print(f"An error occurred while saving suppliers: {e}")
        raise  # Re-raise the exception to propagate it

    finally:
        # Ensure the cursor is closed after operation
        cursor.close()
