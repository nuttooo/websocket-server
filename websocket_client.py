import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:8766"
    try:
        async with websockets.connect(uri) as websocket:
            # Send a registration message with the username
            username = "TestUser"
            register_message = json.dumps({"type": "register", "username": username})
            await websocket.send(register_message)
            
            # Wait for the server's response
            response = await websocket.recv()
            print(f"Received: {response}")

            # Send a start message
            start_message = json.dumps({"type": "start"})
            await websocket.send(start_message)

            # Wait for the server's response
            response = await websocket.recv()
            print(f"Received: {response}")

            # Send a stop message
            stop_message = json.dumps({"type": "stop"})
            await websocket.send(stop_message)

            # Wait for the server's response
            response = await websocket.recv()
            print(f"Received: {response}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed with error: {e}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test())
