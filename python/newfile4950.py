import csv
import re
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
    video_id = "06g6YJ6JCJU"
    api_key = "YOUR_API_KEY"

    video_details = fetch_video_details(video_id, api_key)
    total_comments, comments = fetch_comments(video_id, api_key)

    word_count = 0
    file_number = 1
    file_name = f"video_info_{file_number}.csv"

    with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Video Title', 'View Count', 'Like Count', 'Comment Count', 'Channel Title'])
        writer.writerow([video_details['title'], video_details['view_count'], video_details['like_count'], video_details['comment_count'], video_details['channel_title']])
        writer.writerow([])
        writer.writerow(['Total Comments', total_comments])
        writer.writerow([])
        writer.writerow(['Comment', 'Like Count'])

        for comment_text, like_count in comments:
            writer.writerow([comment_text, like_count])
            word_count += len(comment_text.split())

            if word_count > 4950:
                word_count = 0
                file_number += 1
                file_name = f"video_info_{file_number}.csv"
                
                # Close the current file and open a new one
                csv_file.close()
                csv_file = open(file_name, "w", newline='', encoding='utf-8')
                writer = csv.writer(csv_file)
                writer.writerow(['Comment', 'Like Count'])

    print("Comments saved to CSV files.")

if __name__ == "__main__":
    main()
