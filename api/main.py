from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from api import schemas, database

app = FastAPI(
    title="Medical Telegram Data Warehouse API",
    description="Analytical API exposing Telegram data warehouse insights",
    version="1.0"
)

# Dependency
get_db = database.get_db

# --- Endpoint 1: Top Products ---
@app.get("/api/reports/top-products", response_model=schemas.TopProductsResponse)
def top_products(limit: int = Query(10, ge=1), db: Session = Depends(get_db)):
    query = """
    SELECT product_name, COUNT(*) as mention_count
    FROM analytics.fct_messages
    GROUP BY product_name
    ORDER BY mention_count DESC
    LIMIT :limit;
    """
    result = db.execute(query, {"limit": limit}).fetchall()
    return {"results": [{"product_name": r[0], "mention_count": r[1]} for r in result]}

# --- Endpoint 2: Channel Activity ---
@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivityResponse)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = """
    SELECT DATE(created_at) as date, COUNT(*) as messages_count
    FROM analytics.fct_messages
    WHERE channel_name = :channel_name
    GROUP BY DATE(created_at)
    ORDER BY date;
    """
    result = db.execute(query, {"channel_name": channel_name}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return {
        "channel_name": channel_name,
        "activity": [{"date": str(r[0]), "messages_count": r[1]} for r in result]
    }

# --- Endpoint 3: Message Search ---
@app.get("/api/search/messages", response_model=schemas.MessageSearchResponse)
def message_search(query: str = Query(..., min_length=1), limit: int = Query(20, ge=1), db: Session = Depends(get_db)):
    sql = """
    SELECT message_id, channel_name, text, created_at
    FROM analytics.fct_messages
    WHERE text ILIKE '%' || :query || '%'
    ORDER BY created_at DESC
    LIMIT :limit;
    """
    result = db.execute(sql, {"query": query, "limit": limit}).fetchall()
    return {"results": [{"message_id": r[0], "channel_name": r[1], "text": r[2], "created_at": str(r[3])} for r in result]}

# --- Endpoint 4: Visual Content Stats ---
@app.get("/api/reports/visual-content", response_model=schemas.VisualContentStatsResponse)
def visual_content_stats(db: Session = Depends(get_db)):
    query = """
    SELECT channel_name,
           COUNT(*) FILTER (WHERE image_url IS NOT NULL) AS total_images,
           100.0 * COUNT(*) FILTER (WHERE image_url IS NOT NULL) / COUNT(*) AS image_percentage
    FROM analytics.fct_messages
    GROUP BY channel_name;
    """
    result = db.execute(query).fetchall()
    return {"results": [{"channel_name": r[0], "total_images": r[1], "image_percentage": float(r[2])} for r in result]}
