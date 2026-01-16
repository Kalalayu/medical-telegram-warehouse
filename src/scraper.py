# Imports & Client Setup
import os
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from logger import logger

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("telegram_session", API_ID, API_HASH)

# Channels to Scrape
CHANNELS = [
    "chemed",
    "lobelia4cosmetics",
    "tikvahpharma"
]
# Scraping Logic
async def scrape_channel(channel):
    messages = []
    logger.info(f"Scraping {channel}")

    async for msg in client.iter_messages(channel, limit=1000):
        record = {
            "message_id": msg.id,
            "channel_name": channel,
            "message_date": msg.date.isoformat() if msg.date else None,
            "message_text": msg.text,
            "views": msg.views,
            "forwards": msg.forwards,
            "has_media": msg.media is not None,
            "image_path": None
        }

        if isinstance(msg.media, MessageMediaPhoto):
            img_dir = f"data/raw/images/{channel}"
            os.makedirs(img_dir, exist_ok=True)
            img_path = f"{img_dir}/{msg.id}.jpg"
            await msg.download_media(file=img_path)
            record["image_path"] = img_path

        messages.append(record)

    return messages

# Save Raw JSON Files
async def save_data(channel, data):
    date = datetime.now().strftime("%Y-%m-%d")
    out_dir = f"data/raw/telegram_messages/{date}"
    os.makedirs(out_dir, exist_ok=True)

    with open(f"{out_dir}/{channel}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(data)} messages from {channel}")

# Main Execution
async def main():
    await client.start()
    for channel in CHANNELS:
        try:
            data = await scrape_channel(channel)
            await save_data(channel, data)
        except Exception as e:
            logger.error(f"Error on {channel}: {e}")
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


