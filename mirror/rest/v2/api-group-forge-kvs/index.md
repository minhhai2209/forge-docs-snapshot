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
27
28
29
30
31
32
33
34``curl --request POST \
--url '{FORGE_EGRESS_PROXY_URL}/forge/storage/kvs/v1/transaction' \
--header 'forge-proxy-authorization: Forge as=app,id=invocation-123' \
--header 'Content-Type: application/json' \
--data '{
"set": [
{
"key": "<string>",
"value": "<string>",
"entityName": "<string>",
"conditions": {},
"options": {
"ttl": {
"value": 38,
"unit": "SECONDS"
}
}
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
