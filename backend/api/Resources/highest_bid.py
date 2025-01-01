from flask_restful import Resource
from flask import request, make_response, jsonify
from backend.db_interface import Database
import json
from backend.common import DecimalEncoder, DecimalDecoder


class HighestBid(Resource):

    def __init__(self):
        super().__init__()
        self.db = Database()

    def get(self):
        product_name = request.args.get('product_name')  # Get product_name from query parameters
        if product_name:
            product_data = self.db.get_single_product_highest_bid(product_name)
            print(f"Single Product data: {product_data}")
            if not product_data:
                return {"message": f"Product '{product_name}' not found"}, 404
            return jsonify(product_data)
        
        # If product_name is not provided, return all products
        else:
            all_products_data = self.db.get_all_highest_bids()
            return json.dumps(all_products_data, cls=DecimalEncoder)

if __name__ == '__main__':
    HighestBid()