# The Forge REST API

POST

## Batch get key-value and entity entries

Gets multiple Key-Value Store and/or Custom Entity Store entries in a single operation.
Each request item may include optional `options.metadataFields` to request metadata (createdAt, updatedAt, expireTime) in the response.
Returns `successfulKeys` (each with `value` and optionally metadata) and `failedKeys` (with `error.code`, `error.message`).

##### Scopes

**[OAuth 2.0 scopes](/platform/forge/scopes-for-oauth-2-3LO-and-forge-apps/) required:**

`storage:app`

### Request

#### Request bodyapplication/json

array<anyOf [BatchGetTypedItemSchema, BatchGetUntypedItemSchema]>

### Responses

200OK

Successfully retrieved the requested keys; returns list of successful keys (with value and optionally metadata) and failed keys (with error details).

400Bad Request
