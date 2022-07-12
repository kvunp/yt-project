TEST_VARIABLES := MONGO_CONNECTION_STRING="mongodb://localhost:27017/yt_service" \
SEARCH_RESULTS_REFRESH_INTERVAL_IN_SECONDS="600" \
YT_QUERY_STRING="how to make tea" \
ES_CONNECTION_STRING="http://localhost:9200" \
ES_INDEX_VIDEOS="video_index"

env:
	python3 -m venv env

install:
	pip3 install -r ./requirements.txt

format_code:
	black --check ./src/

run:
	$(TEST_VARIABLES) uvicorn --host 0.0.0.0 --port 5000 src.server:app --reload

