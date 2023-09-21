SELECT video_fact.video_id, video_details.title, video_fact.upload_date FROM youtube_analytics.videos as video_fact
INNER JOIN youtube_analytics.videos_details as video_details
ON video_fact.video_id = video_details.video_id
WHERE video_fact.upload_date BETWEEN {{START_DATE}} AND {{END_DATE}};