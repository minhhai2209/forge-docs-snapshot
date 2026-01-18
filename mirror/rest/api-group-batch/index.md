# The Forge REST API

POST

## Batch set key-value pairs

Sets multiple Key-Value Store and/or Custom Entity Store values in a single operation.
Returns a type `BatchResponse` which contains `successfulKeys` and `failedKeys`.

Forge and OAuth2 apps cannot access this REST resource.

### Request

#### Request bodyapplication/json

array<anyOf [BatchSetTypedItemSchema, BatchSetUntypedItemSchema]>

### Responses

200OK

Successfully set the keys to their corresponding values, returns list of successful and failed keys. Failed keys will contain details of the failure error codes.

400Bad Request
