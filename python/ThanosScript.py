import csv
import re
import googleapiclient.discovery
import datetime
import json

def extract_video_id(video_url):
    # Extract video ID from the YouTube video URL
    match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
    if match:
        return match.group(1)
    else:
        # If the URL doesn't match the expected format, return None
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
        statistics_info = response['items'][0]['statistics']

        video_details = {
            'title': video_info['title'],
            'view_count': statistics_info['viewCount'],
            'like_count': statistics_info.get('likeCount', 0),
            'comment_count': statistics_info.get('commentCount', 0),
            'channel_title': video_info.get('channelTitle', 'Unknown')
        }
    else:
        video_details = None

    return video_details

def fetch_comments(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    comments = set()  # Use a set to store unique comments
    nextPageToken = None
    total_comments = 0
    
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
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
            
            like_count = comment_snippet.get('likeCount', 0)
            
            # Filter out comments with less than six words, more than 150 words,
            # repeating single or short words more than three times,
            # and comments containing repeating phrases more than three times
            if len(comment_text.split()) >= 6 and len(comment_text.split()) <= 150 and not contains_repeating_words(comment_text):
                comments.add((comment_text, like_count))  # Add the comment to the set

        if 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
        else:
            break

    # Convert the set back to a list for further processing
    comments = list(comments)
    comments.sort(key=lambda x: x[1], reverse=True)

    return total_comments, comments

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

def main():
    video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
    api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

    # Extract video ID from the URL
    video_id = extract_video_id(video_url)
    if video_id:
        # Fetch details for the main video
        video_details = fetch_video_details(video_id, api_key)
        total_comments, comments = fetch_comments(video_id, api_key)

        if video_details:
            # Write video details and comments into CSV files
            write_csv(video_details, total_comments, comments)

            print("Video info and comments saved to CSV files.")
        else:
            print("Unable to fetch video details.")
    else:
        print("Invalid YouTube video URL.")

def write_csv(video_details, total_comments, comments):
    word_count = 0
    file_number = 1
    file_name = f"video_info_{file_number}.csv"

    with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Video Title', 'View Count', 'Like Count', 'Comment Count', 'Channel Title', 'Total Comments'])
        writer.writerow([video_details['title'], video_details['view_count'], video_details['like_count'], video_details['comment_count'], video_details['channel_title'], total_comments])
        writer.writerow([])
        writer.writerow(['Comment', 'Like Count'])

        for comment, like_count in comments:
            writer.writerow([comment, like_count])
            word_count += len(comment.split())

            # Check if the word count exceeds 10,000 words
            if word_count >= 10000:
                file_number += 1
                file_name = f"video_info_{file_number}.csv"
                csv_file.close()
                csv_file = open(file_name, "w", newline='', encoding='utf-8')
                writer = csv.writer(csv_file)
                writer.writerow(['Comment', 'Like Count'])
                word_count = 0

if __name__ == "__main__":
    main()




# import csv
# import re
# import googleapiclient.discovery
# import datetime

# def extract_video_id(video_url):
#     # Extract video ID from the YouTube video URL
#     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
#     if match:
#         return match.group(1)
#     else:
#         # If the URL doesn't match the expected format, return None
#         return None

# def fetch_video_details(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=video_id
#     )

#     response = request.execute()

#     if response['items']:
#         video_info = response['items'][0]['snippet']
#         statistics_info = response['items'][0]['statistics']

#         video_details = {
#             'title': video_info['title'],
#             'view_count': statistics_info['viewCount'],
#             'like_count': statistics_info.get('likeCount', 0),
#             'dislike_count': statistics_info.get('dislikeCount', 0),
#             'comment_count': statistics_info.get('commentCount', 0),
#             'channel_title': video_info.get('channelTitle', 'Unknown'),
#             'upload_date': video_info['publishedAt']
#         }
#     else:
#         video_details = None

#     return video_details

# def fetch_related_videos(video_title, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

#     # Fetch related videos based on the title of the main video
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,  # Fetch 10 related videos
#         q=video_title,
#         type="video",
#         order="date",  # Order by date (recent first)
#         publishedAfter=(datetime.datetime.now() - datetime.timedelta(days=365)).isoformat() + "Z"  # Add 'Z' to the timestamp
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_details = fetch_video_details(video_id, api_key)
#         if video_details:
#             related_videos.append(video_details)

#     return related_videos
# def fetch_comments(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     comments = []
#     nextPageToken = None
#     total_comments = 0
    
#     while True:
#         request = youtube.commentThreads().list(
#             part="snippet",
#             videoId=video_id,
#             maxResults=100,
#             pageToken=nextPageToken
#         )

#         response = request.execute()
#         total_comments += response['pageInfo']['totalResults']

#         for item in response['items']:
#             comment_snippet = item['snippet']['topLevelComment']['snippet']
#             comment_text = comment_snippet['textDisplay']
#             like_count = comment_snippet.get('likeCount', 0)  # Default to 0 if likeCount is not present
#             author_display_name = comment_snippet['authorDisplayName'] if 'authorDisplayName' in comment_snippet else 'Unknown'
#             published_at = comment_snippet['publishedAt'] if 'publishedAt' in comment_snippet else 'Unknown'
#             comment_id = item['id']
#             video_id = comment_snippet['videoId'] if 'videoId' in comment_snippet else 'Unknown'
#             parent_id = comment_snippet['parentId'] if 'parentId' in comment_snippet else None  # If it's a reply, include the parent comment ID

#             comment_info = {
#                 'id': comment_id,
#                 'video_id': video_id,
#                 'parent_id': parent_id,
#                 'text': comment_text,
#                 'like_count': like_count,
#                 'author_display_name': author_display_name,
#                 'published_at': published_at
#             }
#             comments.append(comment_info)

#         if 'nextPageToken' in response:
#             nextPageToken = response['nextPageToken']
#         else:
#             break

#     # Sort comments based on published_at in descending order
#     comments.sort(key=lambda x: x['published_at'], reverse=True)

#     # Add total number of comments to the first section of the JSON data
#     comments_data = {'total_comments': total_comments, 'comments': comments}

#     return total_comments, comments


# def remove_timestamps(text):
#     return re.sub(r'\b\d+:\d+\b', '', text)

# def contains_repeating_words(text):
#     words = text.lower().split()
#     word_count = {}
    
#     for word in words:
#         if len(word) > 3:
#             word_count[word] = word_count.get(word, 0) + 1
    
#     for count in word_count.values():
#         if count > 3:
#             return True
    
#     return False

# def main():
#     video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
#     api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

#     # Extract video ID from the URL
#     video_id = extract_video_id(video_url)
#     if video_id:
#         # Fetch details for the main video
#         main_video_details = fetch_video_details(video_id, api_key)

#         if main_video_details:
#             # Fetch related videos
#             related_videos = fetch_related_videos(main_video_details['title'], api_key)

#             if related_videos:
#                 # Write main video details and related videos into a CSV file
#                 with open("video_info.csv", "w", newline='', encoding='utf-8') as csv_file:
#                     writer = csv.writer(csv_file)
#                     writer.writerow(['Video Title', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count', 'Channel Title', 'Upload Date'])
#                     writer.writerow([main_video_details['title'], main_video_details['view_count'], main_video_details['like_count'], main_video_details['dislike_count'], main_video_details['comment_count'], main_video_details['channel_title'], main_video_details['upload_date']])
#                     writer.writerow([])

#                     # Fetch comments for the main video
#                     total_comments, comments = fetch_comments(video_id, api_key)

#                     writer.writerow(['Total Comments', total_comments])
#                     writer.writerow([])

#                     # Write comments to the CSV file
#                     writer.writerow(['Comment', 'Like Count', 'Author', 'Published Date'])
#                     for comment in comments:
#                         writer.writerow([comment['text'], comment['like_count'], comment['author_display_name'], comment['published_at']])

#                 print("Main video info and related videos saved to video_info.csv")
#             else:
#                 print("Unable to fetch related videos.")
#         else:
#             print("Unable to fetch details for the main video.")
#     else:
#         print("Invalid YouTube video URL.")

# if __name__ == "__main__":
#     main()



# import csv
# import re
# import googleapiclient.discovery
# import datetime

# def extract_video_id(video_url):
#     # Extract video ID from the YouTube video URL
#     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
#     if match:
#         return match.group(1)
#     else:
#         # If the URL doesn't match the expected format, return None
#         return None

# def fetch_video_details(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     request = youtube.videos().list(
#         part="snippet,statistics",
#         id=video_id
#     )

#     response = request.execute()

#     if response['items']:
#         video_info = response['items'][0]['snippet']
#         statistics_info = response['items'][0]['statistics']

#         video_details = {
#             'title': video_info['title'],
#             'view_count': statistics_info['viewCount'],
#             'like_count': statistics_info.get('likeCount', 0),
#             'dislike_count': statistics_info.get('dislikeCount', 0),
#             'comment_count': statistics_info.get('commentCount', 0),
#             'channel_title': video_info.get('channelTitle', 'Unknown'),
#             'upload_date': video_info['publishedAt']
#         }
#     else:
#         video_details = None

#     return video_details

# def fetch_related_videos(video_title, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

#     # Fetch related videos based on the title of the main video
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,  # Fetch 10 related videos
#         q=video_title,
#         type="video",
#         order="date",  # Order by date (recent first)
#         publishedAfter=(datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()  # Within the last 12 months
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_details = fetch_video_details(video_id, api_key)
#         if video_details:
#             related_videos.append(video_details)

#     return related_videos

# def fetch_comments(video_id, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     comments = []
#     nextPageToken = None
#     total_comments = 0
    
#     while True:
#         request = youtube.commentThreads().list(
#             part="snippet",
#             videoId=video_id,
#             maxResults=100,
#             pageToken=nextPageToken
#         )

#         response = request.execute()
#         total_comments += response['pageInfo']['totalResults']

#         for item in response['items']:
#             comment_snippet = item['snippet']['topLevelComment']['snippet']
#             comment_text = comment_snippet['textDisplay']
#             like_count = comment_snippet.get('likeCount', 0)  # Default to 0 if likeCount is not present
#             author_display_name = comment_snippet.get('authorDisplayName', 'Unknown')
#             published_at = comment_snippet.get('publishedAt', 'Unknown')
#             comment_id = item['id']
#             video_id = comment_snippet.get('videoId', 'Unknown')
#             parent_id = comment_snippet.get('parentId', None)  # If it's a reply, include the parent comment ID

#             comment_info = {
#                 'id': comment_id,
#                 'video_id': video_id,
#                 'parent_id': parent_id,
#                 'text': comment_text,
#                 'like_count': like_count,
#                 'author_display_name': author_display_name,
#                 'published_at': published_at
#             }
#             comments.append(comment_info)

#         if 'nextPageToken' in response:
#             nextPageToken = response['nextPageToken']
#         else:
#             break

#     # Sort comments based on published_at in descending order
#     comments.sort(key=lambda x: x['published_at'], reverse=True)

#     # Add total number of comments to the first section of the JSON data
#     comments_data = {'total_comments': total_comments, 'comments': comments}

#     return comments_data

# def remove_timestamps(text):
#     return re.sub(r'\b\d+:\d+\b', '', text)

# def contains_repeating_words(text):
#     words = text.lower().split()
#     word_count = {}
    
#     for word in words:
#         if len(word) > 3:
#             word_count[word] = word_count.get(word, 0) + 1
    
#     for count in word_count.values():
#         if count > 3:
#             return True
    
#     return False

# def main():
#     video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
#     api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

#     # Extract video ID from the URL
#     video_id = extract_video_id(video_url)
#     if video_id:
#         # Fetch details for the main video
#         main_video_details = fetch_video_details(video_id, api_key)

#         if main_video_details:
#             # Fetch related videos
#             related_videos = fetch_related_videos(main_video_details['title'], api_key)

#             if related_videos:
#                 # Write main video details and related videos into a CSV file
#                 with open("video_info.csv", "w", newline='', encoding='utf-8') as csv_file:
#                     writer = csv.writer(csv_file)
#                     writer.writerow(['Video Title', 'View Count', 'Like Count', 'Dislike Count', 'Comment Count', 'Channel Title', 'Upload Date'])
#                     writer.writerow([main_video_details['title'], main_video_details['view_count'], main_video_details['like_count'], main_video_details['dislike_count'], main_video_details['comment_count'], main_video_details['channel_title'], main_video_details['upload_date']])
#                     writer.writerow([])

#                     # Fetch comments for the main video
#                     total_comments, comments = fetch_comments(video_id, api_key)

#                     writer.writerow(['Total Comments', total_comments])
#                     writer.writerow([])

#                     # Write comments to the CSV file
#                     writer.writerow(['Comment', 'Like Count', 'Author', 'Published Date'])
#                     for comment in comments:
#                         writer.writerow([comment['text'], comment['like_count'], comment['author_display_name'], comment['published_at']])

#                 print("Main video info and related videos saved to video_info.csv")
#             else:
#                 print("Unable to fetch related videos.")
#         else:
#             print("Unable to fetch details for the main video.")
#     else:
#         print("Invalid YouTube video URL.")

# if __name__ == "__main__":
#     main()
