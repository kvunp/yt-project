from src.common.mongo_db import video_collection

def insert_many_into_video_collection(video_items):
    docs_to_be_inserted = []
    for item in video_items:
        curr = item.get("snippet")
        videoId = item.get("id", {}).get("videoId", None)
        if videoId:
            curr["_id"] = videoId
            docs_to_be_inserted.append(curr)
    
    video_collection.insert_many(docs_to_be_inserted, ordered=False)
