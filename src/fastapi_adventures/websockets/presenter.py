from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .connection_manager import get_presenter_connections

router = APIRouter(
    prefix="/presenter",
    tags=["websockets"],
)


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    presenter_connections: get_presenter_connections,
):
    await presenter_connections.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Client says {data}")
    except WebSocketDisconnect:
        presenter_connections.disconnect(websocket)
