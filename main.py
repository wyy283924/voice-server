from fastapi import FastAPI,Response,status,WebSocket,WebSocketDisconnect
from core.websocket import manager

from config.cache import load_config

app = FastAPI()


@app.get("/config")
async def get_config():
    config = load_config()
    return {"config": config}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

@app.get("/server-status")
async def serverStatus(response: Response,token: str | None=None):
    if token == "Tai":
        data = {
            "运行状态":"正常运行"
        }
        return data
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":"Not Found"}