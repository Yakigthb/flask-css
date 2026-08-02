from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

from action_db import (
    load_products,
    save_products,
    get_product_by_name,
    delete_product,
    update_product
)


app = Flask(__name__)



@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('css', filename)
@app.route("/")
def index():
    products = load_products()

    return render_template(
        "index.html",
        products=products
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        products = load_products()

        product = {
            "id": len(products) + 1,
            "name": request.form["name"],
            "type": request.form["type"],
            "price": request.form["price"]
        }

        products.append(product)
        save_products(products)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<path:name>", methods=["GET", "POST"])
def edit(name):
    product = get_product_by_name(name)

    if product is None:
        return "товар не найден", 404

    if request.method == "POST":
        new_name = request.form["name"]
        product_type = request.form["type"]
        price = request.form["price"]

        update_product(name, new_name, product_type, price)

        return redirect(url_for("index"))

    return render_template(
        "edit.html",
        product=product
    )


@app.route("/delete/<path:name>")
def delete(name):
    product = get_product_by_name(name)

    if product is None:
        return "товар не найден", 404

    delete_product(name)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
