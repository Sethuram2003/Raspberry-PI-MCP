from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.health_check import health_check_router
from app.api.routers.simple_chat import chat_router

from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
app.include_router(chat_router)

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_chat_interface():
    html_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {"message": "Pi-GPT API is running. Place index.html in static folder."}
