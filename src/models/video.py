from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class Thumbnail(BaseModel):
    url: str
    width: str
    height: str

class Thumbnails(BaseModel):
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail

class Video(BaseModel):
    id: str = Field(alias='_id')
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    thumbnails: Thumbnails
    channelTitle: str
    publishTime: datetime


        