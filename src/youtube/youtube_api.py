from src.common.youtube import youtube
from src.common import settings

config = settings.Settings()

def get_latest_youtube_results(api_key):
    youtube_build = youtube(api_key)
    request = youtube_build.search().list(
        part = 'snippet',
        q = config.YT_QUERY_STRING,
        type = 'video',
        publishedAfter = '2022-01-01T00:00:00Z',
        maxResults = 50
    )
    return request.execute()