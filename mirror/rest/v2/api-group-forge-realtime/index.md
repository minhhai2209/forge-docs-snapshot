# The Forge REST API

POST

## Publish an event to a realtime channel

Proxies POST requests to Forge realtime services for publishing events.
All clients in the same context as the sender and subscribed to this realtime channel will receive the event.
"Publish" requests only work when the request originated from a UI context invocation. In the `forge-proxy-authorization` header you must specify the `id` of the invocation; you can't perform operations on behalf of an `installationId`.

Forge and OAuth2 apps cannot access this REST resource.

### Request

Expand all

**forge-proxy-authorization**

string

Required

#### Request bodyapplication/json

Expand all

Event data to be published

### Responses

200OK

Realtime message published successfully

400Bad Request500Internal Server Error
