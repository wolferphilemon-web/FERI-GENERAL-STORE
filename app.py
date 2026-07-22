from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from database import initialize_database

app = Flask(__name__)
app.secret_key = "feri-general-store"

initialize_database()


def get_db_connection():
    connection = sqlite3.connect("store.db")
    connection.row_factory = sqlite3.Row
    return connection


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart


@app.route("/")
def home():
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")

    if category:
        query += " AND lower(category) = ?"
        params.append(category.lower())

    cursor.execute(query, params)
    products = cursor.fetchall()

    connection.close()

    return render_template(
        "index.html",
        products=products,
        search=search,
        category=category,
        cart_count=len(get_cart())
    )
@app.route("/product/<int:product_id>")
def product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    connection.close()

    if product is None:
        return "Product not found", 404

    return render_template("product.html", product=product, cart_count=len(get_cart()))


@app.route("/buy/<int:product_id>")
def buy(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    connection.close()

    if product:
        cart = get_cart()
        cart.append(dict(product))
        save_cart(cart)

    return redirect(url_for("cart_page"))


@app.route("/cart")
def cart_page():
    cart = get_cart()
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total, cart_count=len(cart))


@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    cart = get_cart()
    if 0 <= index < len(cart):
        cart.pop(index)
        save_cart(cart)
    return redirect(url_for("cart_page"))


@app.route("/checkout")
def checkout_page():
    cart = get_cart()
    if not cart:
        return redirect(url_for("cart_page"))
    total = sum(item["price"] for item in cart)
    return render_template("checkout.html", cart=cart, total=total, cart_count=len(cart))


@app.route("/place_order", methods=["POST"])
def place_order():
    cart = get_cart()
    if not cart:
        return redirect(url_for("cart_page"))

    fullname = request.form.get("fullname", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()

    if not all([fullname, phone, address]):
        return redirect(url_for("checkout_page"))

    save_cart([])
    return render_template("order_success.html", fullname=fullname, cart_count=0)


@app.route("/about")
def about_page():
    return render_template("about.html", cart_count=len(get_cart()))


@app.route("/contact")
def contact_page():
    return render_template("contact.html", cart_count=len(get_cart()))


@app.route("/admin")
def admin():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()

    return render_template("admin.html", products=products, cart_count=len(get_cart()))


@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"].strip()
    price = request.form["price"].strip()
    image = request.form["image"].strip()

    if name and price and image:
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
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"].strip()
        price = request.form["price"].strip()
        image = request.form["image"].strip()

        if name and price and image:
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

    return render_template("edit_product.html", product=product, cart_count=len(get_cart()))


if __name__ == "__main__":
    app.run(debug=False)