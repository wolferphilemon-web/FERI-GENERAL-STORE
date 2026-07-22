import sqlite3


def initialize_database():
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        image TEXT NOT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

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
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database is ready!")