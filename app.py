from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os


app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")


# подключение папки css
@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('css', filename)


def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)



def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)



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



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    products = load_products()

    product = next(
        (p for p in products if p["id"] == id),
        None
    )


    if product is None:
        return "Товар не знайдено"


    if request.method == "POST":

        product["name"] = request.form["name"]
        product["type"] = request.form["type"]
        product["price"] = request.form["price"]

        save_products(products)

        return redirect(url_for("index"))


    return render_template(
        "edit.html",
        product=product
    )



@app.route("/delete/<int:id>")
def delete(id):

    products = load_products()

    products = [
        p for p in products
        if p["id"] != id
    ]

    save_products(products)

    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)