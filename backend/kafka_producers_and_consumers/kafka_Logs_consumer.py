import json
import os
import dotenv
from kafka import KafkaConsumer
from datetime import datetime

#backend.kafka_prdoucers_and_consumers.kafka_Logs_consumer

class KafkaLogsConsumerHandler:
    def __init__(self, topic, group_id='bet_consumer'):
        dotenv.load_dotenv()
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[os.getenv('KAFKA_SERVER')],
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v)
        )

        self.logs_file = 'backend/logs/logs.txt'

    def save_logs(self):
        for message in self.consumer:
            print("Received message:", message.value)
            try:
                data = json.loads(message.value)
                username = data.get('username')
                bet_price = data.get('bet_price')
                product_name = data.get('product_name')

                if not all([username, bet_price, product_name]):
                    print("Missing required fields in message:", message.value)
                    continue

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                log_entry = f"{username}[{timestamp}]: product name={product_name}, bet price={bet_price}"

                with open(self.logs_file, mode='a', encoding='utf-8') as file:
                    file.write(log_entry + '\n')

                print(f"Log saved for {username} at {timestamp}")

            except Exception as e:
                print(f"Error processing message: {e}")

if __name__ == '__main__':
    KafkaLogsConsumerHandler('place_bet').save_logs()
