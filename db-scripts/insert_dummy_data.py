import sqlite3
import uuid

def insert_dummy_data(db_path):
    """Inserts dummy data into the 'invoice' and 'invoice_detail' tables.

    Args:
        db_path (str): The path to the SQLite database file.
    """

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Dummy invoice data
    invoice_data = [
        ('4ce18afe-f33a-4bee-a14c-49180a83e1d7', 'John 117', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('1668b372-32d2-4867-a2ef-7b79558f37e1', 'Jerome 092', '0537-01-01', '2024-02-22 00:56:03.172402', '2024-02-22 00:56:03.172402'),
        ('408630b3-220f-499e-b093-bf7ab21a37b1', 'Cortana', '0552-07-21', '2024-02-22 00:57:50.586866', '2024-02-22 00:57:50.586866'),
        ('63faff60-20f4-49f4-be88-ee7f5540e60a', 'Arbiter', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('e8bb5064-9879-4949-a6a0-76baf70d6ac3', 'Sergeant Avery Johnson', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('86ff4f2c-0130-4f6b-8cd5-68725c5898f1', 'Commander Miranda Keyes', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('dfa9c705-809d-46a3-b2a8-1b7775d5ee5b', 'Gravemind', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('06fb9061-cf44-4df5-9d67-3130652f9b9c', 'Fred-104', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('b885b6f0-710c-497b-be27-92fb9fa0ad91', 'Prophet of Regret', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('80e9923b-e8f7-41d0-884d-971598e24ca4', 'Flood', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('29fd0057-57d4-476c-b293-7209db01fde4', 'Dr. Catherine Halsey', '2024-02-22', '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
    ]

    # Insert invoice data
    for invoice_id, customer_name, invoice_date, created_at, updated_at in invoice_data:
        c.execute("""
            INSERT INTO invoice (id, customer_name, invoice_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (invoice_id, customer_name, invoice_date, created_at, updated_at))

    # Dummy invoice detail data
    invoice_detail_data = [
        ('0240b8f7-167e-4e56-a72a-00fd4006bb8d', '4ce18afe-f33a-4bee-a14c-49180a83e1d7', 'Mjolnir', 1, 5200.0, 5200.0, '2024-02-22 00:54:20.602715', '2024-02-22 00:54:20.602715'),
        ('a18364eb-486e-4314-bcfc-e697b2a07f59', '4ce18afe-f33a-4bee-a14c-49180a83e1d7', 'Assault Rifle', 1, 200.0, 200.0, '2024-02-22 00:54:20.603708', '2024-02-22 00:54:20.603708'),
        ('8abe25e3-0b0e-4e9d-8fbb-536ba0738c12', '1668b372-32d2-4867-a2ef-7b79558f37e1', 'Chair', 1, 2.0, 2.0, '2024-02-22 00:56:03.172402', '2024-02-22 00:56:03.172402'),
        ('7d52335e-e354-4939-8e47-2c97c2af1743', '408630b3-220f-499e-b093-bf7ab21a37b1', 'Master Chief Plushie', 10, 466.0, 4660.0, '2024-02-22 00:57:50.586866', '2024-02-22 00:57:50.586866'),
        ('2d09703d-b8f7-4ec3-8264-b6bff22c6cbd', '63faff60-20f4-49f4-be88-ee7f5540e60a', 'Enerygy Sword', 2, 250.0, 500.0, '2024-02-22 01:55:54.859375', '2024-02-22 01:55:54.859375'),
        ('ab4e0088-a24c-47bd-b0e0-92ae6a7374f4', 'e8bb5064-9879-4949-a6a0-76baf70d6ac3', 'Warthog', 1, 12000.0, 12000.0, '2024-02-22 01:56:30.893956', '2024-02-22 01:56:30.893956'),
        ('111e5638-d60a-44d4-a077-d511af1d7977', '86ff4f2c-0130-4f6b-8cd5-68725c5898f1', 'Pelican', 1, 47000.0, 47000.0, '2024-02-22 01:56:57.142266', '2024-02-22 01:56:57.142266'),
        ('0d3baa30-6074-4ba7-9dca-c49146e788e7', 'dfa9c705-809d-46a3-b2a8-1b7775d5ee5b', 'Cortana', 1, 2.0, 2.0, '2024-02-22 01:58:03.581203', '2024-02-22 01:58:03.581203'),
        ('d742d072-5f39-40f0-bf85-cc45d9fc7634', '06fb9061-cf44-4df5-9d67-3130652f9b9c', 'Elephant Supercarrier', 3, 45620.0, 136860.0, '2024-02-22 01:59:25.293679', '2024-02-22 01:59:25.293679'),
        ('8848a2fb-93f2-4411-9157-789cae5a51bc', 'b885b6f0-710c-497b-be27-92fb9fa0ad91', 'Frag Grenade', 1, 1.0, 1.0, '2024-02-22 02:00:55.485880', '2024-02-22 02:00:55.485880'),
        ('6b35e1a6-2ae2-4672-8740-fb60e092ebaf', '80e9923b-e8f7-41d0-884d-971598e24ca4', 'Living beings', 67000, 22.0, 1474000.0, '2024-02-22 02:01:26.975406', '2024-02-22 02:01:26.975406'),
        ('43bcc35b-fe95-432d-9c75-23a08edbbd3e', '29fd0057-57d4-476c-b293-7209db01fde4', 'Children', 234, 108.0, 25272.0, '2024-02-22 02:02:32.914539', '2024-02-22 02:02:32.914539'),
            ]

    # Insert invoice detail data
    for detail_id, invoice_id, description, quantity, unit_price, price, created_at, updated_at in invoice_detail_data:
        c.execute("""
            INSERT INTO invoice_detail (id, invoice_id, description, quantity, unit_price, price, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (detail_id, invoice_id, description, quantity, unit_price, price, created_at, updated_at))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = "db.sqlite3"  # Replace with your desired database path
    insert_dummy_data(db_path)
    print(f"Dummy data inserted successfully into '{db_path}'")
