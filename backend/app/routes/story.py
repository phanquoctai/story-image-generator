from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid
from datetime import datetime

from app.services.story_generator import StoryGenerator

router = APIRouter()
generator = StoryGenerator()


@router.post("/story/generate")
async def generate_story(
    file_id: str,
    image_analysis: Dict[str, Any],
    num_scenes: int = 8,
    language: str = "vi",
    style: str = "realistic"
) -> Dict[str, Any]:
    """Generate story from cover image analysis"""
    
    try:
        story_id = str(uuid.uuid4())
        
        # Generate story
        story_data = await generator.generate_story(
            cover_analysis=image_analysis,
            num_scenes=num_scenes,
            language=language
        )
        
        story_data["story_id"] = story_id
        story_data["created_at"] = datetime.utcnow().isoformat()
        story_data["style"] = style
        story_data["num_images"] = num_scenes
        story_data["status"] = "generated"
        
        return {
            "success": True,
            "story": story_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/story/{story_id}")
async def get_story(story_id: str) -> Dict[str, Any]:
    """Get story details"""
    try:
        # TODO: Fetch from database
        return {"story_id": story_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
