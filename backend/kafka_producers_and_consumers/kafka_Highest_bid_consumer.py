import json
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
from backend.db_interface import Database

class KafkaHihesteBidConsumer:
    def __init__(self, topic):
        load_dotenv()
        self.db = Database()
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=os.getenv("KAFKA_SERVER"),
            group_id="kafka_socket_bridge_group",
            value_deserializer=lambda m: json.loads(m.decode("utf-8"))
        )


    def consume_messages(self):
        try:

            for message in self.consumer:
                print(f"Consuming Kafka message: {message.value}")
                data = json.loads(message.value)

                # payload = {
                #     "data": [
                #         data.get("product_name", "Unknown"),
                #         data.get("bet_price", 0)
                #     ]
                # }

                self.db.insert_highest_bid(
                    id=data.get("id"), 
                    product_name=data.get("product_name"), 
                    bet_price=data.get("bet_price")
                    )


        except Exception as e:
            print(f"Error in consuming messages: {e}")


if __name__ == "__main__":
    KafkaHihesteBidConsumer("place_bet").consume_messages()
