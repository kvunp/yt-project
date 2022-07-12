## Setup
### Clone the repository
`
git clone https://github.com/kvunp/yt-project.git
`

### Run mongodb and elasticsearch using docker images
`
docker-compose up
`
* Note : Make sure ports 27017, 9200 are available

### Run server
* `
Navigate to repo directory
`
* `
python3 -m venv env
` 
* `
source env/bin/activate
`
* `
make install
`
* `
make run
`
* Note : Make sure port 5000 is available

## API Details
* Base url - http://localhost:5000
* Endpoint 1 - /get_yt_reults

Get Paginated results which were already fetched and stored in db

`
curl --location --request GET 'localhost:5000/get_yt_results' \
--header 'Content-Type: application/json' \
--data-raw '{
    "skip":0,
    "limit":10
}'
`
* Endpoint 2 - /search_yt_results

Search for query in title or description using elasticsearch and fetch corresponding docs from db

`
curl --location --request GET 'localhost:5000/search_yt_results' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query":"tea"
}'
`
## How it works
* Youtube results are fetched at app startup and periodically(period in env) for a pre defined query string(query string in env) and are added to mongo(all fields) and es(only title, description, id)
* Api keys can be fetched from db on app startup or will be fetched from static json file if not db (app restart is required if new api keys is added)
* _id is a default index in mongo collection and is the only field being queried on(/search_yt_results), /get_yt_results is using pagination(skip, query), No new index is required
* Mongo Collection names - videos, api_keys
* Elasticsearch index name - video_index

##### Next Steps (Dev)
##### TODO:
* Remove yt results from json and attach yt v3 api [Done]
* search both in title and description [Done]
* Refactor api methods into corresponding helpers(db ,es)
* search results pagination

##### Known Issues:
* include server in docker (error while connecting to http://elasticsearch:9200)
* Acknowledgement of insert document in mongo, es(if any one server is non reachable, there is no way of ack or retry at the moment) - inconsistency may be created between mongo and es
* Repitition of mongo documents in elastic search (Temporary fix applied)
* Api Key Store(Pydantic) repair (compilation error) [Temporary fix applied]
