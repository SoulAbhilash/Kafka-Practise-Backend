from kafka import KafkaProducer
from backend.common import DecimalEncoder
import json
from os import getenv

#backend.kafka_prducers_and_consumers.kafka_producer
class KafkaProducerHandler:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[getenv("KAFKA_SERVER")],
            value_serializer=lambda v: json.dumps(v, cls=DecimalEncoder).encode('utf-8')
        )

    def send_message(self, topic, message):
        print("Producer sending message: ", message)
        self.producer.send(topic, message)
        self.producer.flush()

        
if __name__ == "__main__":
    KafkaProducerHandler()