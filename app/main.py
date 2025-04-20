from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, home, chat
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()  # Load from .env file

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Replace with a secure key
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("SESSION_SECRET_KEY"),
                   session_cookie="session_cookie",
                   https_only=True)

app.include_router(auth.router)
app.include_router(home.router)
# app.include_router(chat.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
