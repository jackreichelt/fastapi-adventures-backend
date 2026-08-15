from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .connection_manager import get_audience_connections

router = APIRouter(
    prefix="/audience",
    tags=["websockets"],
)


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    audience_connections: get_audience_connections,
):
    await audience_connections.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Audience says {data}")
    except WebSocketDisconnect:
        audience_connections.disconnect(websocket)
