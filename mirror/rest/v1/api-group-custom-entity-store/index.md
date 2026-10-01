# The Forge REST API

`1curl --request POST \
2 --url 'https://api.atlassian.com/forge/storage/kvs/v1/entity/query' \
3 --header 'Accept: application/json' \
4 --header 'Content-Type: application/json' \
5 --data '{
6 "entityName": "<string>",
7 "indexName": "<string>",
8 "partition": [
9 "<string>"
10 ],
11 "range": {
12 "condition": "BEGINS_WITH",
13 "values": [
14 "<string>"
15 ]
16 },
17 "filters": {},
18 "sort": "ASC",
19 "cursor": "<string>",
20 "limit": 2154,
21 "options": {
22 "metadataFields": [
23 "CREATED_AT"
24 ]
25 }
26}'`
