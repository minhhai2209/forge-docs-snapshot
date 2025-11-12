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
26
27``curl --request POST \
--url 'https://api.atlassian.com/forge/storage/kvs/v1/transaction' \
--header 'Content-Type: application/json' \
--data '{
"set": [
{
"key": "<string>",
"value": "<string>",
"entityName": "<string>",
"conditions": {}
}
],
"delete": [
{
"key": "<string>",
"entityName": "<string>",
"conditions": {}
}
],
"check": [
{
"key": "<string>",
"entityName": "<string>",
"conditions": {}
}
]
}'`
