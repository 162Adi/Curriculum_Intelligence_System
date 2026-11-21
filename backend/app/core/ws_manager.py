"""
WebSocket Connection Manager for streaming real-time agent execution events
to the React Flow Agent Control Room and UI dashboards.
"""

import json
import logging
from typing import Dict, List
from fastapi import WebSocket

logger = logging.getLogger("cis.websocket")


class ConnectionManager:
    def __init__(self):
        # Maps execution_id -> List of active WebSocket connections
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, execution_id: str):
        await websocket.accept()
        if execution_id not in self.active_connections:
            self.active_connections[execution_id] = []
        self.active_connections[execution_id].append(websocket)
        logger.info(f"WebSocket client connected to execution stream: {execution_id}")

    def disconnect(self, websocket: WebSocket, execution_id: str):
        if execution_id in self.active_connections:
            if websocket in self.active_connections[execution_id]:
                self.active_connections[execution_id].remove(websocket)
            if not self.active_connections[execution_id]:
                del self.active_connections[execution_id]
        logger.info(f"WebSocket client disconnected from execution stream: {execution_id}")

    async def broadcast(self, execution_id: str, message: dict):
        """Send execution event payload to all clients listening to execution_id."""
        if execution_id in self.active_connections:
            payload = json.dumps(message)
            disconnected = []
            for connection in self.active_connections[execution_id]:
                try:
                    await connection.send_text(payload)
                except Exception as e:
                    logger.warning(f"Error sending message to websocket: {e}")
                    disconnected.append(connection)
            for dead_conn in disconnected:
                self.disconnect(dead_conn, execution_id)


ws_manager = ConnectionManager()
