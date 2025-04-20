from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, home, chat

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Replace with a secure key
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(chat.router)
