import sqlite3

db_path = "db.sqlite3"  # Replace with your actual database path
conn = sqlite3.connect(db_path)
c = conn.cursor()

invoice_query = """
    SELECT * FROM invoice_detail
"""
c.execute(invoice_query)
invoice_data = c.fetchall()

# Print or process the invoice data
for invoice in invoice_data:
    print(invoice)

conn.close()
