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
            
            # Check if the comment contains keywords related to questions, issues, suggestions, or solutions
            if contains_keywords(comment_text):
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

def contains_keywords(text):
    keywords = ['question', 'issue', 'problem', 'suggestion', 'solution']
    for keyword in keywords:
        if keyword in text.lower():
            return True
    return False
