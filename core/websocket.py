from typing import Set

from fastapi import WebSocket

from core.connection import ConnectionHandler


class WebSocketServer:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.handler: Set[ConnectionHandler] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        self.handler.add(ConnectionHandler())

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str|bytes, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str|bytes):
        for connection in self.active_connections:
            await connection.send_text(message)