import csv
import re
import googleapiclient.discovery

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
                    reply = f"({reply_author}: {reply_text})"  # Include reply inside parentheses
                
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
    video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
    api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

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
            write_csv(all_comments)  # Pass only the comments data
            print("Video info and comments saved to CSV file.")
        else:
            print("Unable to fetch video details for the main video.")
    else:
        print("Invalid YouTube video URL.")

def write_csv(all_comments):
    file_name = f"video_comments.csv"

    with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        for video_id, data in all_comments.items():
            video_details = data['video_details']
            comments = data['comments']

            # Write video details
            writer.writerow(["Video Title", "Video URL", "View Count", "Comment Count", "Channel Title"])
            writer.writerow([video_details['title'], video_details['url'], video_details['view_count'],
                             video_details['comment_count'], video_details['channel_title']])
            writer.writerow([])  # Empty row

            # Write comments
            writer.writerow([f"Comments for Video ID: {video_id}"])
            writer.writerow(['Comment', 'Reply'])
            
            for comment in comments:
                writer.writerow([comment[0], comment[1]])

            writer.writerow([])  # Empty row

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




# import csv
# import re
# import googleapiclient.discovery

# def extract_video_id(video_url):
#     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
#     if match:
#         return match.group(1)
#     else:
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
#         statistics_info = response['items'][0].get('statistics', {})

#         video_details = {
#             'title': video_info['title'],
#             'url': f"https://www.youtube.com/watch?v={video_id}",
#             'view_count': statistics_info.get('viewCount', 0),
#             'comment_count': statistics_info.get('commentCount', 0),
#             'channel_title': video_info.get('channelTitle', 'Unknown'),
#             'like_count': statistics_info.get('likeCount', 0)  # Handle missing like count
#         }
#     else:
#         video_details = None

#     return video_details
# def fetch_comments(video_ids, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     all_comments = {}

#     for video_id in video_ids:
#         comments = []  # Using a list to preserve order
#         nextPageToken = None
#         total_comments = 0
        
#         # Fetch comments for the current video
#         while True:
#             request = youtube.commentThreads().list(
#                 part="snippet,replies",
#                 videoId=video_id,
#                 maxResults=100,
#                 pageToken=nextPageToken
#             )

#             response = request.execute()
#             total_comments += response['pageInfo']['totalResults']

#             for item in response['items']:
#                 comment_snippet = item['snippet']['topLevelComment']['snippet']
#                 comment_text = comment_snippet['textDisplay']
                
#                 # Remove timestamps like "7:55" from comments
#                 comment_text = remove_timestamps(comment_text)
                
#                 # Remove HTML tags
#                 comment_text = re.sub(r'<[^>]*>', '', comment_text)
                
#                 like_count = comment_snippet.get('likeCount', 0)
                
#                 # Fetch the first reply for this comment, if any
#                 reply = ""
#                 if 'replies' in item:
#                     reply_snippet = item['replies']['comments'][0]['snippet']
#                     reply_text = reply_snippet['textDisplay']
#                     reply_author = reply_snippet.get('authorDisplayName', 'Unknown')
#                     reply = f"({reply_author}: {reply_text})"  # Include reply inside parentheses
                
#                 # Format the reply or (0) if there are no replies
#                 formatted_reply = reply if reply else "(0)"
                
#                 # Filter out comments with less than six words, more than 150 words,
#                 # repeating single or short words more than three times,
#                 # and comments containing repeating phrases more than three times
#                 if len(comment_text.split()) >= 6 and len(comment_text.split()) <= 150 and not contains_repeating_words(comment_text):
#                     comments.append((comment_text, formatted_reply, like_count))  # Add the comment to the list

#             if 'nextPageToken' in response:
#                 nextPageToken = response['nextPageToken']
#             else:
#                 break

#         # Store the comments and video details in the all_comments dictionary
#         video_details = fetch_video_details(video_id, api_key)
#         all_comments[video_id] = {
#             'video_details': video_details,
#             'comments': comments[::-1]  # Reverse the order of comments and replies
#         }

#     return all_comments


# def fetch_related_videos(video_title, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

#     # Fetch related videos based on the title of the main video
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,  # Fetch at most 10 related videos
#         q=video_title,
#         type="video"
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_details = fetch_video_details(video_id, api_key)
#         if video_details:
#             related_videos.append(video_details)

#     return related_videos

# def main():
#     video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
#     api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

#     # Extract video ID from the URL
#     video_id = extract_video_id(video_url)
#     if video_id:
#         print("Extracted Video ID:", video_id)  # Print the extracted video ID
#         # Fetch details for the main video
#         main_video_details = fetch_video_details(video_id, api_key)

#         if main_video_details:
#             # Fetch related videos
#             related_videos = fetch_related_videos(main_video_details['title'], api_key)
#             video_ids = [video_id]  # Add the main video ID
#             for video in related_videos:
#                 video_ids.append(extract_video_id(video['url']))

#             all_comments = fetch_comments(video_ids, api_key)  # Pass video_ids instead of video_id
#             write_csv(all_comments)  # Pass only the comments data
#             print("Video info and comments saved to CSV file.")
#         else:
#             print("Unable to fetch video details for the main video.")
#     else:
#         print("Invalid YouTube video URL.")

# def write_csv(all_comments):
#     file_name = f"video_comments.csv"

#     with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file)
        
#         for video_id, data in all_comments.items():
#             video_details = data['video_details']
#             comments = data['comments']

#             # Write video details
#             writer.writerow(["Video Title", "Video URL", "View Count", "Like Count", "Comment Count", "Channel Title"])
#             writer.writerow([video_details['title'], video_details['url'], video_details['view_count'],
#                              video_details.get('like_count', 0), video_details['comment_count'],
#                              video_details['channel_title']])
#             writer.writerow([])  # Empty row

#             # Write comments
#             writer.writerow([f"Comments for Video ID: {video_id}"])
#             writer.writerow(['Comment', 'Reply', 'Like Count'])
            
#             for comment in comments:
#                 writer.writerow([comment[0], comment[1], comment[2]])

#             writer.writerow([])  # Empty row

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

# if __name__ == "__main__":
#     main()




# import csv
# import re
# import googleapiclient.discovery

# def extract_video_id(video_url):
#     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
#     if match:
#         return match.group(1)
#     else:
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
#         statistics_info = response['items'][0].get('statistics', {})

#         video_details = {
#             'title': video_info['title'],
#             'url': f"https://www.youtube.com/watch?v={video_id}",
#             'view_count': statistics_info.get('viewCount', 0),
#             'comment_count': statistics_info.get('commentCount', 0),
#             'channel_title': video_info.get('channelTitle', 'Unknown'),
#             'like_count': statistics_info.get('likeCount', 0)  # Handle missing like count
#         }
#     else:
#         video_details = None

#     return video_details

# def fetch_comments(video_ids, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     all_comments = {}

#     for video_id in video_ids:
#         comments = set()  # Using a set to avoid duplicate comments
#         nextPageToken = None
#         total_comments = 0
        
#         # Fetch comments for the current video
#         while True:
#             request = youtube.commentThreads().list(
#                 part="snippet,replies",
#                 videoId=video_id,
#                 maxResults=100,
#                 pageToken=nextPageToken
#             )

#             response = request.execute()
#             total_comments += response['pageInfo']['totalResults']

#             for item in response['items']:
#                 comment_snippet = item['snippet']['topLevelComment']['snippet']
#                 comment_text = comment_snippet['textDisplay']
                
#                 # Remove timestamps like "7:55" from comments
#                 comment_text = remove_timestamps(comment_text)
                
#                 # Remove HTML tags
#                 comment_text = re.sub(r'<[^>]*>', '', comment_text)
                
#                 like_count = comment_snippet.get('likeCount', 0)
                
#                 # Filter out comments with less than six words, more than 150 words,
#                 # repeating single or short words more than three times,
#                 # and comments containing repeating phrases more than three times
#                 if len(comment_text.split()) >= 6 and len(comment_text.split()) <= 150 and not contains_repeating_words(comment_text):
#                     comments.add(comment_text)  # Add the comment to the set

#             if 'nextPageToken' in response:
#                 nextPageToken = response['nextPageToken']
#             else:
#                 break

#         # Store the comments and video details in the all_comments dictionary
#         video_details = fetch_video_details(video_id, api_key)
#         all_comments[video_id] = {
#             'video_details': video_details,
#             'comments': comments
#         }

#     return all_comments

# def fetch_related_videos(video_title, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

#     # Fetch related videos based on the title of the main video
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,  # Fetch at most 10 related videos
#         q=video_title,
#         type="video"
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_details = fetch_video_details(video_id, api_key)
#         if video_details:
#             related_videos.append(video_details)

#     return related_videos

# def main():
#     video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
#     api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

#     # Extract video ID from the URL
#     video_id = extract_video_id(video_url)
#     if video_id:
#         print("Extracted Video ID:", video_id)  # Print the extracted video ID
#         # Fetch details for the main video
#         main_video_details = fetch_video_details(video_id, api_key)

#         if main_video_details:
#             # Fetch related videos
#             related_videos = fetch_related_videos(main_video_details['title'], api_key)
#             video_ids = [video_id]  # Add the main video ID
#             for video in related_videos:
#                 video_ids.append(extract_video_id(video['url']))

#             all_comments = fetch_comments(video_ids, api_key)  # Pass video_ids instead of video_id
#             write_csv(all_comments)  # Pass only the comments data
#             print("Video info and comments saved to CSV file.")
#         else:
#             print("Unable to fetch video details for the main video.")
#     else:
#         print("Invalid YouTube video URL.")

# def write_csv(all_comments):
#     file_name = f"video_comments.csv"

#     with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file)
        
#         for video_id, data in all_comments.items():
#             video_details = data['video_details']
#             comments = data['comments']

#             # Write video details
#             writer.writerow(["Video Title", "Video URL", "View Count", "Like Count", "Comment Count", "Channel Title"])
#             writer.writerow([video_details['title'], video_details['url'], video_details['view_count'],
#                              video_details.get('like_count', 0), video_details['comment_count'],
#                              video_details['channel_title']])
#             writer.writerow([])  # Empty row

#             # Write comments
#             writer.writerow([f"Comments for Video ID: {video_id}"])
#             writer.writerow(['Comment'])
            
#             for comment in comments:
#                 writer.writerow([comment])

#             writer.writerow([])  # Empty row

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

# if __name__ == "__main__":
#     main()





# import csv
# import re
# import googleapiclient.discovery

# def extract_video_id(video_url):
#     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
#     if match:
#         return match.group(1)
#     else:
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
#         statistics_info = response['items'][0].get('statistics', {})

#         video_details = {
#             'title': video_info['title'],
#             'url': f"https://www.youtube.com/watch?v={video_id}",
#             'view_count': statistics_info.get('viewCount', 0),
#             'comment_count': statistics_info.get('commentCount', 0),
#             'channel_title': video_info.get('channelTitle', 'Unknown'),
#             'like_count': statistics_info.get('likeCount', 0)  # Handle missing like count
#         }
#     else:
#         video_details = None

#     return video_details
# def fetch_comments(video_ids, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
#     all_comments = {}

#     for video_id in video_ids:
#         comments = []
#         nextPageToken = None
#         total_comments = 0
        
#         # Fetch comments for the current video
#         while True:
#             request = youtube.commentThreads().list(
#                 part="snippet,replies",
#                 videoId=video_id,
#                 maxResults=100,
#                 pageToken=nextPageToken
#             )

#             response = request.execute()
#             total_comments += response['pageInfo']['totalResults']

#             for item in response['items']:
#                 comment_snippet = item['snippet']['topLevelComment']['snippet']
#                 comment_text = comment_snippet['textDisplay']
#                 like_count = comment_snippet.get('likeCount', 0)  # Default to 0 if likeCount is not present
#                 author_display_name = comment_snippet.get('authorDisplayName', 'Unknown')
#                 published_at = comment_snippet.get('publishedAt', 'Unknown')
#                 comment_id = item['id']
#                 parent_id = comment_snippet.get('parentId', None)  # If it's a reply, include the parent comment ID

#                 # Fetch replies for this comment
#                 replies = []
#                 if 'replies' in item:
#                     for reply_item in item['replies']['comments']:
#                         reply_snippet = reply_item['snippet']
#                         reply_text = reply_snippet['textDisplay']
#                         reply_like_count = reply_snippet.get('likeCount', 0)
#                         reply_author_display_name = reply_snippet.get('authorDisplayName', 'Unknown')
#                         reply_published_at = reply_snippet.get('publishedAt', 'Unknown')
#                         reply_id = reply_item['id']
                        
#                         reply_info = {
#                             'id': reply_id,
#                             'parent_id': comment_id,  # Parent ID is the ID of the comment this is replying to
#                             'text': reply_text,
#                             'like_count': reply_like_count,
#                             'author_display_name': reply_author_display_name,
#                             'published_at': reply_published_at
#                         }
#                         replies.append(reply_info)

#                 comment_info = {
#                     'id': comment_id,
#                     'text': comment_text,
#                     'like_count': like_count,
#                     'author_display_name': author_display_name,
#                     'published_at': published_at,
#                     'replies': replies  # Include replies for this comment
#                 }
#                 comments.append(comment_info)

#             if 'nextPageToken' in response:
#                 nextPageToken = response['nextPageToken']
#             else:
#                 break

#         # Store the comments and video details in the all_comments dictionary
#         video_details = fetch_video_details(video_id, api_key)
#         all_comments[video_id] = {
#             'video_details': video_details,
#             'comments': comments
#         }

#     return all_comments


# def fetch_related_videos(video_title, api_key):
#     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

#     # Fetch related videos based on the title of the main video
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=10,  # Fetch at most 10 related videos
#         q=video_title,
#         type="video"
#     )

#     response = request.execute()

#     related_videos = []
#     for item in response['items']:
#         video_id = item['id']['videoId']
#         video_details = fetch_video_details(video_id, api_key)
#         if video_details:
#             related_videos.append(video_details)

#     return related_videos
# def main():
#     video_url = "https://www.youtube.com/watch?v=WoDQaSx7ifI"
#     api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

#     # Extract video ID from the URL
#     video_id = extract_video_id(video_url)
#     if video_id:
#         print("Extracted Video ID:", video_id)  # Print the extracted video ID
#         # Fetch details for the main video
#         main_video_details = fetch_video_details(video_id, api_key)

#         if main_video_details:
#             # Fetch related videos
#             related_videos = fetch_related_videos(main_video_details['title'], api_key)
#             video_ids = [video_id]  # Add the main video ID
#             for video in related_videos:
#                 video_ids.append(extract_video_id(video['url']))

#             all_comments = fetch_comments(video_ids, api_key)  # Pass video_ids instead of video_id
#             write_csv(all_comments)  # Pass only the comments data
#             print("Video info and comments saved to CSV file.")
#         else:
#             print("Unable to fetch video details for the main video.")
#     else:
#         print("Invalid YouTube video URL.")
# def write_csv(all_comments):
#     file_name = f"video_comments.csv"

#     with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file)
        
#         for video_id, data in all_comments.items():
#             video_details = data['video_details']
#             comments = data['comments']

#             # Write video details
#             writer.writerow(["Video Title", "Video URL", "View Count", "Like Count", "Comment Count", "Channel Title"])
#             writer.writerow([video_details['title'], video_details['url'], video_details['view_count'],
#                              video_details.get('like_count', 0), video_details['comment_count'],
#                              video_details['channel_title']])
#             writer.writerow([])  # Empty row

#             # Write comments
#             writer.writerow([f"Comments for Video ID: {video_id}"])
#             writer.writerow(['Comment', 'Replies'])
            
#             for comment_info in comments:
#                 comment_text = comment_info['text']
#                 replies = comment_info['replies']
#                 formatted_replies = f"({len(replies)})" if replies else "(0)"
#                 writer.writerow([comment_text, formatted_replies])

#             writer.writerow([])  # Empty row


# if __name__ == "__main__":
#     main()
