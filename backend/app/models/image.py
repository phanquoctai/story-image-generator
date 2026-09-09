from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class StoryImage(Base):
    __tablename__ = "story_images"
    
    id = Column(String, primary_key=True, index=True)
    story_id = Column(String, ForeignKey("stories.id"), index=True)
    
    # Image Details
    scene_index = Column(Integer)  # 0-based index in story
    scene_title = Column(String, nullable=True)
    scene_description = Column(Text)
    prompt = Column(Text)  # Generated prompt for DALL-E
    
    # Generated Image
    image_url = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    image_size = Column(String, default="1024x1024")
    
    # Character Consistency
    character_embeddings = Column(String, nullable=True)  # JSON encoded face embeddings
    character_description = Column(Text, nullable=True)
    
    # Status
    status = Column(String, default="pending")  # pending, generating, completed, failed
    error_message = Column(String, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    generation_time = Column(Integer, nullable=True)  # seconds
    
    def __repr__(self):
        return f"<StoryImage {self.id}>"
