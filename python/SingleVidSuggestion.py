import googleapiclient.discovery
import json

def fetch_video_details(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )

    response = request.execute()

    if response['items']:
        video_info = response['items'][0]
        snippet = video_info['snippet']
        statistics = video_info['statistics']
        
        video_title = snippet['title']
        channel_title = snippet['channelTitle']
        upload_date = snippet['publishedAt']
        total_likes = statistics.get('likeCount', 0)
        total_dislikes = statistics.get('dislikeCount', 0)
        total_comments = statistics.get('commentCount', 0)
    else:
        return None

    return {
        'title': video_title,
        'video_id': video_id,
        'video_link': f"https://www.youtube.com/watch?v={video_id}",
        'channel_title': channel_title,
        'upload_date': upload_date,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': total_comments
    }

def fetch_related_videos(video_title, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Fetch related videos based on the title of the main video
    request = youtube.search().list(
        part="snippet",
        maxResults=20,  # Fetch at most 20 related videos
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
    video_id = "YLagvzoWCL0"  # Video ID without timestamp
    api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

    # Fetch details for the main video
    main_video_details = fetch_video_details(video_id, api_key)

    if main_video_details:
        # Fetch related videos
        related_videos = fetch_related_videos(main_video_details['title'], api_key)

        if related_videos:
            # Write main video details and related videos into a JSON file
            video_info = [main_video_details] + related_videos[:19]  # Keep at most 20 videos including the main video
            with open("video_info.json", "w") as json_file:
                json.dump(video_info, json_file, indent=4)

            print("Main video info and related videos saved to video_info.json")
        else:
            print("Unable to fetch related videos.")
    else:
        print("Unable to fetch details for the main video.")

if __name__ == "__main__":
    main()

# -------------------------------------------------------------



# import googleapiclient.discovery
# import json

# def fetch_video_details(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=video_id
#     )

#     response = request.execute()

#     if response['items']:
#         video_info = response['items'][0]
#         snippet = video_info['snippet']
#         statistics = video_info['statistics']
        
#         video_title = snippet['title']
#         channel_title = snippet['channelTitle']
#         upload_date = snippet['publishedAt']
#         total_likes = statistics.get('likeCount', 0)
#         total_dislikes = statistics.get('dislikeCount', 0)
#         total_comments = statistics.get('commentCount', 0)
#     else:
#         return None

#     return {
#         'title': video_title,
#         'video_id': video_id,
#         'video_link': f"https://www.youtube.com/watch?v={video_id}",
#         'channel_title': channel_title,
#         'upload_date': upload_date,
#         'total_likes': total_likes,
#         'total_dislikes': total_dislikes,
#         'total_comments': total_comments
#     }

# def main():
#     videos = [
#         {"video_id": "MLagf3_APuY", "channel_title": "Connor Byers"},
#         {"video_id": "7EVlx7mpZ4M", "channel_title": "HBA Services"}
#         # Add more video IDs and channel titles as needed
#     ]
#     api_key = "AIzaSyCVVe3CKVgaHtKSNyK9wJ__7rvZ3MKuoxM"

#     video_details = []
#     for video in videos:
#         details = fetch_video_details(video['video_id'], api_key)
#         if details:
#             video_details.append(details)
#         else:
#             print(f"Unable to fetch details for video ID: {video['video_id']}")

#     if video_details:
#         # Write video details into a JSON file
#         with open("video_info.json", "w") as json_file:
#             json.dump(video_details, json_file, indent=4)

#         print("Video info saved to video_info.json")
#     else:
#         print("Unable to fetch video details for any videos.")

# if __name__ == "__main__":
#     main()


# import googleapiclient.discovery
# import json

# def fetch_video_details(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=video_id
#     )

#     response = request.execute()

#     if response['items']:
#         video_info = response['items'][0]
#         snippet = video_info['snippet']
#         statistics = video_info['statistics']
        
#         video_title = snippet['title']
#         channel_title = snippet['channelTitle']
#         upload_date = snippet['publishedAt']
#         total_likes = statistics.get('likeCount', 0)
#         total_dislikes = statistics.get('dislikeCount', 0)
#         total_comments = statistics.get('commentCount', 0)
#     else:
#         return None

#     # Search for related videos based on the broader terms related to the main video's title
#     query = f"{video_title} tutorial"
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=15,  # Fetching more related videos
#         q=query,
#         type="video"
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_title = item['snippet']['title']
#         video_link = f"https://www.youtube.com/watch?v={video_id}"
#         channel_title = item['snippet']['channelTitle']  # Extract channel title from related video
#         upload_date = item['snippet']['publishedAt']  # Extract upload date from related video
#         related_videos.append({
#             'title': video_title,
#             'video_id': video_id,
#             'video_link': video_link,
#             'channel_title': channel_title,
#             'upload_date': upload_date,
#             'total_likes': 0,  # Initialize likes, dislikes, and comments to 0 for related videos
#             'total_dislikes': 0,
#             'total_comments': 0
#         })

#     return related_videos

# def main():
#     video_id = "MLagf3_APuY"  # Video ID without timestamp
#     api_key = "AIzaSyCVVe3CKVgaHtKSNyK9wJ__7rvZ3MKuoxM"

#     video_details = fetch_video_details(video_id, api_key)

#     if video_details:
#         # Write video details and related videos into a JSON file
#         with open("video_info.json", "w") as json_file:
#             json.dump(video_details, json_file, indent=4)

#         print("Video info saved to video_info.json")
#     else:
#         print("Unable to fetch video details.")

# if __name__ == "__main__":
#     main()


