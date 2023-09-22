SELECT video_fact.video_id, video_details.title, content_details.duration as duration_minutes, video_fact.upload_date
FROM youtube_analytics.uploaded_videos as video_fact
INNER JOIN youtube_analytics.videos_details as video_details
ON video_fact.video_id = video_details.video_id
INNER JOIN youtube_analytics.content_details as content_details
ON video_fact.video_id = content_details.video_id
WHERE content_details.duration > {{REQUIRED_DEURATION}};