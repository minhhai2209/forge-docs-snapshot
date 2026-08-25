# The Forge REST API

`1curl --request POST \
2 --url 'https://api.atlassian.com/forge/storage/kvs/v1/transaction' \
3 --header 'Content-Type: application/json' \
4 --data '{
5 "set": [
6 {
7 "key": "<string>",
8 "value": "<string>",
9 "entityName": "<string>",
10 "conditions": {},
11 "options": {
12 "ttl": {
13 "value": 38,
14 "unit": "SECONDS"
15 }
16 }
17 }
18 ],
19 "delete": [
20 {
21 "key": "<string>",
22 "entityName": "<string>",
23 "conditions": {}
24 }
25 ],
26 "check": [
27 {
28 "key": "<string>",
29 "entityName": "<string>",
30 "conditions": {}
31 }
32 ]
33}'`
