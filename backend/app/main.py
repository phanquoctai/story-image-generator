from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.routes import upload, story, images, export

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    logger.info("🚀 Starting Story Image Generator API")
    yield
    logger.info("🛑 Shutting down Story Image Generator API")


app = FastAPI(
    title="Story Image Generator API",
    description="Công cụ tạo ảnh câu chuyện hàng loạt từ ảnh bìa",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(story.router, prefix="/api/v1", tags=["Story"])
app.include_router(images.router, prefix="/api/v1", tags=["Images"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])


@app.get("/")
async def root():
    return {
        "message": "🎨 Story Image Generator API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)