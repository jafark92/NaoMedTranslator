from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, home, chat
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Replace with a secure key
app.add_middleware(SessionMiddleware,
                   secret_key=os.getenv("SESSION_SECRET_KEY"),
                   session_cookie="session_cookie",
                   https_only=True)

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(chat.router)
