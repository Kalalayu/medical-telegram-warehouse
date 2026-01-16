import json
import psycopg2
from glob import glob

conn = psycopg2.connect(
    host="localhost",
    dbname="medical_dw",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

files = glob("data/raw/telegram_messages/*/*.json")

for file in files:
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
        for m in data:
            cur.execute("""
                INSERT INTO raw.telegram_messages
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                m["message_id"],
                m["channel_name"],
                m["message_date"],
                m["message_text"],
                m["views"],
                m["forwards"],
                m["has_media"],
                m["image_path"]
            ))

conn.commit()
cur.close()
conn.close()
