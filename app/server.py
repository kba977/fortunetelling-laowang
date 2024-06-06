from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.master import Master

app = FastAPI()
# 加载server.py



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(query: str):
    master = Master()
    return master.run(query)


@app.post("/add_urls")
def add_urls():
    return {"response": "URLs add!"}


@app.post("/add_pdfs")
def add_pdfs():
    return {"response": "Pdfs add!"}


@app.post("/add_texts")
def add_texts():
    return {"response": "Texts add!"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    master = Master()
    try:
        while True:
            data = await websocket.receive_text()
            res = master.run(data)
            await websocket.send_text(f"AI: {res.get('output')}")
    except WebSocketDisconnect:
        print("WebSocket closed")
        await websocket.close()