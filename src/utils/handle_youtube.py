from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    parsed_url = urlparse(url)
    
    if parsed_url.netloc == 'www.youtube.com' or parsed_url.netloc == 'youtube.com':
        if parsed_url.path == '/watch':
            query_params = parse_qs(parsed_url.query)
            return query_params['v'][0] if 'v' in query_params else None
        elif parsed_url.path.startswith('/shorts/'):
            # For YouTube shorts
            return parsed_url.path.split('/')[-1]
    elif parsed_url.netloc == 'youtu.be':
        # For youtu.be short URLs
        return parsed_url.path[1:]
    
    return None


def yt_info(video_url):
    API_KEY = "AIzaSyA5xJXjhTA8FzOilw5SFibmTsnRFlMMsXs"

    # Build the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    #Get video id from URL
    video_id = get_video_id(video_url)

    # Request video details
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )

    response = request.execute()

    # Extract the video title and description
    video_title = response['items'][0]['snippet']['title']
    video_description = response['items'][0]['snippet']['description']

    dict = {"title": video_title, "content": video_description}