import csv
import googleapiclient.discovery

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
            like_count = comment_snippet.get('likeCount', 0)
            comments.append([comment_text, like_count])

        if 'nextPageToken' in response:
            nextPageToken = response['nextPageToken']
        else:
            break

    comments.sort(key=lambda x: x[1], reverse=True)

    return total_comments, comments

def main():
    video_id = "lHUUTboLuQ4"
    api_key = "AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls"

    video_details = fetch_video_details(video_id, api_key)
    total_comments, comments = fetch_comments(video_id, api_key)

    with open("video_info.csv", "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Video Title', 'View Count', 'Like Count', 'Comment Count', 'Channel Title'])
        writer.writerow([video_details['title'], video_details['view_count'], video_details['like_count'], video_details['comment_count'], video_details['channel_title']])
        writer.writerow([])
        writer.writerow(['Total Comments', total_comments])
        writer.writerow([])
        writer.writerow(['Comment', 'Like Count'])
        writer.writerows(comments)

    print("Video info saved to video_info.csv")

if __name__ == "__main__":
    main()
