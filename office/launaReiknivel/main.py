import sqlite3

def ensure_table_exists(db_name, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name=?;
    """, (table_name,))
    result = cursor.fetchone()

    # If the table does not exist, create it
    if not result:
        cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            column1 TEXT,
            column2 INTEGER
        );
        """)
        print(f"Table '{table_name}' created.")
    else:
        print(f"Table '{table_name}' already exists.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Usage example
db_name = "launaReiknivel.db"
table_name = "Kristófer_Orri_Guðmundsson"
ensure_table_exists(db_name, table_name)
