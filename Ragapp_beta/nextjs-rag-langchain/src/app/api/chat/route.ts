import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';

export const dynamic = 'force-dynamic'

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
});

export async function POST(req: Request) {
    // Extract the `messages` from the body of the request
    const { input } = await req.json();

    // Request the OpenAI API for the response based on the prompt
    const response = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo',
        stream: true,
        messages: input,
    });

    // Convert the response into a friendly text-stream
    const stream = OpenAIStream(response);

    // Respond with the stream
    return new StreamingTextResponse(stream);
}

// py2.py file-------vvvvvvvv
// import json
// import re
// import googleapiclient.discovery
// import os
// import io
// from dotenv import load_dotenv
// from typing import Any

// # Load environment variables from the .env file
// load_dotenv()

// # Access the GOOGLE_API_KEY from the environment
// API_KEY = os.getenv('GOOGLE_API_KEY')

// FLAG_FILE = "script_ran.flag"

// # Define function to check for repeating words in a comment
// def contains_repeating_words(comment):
//     words = comment.lower().split()
//     word_count = {}
//     for word in words:
//         if len(word) > 1:  # Ignore single character words
//             if word in word_count:
//                 word_count[word] += 1
//                 if word_count[word] > 3:  # Check if word repeats more than three times
//                     return True
//             else:
//                 word_count[word] = 1
//     return False

// # Define function to get formatted reply
// def get_formatted_reply(item):
//     if 'replies' in item:
//         reply_snippet = item['replies']['comments'][0]['snippet']
//         reply_text = reply_snippet['textDisplay']
//         reply_author = reply_snippet.get('authorDisplayName', 'Unknown')
//         return f"({reply_author}: {reply_text})"  # Include reply inside parentheses
//     else:
//         return "(0)"  # Return (0) if there are no replies

// # Now integrate these functions into the existing code.


// def extract_video_id(video_url):
//     match = re.search(r"youtube\.com/watch\?v=([^\s&]+)", video_url)
//     if match:
//         return match.group(1)
//     else:
//         return None

// def fetch_video_details(video_id, api_key):
//     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
//     request = youtube.videos().list(
//         part="snippet",
//         id=video_id
//     )

//     response = request.execute()

//     if response['items']:
//         video_info = response['items'][0]['snippet']

//         video_details = {
//             'title': video_info['title'],
//             'url': f"https://www.youtube.com/watch?v={video_id}"
//         }
//     else:
//         video_details = None

//     return video_details

// def remove_timestamps(text):
//     return re.sub(r'\b\d+:\d+\b', '', text)

// def fetch_comments(video_url, api_key):
//     video_id = extract_video_id(video_url)
//     if not video_id:
//         print("Invalid YouTube video URL.")
//         return

//     youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
//     all_comments = []  # List to store all comments

//     nextPageToken = None
    
//     # Fetch comments for the current video
//     while True:
//         request = youtube.commentThreads().list(
//             part="snippet,replies",
//             videoId=video_id,
//             maxResults=100,
//             pageToken=nextPageToken
//         )

//         response = request.execute()

//         for item in response['items']:
//             comment_snippet = item['snippet']['topLevelComment']['snippet']
//             comment_text = comment_snippet['textDisplay']
            
//             # Remove timestamps like "7:55" from comments
//             comment_text = remove_timestamps(comment_text)
            
//             # Remove HTML tags
//             comment_text = re.sub(r'<[^>]*>', '', comment_text)
            
//             # Filter out comments with less than six words, more than 150 words,
//             # repeating single or short words more than three times,
//             # and comments containing repeating phrases more than three times
//             if len(comment_text.split()) >= 6 and len(comment_text.split()) <= 150 and not contains_repeating_words(comment_text):
//                 formatted_reply = get_formatted_reply(item)
//                 all_comments.append((comment_text, formatted_reply))

//         if 'nextPageToken' in response:
//             nextPageToken = response['nextPageToken']
//         else:
//             break

//     # Store the comments and video details in the dictionary
//     video_details = fetch_video_details(video_id, api_key)
//     all_comments_dict = {
//         'video_details': video_details,
//         'all_comments': all_comments
//     }

//     return all_comments_dict

// def write_json(video_url, all_comments):
//     video_id = extract_video_id(video_url)
//     if not video_id:
//         print("Invalid YouTube video URL.")
//         return

//     # Set of words indicating problems
//     problem_words = {'problem', 'failed', 'build error', 'build', 'issue', 'error', 'fake', 'notworking', 'bug', 'glitch', 'malfunction',
//                      'fault', 'flaw', 'breakdown', 'failure', 'defect', 'bug', 'error', 'exception', 'crash', 'issue', 'fault', 'flaw', 'defect',
//                      'glitch', 'compile', 'runtime error', 'logic', 'memory', 'performance', 'debug',
//                      'warning', 'failure', 'breakdown', 'malfunction', 'timeout', 'stack overflow',
//                      'infinite loop', 'deadlock', 'race condition'}
//     # Set of words indicating questions
//     question_words = {
//         'what', 'why', 'how', 'where', 'when are', 'which', 'who', 'whom', 'whose', 'whence',
//         'whither', 'whatever', 'whichever', 'whoever', 'whomever', 'wheresoever', 'whencesoever',
//         'whithersoever', 'how come', 'can', 'could you', 'will you ', 'would you', 'should you', 'Is he', 'Is she', 'are you', 'is there any', 'Is it ',
//         'do you', 'did you', 'can\'t you', 'can\'t this', 'can\'t it', 'won\'t', 'won\'t you',
//         'won\'t this', 'won\'t it', 'couldn\'t you', 'couldn\'t this', 'couldn\'t it',
//         'wouldn\'t', 'wouldn\'t you', 'wouldn\'t this', 'wouldn\'t it', 'shouldn\'t', 'shouldn\'t you',
//         'shouldn\'t this', 'shouldn\'t it', 'isn\'t it', 'aren\'t', 'aren\'t you',
//         'aren\'t this', 'aren\'t it', 'doesn\'t it', 'didn\'t you',
//         'didn\'t this', 'didn\'t it', 'has it', 'hasn\'t', 'hasn\'t it', 'have you', 'have it', 'haven\'t it', 'had', 'had it', 'hadn\'t', 'hadn\'t it', 'will you',
//         'will this', 'will it', 'won\'t you', 'won\'t this', 'won\'t it',
//         'would you', 'would this', 'would it', 'wouldn\'t', 'wouldn\'t you', 'wouldn\'t this',
//         'wouldn\'t it', 'could you', 'could this', 'could it', 'couldn\'t', 'couldn\'t you',
//         'couldn\'t this', 'couldn\'t it', 'can you', 'can this', 'can it', 'can\'t',
//         'can\'t you', 'can\'t this', 'can\'t it', 'may you', 'may this', 'may it',
//         'might you', 'might this', 'might it', 'must', 'must you', 'must this', 'must it',
//         'should you', 'should this', 'should it', 'shall you', 'shall this', 'shall it',
//         'ought you', 'ought this', 'ought it', 'dare you', 'dare this', 'dare it',
//         'need you', 'need this', 'need it', 'used', 'used you', 'used this', 'used it',
//         'expect you', 'expect this', 'expect it', 'what\'s', 'what\'s this', 'where\'s',
//         'where\'s this', 'when\'s', 'when\'s this', 'why\'s this', 'who\'s', 'who\'s this',
//         'which\'s', 'which\'s this', 'how\'s', 'how\'s this', '?'
//     }

//     # Extract comments and replies into dictionaries
//     comments = []
//     for comment, reply in all_comments['all_comments']:
//         comment_dict = {'Comment': comment, 'Reply': reply}
//         comments.append(comment_dict)

//     # Filter comments based on problem words
//     comments_problem = [comment for comment in comments if any(word in comment['Comment'].lower() for word in problem_words)]

//     # Filter comments based on question words
//     comments_question = [comment for comment in comments if any(word in comment['Comment'].lower() for word in question_words)]

//     # Define file paths
//     file_problem = f"src/data/Comments_problem.json"
//     file_question = f"src/data/Comments_question.json"
//     file_all_comments = f"src/data/all_comments.json"

//     # Write comments to JSON files
//     with open(file_problem, "w", encoding='utf-8') as json_file:
//         json.dump(comments_problem, json_file, ensure_ascii=False, indent=4)

//     with open(file_question, "w", encoding='utf-8') as json_file:
//         json.dump(comments_question, json_file, ensure_ascii=False, indent=4)

//     with open(file_all_comments, "w", encoding='utf-8') as json_file:
//         json.dump(comments, json_file, ensure_ascii=False, indent=4)



// def main():
//     # Load the last accessed video URL from a file, if it exists
//     last_video_url = None
//     if os.path.exists("last_video_url.txt"):
//         with open("last_video_url.txt", "r") as file:
//             last_video_url = file.read().strip()

//     current_video_url = "https://www.youtube.com/watch?v=R9mHKiZQxac"

//     # Check if the URL has changed since the last execution
//     if current_video_url != last_video_url:
//         fetch_comments_and_write_json(current_video_url)
//         print("Comments filtered and saved to JSON files.")
//     else:
//         print("URL has not changed since the last execution. Skipping script execution.")

//     # Write the current video URL to the file for future reference
//     with open("last_video_url.txt", "w") as file:
//         file.write(current_video_url)

// def fetch_comments_and_write_json(video_url):
//     api_key = API_KEY  # Replace with your own API key
//     all_comments = fetch_comments(video_url, api_key)
//     if all_comments:
//         write_json(video_url, all_comments)
//     else:
//         print("Failed to fetch comments for the video.")

// if __name__ == "__main__":
//     main()



