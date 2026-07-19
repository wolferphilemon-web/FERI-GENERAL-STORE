import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    image TEXT NOT NULL
)
""")

# Check if products already exist
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

# Add sample products only if the table is empty
if count == 0:
    cursor.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        ("T-Shirt", 800, "tshirt.jpg")
    )

    cursor.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        ("Jeans", 2000, "jeans.jpg")
    )

    cursor.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        ("Hoodie", 2500, "hoodie.jpg")
    )

connection.commit()
cursor.execute("SELECT * FROM products")

rows = cursor.fetchall()

print(rows)
connection.close()

print("Database is ready!")