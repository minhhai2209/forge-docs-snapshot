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
19``curl --request POST \
--url 'https://api.atlassian.com/forge/storage/kvs/v1/set' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
"key": "<string>",
"value": "<string>",
"options": {
"ttl": {
"value": 38,
"unit": "SECONDS"
},
"keyPolicy": "FAIL_IF_EXISTS",
"returnValue": "PREVIOUS",
"returnMetadataFields": {
"0": "CREATED_AT"
}
}
}'`
