# Jira Service Management events

Forge apps can subscribe to Jira Service Management events for:

Your Forge app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

## Request type events

You can subscribe to the following Jira Service Management request type events in Forge apps:

### Request type created, updated, deleted

An event with the name `avi:jsm-entity:created:request-type` / `avi:jsm-entity:updated:request-type` / `avi:jsm-entity:deleted:request-type` is sent when a request type is `created` / `updated` / `deleted` respectively.

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:requesttype:jira-service-management`

The payload for all of these events is the same.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI, one of: `avi:jsm-entity:created:request-type`, `avi:jsm-entity:updated:request-type`, `avi:jsm-entity:deleted:request-type`. |
| entityId | `string` | The unique identifier of the request type entity. |
| entityType | `string` | The type of entity. Always `"request-type"`. |
| activationId | `string` | The activation ID of the Jira instance. |
| entityUpdateTimeStamp | `string` | The timestamp of the entity update. |
| sequenceNumber | `number` | A sequence number for ordering events. |

#### Example

This is an example of a payload for a newly created request type.

```
```
1
2
```



```
{
  "eventType": "avi:jsm-entity:created:request-type",
  "entityId": "10001",
  "entityType": "request-type",
  "activationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "entityUpdateTimeStamp": "2025-07-31T10:30:00.000Z",
  "sequenceNumber": 1
}
```
```
