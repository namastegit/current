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
        video_info = response['items'][0]['snippet']
        statistics_info = response['items'][0]['statistics']

        video_details = {
            'title': video_info['title'],
            # 'description': video_info.get('description', 'Unknown'),
            # 'upload_date': video_info['publishedAt'],
            'view_count': statistics_info['viewCount'],
            'like_count': statistics_info.get('likeCount', 0),
            # 'dislike_count': statistics_info.get('dislikeCount', 0),
            'comment_count': statistics_info.get('commentCount', 0),
            'channel_title': video_info.get('channelTitle', 'Unknown')
        }
    else:
        video_details = None

    return video_details

def fetch_comments(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    comments = []
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
            like_count = comment_snippet.get('likeCount', 0)  # Default to 0 if likeCount is not present
            author_display_name = comment_snippet.get('authorDisplayName', 'Unknown')
            published_at = comment_snippet.get('publishedAt', 'Unknown')
            comment_id = item['id']
            video_id = comment_snippet.get('videoId', 'Unknown')
            parent_id = comment_snippet.get('parentId', None)  # If it's a reply, include the parent comment ID

            comment_info = {
                # 'id': comment_id,
                # 'video_id': video_id,
                # 'parent_id': parent_id,
                'text': comment_text,
                'like_count': like_count,
                # 'author_display_name': author_display_name,
                # 'published_at': published_at
            }
            comments.append(comment_info)

        if 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
        else:
            break

    # Sort comments based on like_count in descending order
    comments.sort(key=lambda x: x['like_count'], reverse=True)

    # Add total number of comments to the first section of the JSON data
    comments_data = {'total_comments': total_comments, 'comments': comments}

    return comments_data

def main():
    video_id = "8uwud1igM_E"  # Video ID without timestamp
    api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

    video_details = fetch_video_details(video_id, api_key)
    comments_data = fetch_comments(video_id, api_key)

    # Combine video details and comments into one dictionary
    video_info = {'video_details': video_details, 'comments_data': comments_data}

    # Write combined data to a JSON file
    with open("video_info.json", "w") as json_file:
        json.dump(video_info, json_file, indent=4)

    print("Video info saved to video_info.json")

if __name__ == "__main__":
    main()
