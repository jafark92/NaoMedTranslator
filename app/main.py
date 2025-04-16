import json
from app.translator import translate_message
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# In-memory chat management
active_connections = []


@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/translate")
async def translate(request: Request):
    data = await request.json()
    text = data.get("text")
    source = data.get("source_lang", "auto")
    target = data.get("target_lang", "en")

    translated_text = await translate_message(text, source, target)

    return {
        "original": text,
        "translated": translated_text
    }


@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            for conn in active_connections:
                await conn.send_text(json.dumps(payload))
    except WebSocketDisconnect:
        active_connections.remove(websocket)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
