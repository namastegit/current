# from googleapiclient.discovery import build
# import csv

# def retrieve_comments(video_id, api_key):
#     youtube = build('youtube', 'v3', developerKey=api_key)
#     comments = []
    
#     # Retrieve top-level comments
#     request = youtube.commentThreads().list(
#         part="snippet",
#         videoId=video_id,
#         maxResults=100
#     )
#     while request is not None:
#         response = request.execute()
#         comments.extend([item['snippet']['topLevelComment']['snippet'] for item in response['items']])
#         request = youtube.commentThreads().list_next(request, response)

#     # Retrieve replies to comments
#     for comment in comments:
#         comment_id = comment['id']
#         replies = []
#         request = youtube.comments().list(
#             part="snippet",
#             parentId=comment_id,
#             maxResults=100
#         )
#         while request is not None:
#             response = request.execute()
#             replies.extend([item['snippet'] for item in response['items']])
#             request = youtube.comments().list_next(request, response)
#         comment['replies'] = replies
    
#     return comments

# def save_comments_to_csv(comments, filename):
#     with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
#         fieldnames = ['authorDisplayName', 'textDisplay', 'publishedAt']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for comment in comments:
#             writer.writerow({
#                 'authorDisplayName': comment['authorDisplayName'],
#                 'textDisplay': comment['textDisplay'],
#                 'publishedAt': comment['publishedAt']
#             })

# if __name__ == "__main__":
#     # Replace 'YOUR_API_KEY' with your actual API key
#     api_key = 'AIzaSyD_jZ0ZbOqCjYrV7Jx1mjuE7AaV6xoD_Ls'
#     # Replace 'XTjtPc0uiG8' with the ID of the YouTube video you want to retrieve comments from
#     video_id = '9OOWI2imCOQ'
#     # Specify the filename to save the comments to
#     filename = 'youtube_comments.csv'

#     comments = retrieve_comments(video_id, api_key)
#     save_comments_to_csv(comments, filename)
