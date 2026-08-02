import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.json")


def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)


def get_product_by_name(name):
    products = load_products()

    for product in products:
        if product["name"] == name:
            return product

    return None


def delete_product(name):
    products = load_products()

    new_products = []

    for product in products:
        if product["name"] != name:
            new_products.append(product)

    save_products(new_products)


def update_product(old_name, new_name, product_type, price):
    products = load_products()

    for product in products:
        if product["name"] == old_name:
            product["name"] = new_name
            product["type"] = product_type
            product["price"] = price

    save_products(products)
