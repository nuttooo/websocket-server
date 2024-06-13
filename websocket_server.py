import asyncio
import websockets
import json

connected_clients = set()
usernames = set()
clients = {}

async def notify_clients(message):
    if connected_clients:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handler(websocket, path):
    global connected_clients, usernames, clients
    
    # Add the new client connection to the set of connected clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            data = json.loads(message)

            if data["type"] == "register":
                username = data["username"]
                if username in usernames:
                    await websocket.send(json.dumps({"type": "error", "message": "Username already taken"}))
                else:
                    usernames.add(username)
                    clients[websocket] = username
                    await websocket.send(json.dumps({"type": "success", "message": f"Welcome, {username}!"}))
                    await notify_clients(json.dumps({"type": "new_user", "username": username}))
            elif data["type"] == "start":
                await notify_clients(json.dumps({"type": "start"}))
            elif data["type"] == "stop":
                await notify_clients(json.dumps({"type": "stop"}))
            else:
                await notify_clients(message)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
        username = clients.get(websocket)
        if username:
            usernames.remove(username)
            del clients[websocket]
            await notify_clients(json.dumps({"type": "user_left", "username": username}))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8766):
        print("WebSocket server started on ws://0.0.0.0:8766")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
