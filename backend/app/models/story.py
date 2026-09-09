from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class StoryStatus(str, enum.Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    GENERATING_STORY = "generating_story"
    GENERATING_IMAGES = "generating_images"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Story(Base):
    __tablename__ = "stories"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String, nullable=True)
    cover_image_path = Column(String, nullable=True)
    
    # Story Content
    story_text = Column(Text, nullable=True)
    scenes = Column(JSON, nullable=True)  # List of scene descriptions
    characters = Column(JSON, nullable=True)  # Character descriptions
    
    # Generation Settings
    style = Column(String, default="realistic")  # realistic, anime, cartoon, etc.
    num_images = Column(Integer, default=8)
    language = Column(String, default="vi")
    
    # Status
    status = Column(String, default=StoryStatus.PENDING)
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Output
    output_video_url = Column(String, nullable=True)
    output_slideshow_url = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Story {self.id}>"
