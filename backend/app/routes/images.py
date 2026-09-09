from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import uuid
from datetime import datetime

from app.services.image_generator import ImageGenerator

router = APIRouter()
generator = ImageGenerator()


@router.post("/images/generate-batch")
async def generate_batch_images(
    story_id: str,
    scenes: List[Dict[str, Any]],
    character_description: str,
    style: str = "realistic"
) -> Dict[str, Any]:
    """Generate batch of images for story scenes"""
    
    try:
        images = []
        
        for idx, scene in enumerate(scenes):
            image_id = str(uuid.uuid4())
            
            # Create prompt from scene
            prompt = f"{scene['description']}. {character_description}"
            
            # Generate image
            image_data = await generator.generate_image(
                prompt=prompt,
                size="1024x1024",
                quality="hd"
            )
            
            images.append({
                "image_id": image_id,
                "scene_index": idx,
                "scene_title": scene.get('title', f'Scene {idx + 1}'),
                "url": image_data["url"],
                "prompt": image_data["prompt"],
                "generated_at": datetime.utcnow().isoformat()
            })
        
        return {
            "success": True,
            "story_id": story_id,
            "images_count": len(images),
            "images": images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/{story_id}")
async def get_story_images(story_id: str) -> Dict[str, Any]:
    """Get all images for a story"""
    try:
        # TODO: Fetch from database
        return {"story_id": story_id, "images": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
