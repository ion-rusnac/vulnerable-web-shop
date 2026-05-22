from flask import Flask, render_template, request, jsonify
from flask_session import Session
import random
import sqlite3

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
DATABASE = "shop.db"


def get_db():
    """Open a new connection per call (sqlite3 objects aren't thread-safe)."""
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


# ── Routes ────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    con = get_db()
    products = con.execute("SELECT * FROM products").fetchall()
    con.close()
    return render_template("main.html", products=products)


@app.route("/cart", methods=["GET"])
def cart():
    con = get_db()
    personalProducts = con.execute("SELECT * FROM products LIMIT 1").fetchall()
    con.close()
    return render_template("cart.html", personalProducts=personalProducts)
