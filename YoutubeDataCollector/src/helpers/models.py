"""
The module contains SQLAlchemy models for the required tables
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseClass(Base):
    __abstract__ = True
    __table_args__ = {"schema": "youtube_analytics"}
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime)


class Video(BaseClass):
    __tablename__ = 'uploaded_videos'

    video_id = Column(String)
    channel_id = Column(String)
    upload_date = Column(DateTime)

    def __init__(self, video_id, upload_date, channel_id):
        self.video_id = video_id
        self.upload_date = upload_date
        self.channel_id = channel_id
        self.created_on = datetime.now()


class Channel(BaseClass):
    __tablename__ = 'channels'

    channel_id = Column(String)
    title = Column(String)
    subscribers_amount = Column(Integer)

    def __init__(self, channel_id, title, subscribers_amount):
        self.channel_id = channel_id
        self.title = title
        self.subscribers_amount = subscribers_amount
        self.created_on = datetime.now()


class Tag(BaseClass):
    __tablename__ = "tags"

    video_id = Column(String)
    tag = Column(String)

    def __init__(self, video_id, tag):
        self.video_id = video_id
        self.tag = tag
        self.created_on = datetime.now()


class VideoDetail(BaseClass):
    __tablename__ = 'videos_details'

    video_id = Column(String)
    title = Column(String)
    description = Column(String)
    category_id = Column(String)
    live_broadcast_content = Column(Boolean)

    def __init__(self, video_id, title, description, category_id):
        self.video_id = video_id
        self.title = title
        self.description = description
        self.category_id = category_id
        self.created_on = datetime.now()


class VideoStatistics(BaseClass):
    __tablename__ = "video_statistics"

    video_id = Column(String)
    view_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)

    def __init__(self, video_id, view_count, like_count, comment_count):
        self.video_id = video_id
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.created_on = datetime.now()


class ContentDetails(BaseClass):
    __tablename__ = "content_details"

    video_id = Column(String)
    dimension = Column(String)
    definition = Column(String)
    caption = Column(String)
    licensed_content = Column(Boolean)
    duration = Column(Float)
    projection = Column(String)

    def __init__(self, video_id, dimension, definition, caption, licensed_content, duration, projection):
        self.video_id = video_id
        self.dimension = dimension
        self.definition = definition
        self.caption = caption
        self.licensed_content = licensed_content
        self.duration = duration
        self.projection = projection
        self.created_on = datetime.now()
