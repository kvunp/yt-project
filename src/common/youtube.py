from googleapiclient.discovery import build


def youtube(api_key):
    return build("youtube", "v3", developerKey=api_key)