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

The payload for all of these events is the same. Request type events carry no additional properties beyond the common fields below.

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
3
4
5
6
7
8
9
```



```
{
  "eventType": "avi:jsm-entity:created:request-type",
  "entityId": "10001",
  "entityType": "request-type",
  "activationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "entityUpdateTimeStamp": "2026-08-19T10:30:00.000Z",
  "sequenceNumber": 1
}
```
```

## Request type group events

You can subscribe to the following Jira Service Management request type group events in Forge apps:

### Request type group created, updated, deleted

An event with the name `avi:jsm-entity:created:request-type-group` / `avi:jsm-entity:updated:request-type-group` / `avi:jsm-entity:deleted:request-type-group` is sent when a request type group is `created` / `updated` / `deleted` respectively.

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:requesttype:jira-service-management`

The payload for all of these events is the same.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI, one of: `avi:jsm-entity:created:request-type-group`, `avi:jsm-entity:updated:request-type-group`, `avi:jsm-entity:deleted:request-type-group`. |
| entityId | `string` | The unique identifier of the request type group entity. |
| entityType | `string` | The type of entity. Always `"request-type-group"`. |
| activationId | `string` | The activation ID of the Jira instance. |
| entityUpdateTimeStamp | `string` | The timestamp of the entity update. |
| sequenceNumber | `number` | A sequence number for ordering events. |
| requestTypeGroupEventPropertyValue | `RequestTypeGroupEventPropertyValue` | The properties of the request type group, including its ID, name, and associated project ID. |

#### Type reference

```
```
1
2
3
4
5
6
```



```
interface RequestTypeGroupEventPropertyValue {
    requestTypeGroupId: string; // Same value as the top-level entityId.
    projectId: string;
    name: string;
}
```
```

#### Example

This is an example of a payload for a newly created request type group.

```
```
1
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
```



```
{
  "eventType": "avi:jsm-entity:created:request-type-group",
  "entityId": "10001",
  "entityType": "request-type-group",
  "activationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "entityUpdateTimeStamp": "2026-08-19T10:30:00.000Z",
  "sequenceNumber": 1,
  "requestTypeGroupEventPropertyValue": {
    "requestTypeGroupId": "10001",
    "projectId": "10000",
    "name": "IT Support"
  }
}
```
```

## Service desk events

You can subscribe to the following Jira Service Management service desk events in Forge apps:

### Service desk created, updated, deleted

An event with the name `avi:jsm-entity:created:service-desk` / `avi:jsm-entity:updated:service-desk` / `avi:jsm-entity:deleted:service-desk` is sent when a service desk is `created` / `updated` / `deleted` respectively.

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:servicedesk:jira-service-management`

The payload for all of these events is the same.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI, one of: `avi:jsm-entity:created:service-desk`, `avi:jsm-entity:updated:service-desk`, `avi:jsm-entity:deleted:service-desk`. |
| entityId | `string` | The unique identifier of the service desk entity. |
| entityType | `string` | The type of entity. Always `"service-desk"`. |
| activationId | `string` | The activation ID of the Jira instance. |
| entityUpdateTimeStamp | `string` | The timestamp of the entity update. |
| sequenceNumber | `number` | A sequence number for ordering events. |
| serviceDeskEventPropertyValue | `ServiceDeskEventPropertyValue` | The properties of the service desk, including its ID, associated project ID, and project name. |

#### Type reference

```
```
1
2
3
4
5
6
```



```
interface ServiceDeskEventPropertyValue {
    serviceDeskId: string; // Same value as the top-level entityId.
    projectId: string;
    projectName: string;
}
```
```

#### Example

This is an example of a payload for a newly created service desk.

```
```
1
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
```



```
{
  "eventType": "avi:jsm-entity:created:service-desk",
  "entityId": "10012",
  "entityType": "service-desk",
  "activationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "entityUpdateTimeStamp": "2026-08-24T05:22:31.258Z",
  "sequenceNumber": 1,
  "serviceDeskEventPropertyValue": {
    "serviceDeskId": "10012",
    "projectId": "10001",
    "projectName": "IT Support"
  }
}
```
```
