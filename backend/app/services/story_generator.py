import logging
from anthropic import Anthropic
from typing import Dict, Any, List
import json

from app.config import settings

logger = logging.getLogger(__name__)


class StoryGenerator:
    """Generate story from cover image analysis"""
    
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_story(
        self,
        cover_analysis: Dict[str, Any],
        num_scenes: int = 8,
        language: str = "vi"
    ) -> Dict[str, Any]:
        """Generate complete story from cover image analysis"""
        
        prompt = self._build_story_prompt(
            cover_analysis,
            num_scenes,
            language
        )
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response_text = message.content[0].text
            story_data = self._parse_story_response(response_text, language)
            
            logger.info(f"Story generated successfully with {len(story_data['scenes'])} scenes")
            return story_data
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            raise
    
    def _build_story_prompt(self, cover_analysis: Dict, num_scenes: int, language: str) -> str:
        """Build prompt for story generation"""
        
        language_instruction = "Vietnamese" if language == "vi" else "English"
        
        prompt = f"""Bạn là một tác giả sáng tạo câu chuyện hứa hẹn. Dựa trên những thông tin sau về một ảnh bìa, hãy tạo ra một câu chuyện hoàn chỉnh.

Thông tin ảnh bìa:
- Chủ đề chính: {json.dumps(cover_analysis.get('labels', [])[:5])}
- Số nhân vật: {cover_analysis.get('faces_count', 0)}
- Tâm trạng: {cover_analysis.get('estimated_mood', 'neutral')}
- Bối cảnh: {cover_analysis.get('estimated_setting', 'general')}
- Văn bản trích xuất: {cover_analysis.get('extracted_text', '')}

Yêu cầu:
1. Tạo một câu chuyện có {num_scenes} cảnh (scene)
2. Mỗi cảnh phải có:
   - Tiêu đề cảnh
   - Mô tả chi tiết (150-200 từ)
   - Tên nhân vật chính
   - Chi tiết về nhân vật (ngoại hình, tâm trạng, hành động)
   - Chi tiết về bối cảnh
3. Câu chuyện phải có sự phát triển logic từ đầu đến cuối
4. Mỗi cảnh phải có thể biến thành 1 bức ảnh

Vui lòng trả lời bằng JSON với cấu trúc sau:
{{
  "title": "Tiêu đề câu chuyện",
  "summary": "Tóm tắt câu chuyện",
  "main_character": {{
    "name": "Tên",
    "description": "Mô tả ngoại hình chi tiết",
    "personality": "Tính cách"
  }},
  "scenes": [
    {{
      "index": 0,
      "title": "Tiêu đề cảnh",
      "description": "Mô tả cảnh chi tiết",
      "setting": "Bối cảnh",
      "characters_involved": ["tên nhân vật"],
      "mood": "Tâm trạng/khí đặc"
    }}
  ]
}}

Viết bằng tiếng {language_instruction}."""
        
        return prompt
    
    def _parse_story_response(self, response_text: str, language: str) -> Dict[str, Any]:
        """Parse story response from Claude"""
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}")
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx + 1]
                story_data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            return story_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            # Return a default structure
            return {
                "title": "Câu chuyện",
                "summary": response_text[:200],
                "main_character": {
                    "name": "Nhân vật chính",
                    "description": "Một nhân vật",
                    "personality": "Tích cực"
                },
                "scenes": []
            }
