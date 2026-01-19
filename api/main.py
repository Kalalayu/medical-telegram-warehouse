from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from pydantic import BaseModel
from db import get_db  

app = FastAPI(title="Medical Telegram Analytics API")

# ---------------------------
# Pydantic Models
# ---------------------------
class MessageResponse(BaseModel):
    message_id: int
    channel_name: str
    text: str
    created_at: str

class ChannelResponse(BaseModel):
    channel_name: str
    message_count: int

# ---------------------------
# Health Endpoint
# ---------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}

# ---------------------------
# Messages Search Endpoint
# ---------------------------
@app.get("/api/search/messages", response_model=List[MessageResponse], tags=["Messages"])
def message_search(
    query: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    sql = """
        SELECT message_id, channel_name, text, created_at
        FROM analytics.fct_messages
        WHERE text ILIKE '%' || :query || '%'
        ORDER BY created_at DESC
        LIMIT :limit;
    """
    try:
        result = db.execute(text(sql), {"query": query, "limit": limit}).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if not result:
        raise HTTPException(status_code=404, detail="No messages found")

    return result

# ---------------------------
# Top Channels Endpoint
# ---------------------------
@app.get("/api/channels/top", response_model=List[ChannelResponse], tags=["Channels"])
def top_channels(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    sql = """
        SELECT channel_name, COUNT(*) AS message_count
        FROM analytics.fct_messages
        GROUP BY channel_name
        ORDER BY message_count DESC
        LIMIT :limit;
    """
    try:
        result = db.execute(text(sql), {"limit": limit}).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if not result:
        raise HTTPException(status_code=404, detail="No channels found")

    return result
