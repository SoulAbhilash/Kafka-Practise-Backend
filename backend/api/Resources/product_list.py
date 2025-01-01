from flask_restful import Resource
from flask import request, make_response
from backend.db_interface import Database


class ProductList(Resource):

    def __init__(self):
        super().__init__()
        self.db = Database()

    def get(self):
        products = self.db.get_product_list()
        return make_response(products)

if __name__ == '__main__':
    ProductList()