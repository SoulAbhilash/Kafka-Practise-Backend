import socketio

sio = socketio.AsyncClient()

async def connect_and_send():
    await sio.connect("http://localhost:5000")
    await sio.emit('kafka_message', {'data': 'Test bid message'})
    await sio.wait()

sio.event
async def on_connect():
    print("Connected to Flask Server")

sio.event
async def on_message(data):
    print(f"Received message from server: {data}")

import asyncio
asyncio.run(connect_and_send())
