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
13``curl --request POST \
--url '{FORGE_EGRESS_PROXY_URL}/forge/storage/os/v1/upload-url' \
--header 'Accept: application/json' \
--header 'forge-proxy-authorization: Forge as=app,id=invocation-123' \
--header 'Content-Type: application/json' \
--data '{
"key": "<string>",
"length": 2154,
"checksum": "<string>",
"checksumType": "SHA1",
"ttlSeconds": 2154,
"overwrite": true
}'`
