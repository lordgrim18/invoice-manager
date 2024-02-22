import sqlite3
import uuid

def create_tables(db_path):
    """Creates the 'invoice' and 'invoice_detail' tables in an SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
    """

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create the 'invoice' table
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoice (
            id TEXT PRIMARY KEY UNIQUE,
            customer_name TEXT NOT NULL,
            invoice_date DATE NOT NULL
        )
    """)

    # Create the 'invoice_detail' table
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoice_detail (
            id TEXT PRIMARY KEY UNIQUE,
            invoice_id TEXT NOT NULL REFERENCES invoice(id) ON DELETE CASCADE,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            price REAL NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = "db.sqlite3"  # Replace with your desired database path
    create_tables(db_path)
    print(f"Tables created successfully in '{db_path}'")