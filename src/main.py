from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.utils.settings import STATIC_DIR
from src.api.v1 import auth

app = FastAPI(
    title="backend",
    version="0.1.0",
    debug=True,
    docs_url="/api/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static directory path
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

API_V1_PREFIX = "/api/v1"

# Adding routers
app.include_router(auth.router, prefix=API_V1_PREFIX, tags=["Auth"])