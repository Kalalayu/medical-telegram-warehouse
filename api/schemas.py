from pydantic import BaseModel
from typing import List, Optional

# Top products response
class TopProduct(BaseModel):
    product_name: str
    mention_count: int

class TopProductsResponse(BaseModel):
    results: List[TopProduct]

# Channel activity response
class ChannelActivity(BaseModel):
    date: str
    messages_count: int

class ChannelActivityResponse(BaseModel):
    channel_name: str
    activity: List[ChannelActivity]

# Message search response
class Message(BaseModel):
    message_id: int
    channel_name: str
    text: str
    created_at: str

class MessageSearchResponse(BaseModel):
    results: List[Message]

# Visual content stats response
class VisualContentStat(BaseModel):
    channel_name: str
    total_images: int
    image_percentage: float

class VisualContentStatsResponse(BaseModel):
    results: List[VisualContentStat]
