
CREATE SCHEMA IF NOT EXISTS youtube_analytics;

CREATE TABLE IF NOT EXISTS youtube_analytics.uploaded_videos (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP NOT NULL,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS youtube_analytics.videos_details (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category_id VARCHAR(255),
    live_broadcast_content BOOLEAN,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS youtube_analytics.channels (
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    subscribers_amount INT,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS youtube_analytics.tags (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    tag VARCHAR(255),
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS youtube_analytics.video_statistics (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    view_count INT,
    like_count INT,
    comment_count INT,
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS youtube_analytics.content_details (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    dimension VARCHAR(255),
    definition VARCHAR(255),
    caption VARCHAR(255),
    licensed_content BOOLEAN,
    duration DECIMAL NOT NULL,
    projection VARCHAR(255),
    created_on TIMESTAMP NOT NULL DEFAULT NOW()
);
