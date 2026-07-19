from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

cart = []


@app.route("/")
def home():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return render_template("index.html", products=products)


@app.route("/buy/<int:product_id>")
def buy(product_id):
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    connection.close()

    if product:
        cart.append(product)

    return redirect(url_for("cart_page"))


@app.route("/cart")
def cart_page():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)


@app.route("/admin")
def admin():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    connection.close()

    return render_template("admin.html", products=products)


@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = request.form["price"]
    image = request.form["image"]

    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
        (name, price, image)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))


@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    connection = sqlite3.connect("store.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))

    connection.commit()
    connection.close()

    return redirect(url_for("admin"))


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image = request.form["image"]

        cursor.execute(
            "UPDATE products SET name=?, price=?, image=? WHERE id=?",
            (name, price, image, product_id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("admin"))

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()

    connection.close()

    return render_template("edit_product.html", product=product)


if __name__ == "__main__":
    app.run(debug=True)