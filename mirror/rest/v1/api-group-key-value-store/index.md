# The Forge REST API

POST

## Set secret value by key

Stores sensitive credentials in JSON format, with encryption.
Values set with this method can only be accessed with [Get secret value by key](/platform/forge/rest/api-group-key-value-store/#api-v1-secret-get-post).
Write conflicts are resolved using a last-write-wins strategy by default, but this can be configured via the key policy option.
Optionally, you can specify a TTL (Time To Live) to automatically expire the data after a specified duration.

Forge and OAuth2 apps cannot access this REST resource.

### Request

#### Request bodyapplication/json

**value**

oneOf [string, boolean, number, array<undefined>, object]

Required

**options**

ExtendedSetOptions

### Responses

200OK

Successfully set the value with metadata fields returned

204No Content400Bad Request409Conflict
