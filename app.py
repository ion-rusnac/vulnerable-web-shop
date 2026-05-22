from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ── Product catalogue ──────────────────────────────────────────────────
# Each dict mirrors what was previously hard-coded in main.html.
#   • badge        – optional label shown on the card (e.g. "Hot", "New", "Limited")
#   • badge_color  – Bootstrap bg- class for the badge
#   • rating       – number of filled stars (0 = no stars shown)
#   • action       – button label ("Add to Cart" or "Configure")

products = [
    {
        "name": "Articulated Dragon",
        "price": 35.00,
        "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Articulated Crystal Dragon",
        "badge": None,
        "badge_color": None,
        "rating": 0,
        "action": "Add to Cart",
    },
    {
        "name": "Flexi Octopus",
        "price": 15.00,
        "image": "https://images.unsplash.com/photo-1558060370-d644479cb6f7?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Flexi Octopus",
        "badge": "Hot",
        "badge_color": "bg-primary",
        "rating": 5,
        "action": "Add to Cart",
    },
    {
        "name": "Low-Poly T-Rex",
        "price": 22.00,
        "image": "https://images.unsplash.com/photo-1532330393533-443990a51d10?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Low-Poly T-Rex",
        "badge": None,
        "badge_color": None,
        "rating": 0,
        "action": "Add to Cart",
    },
    {
        "name": "Custom D&D Mini",
        "price": 45.00,
        "image": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Custom D&D Mini",
        "badge": None,
        "badge_color": None,
        "rating": 5,
        "action": "Configure",
    },
    {
        "name": "Robot Explorer",
        "price": 28.00,
        "image": "https://images.unsplash.com/photo-1566131444841-9442f360c704?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Robot Action Figure",
        "badge": "New",
        "badge_color": "bg-dark",
        "rating": 0,
        "action": "Add to Cart",
    },
    {
        "name": "Puzzle Cube",
        "price": 18.00,
        "image": "https://images.unsplash.com/photo-1587654538522-6bcd2483b1db?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Puzzle Cube",
        "badge": None,
        "badge_color": None,
        "rating": 0,
        "action": "Add to Cart",
    },
    {
        "name": "Spaceship Model",
        "price": 55.00,
        "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Spaceship Model",
        "badge": "Limited",
        "badge_color": "bg-primary",
        "rating": 5,
        "action": "Add to Cart",
    },
    {
        "name": "Medieval Castle",
        "price": 75.00,
        "image": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Medieval Castle Set",
        "badge": None,
        "badge_color": None,
        "rating": 0,
        "action": "Add to Cart",
    },
]
personalProducts = [
    {
        "name": "Articulated Dragon",
        "price": 35.00,
        "image": "https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&q=80&w=450&h=300",
        "alt": "Articulated Crystal Dragon",
        "badge": None,
        "badge_color": None,
        "rating": 0,
        "action": "Add to Cart",
    },
]


@app.route("/", methods=["GET"])
def index():
    return render_template("main.html", products=products)


@app.route("/cart", methods=["GET"])
def cart():
    return render_template("cart.html", personalProducts=personalProducts)
