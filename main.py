from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.query import router as query_router
from routes.health import router as health_router

app = FastAPI(title="CthulhuAssistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)
app.include_router(health_router)