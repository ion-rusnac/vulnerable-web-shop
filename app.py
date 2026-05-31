from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash,
)
import sqlite3

app = Flask(__name__)

# Configure session to use default Flask signed cookies
# VULNERABILITY: Weak secret key allows session forgery and exposes session data
app.secret_key = "secret"
app.config["SESSION_PERMANENT"] = False
DATABASE = "shop.db"


def get_db():
    """Open a new connection per call (sqlite3 objects aren't thread-safe)."""
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

@app.context_processor
def inject_balance():
    if "balance" not in session:
        session["balance"] = 0.0
    return dict(user_balance=session["balance"])


# ── Cart helpers ──────────────────────────────────────────────────────


def get_cart():
    """Return the cart list stored in the session (creates it if missing)."""
    if "cart" not in session:
        session["cart"] = []  # list of {"product_id": int, "quantity": int}
    return session["cart"]


def save_cart(cart):
    """Persist the cart back into the session."""
    session["cart"] = cart
    session.modified = True


# ── Routes ────────────────────────────────────────────────────────────


@app.route("/", methods=["GET"])
def index():
    con = get_db()
    products = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return render_template("main.html", products=products)

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/items", methods=["GET"])
@app.route("/items/filter=<category>", methods=["GET"])
def items(category=None):
    con = get_db()
    if category == "articulated":
        products = con.execute("SELECT * FROM products WHERE name LIKE '%Articulated%' OR name LIKE '%Flexi%'").fetchall()
    elif category == "custom":
        products = con.execute("SELECT * FROM products WHERE name LIKE '%Custom%'").fetchall()
    else:
        products = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return render_template("main.html", products=products)


@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):
    cart = get_cart()
    # If product already in cart, increment quantity
    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += 1
            save_cart(cart)
            flash("Item added to cart!", "success")
            return redirect(url_for("index"))
    # Otherwise add new entry
    cart.append({"product_id": product_id, "quantity": 1})
    save_cart(cart)
    flash("Item added to cart!", "success")
    return redirect(url_for("index"))


@app.route("/remove-from-cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = get_cart()
    cart = [item for item in cart if item["product_id"] != product_id]
    save_cart(cart)
    flash("Item removed from cart.", "warning")
    return redirect(url_for("cart"))


@app.route("/update-cart/<int:product_id>/<int:quantity>")
def update_cart(product_id, quantity):
    cart = get_cart()
    if quantity <= 0:
        cart = [item for item in cart if item["product_id"] != product_id]
    else:
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                break
    save_cart(cart)
    return redirect(url_for("cart"))


@app.route("/cart", methods=["GET"])
def cart():
    cart_items = get_cart()
    if not cart_items:
        return render_template("cart.html", personalProducts=[])

    con = get_db()
    # Build a list of product dicts enriched with quantity info
    personalProducts = []
    for entry in cart_items:
        row = con.execute(
            "SELECT * FROM products WHERE id = ?", (entry["product_id"],)
        ).fetchone()
        if row:
            product = dict(row)
            product["quantity"] = entry["quantity"]
            product["line_total"] = row["price"] * entry["quantity"]
            personalProducts.append(product)
    con.close()
    return render_template("cart.html", personalProducts=personalProducts)


@app.route("/wallet", methods=["GET", "POST"])
def wallet():
    if request.method == "POST":
        amount_str = request.form.get("amount", "0")
        card_number = request.form.get("card_number")
        expiry = request.form.get("expiry")
        cvv = request.form.get("cvv")
        
        # Simulate payment processing failure regardless of the input data
        if amount_str and card_number and expiry and cvv:
            flash("Error processing payment: Bank declined the transaction. Please try another card or contact your bank.", "danger")
        else:
            flash("Please provide all required payment details.", "danger")
            
        return redirect(url_for("wallet"))
    
    if "balance" not in session:
        session["balance"] = 0.0
    return render_template("wallet.html", balance=session["balance"])

@app.route("/admin", methods=["GET"])
def admin():
    con = get_db()
    customers = con.execute("SELECT * FROM customers").fetchall()
    orders = con.execute("SELECT * FROM orders").fetchall()
    products = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return render_template(
        "admin.html", customers=customers, orders=orders, products=products
    )


@app.route("/admin/update_product/<int:product_id>", methods=["POST"])
def update_product(product_id):
    price = request.form.get("price", type=float)
    stock = request.form.get("stock", type=int)

    con = get_db()
    con.execute(
        "UPDATE products SET price = ?, stock = ? WHERE id = ?",
        (price, stock, product_id),
    )
    con.commit()
    con.close()

    flash(f"Product #{product_id} updated successfully via backdoor!", "warning")
    return redirect(url_for("admin"))


@app.route("/checkout", methods=["POST"])
def checkout():
    cart_items = get_cart()
    if not cart_items:
        return redirect(url_for("cart"))

    con = get_db()

    # Calculate total
    total = 0
    for entry in cart_items:
        row = con.execute(
            "SELECT price FROM products WHERE id = ?", (entry["product_id"],)
        ).fetchone()
        if row:
            total += row["price"] * entry["quantity"]

    # Check balance from session
    if "balance" not in session:
        session["balance"] = 0.0
    balance = session["balance"]

    if balance < total:
        con.close()
        flash(f"Insufficient funds! You need ${total:.2f} but only have ${balance:.2f}. Please add money to your wallet.", "danger")
        return redirect(url_for("cart"))

    # Deduct balance
    session["balance"] = balance - total
    session.modified = True

    # Create order (customer_id = 1 as placeholder)
    cur = con.execute(
        "INSERT INTO orders (customer_id, status, total) VALUES (?, 'pending', ?)",
        (1, total),
    )
    order_id = cur.lastrowid

    # Create order items
    for entry in cart_items:
        row = con.execute(
            "SELECT price FROM products WHERE id = ?", (entry["product_id"],)
        ).fetchone()
        if row:
            con.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, entry["product_id"], entry["quantity"], row["price"]),
            )

    con.commit()
    con.close()

    # Clear the cart
    save_cart([])

    return render_template("checkout_success.html", order_id=order_id, total=total)
