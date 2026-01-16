SELECT
    message_id,
    channel_name,
    message_date::timestamp AS message_date,
    message_text,
    LENGTH(message_text) AS message_length,
    views::int AS view_count,
    forwards::int AS forward_count,
    has_media AS has_image,
    image_path
FROM raw.telegram_messages
WHERE message_text IS NOT NULL
