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
        comments = []
        nextPageToken = None
        total_comments = 0

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

                # Check if replies exist for the comment
                if 'replies' in item['snippet']:
                    replies_data = item['snippet']['replies']['comments']
                    # Fetch at most one reply for each comment
                    replies = fetch_comment_replies(replies_data, 1)
                else:
                    replies = []

                comments.append((comment_text, replies))

            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
            else:
                break

        all_comments[video_id] = (total_comments, comments)

    return all_comments

def fetch_comment_replies(replies_data, max_replies):
    replies = []
    for reply in replies_data:
        if max_replies == 0:
            break
        reply_snippet = reply['snippet']
        reply_text = reply_snippet['textDisplay']
        replies.append(reply_text)
        max_replies -= 1
    return replies

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
            video_ids = [extract_video_id(video['url']) for video in related_videos]
            video_ids.append(video_id)  # Add the main video ID

            all_comments = fetch_comments(video_ids, api_key)
            write_csv(all_comments, main_video_details)  # Pass both arguments
            print("Video info and comments saved to CSV file.")
        else:
            print("Unable to fetch video details for the main video.")
    else:
        print("Invalid YouTube video URL.")

def write_csv(all_comments, video_details):
    file_name = f"video_comments.csv"

    with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write video details
        writer.writerow(["Video Title", "Video URL", "View Count", "Like Count", "Comment Count", "Channel Title"])
        writer.writerow([video_details['title'], video_details['url'], video_details['view_count'],
                         video_details.get('like_count', 0), video_details['comment_count'],
                         video_details['channel_title']])
        writer.writerow([])  # Empty row

        # Write comments
        for video_id, (total_comments, comments) in all_comments.items():
            writer.writerow([f"Comments for Video ID: {video_id}"])
            writer.writerow(['Comment', 'Replies'])
            for comment_text, replies in comments:
                formatted_replies = f"({'; '.join(replies)})" if replies else "(0)"
                writer.writerow([comment_text, formatted_replies])
            writer.writerow([])  # Empty row



if __name__ == "__main__":
    main()
