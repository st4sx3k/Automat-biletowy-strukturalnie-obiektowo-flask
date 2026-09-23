from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, "prices.json")

with open(JSON_FILE, encoding="utf-8") as f:
    prices = json.load(f)

cart = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bilety")
def bilety():
    discount = request.args.get("discount")
    ticket_type = request.args.get("type")

    available = prices.get(discount, {}).get(ticket_type, {})

    return render_template(
        "bilety.html",
        discount=discount,
        ticket_type=ticket_type,
        tickets=available
    )


@app.route("/dodaj", methods=["POST"])
def dodaj():
    discount = request.form["discount"]
    ticket_type = request.form["ticket_type"]
    name = request.form["name"]
    quantity = int(request.form["quantity"])

    price = prices[discount][ticket_type][name]

    cart.append({
        "discount": discount,
        "type": ticket_type,
        "name": name,
        "price": price,
        "quantity": quantity
    })

    return redirect(url_for("kasa"))


@app.route("/kasa")
def kasa():
    total = sum(
        item["price"] * item["quantity"]
        for item in cart
    )

    return render_template(
        "kasa.html",
        cart=cart,
        total=total
    )


@app.route("/wyczysc")
def wyczysc():
    cart.clear()
    return redirect(url_for("kasa"))


if __name__ == "__main__":
    app.run(debug=True)