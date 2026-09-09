import logging
from google.cloud import vision
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ImageAnalyzer:
    """Analyze cover image to extract story elements"""
    
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
    
    async def analyze_cover_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze cover image and extract story elements"""
        try:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Detect labels (themes, objects)
            labels_response = self.client.label_detection(image=image)
            labels = [
                {"description": label.description, "confidence": label.score}
                for label in labels_response.label_annotations
            ]
            
            # Detect faces
            faces_response = self.client.face_detection(image=image)
            faces = [
                {
                    "confidence": face.detection_confidence,
                    "joy": face.joy_likelihood,
                    "sorrow": face.sorrow_likelihood,
                    "anger": face.anger_likelihood,
                    "surprise": face.surprise_likelihood,
                }
                for face in faces_response.face_annotations
            ]
            
            # Detect text
            text_response = self.client.text_detection(image=image)
            text = text_response.text_annotations[0].description if text_response.text_annotations else ""
            
            # Detect colors (using web detection as proxy)
            web_response = self.client.web_detection(image=image)
            
            analysis = {
                "labels": labels[:10],  # Top 10 labels
                "faces_count": len(faces),
                "faces": faces[:3],  # Top 3 faces
                "extracted_text": text,
                "dominant_colors": self._extract_colors(web_response),
                "estimated_setting": self._estimate_setting(labels),
                "estimated_mood": self._estimate_mood(faces),
            }
            
            logger.info(f"Image analysis completed: {json.dumps(analysis, indent=2)}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            raise
    
    def _extract_colors(self, web_response) -> list:
        """Extract dominant colors from web detection"""
        colors = []
        for color in web_response.web_detection.best_guess_labels[:5]:
            colors.append(color.label)
        return colors
    
    def _estimate_setting(self, labels) -> str:
        """Estimate story setting from labels"""
        setting_keywords = {
            "indoor": ["house", "room", "indoor", "building"],
            "outdoor": ["outdoor", "nature", "forest", "beach", "mountain"],
            "urban": ["city", "street", "urban", "building"],
            "fantasy": ["fantasy", "castle", "magic", "mystical"],
            "scifi": ["space", "technology", "future", "robot"],
        }
        
        label_text = " ".join([l["description"].lower() for l in labels])
        
        for setting, keywords in setting_keywords.items():
            if any(kw in label_text for kw in keywords):
                return setting
        
        return "general"
    
    def _estimate_mood(self, faces) -> str:
        """Estimate mood from face detection"""
        if not faces:
            return "neutral"
        
        avg_joy = sum(f["joy"] for f in faces) / len(faces)
        avg_sorrow = sum(f["sorrow"] for f in faces) / len(faces)
        avg_anger = sum(f["anger"] for f in faces) / len(faces)
        
        if avg_joy > 0.5:
            return "happy"
        elif avg_sorrow > 0.5:
            return "sad"
        elif avg_anger > 0.5:
            return "angry"
        else:
            return "neutral"
