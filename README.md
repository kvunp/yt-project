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

`
curl --location --request GET 'localhost:5000/get_yt_results' \
--header 'Content-Type: application/json' \
--data-raw '{
    "skip":0,
    "limit":10
}'
`
* Endpoint 2 - /search_yt_results

`
curl --location --request GET 'localhost:5000/search_yt_results' \
--header 'Content-Type: application/json' \
--data-raw '{
    "query":"tea"
}'
`

##### Next Steps (Dev)
##### TODO:
* Remove yt results from json and attach yt v3 api 
* search both in title and description
* Refactor api methods into corresponding helpers(db ,es)
* search results pagination

##### Known Issues:
* include server in docker (error while connecting to http://elasticsearch:9200)
* Acknowledgement of insert document in mongo, es(if any one server is non reachable, there is no way of ack or retry at the moment) 
* Repitition of mongo documents in elastic search (Temporary fix applied)
* Api Key Store(Pydantic) repair (compilation error)