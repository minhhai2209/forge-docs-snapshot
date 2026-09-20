# The Forge REST API

`1curl --request POST \
2 --url '{FORGE_EGRESS_PROXY_URL}/forge/storage/kvs/v1/transaction' \
3 --header 'forge-proxy-authorization: Forge as=app,id=invocation-123' \
4 --header 'Content-Type: application/json' \
5 --data '{
6 "set": [
7 {
8 "key": "<string>",
9 "value": "<string>",
10 "entityName": "<string>",
11 "conditions": {},
12 "options": {
13 "ttl": {
14 "value": 38,
15 "unit": "SECONDS"
16 }
17 }
18 }
19 ],
20 "delete": [
21 {
22 "key": "<string>",
23 "entityName": "<string>",
24 "conditions": {}
25 }
26 ],
27 "check": [
28 {
29 "key": "<string>",
30 "entityName": "<string>",
31 "conditions": {}
32 }
33 ]
34}'`
