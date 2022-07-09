

def fun():
    request = youtube.search().list(
        part = 'snippet',
        q = 'How to make tea?',
        type = 'video',
        maxResults = 50
    )
    response = request.execute()