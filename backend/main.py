from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from app.database import init_db
from app.seed import seed_database
from app.routes import offline, online


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database()
    yield


app = FastAPI(
    title="MediScan AI Pro",
    description="Hybrid Disease Identifier with Offline Engine + Online AI Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(offline.router)
app.include_router(online.router)


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "app": "MediScan AI Pro"}


frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = os.path.join(frontend_dir, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_dir, "index.html"))
