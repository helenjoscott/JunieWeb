"""
WebSocket connection manager for the FastAPI demo application.
"""

from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    """
    Manages WebSocket connections and broadcasts messages.
    """
    def __init__(self):
        # Store active connections: client_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        """
        Accept a new WebSocket connection.
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await self.broadcast(f"Client {client_id} joined the chat")

    def disconnect(self, websocket: WebSocket, client_id: int):
        """
        Remove a WebSocket connection.
        """
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: int):
        """
        Send a message to a specific client.
        """
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        """
        Broadcast a message to all connected clients.
        """
        disconnected_clients = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
            except Exception:
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(self.active_connections[client_id], client_id)

    async def broadcast_json(self, data: dict):
        """
        Broadcast JSON data to all connected clients.
        """
        disconnected_clients = []
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(data)
            except Exception:
                disconnected_clients.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(self.active_connections[client_id], client_id)

    def get_client_count(self) -> int:
        """
        Get the number of connected clients.
        """
        return len(self.active_connections)

    def is_connected(self, client_id: int) -> bool:
        """
        Check if a client is connected.
        """
        return client_id in self.active_connections