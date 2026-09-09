import logging
from openai import OpenAI
from typing import Dict, Any
from app.config import settings
import os
import aiofiles

logger = logging.getLogger(__name__)


class ImageGenerator:
    """Generate images using DALL-E 3"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "dall-e-3"
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "hd"
    ) -> Dict[str, str]:
        """Generate single image from prompt"""
        
        try:
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            
            image_url = response.data[0].url
            logger.info(f"Image generated: {image_url}")
            
            return {
                "url": image_url,
                "prompt": prompt,
                "size": size
            }
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise
    
    def _enhance_prompt(self, base_prompt: str, character_description: str, style: str) -> str:
        """Enhance prompt with character consistency and style"""
        
        style_modifiers = {
            "realistic": "photorealistic, high quality, professional photography, sharp details",
            "anime": "anime style, beautiful illustration, manga art, vibrant colors",
            "cartoon": "cartoon style, colorful, fun, family-friendly, illustration",
            "oil_painting": "oil painting, classical art, masterpiece, detailed brushwork",
            "watercolor": "watercolor painting, soft colors, artistic, flowing",
            "3d": "3D render, professional 3D art, high quality, cinematic lighting"
        }
        
        style_text = style_modifiers.get(style, "high quality, detailed")
        
        enhanced = f"{base_prompt}. Character: {character_description}. Style: {style_text}"
        
        return enhanced
