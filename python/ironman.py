import csv
import re
import googleapiclient.discovery

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
            'video_id': video_id,  # Add video ID to the details
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

            # Fetch replies to comments
            replies = fetch_comment_replies(item['id'], api_key)
            comments.update(replies)

        if 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
        else:
            break

    # Convert the set back to a list for further processing
    comments = list(comments)
    comments.sort(key=lambda x: x[1], reverse=True)

    return total_comments, comments

def fetch_comment_replies(parent_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    replies = set()

    request = youtube.comments().list(
        part="snippet",
        parentId=parent_id,
        maxResults=100
    )

    response = request.execute()

    for item in response['items']:
        reply_snippet = item['snippet']
        reply_text = reply_snippet['textDisplay']
        reply_like_count = reply_snippet.get('likeCount', 0)

        replies.add((reply_text, reply_like_count))

    return replies

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
        # Fetch details for the main video
        main_video_details = fetch_video_details(video_id, api_key)

        if main_video_details:
            # Fetch related videos
            related_videos = fetch_related_videos(main_video_details['title'], api_key)
            
            # Add the main video to the list of related videos
            all_videos = [main_video_details] + related_videos
            
            # Fetch comments for all videos
            for video in all_videos:
                total_comments, comments = fetch_comments(video['video_id'], api_key)
                # Write video details and comments into CSV files
                write_csv(video, total_comments, comments)

            print("Video info and comments saved to CSV files.")
        else:
            print("Unable to fetch video details for the main video.")
    else:
        print("Invalid YouTube video URL.")
def write_csv(video_details, total_comments, comments):
    word_count = 0
    file_name = f"video_info_combined.csv"

    with open(file_name, "a", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write video details
        writer.writerow(['Video Title', 'Video URL', 'View Count', 'Like Count', 'Comment Count', 'Channel Title', 'Comment', 'Like Count'])
        writer.writerow([video_details['title'], f"https://www.youtube.com/watch?v={video_details['video_id']}", video_details['view_count'], video_details['like_count'], video_details['comment_count'], video_details['channel_title'], '', ''])
        
        # Write comments
        for comment_text, like_count in comments:
            # Remove any unwanted characters from the comment
            cleaned_comment = re.sub(r"[^\w\s]", "", comment_text)
            
            # Write the cleaned comment to the CSV file
            writer.writerow(['', '', '', '', '', '', cleaned_comment, like_count])
            word_count += len(cleaned_comment.split())

            if word_count >= 9000:
                writer.writerow(['', '', '', '', '', '', 'Continuation...', ''])
                word_count = 0


if __name__ == "__main__":
    main()
