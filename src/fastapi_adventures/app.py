import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import presentation_sessions, slide_decks, slides, votes
from .websockets import audience, presenter
from .websockets.connection_manager import get_audience_connections, get_presenter_connections

app = FastAPI(swagger_ui_parameters={"persistAuthorization": True}, docs_url="/docs")

# Configure the CORs middleware
# TODO: Work out a better, more restrictive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173", "https://fastapi-adventures.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# parent_path = pathlib.Path(__file__).parent.parent
# static_files = StaticFiles(directory=parent_path / "fastapi_adventures" / "static")
# app.mount("/static", static_files, name="static")


v1_apis = [
    presentation_sessions,
    slide_decks,
    slides,
    votes,
]
for api in v1_apis:
    app.include_router(api.router, prefix="/api/v1")

ws_routers = [
    presenter,
    audience,
]
for ws in ws_routers:
    app.include_router(ws.router, prefix="/ws/v1")


count = 0


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel"}


@app.post("/count")
async def increment(
    presenter_connections: get_presenter_connections,
    audience_connections: get_audience_connections,
):
    global count
    await presenter_connections.broadcast(f"Presenter Count: {count}")
    await audience_connections.broadcast(f"Audience Count: {count}")
    count += 1


def run():
    """
    Serving the app
    """
    uvicorn.run(
        __name__ + ":app",
        reload=True,
        host="0.0.0.0",
        port=8080,
        log_level="debug",
    )


if __name__ == "__main__":
    run()
