WITH detections AS (
    SELECT
        message_id::BIGINT,
        channel_name,
        detected_class,
        confidence_score,
        image_category
    FROM {{ source('raw', 'image_detections') }}
),

messages AS (
    SELECT
        message_id,
        channel_key,
        date_key
    FROM {{ ref('fct_messages') }}
)

SELECT
    d.message_id,
    m.channel_key,
    m.date_key,
    d.detected_class,
    d.confidence_score,
    d.image_category
FROM detections d
JOIN messages m
    ON d.message_id = m.message_id
