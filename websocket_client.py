import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://0.0.0.0:8766"

    async with websockets.connect(uri) as websocket:
        # Register a username
        register_message = json.dumps({
            "type": "register",
            "username": "test_user"
        })
        await websocket.send(register_message)
        response = await websocket.recv()
        print(f"Response to registration: {response}")

        # Start message
        start_message = json.dumps({
            "type": "start"
        })
        await websocket.send(start_message)
        response = await websocket.recv()
        print(f"Response to start: {response}")

        # Send a custom message
        custom_message = json.dumps({
            "type": "message",
            "message": "Hello, World!"
        })
        await websocket.send(custom_message)
        response = await websocket.recv()
        print(f"Response to custom message: {response}")

        # Stop message
        stop_message = json.dumps({
            "type": "stop"
        })
        await websocket.send(stop_message)
        response = await websocket.recv()
        print(f"Response to stop: {response}")

        # Receive and print all remaining messages
        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

asyncio.get_event_loop().run_until_complete(test_websocket())
