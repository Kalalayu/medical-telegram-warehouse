from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from db import get_db  # this now works


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/api/search/messages")
def message_search(query: str, limit: int = 10, db: Session = Depends(get_db)):
    sql = """
    SELECT message_id, channel_name, text, created_at
    FROM analytics.fct_messages
    WHERE text ILIKE '%' || :query || '%'
    ORDER BY created_at DESC
    LIMIT :limit;
    """
    result = db.execute(text(sql), {"query": query, "limit": limit}).fetchall()

    # Each r is a SQLAlchemy Row object
    return [
        {
            "message_id": r.message_id,
            "channel_name": r.channel_name,
            "text": r.text,
            "created_at": r.created_at,
        }
        for r in result
    ]
