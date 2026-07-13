from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.models import models  # noqa: F401 (ensures models are registered)
from app.routers import auth, couples, memories

app = FastAPI(title="Keepsake API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten once you have a real Expo/production origin
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(couples.router)
app.include_router(memories.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
