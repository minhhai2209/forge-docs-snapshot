# The Forge REST API

POST

## Batch get key-value and entity entries

Gets multiple Key-Value Store and/or Custom Entity Store entries in a single operation.
Each request item may include optional `options.metadataFields` to request metadata (createdAt, updatedAt, expireTime) in the response.
Returns `successfulKeys` (each with `value` and optionally metadata) and `failedKeys` (with `error.code`, `error.message`).

Forge and OAuth2 apps cannot access this REST resource.

### Request

#### Request bodyapplication/json

array<anyOf [BatchGetTypedItemSchema, BatchGetUntypedItemSchema]>

### Responses

200OK

Successfully retrieved the requested keys; returns list of successful keys (with value and optionally metadata) and failed keys (with error details).

400Bad Request

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
15``curl --request POST \
--url 'https://api.atlassian.com/forge/storage/kvs/v1/batch/get' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '[
{
"key": "<string>",
"entityName": "<string>",
"options": {
"metadataFields": [
"CREATED_AT"
]
}
}
]'`

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
22``{
"successfulKeys": [
{
"key": "<string>",
"entityName": "<string>",
"value": "<string>",
"createdAt": 116,
"updatedAt": 121,
"expireTime": "<string>"
}
],
"failedKeys": [
{
"key": "<string>",
"entityName": "<string>",
"error": {
"code": "<string>",
"message": "<string>"
}
}
]
}`
