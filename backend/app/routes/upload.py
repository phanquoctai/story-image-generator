from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import uuid
import os
from datetime import datetime

from app.config import settings
from app.services.image_analyzer import ImageAnalyzer

router = APIRouter()
analyzer = ImageAnalyzer()


@router.post("/upload")
async def upload_cover_image(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload and analyze cover image"""
    
    try:
        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Create upload directory if not exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Save file
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        async with open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)
        
        # Analyze image
        analysis = await analyzer.analyze_cover_image(file_path)
        
        return {
            "success": True,
            "file_id": file_id,
            "file_path": file_path,
            "original_filename": file.filename,
            "uploaded_at": datetime.utcnow().isoformat(),
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
