import socketio
import dotenv
import json
from os import getenv
from backend.common import DecimalEncoder
import asyncio

class SocketManager:
    def __init__(self):
        dotenv.load_dotenv()
        self.sio = socketio.AsyncClient(ssl_verify=False, request_timeout=10)

    async def connect(self):
        try:
            await self.sio.connect(getenv("SERVER_URL"))
            print("Connected to Flask server")
        except Exception as e:
            print(f"Connection failed: {e}")

    async def send_live_message_to_server(self, payload):
        try:
            log = {"data": list(payload)}
            print(f"Sending message to Flask server: {log}")
            await self.sio.emit(event='new_bid', data={"data": "hi"})
            print(f"Sent highest bid to Flask: {log}")
        except Exception as e:
            print(f"Error sending message: {e}")
        # await self.disconnect()

    async def disconnect(self):
        try:
            await self.sio.disconnect()
            print("Disconnected from Flask server")
        except Exception as e:
            print(f"Error during disconnect: {e}")

if __name__ == "__main__":
    socket_manager = SocketManager()
    asyncio.run(socket_manager.connect())
    # To send a message, you can call `send_live_message_to_server` like:
    # asyncio.run(socket_manager.send_live_message_to_server(payload))
