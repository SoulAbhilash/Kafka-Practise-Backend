from flask import Flask, jsonify, request, make_response
from flask_restful import Api
from dotenv import load_dotenv
from .Resources.place_bet import PlaceBet
from .Resources.highest_bid import HighestBid
from .Resources.product_list import ProductList
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from backend.db_interface import Database
# from flask_sslify import SSLify


# ---------------------------------------------- INITIALIZATIONS -------------------------------#
app = Flask(__name__)
api = Api(app)
CORS(app)
# sslify = SSLify(app)
socketio = SocketIO(app, cors_allowed_origins="*")
load_dotenv()
db = Database()
# ----------------------------------------------------------------------------------------------#

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Welcome to Flask WebSocket!'}, broadcast=True)

@socketio.on('message')
def handle_message(json):
    print(f"Received message: {json}")
    if "data" in json:
        product_name, bid_price = json["data"]
        print(f"Product: {product_name}, Bid: {bid_price}")
        emit('message', {'data': f"Received your bid for {product_name} with bid {bid_price}"}, broadcast=True)
    else:
        print("Invalid message format received.")

def highest_bid_event_listener():
    while notify:=db.highest_bid_trigger_listener():
        with app.app_context():
            socketio.emit('db_update', notify)




api.add_resource(PlaceBet, '/place-bet')
api.add_resource(HighestBid, '/highest-bet')
api.add_resource(ProductList, '/product-list')


if __name__ == '__main__':
    from threading import Thread
    listener_thread = Thread(target=highest_bid_event_listener)
    listener_thread.daemon = True
    listener_thread.start()
    # app.run(host='localhost', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, log_output=True)
