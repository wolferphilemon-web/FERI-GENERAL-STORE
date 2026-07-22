import sqlite3

connection = sqlite3.connect("store.db")
cursor = connection.cursor()

cursor.execute("UPDATE products SET category='Men' WHERE name='tshirt'")
cursor.execute("UPDATE products SET category='Men' WHERE name='Jeans'")
cursor.execute("UPDATE products SET category='Men' WHERE name='Hoodie'")
cursor.execute("UPDATE products SET category='Shoes' WHERE TRIM(name)='jordan4'")

connection.commit()

cursor.execute("SELECT name, category FROM products")
for row in cursor.fetchall():
    print(row)

connection.close()

print("Done!")