# The Forge REST API

`1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26``curl --request POST \
--url 'https://api.atlassian.com/forge/storage/kvs/v1/entity/query' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
"entityName": "<string>",
"indexName": "<string>",
"partition": [
"<string>"
],
"range": {
"condition": "BEGINS_WITH",
"values": [
"<string>"
]
},
"filters": {},
"sort": "ASC",
"cursor": "<string>",
"limit": 2154,
"options": {
"metadataFields": [
"CREATED_AT"
]
}
}'`
