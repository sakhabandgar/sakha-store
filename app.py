from flask import Flask, render_template, session, redirect
import csv
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"

# ---------------- LOAD DATA ----------------
def load_data():
    with open("dataset.csv", newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    data = load_data()

    # unique products only
    products = {}
    for d in data:
        if d["product"] not in products:
            products[d["product"]] = d

    return render_template("index.html", products=products.values())

# ---------------- PRODUCT PAGE ----------------
@app.route("/product/<name>")
def product(name):
    data = load_data()

    selected = None
    related = []

    # find selected product
    for d in data:
        if d["product"] == name:
            selected = d

            # find related products
            for r in data:
                if r["product"] == d["related_product"]:
                    related.append(r)

    return render_template("product.html",
                           product=selected,
                           related=related)

# ---------------- ADD TO CART ----------------
@app.route("/add/<name>")
def add(name):
    data = load_data()

    product = next((d for d in data if d["product"] == name), None)

    if product is None:
        return "Product not found", 404

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(product)
    session.modified = True

    return redirect("/cart")

# ---------------- CART PAGE ----------------
@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(int(i["price"]) for i in cart)

    return render_template("cart.html",
                           cart=cart,
                           total=total)

# ---------------- REMOVE ITEM ----------------
@app.route("/remove/<name>")
def remove(name):
    cart = session.get("cart", [])

    cart = [i for i in cart if i["product"] != name]

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")

# ---------------- RUN (IMPORTANT FOR RENDER) ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)