import asyncio
import websockets
import json
import random
from aiohttp import web

connected_clients = set()
usernames = set()
clients = {}
admin_password = "admin_password"  # Change this to a secure password

async def notify_clients(message):
    if connected_clients:  # asyncio.wait doesn't accept an empty list
        await asyncio.wait([client.send(message) for client in connected_clients])

async def register(request):
    data = await request.json()
    username = data.get('username')

    if not username:
        return web.json_response({'message': 'Username is required'}, status=400)

    if username in usernames:
        return web.json_response({'message': 'Username already taken'}, status=400)

    usernames.add(username)
    await notify_clients(json.dumps({"type": "new_user", "username": username}))
    return web.json_response({'message': f'Welcome, {username}!'})

async def login(request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if username == "admin" and password == admin_password:
        return web.json_response({'success': True})
    else:
        return web.json_response({'success': False, 'message': 'Invalid credentials'}, status=401)

async def admin_start(request):
    await notify_clients(json.dumps({"type": "start"}))
    return web.json_response({'message': 'Game started'})

async def admin_stop(request):
    await handle_stop()
    return web.json_response({'message': 'Game stopped'})

async def handler(websocket, path):
    global connected_clients, usernames, clients

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
                await handle_stop()
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

async def handle_stop():
    if usernames:
        winner = random.choice(list(usernames))
        await notify_clients(json.dumps({"type": "stop", "winner": winner}))

async def init_app():
    app = web.Application()
    app.add_routes([
        web.post('/register', register),
        web.post('/login', login),
        web.post('/admin/start', admin_start),
        web.post('/admin/stop', admin_stop)
    ])
    return app

async def main():
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8766)
    await site.start()
    print("HTTP server started on http://0.0.0.0:8766")

    async with websockets.serve(handler, "0.0.0.0", 8767):
        print("WebSocket server started on ws://0.0.0.0:8767")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
