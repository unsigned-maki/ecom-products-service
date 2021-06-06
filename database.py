import json
import pymongo
import os
from utils import generate_uid

client = pymongo.MongoClient(os.getenv("MONGO_DB"))
database = client["Ecom"]
categories = database["categories"]
products = database["products"]


class Category:

    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", generate_uid())
        self.id = self.__id
        self.pos = kwargs.get("pos", 0)
        self.title = kwargs.get("title", "Unknown")
        self.products = kwargs.get("products", [])

    @staticmethod
    def from_id(id_):
        result = categories.find({"id": id_})

        if result.count() > 0:
            return CursorCategory(result[0])

        return False

    def patch(self, **kwargs):
        self.pos = kwargs.get("pos", self.pos)
        self.title = kwargs.get("title", self.title)

    def to_dict(self):
        products = list()

        for product in self.products:
            products.append(product.to_dict())

        return {"id": self.__id, "pos": self.pos, "title": self.title, "products": products}

    def serialize(self):
        return json.dumps(self.to_dict)


class CursorCategory(Category):

    def __init__(self, cursor):
        super().__init__(id=cursor["id"], pos=cursor["pos"], title=cursor["title"])

        for product in products.find({"category": self.id}):
            self.products.append(CursorProduct(product))

    def update(self):
        categories.update_many({"id": self.id}, {"$set": {"pos": self.pos, "title": self.title}})

    def remove(self):
        categories.delete_many({"id": self.id})


class NewCategory(CursorCategory):

    def __init__(self, **kwargs):
        uid = generate_uid()

        categories.insert_one({"id": uid,
                               "pos": kwargs.get("pos", 0),
                               "title": kwargs.get("title", "Unknown"),
                               "description": kwargs.get("description", "No description"),
                               "category": kwargs.get("category", "None"),
                               "price": kwargs.get("price", 0),
                               "stock": kwargs.get("stock", 0),
                               "thumbnail": kwargs.get("thumbnail", "None")})

        super().__init__(categories.find_one({"id": uid}))


class Categories:

    @staticmethod
    def to_list():
        category_list = list()

        for category in categories.find():
            category_list.append(CursorCategory(category).to_dict())

        return category_list

    @staticmethod
    def serialize():
        return json.dumps(Categories.to_list())


class Product:

    def __init__(self, **kwargs):
        self.__id = kwargs.get("id", generate_uid())
        self.id = self.__id
        self.pos = kwargs.get("pos", 0)
        self.title = kwargs.get("title", "Unknown")
        self.description = kwargs.get("description", "No description")
        self.category = kwargs.get("category", "None")
        self.price = kwargs.get("price", 0)
        self.stock = kwargs.get("stock", 0)
        self.thumbnail = kwargs.get("thumbnail", "None")
        self.checkout = kwargs.get("checkout", "default")
        self.type = kwargs.get("type", "digital")

    @staticmethod
    def from_id(id_):
        result = products.find({"id": id_})

        if result.count() > 0:
            return CursorProduct(result[0])

        return False

    def patch(self, **kwargs):
        self.pos = kwargs.get("pos", self.pos)
        self.title = kwargs.get("title", self.title)
        self.description = kwargs.get("description", self.description)
        self.category = kwargs.get("category", self.category)
        self.price = kwargs.get("price", self.price)
        self.stock = kwargs.get("stock", self.stock)
        self.thumbnail = kwargs.get("thumbnail", self.thumbnail)
        self.checkout = kwargs.get("checkout", self.checkout)
        self.type = kwargs.get("type", self.type)

    def to_dict(self):
        return {"id": self.__id,
                "pos": self.pos,
                "title": self.title,
                "description": self.description,
                "category": self.category,
                "price": self.price,
                "stock": self.stock,
                "thumbnail": self.thumbnail,
                "checkout": self.checkout,
                "type": self.type}

    def serialize(self):
        return json.dumps(self.to_dict)


class CursorProduct(Product):

    def __init__(self, cursor: pymongo.cursor.Cursor):
        super().__init__(id=cursor["id"],
                         pos=cursor["pos"],
                         title=cursor["title"],
                         description=cursor["description"],
                         category=cursor["category"],
                         price=cursor["price"],
                         stock=cursor["stock"],
                         thumbnail=cursor["thumbnail"],
                         checkout=cursor["checkout"],
                         type=cursor["type"])

    def update(self):
        if self.checkout not in ["default", "external"]:
            self.checkout = "default"

        if self.type not in ["digital", "udigital", "physical"]:
            self.type = "digital"

        products.update_many({"id": self.id}, {"$set": {"pos": self.pos,
                                                        "title": self.title,
                                                        "description": self.description,
                                                        "category": self.category,
                                                        "price": self.price,
                                                        "stock": self.stock,
                                                        "thumbnail": self.thumbnail,
                                                        "checkout": self.checkout,
                                                        "type": self.type}})

    def remove(self):
        products.delete_many({"id": self.id})


class NewProduct(CursorProduct):

    def __init__(self, **kwargs):
        if categories.find({"id": kwargs.get("category", "None")}).count() < 1:
            kwargs["category"] = "None"

        uid = generate_uid()

        if kwargs.get("checkout", "digital") not in ["default", "external"]:
            kwargs["checkout"] = "default"

        if kwargs.get("type", "digital") not in ["digital", "udigital", "physical"]:
            kwargs["type"] = "digital"

        products.insert_one({"id": uid,
                             "pos": kwargs.get("pos", 0),
                             "title": kwargs.get("title", "Unknown"),
                             "description": kwargs.get("description", "No description"),
                             "category": kwargs.get("category", "None"),
                             "price": kwargs.get("price", 0),
                             "stock": kwargs.get("stock", 0),
                             "thumbnail": kwargs.get("thumbnail", "None"),
                             "checkout": kwargs.get("checkout", "default"),
                             "type": kwargs.get("type", "digital")})

        super().__init__(products.find_one({"id": uid}))


class Products:

    @staticmethod
    def to_list():
        product_list = list()

        for product in products.find():
            product_list.append(CursorProduct(product).to_dict())

        return product_list

    @staticmethod
    def serialize():
        return json.dumps(Products.to_list())

