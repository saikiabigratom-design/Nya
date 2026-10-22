"""
Main FastAPI Application Entrypoint for ঞ (Nya) — Vocal for Local.
"""

import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure packages and local directories are in python path
current_dir = Path(__file__).resolve().parent
repo_root = current_dir.parent.parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(repo_root))

from config import settings
from db.session import init_db
from api.routes import router
from api.middleware import PrivacyAndSecurityMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schemas on startup
    await init_db()
    yield


app = FastAPI(
    title="ঞ (Nya) — Vocal for Local API",
    description="Assamese-first, multilingual web search with source-grounded AI answers.",
    version="0.1.0-beta",
    lifespan=lifespan,
)

# Privacy and Security Middleware
app.add_middleware(PrivacyAndSecurityMiddleware)

# Cross-Origin Resource Sharing (CORS)
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https?://.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register API v1 routes
app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "ঞ (Nya) — Vocal for Local API",
        "tagline": "Search beyond language.",
        "status": "online",
        "docs_url": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
