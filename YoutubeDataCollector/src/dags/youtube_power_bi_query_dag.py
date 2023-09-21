"""
The module contains dag for fetching data from Youtube API by the specified query
"""
import os
import logging
from airflow.decorators import task, dag
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from googleapiclient.discovery import build
from models import Video, Channel, Tag, VideoDetail, VideoStatistics, ContentDetails
from helpers import convert_duration_to_minutes
from constants import (
    MIN_REQUIRED_SUBS,
    VIDEO_TYPE,
    ISO_DATE_FORMAT,
    YOUTUBE_KEY,
    V3_KEY,
    SEARCH_QUERY,
    ID_KEY,
    SNIPPET_KEY,
    STATISTICS_KEY,
    ITEMS_KEY,
    CONTENT_DETAILS_KEY
)

logger = logging.getLogger(__name__)

DEVELOPER_KEY = os.environ.get("DEVELOPER_KEY", "")
ANALYTICS_DB_USER = os.environ.get("ANALYTICS_DB_USER", "")
ANALYTICS_DB_PASSWORD = os.environ.get("ANALYTICS_DB_PASSWORD", "")
ANALYTICS_DB_DATABASE = os.environ.get('ANALYTICS_DB_DATABASE', "")
ANALYTICS_DB_CONTAINER_NAME = "analytics_db"

@dag(
    schedule="@daily",
    start_date=days_ago(0),
    catchup=False,
    tags=["youtube_data_fetch"]
)
def youtube_power_bi_query_videos_dag():

    engine = create_engine(f"postgresql+psycopg2://{ANALYTICS_DB_USER}:{ANALYTICS_DB_PASSWORD}"
                           f"@{ANALYTICS_DB_CONTAINER_NAME}/{ANALYTICS_DB_DATABASE}")
    client = build(YOUTUBE_KEY, V3_KEY, developerKey=DEVELOPER_KEY)

    @task()
    def get_videos_by_subject() -> dict:
        """
        Method for fetching data from YOUTUBE API by the specified query

        :return: Dict with data matched the specified query
        """
        yesterday_date = days_ago(1).strftime(ISO_DATE_FORMAT)
        new_videos_list_request = client.search().list(
            q=SEARCH_QUERY,
            type=VIDEO_TYPE,
            part=f'{ID_KEY}, {SNIPPET_KEY}',
            publishedAfter=yesterday_date
        )
        logger.info(f"Fetching records from Youtube API by query: {SEARCH_QUERY}")
        return new_videos_list_request.execute()

    @task()
    def get_channels_data(videos_data: dict) -> dict:
        """
        Method for fetching of channels related data from YOUTUBE API (by provided video ids)

        :param videos_data: Dict with video related data
        :return: Dict with channels related data
        """
        ids = [i[SNIPPET_KEY]['channelId'] for i in videos_data[ITEMS_KEY]]
        channel_details_request = client.channels().list(
            id=','.join(ids),
            part=f'{SNIPPET_KEY},{STATISTICS_KEY}')
        logger.info(f"Fetching channels for video ids: {ids}")
        return channel_details_request.execute()

    @task(multiple_outputs=True)
    def filter_by_channels_req(videos_data: dict, channels_data: dict) -> dict:
        """
        Method for filtration of videos by the number of min channel subscribers

        :param videos_data: Dict with video related data
        :param channels_data: Dict with channels related data
        :return: Dict with filtered channels and video data
        """
        logger.info(f"Filtering videos by min number of channel subscribers ({MIN_REQUIRED_SUBS})")
        filtered_channels = [i for i in channels_data[ITEMS_KEY] if
                             int(i[STATISTICS_KEY]['subscriberCount']) > MIN_REQUIRED_SUBS]
        filtered_channels_ids = [i[ID_KEY] for i in filtered_channels]
        filtered_videos = list(
            filter(lambda x: x[SNIPPET_KEY]['channelId'] in filtered_channels_ids, videos_data[ITEMS_KEY]))
        return {"filtered_videos": filtered_videos, "filtered_channels": filtered_channels}

    @task()
    def get_video_details_data(filtered_videos: list) -> dict:
        """
        Method for fetching data for details of each video by the provided video_ids

        :param filtered_videos: list with filtered by channel subscribers videos
        :return: Dict with extended video details
        """

        video_ids = [i[ID_KEY]['videoId'] for i in filtered_videos]
        logger.info(f"Fetching video details by the video_ids: {video_ids}")
        video_details_request = client.videos().list(
            id=','.join(video_ids),
            part=f'{SNIPPET_KEY},{CONTENT_DETAILS_KEY}, {STATISTICS_KEY}')
        return video_details_request.execute()

    @task()
    def upsert_channels_data(filtered_channels: list) -> None:
        """
        Method inserts new records to Channels table and updates those records, that are already exist in the database

        :param filtered_channels: list with filtered channels (by min subscribers amount)
        """
        new_channels = []
        updated_channels = []

        with Session(engine) as session:
            for data in filtered_channels:
                channel_id = data[ID_KEY]
                title = data[SNIPPET_KEY]["title"]
                subscribers_amount = data[STATISTICS_KEY]["subscriberCount"]

                # Check if the channel exists in the database
                existing_channel = session.query(Channel).filter_by(channel_id=channel_id).first()

                if existing_channel is None:
                    # Create a new channel record
                    new_channel = Channel(channel_id=channel_id, title=title, subscribers_amount=subscribers_amount)
                    new_channels.append(new_channel)
                else:
                    # Update the existing channel record
                    existing_channel.title = title
                    existing_channel.subscribers_amount = subscribers_amount
                    updated_channels.append(existing_channel)

            # Bulk insert new channel records
            if new_channels:
                logger.info("Inserting new records to the channels table.")
                session.bulk_save_objects(new_channels)

            # Bulk update existing channel records
            if updated_channels:
                logger.info("Updating existing records in the channels table.")
                session.bulk_update_mappings(Channel,
                                             [{ID_KEY: channel.id, "subscribers_amount": channel.subscribers_amount} for
                                              channel in updated_channels])
            session.commit()

    def create_records_objects(ext_video_details: dict) -> dict:
        """
        Method creates SQLAlchemy objects of video-related records for further fetching it to the target database
        :param ext_video_details: dict with extended video details
        :return: Dict with lists of created SQLAlchemy objects
        """
        tags = []
        video_details = []
        video_statistics = []
        content_details = []
        uploaded_videos = []
        logger.info("Creating SQLAlchemy objects for further insertion.")
        for data in ext_video_details[ITEMS_KEY]:
            video_id = data[ID_KEY]
            # video_fact table
            upload_date = data[SNIPPET_KEY]['publishedAt']
            channel_id = data[SNIPPET_KEY]['channelId']
            uploaded_videos.append(Video(video_id, upload_date, channel_id))
            # video_details table
            title = data[SNIPPET_KEY]['title']
            description = data[SNIPPET_KEY]['description']
            category_id = data[SNIPPET_KEY]['categoryId']
            video_details.append(VideoDetail(video_id, title, description, category_id))
            # video_statistics table
            view_count = data[STATISTICS_KEY]['viewCount']
            like_count = data[STATISTICS_KEY]['likeCount']
            comment_count = data[STATISTICS_KEY]['commentCount']
            video_statistics.append(VideoStatistics(video_id, view_count, like_count, comment_count))
            # content_details table
            dimension = data[CONTENT_DETAILS_KEY]['dimension']
            definition = data[CONTENT_DETAILS_KEY]['definition']
            caption = data[CONTENT_DETAILS_KEY]['caption']
            licensed_content = data[CONTENT_DETAILS_KEY]['licensedContent']
            duration = convert_duration_to_minutes(data[CONTENT_DETAILS_KEY]['duration'])
            projection = data[CONTENT_DETAILS_KEY]['projection']
            content_details.append(ContentDetails(video_id, dimension, definition, caption,
                                                  licensed_content, duration, projection))
            # tags table
            if 'tags' in data[SNIPPET_KEY]:
                for tag in data[SNIPPET_KEY]['tags']:
                    tags.append(Tag(video_id, tag))
        logger.info("Completed creation of SQLAlchemy objects")
        return {
            "video_details": video_details,
            "video_statistics": video_statistics,
            "content_details": content_details,
            "uploaded_videos": uploaded_videos,
            "tags": tags}

    @task()
    def write_video_data(ext_video_details: dict) -> None:
        """
        Method for writing data to the target database.
        :param ext_video_details: dict with extended videos details
        """
        orm_objects_dict = create_records_objects(ext_video_details)
        with Session(engine) as session:
            for table_name, objs_list in orm_objects_dict.items():
                session.bulk_save_objects(objs_list)
                logger.info(f"Insertion of new records to {table_name} table")
            session.commit()

    # get videos and channels related records
    videos_by_theme = get_videos_by_subject()
    channels_data = get_channels_data(videos_by_theme)

    # filter videos and channels by min subscribers number
    filter_result = filter_by_channels_req(videos_by_theme, channels_data)
    filtered_videos = filter_result['filtered_videos']
    filtered_channels = filter_result['filtered_channels']

    # get extended video details
    video_details = get_video_details_data(filtered_videos)

    # write channels and videos data
    upsert_channels_data(filtered_channels)
    write_video_data(video_details)


youtube_power_bi_query_videos_dag()
