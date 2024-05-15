#fetch_comments.py - fine name

import re
import json
import googleapiclient.discovery

import os  # Type hint added for the os module
import io
from dotenv import load_dotenv
from typing import Any

def load_dotenv(dotenv_path: str | None = None, stream: io.StringIO | None = None, verbose: bool = False, override: bool = False, interpolate: bool = True, encoding: str | None = "utf-8") -> bool:
    pass

os: Any  # Type hint for the os module

# Load environment variables from the .env file
load_dotenv()

# Access the GOOGLE_API_KEY from the environment
API_KEY = os.getenv('GOOGLE_API_KEY')
 

# ... (rest of your Python script)

def extract_video_id(video_url):
    match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
    if match:
        return match.group(1)
    else:
        return None

def fetch_video_details(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )

    response = request.execute()

    if response['items']:
        video_info = response['items'][0]['snippet']
        statistics_info = response['items'][0].get('statistics', {})

        video_details = {
            'title': video_info['title'],
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'view_count': statistics_info.get('viewCount', 0),
            'comment_count': statistics_info.get('commentCount', 0),
            'channel_title': video_info.get('channelTitle', 'Unknown'),
            'like_count': statistics_info.get('likeCount', 0)  # Handle missing like count
        }
    else:
        video_details = None

    return video_details

def fetch_comments(video_ids, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    all_comments = {}

    for video_id in video_ids:
        comments = []  # Using a list to preserve order
        nextPageToken = None
        total_comments = 0
        
        # Fetch comments for the current video
        while True:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=nextPageToken
            )

            response = request.execute()
            total_comments += response['pageInfo']['totalResults']

            for item in response['items']:
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = comment_snippet['textDisplay']
                
                # Remove timestamps like "7:55" from comments
                comment_text = remove_timestamps(comment_text)
                
                # Remove HTML tags
                comment_text = re.sub(r'<[^>]*>', '', comment_text)
                
                # Fetch the first reply for this comment, if any
                reply = ""
                if 'replies' in item:
                    reply_snippet = item['replies']['comments'][0]['snippet']
                    reply_text = reply_snippet['textDisplay']
                    reply_author = reply_snippet.get('authorDisplayName', 'Unknown')
                    reply = f"(Comment Reply -{reply_author}: {reply_text})"  # Include reply inside parentheses
                
                # Format the reply or (0) if there are no replies
                formatted_reply = reply if reply else "(0)"
                
                # Filter out comments with less than six words, more than 150 words,
                # repeating single or short words more than three times,
                # and comments containing repeating phrases more than three times
                if len(comment_text.split()) >= 6 and len(comment_text.split()) <= 150 and not contains_repeating_words(comment_text):
                    comments.append((comment_text, formatted_reply))  # Add the comment to the list

            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
            else:
                break

        # Store the comments and video details in the all_comments dictionary
        video_details = fetch_video_details(video_id, api_key)
        all_comments[video_id] = {
            'video_details': video_details,
            'comments': comments[::-1]  # Reverse the order of comments and replies
        }

    return all_comments

def fetch_related_videos(video_title, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Fetch related videos based on the title of the main video
    request = youtube.search().list(
        part="snippet",
        maxResults=10,  # Fetch at most 10 related videos
        q=video_title,
        type="video"
    )

    response = request.execute()

    related_videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_details = fetch_video_details(video_id, api_key)
        if video_details:
            related_videos.append(video_details)

    return related_videos

def main():
    video_url = "https://www.youtube.com/watch?v=rR_ZWFXxFvM"
    api_key = API_KEY

    # Extract video ID from the URL
    video_id = extract_video_id(video_url)
    if video_id:
        print("Extracted Video ID:", video_id)  # Print the extracted video ID
        # Fetch details for the main video
        main_video_details = fetch_video_details(video_id, api_key)

        if main_video_details:
            # Fetch related videos
            related_videos = fetch_related_videos(main_video_details['title'], api_key)
            video_ids = [video_id]  # Add the main video ID
            for video in related_videos:
                video_ids.append(extract_video_id(video['url']))

            all_comments = fetch_comments(video_ids, api_key)  # Pass video_ids instead of video_id
            json_file = write_json_data(all_comments)  # Save data to JSON file
            print("JSON file saved:", json_file)
        else:
            print("Unable to fetch video details for the main video.")
    else:
        print("Invalid YouTube video URL.")

def write_json_data(all_comments):
    # Create JSON structure
    data = []

    # Populate comments for each video
    for video_id, video_data in all_comments.items():
        # Extract video details
        video_details = video_data['video_details']

        # Create video dictionary
        video_dict = {
            "Video ID": video_id,
            "Video Title": video_details['title'],
            "Video URL": video_details['url'],
            "View Count": video_details['view_count'],
            "Comment Count": video_details['comment_count'],
            "Channel Title": video_details['channel_title'],
            "Comments": []
        }

        # Populate comments
        comments = video_data['comments']
        for comment, reply in comments:
            video_dict["Comments"].append({
                "Comment": comment,
                "Reply": reply
            })

        # Append video dictionary to data
        data.append(video_dict)

    # Save data to JSON file
    json_file = "src/data/Comments_Data.json"
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    return json_file


def remove_timestamps(text):
    return re.sub(r'\b\d+:\d+\b', '', text)

def contains_repeating_words(text):
    words = text.lower().split()
    word_count = {}
    
    for word in words:
        if len(word) > 3:
            word_count[word] = word_count.get(word, 0) + 1
    
    for count in word_count.values():
        if count > 3:
            return True
    
    return False

if __name__ == "__main__":
    main()
