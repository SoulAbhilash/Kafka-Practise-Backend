from flask_restful import Resource
from flask import request, Response, make_response
from backend.db_interface import Database
from backend.kafka_producers_and_consumers.kafka_producer import KafkaProducerHandler
from backend.common import DecimalEncoder
import json
from decimal import Decimal

class PlaceBet(Resource):

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.kafka_producer = KafkaProducerHandler()

    def _send_to_producer(self, id, user_name, bet_price, product_name):

        message = {
            "id": id, "username": user_name, "bet_price": Decimal(bet_price), "product_name": product_name
        }

        self.kafka_producer.send_message('place_bet', json.dumps(message, cls=DecimalEncoder))

    def post(self):

        data = request.get_json()
        user_name = data.get('username')
        bet_price = data.get('price')
        product_name = data.get('product_name')

        if not all([user_name, bet_price, product_name]):
            return {"error": "Missing required fields"}, 400
        
        response = self.db.insert_product_bet(user_name, bet_price, product_name)

        self._send_to_producer(
            id=response['id'], 
            user_name=response['user_name'], 
            bet_price=response['bet_price'], 
            product_name=response['product_name'])


        status_code = 500 if "error" in response else 201
        return Response(response=response, status=status_code, mimetype='application/json')


if __name__ == '__main__':
    PlaceBet()