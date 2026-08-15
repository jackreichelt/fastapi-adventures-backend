from typing import Annotated

from fastapi import Depends, WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self, name):
        self.name = name
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"{self.name} Websocket connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"{self.name} Websocket disconnected")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


presenter_connections = ConnectionManager("presenters")
audience_connections = ConnectionManager("audience")


async def _get_presenter_connections():
    """
    Yields a session. Sessions are a transactional connection to the database.
    """
    yield presenter_connections


async def _get_audience_connections():
    """
    Yields a session. Sessions are a transactional connection to the database.
    """
    yield audience_connections


get_presenter_connections = Annotated[ConnectionManager, Depends(_get_presenter_connections)]
get_audience_connections = Annotated[ConnectionManager, Depends(_get_audience_connections)]
