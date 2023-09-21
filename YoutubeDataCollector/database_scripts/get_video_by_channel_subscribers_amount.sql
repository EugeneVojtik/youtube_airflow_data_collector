SELECT video_fact.video_id, video_details.title, video_fact.upload_date, channels.subscribers_amount FROM
youtube_analytics.videos as video_fact
INNER JOIN youtube_analytics.videos_details as video_details
ON video_fact.video_id = video_details.video_id
INNER JOIN youtube_analytics.channels as channels
ON video_fact.channel_id = channels.channel_id
WHERE channels.subscribers_amount > {{REQUIRED_AMOUNT}};
