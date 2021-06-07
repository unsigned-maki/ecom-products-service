import json
import database
from flask import Flask, request

app = Flask(__name__)


def not_found():
    return json.dumps({"success": False, "code": 404, "message": "Not Found"})


def method_not_allowed():
    return json.dumps({"success": False, "code": 405, "message": "Method Not Allowed"})


def ok():
    return json.dumps({"success": True, "code": 200, "message": "OK"})


@app.route("/category", methods=["GET", "POST"])
def category_handler():
    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "categories": database.Categories.to_list()})
    elif request.method == "POST":
        database.NewCategory(**request.form)
        return ok()
    else:
        return method_not_allowed()


@app.route("/category/<id_>", methods=["GET", "PATCH", "DELETE"])
def category_handler_id(id_):
    category = database.Category.from_id(id_)

    if not category:
        return not_found()

    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "product": category.to_dict()})
    elif request.method == "PATCH":
        category.patch(**request.form)
        category.update()
        return ok()
    elif request.method == "DELETE":
        category.remove()
        return ok()
    else:
        return method_not_allowed()


@app.route("/product", methods=["GET", "POST"])
def product_handler():
    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "products": database.Products.to_list()})
    elif request.method == "POST":
        database.NewProduct(**request.form)
        return ok()
    else:
        return method_not_allowed()


@app.route("/product/<id_>", methods=["GET", "PATCH", "DELETE"])
def product_handler_id(id_):
    product = database.Product.from_id(id_)
    
    if not product:
        return not_found()

    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "product": product.to_dict()})
    elif request.method == "PATCH":
        product.patch(**request.form)
        product.update()
        return ok()
    elif request.method == "DELETE":
        product.remove()
        return ok()
    else:
        return method_not_allowed()


@app.route("/item", methods=["GET", "POST"])
def item_handler():
    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "products": database.Items.to_list()})
    elif request.method == "POST":
        database.NewItem(**request.form)
        return ok()
    else:
        return method_not_allowed()


@app.route("/item/<id_>", methods=["GET", "PATCH", "DELETE"])
def item_handler_id(id_):
    item = database.Item.from_id(id_)
    
    if not item:
        return not_found()

    if request.method == "GET":
        return json.dumps({"success": True, "code": 200, "message": "OK", "product": item.to_dict()})
    elif request.method == "PATCH":
        item.patch(**request.form)
        item.update()
        return ok()
    elif request.method == "DELETE":
        item.remove()
        return ok()
    else:
        return method_not_allowed()

if __name__ == '__main__':
    app.run()
