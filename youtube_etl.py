import os
import csv
import boto3
from googleapiclient.discovery import build
import pandas as pd
from dotenv import load_dotenv
import logging
import datetime

# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set your AWS S3 credentials and YouTube API key from environment variables
api_key = os.getenv('YOUTUBE_API_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)

# Initialize the S3 client
def initialize_s3_client():
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        logging.info("S3 client initialized successfully.")
        return s3_client
    except Exception as e:
        logging.error(f"Failed to initialize S3 client: {e}")
        raise

# Function to get videos from a specific YouTube channel
def get_videos_from_channel(channel_id, max_results=10):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results
    )

    response = request.execute()
    video_data = []
    for item in response["items"]:
        # Check if the item is a video
        if item['id']['kind'] == 'youtube#video':
            video_info = {
                "title": item['snippet']['title'],
                "description": item['snippet']['description'],
                "video_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            video_data.append(video_info)
        else:
            logging.info(f"Skipping non-video item: {item['id']['kind']}")

    return video_data

# Transform the data (you can apply more transformations here if needed)
def transform_data(video_data):
    for video in video_data:
        video["description"] = video["description"].replace("&amp;", "&")
    return video_data

# Function to save data to a CSV file with a unique name
def save_to_csv(video_data, filename="youtube_data.csv"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename.replace('.csv', '')}_{timestamp}.csv"

    df = pd.DataFrame(video_data)
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")
    return filename

# Upload the CSV file to S3
def upload_to_s3(filename):
    s3_client = initialize_s3_client()

    try:
        s3_client.upload_file(filename, BUCKET_NAME, filename)
        logging.info(f"File uploaded to S3: {filename}")
    except boto3.exceptions.S3UploadFailedError as e:
        logging.error(f"Upload failed: {e}")
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")

# Main ETL Process
def run_etl_process(channel_id, max_results=10):
    video_data = get_videos_from_channel(channel_id, max_results)
    if video_data:
        transformed_data = transform_data(video_data)
        filename = save_to_csv(transformed_data)
        upload_to_s3(filename)
    else:
        logging.warning("No video data to process.")

# Example: Replace with the YouTube channel ID you want to fetch data from
channel_id = "UCLkAepWjdylmXSltofFvsYQ"  # Example channel ID for testing
run_etl_process(channel_id)

