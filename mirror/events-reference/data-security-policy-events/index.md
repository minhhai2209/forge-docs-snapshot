# Data security policy events

Data security policy events are generated when an app's access to certain data within Confluence, Jira Cloud, Jira Service Management, or Jira Software
has been blocked by an administrative policy. Currently, the only data security policy blocking access to data is the [App access rule](https://support.atlassian.com/security-and-access-policies/docs/block-app-access/).

App access events are triggered by policy changes, including policy creation, deletion, or modification, or when content is moved
to a location subject to policy controls. They are NOT triggered by changes in app installs or uninstalls.
Therefore, if an app is installed after policies have been created, no notifications are sent out that app access (by that app) is blocked.

If your app needs to determine which items are blocked or not blocked as of when the app is first run, you can use Atlassian app-specific APIs
to obtain that information. See the Confluence [Data security policy developer guide](/cloud/confluence/data-security-policy-developer-guide/)
and [Jira data security policy developer guide](/cloud/jira/platform/data-security-policy-developer-guide/) for more information. Items already blocked to an app on install will not
appear in subsequent search or any other data retrieval results, nor will the app be able to update them.

This event documentation uses the terms container and objects in the following way:

* **container**: A container is a Confluence space or Jira project.
* **object**: An object is metadata or user-generated content, such as a page, blogpost, whiteboard, database, or issue. Every object is associated with a container.

Forge apps can define a [trigger](/platform/forge/manifest-reference/modules/trigger) module to subscribe to data security policy events affecting:

* containers in the Atlassian app instance in which the Forge app is running
* objects in particular containers in the Atlassian app instance in which the Forge app is running

For more information about data security policies and which objects are subject to app access rules, see the following documentation:

An [AsyncAPI spec](#AsyncAPI_spec) for these events is available below.

AsyncAPI defines a document format used to describe an application's event-driven API contract. More information can be found at the [AsyncAPI project site](http://asyncapi.com).

## App Access to Objects Blocked

**Event**: `avi:ecosystem.app_policy:blocked:app_access_to_objects.v2`  
**Description**: The app's access to one or more objects such as Confluence pages, blogposts, whiteboards, databases, or Jira issues, has been blocked. The payload contains a list of blocked object identifiers.

Access can be blocked when the app has been added to a policy with an app access rule that blocks specific apps, when the app has been removed from a policy with an app access rule that allows specific apps,
or the list of spaces and projects covered by a policy associated with that app has changed, or some other cause.

When a space or project is added to an app access rule, access to many objects is potentially affected. Therefore, this event may generate large numbers of events,
each containing a large number of object identifiers. When the limit for the number of objects in the
object list is exceeded, that event is sent and notifications about additional objects are sent in subsequent events.

This event does not require any additional Forge scopes.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| (root) | object |  |
| specversion | string | The version of the CloudEvents specification which the event uses. **Valid values:** `"1.0"` |
| id | string | Uniquely identifies the event. |
| source | string | Identifies the context within which an event occurred. |
| type | string | Describes the type of event related to the originating occurrence. The event type is suffixed by the event type version. **Examples:** `avi:ecosystem.app_policy:blocked:app_access_to_objects.v2` |
| time | string | Timestamp of when the occurrence happened. Must adhere to RFC 3339. |
| data | object |  |
| data.workspace | object | The event payload. |
| data.workspace.cloudId | string |  |
| data.objects | array<object> | The objects that have been blocked. |
| data.objects.product | string | Identifier of the Atlassian app. Currently one of: `Confluence`, `Jira`. |
| data.objects.type | string | Object type. For `Jira`, the only supported object type is `issue`. For `Confluence`, the supported object types are: `page`, `blogpost`, `whiteboard`, and `database`. |
| data.objects.ids | array |  |
| data.objects.ids (single item) | string | Object identifier. |

### Examples of payload

```
```
1
2
```



```
{
  "specversion": "1.0",
  "type": "avi:ecosystem.app_policy:blocked:app_access_to_objects.v2",
  "source": "atlassian.com/ecosystem",
  "id": "7a6796c0-746d-4504-92cd-819eca234306",
  "time": "2023-10-24T08:08:08Z",
  "data": {
    "workspace": {
      "cloudId": "abc123"
    },
    "objects": [
      {
        "product": "confluence",
        "type": "page",
        "ids": [
          "123456",
          "234567",
          "345678"
        ]
      },
      {
        "product": "confluence",
        "type": "whiteboard",
        "ids": [
          "45678",
          "56789",
          "67890"
        ]
      }
    ]
  }
}
```
```

## App Access to Objects in Container Blocked

**Event**: `avi:ecosystem.app_policy:blocked:app_access_to_objects_in_container.v2`  
**Description**: The app's access to all objects in a specific container such as a Confluence space or Jira project has been blocked. The payload contains a list of blocked container identifiers.

An example use case for this condition is an app that uses an [admin page](/cloud/confluence/modules/admin-page/),
[global page](/platform/forge/manifest-reference/modules/confluence-global-page),
[global settings](/platform/forge/manifest-reference/modules/confluence-global-settings/),
or [homepage feed](/platform/forge/manifest-reference/modules/confluence-homepage-feed/) module.

The app is not blocked from accessing data about the container itself, only for all objects *within* the container, that are restricted by the policy - a subtle but important semantic difference.

This event is intended for use when a Forge app works across multiple containers (that is, projects or spaces) within the Atlassian app.
In these circumstances it may be useful to know when specific containers are blocked, for customer support purposes,
or for modifying background processes such as container synchronisation, or for other purposes at the granularity of a container.

This event type *must not* be used to determine which objects have been blocked (for example, in response to a container having been blocked) - this will result in missing data.
Instead, you should use the `App Access to Objects Blocked` event type for this purpose.

This event does not require any additional Forge scopes.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| (root) | object |  |
| specversion | string | The version of the CloudEvents specification which the event uses. **Valid values:** `"1.0"` |
| id | string | Uniquely identifies the event. |
| source | string | Identifies the context within which an event occurred. |
| type | string | Describes the type of event related to the originating occurrence. The event type is suffixed by the event type version. **Examples:** `avi:ecosystem.app_policy:blocked:app_access_to_objects_in_container.v2` |
| time | string | Timestamp of when the occurrence happened. Must adhere to RFC 3339. |
| data | object |  |
| data.workspace | object |  |
| data.workspace.cloudId | string |  |
| data.container | object | Container that the app has been blocked from accessing. |
| data.container.product | string | Identifier of the Atlassian app. Currently one of: `Confluence`, `Jira`. |
| data.container.id | string | Identifier of the container |

### Examples of payload

```
```
1
2
```



```
{
  "specversion": "1.0",
  "type": "avi:ecosystem.app_policy:blocked:app_access_to_objects_in_container.v2",
  "source": "atlassian.com/ecosystem",
  "id": "7a6796c0-746d-4504-92cd-819eca234306",
  "time": "2023-10-24T08:08:08Z",
  "data": {
    "workspace": {
      "cloudId": "abc123"
    },
    "container": {
      "product": "confluence",
      "id": "123456"
    }
  }
}
```
```

## AsyncAPI spec

The app policy service schema appears below. You can use a tool such as [AsyncAPI Studio](https://studio.asyncapi.com/) to preview the documentation and event architecture.

```
```
1
2
```



```
asyncapi: '2.6.0'
tags:
  - name: ecosystem
id: 'urn:com.atlassian.ecosystem.app_policy.webhooks'
info:
  title: App Policy Service
  version: 0.1.0
  description: Atlassian service which publishes App Policy events to App webhooks.

channels:
  atlassian/webhooks:
    subscribe:
      bindings:
        http:
          type: request
          method: POST
          headers:
            content-type:
              type: string
              enum:
                - 'application/cloudevents+json; charset=UTF-8'
      summary: Receive notifications of changes to App Access Rules that affect App access to data.
      message:
        oneOf:
          - $ref: '#/components/messages/appAccessToObjectsBlocked'
          - $ref: '#/components/messages/appAccessToObjectsInContainerBlocked'

components:
  messages:
    appAccessToObjectsInContainerBlocked:
      title: Event - App Access to Objects in Container Blocked
      description: |-
       Published when an App's access to a set of objects (such as Confluence pages, blogposts, whiteboards, databases, or Jira issues) within a specific container has been blocked.
       This event is not named `AppAccessToContainerBlocked` because that would be misleading; the app is not blocked from accessing data for the container itself, only for objects _within_ the container - a subtle but important semantic difference.

       The semantics of this event are intended for use when an app works at the workspace level - ie across multiple containers.  In these circumstances it may be useful to know when specific containers are blocked, for customer support purposes, or for modifying background processes such as container synchronisation, or for other purposes at the granularity of a container.

       This event type _must not_ be used to determine which objects have been blocked (for eg in response to a container having been blocked) - this will result in missing data.  Instead the `AppAccessToObjectsBlocked` event type may be used for this purpose.
      payload:
        type: object
        required:
          - specversion
          - id
          - source
          - type
          - time
          - data
        properties:
          specversion:
            type: string
            description: The version of the CloudEvents specification which the event uses.
            enum:
              - "1.0"
          id:
            type: string
            minLength: 1
            description: Uniquely identifies the event.
          source:
            type: string
            format: uri-reference
            minLength: 1
            description: Identifies the context within which an event occurred.
          type:
            type: string
            minLength: 1
            description: Describes the type of event related to the originating occurrence. The event type is suffixed by the event type version.
            examples:   
              - "avi:ecosystem.app_policy:blocked:app_access_to_objects_in_container.v2"
          time:
            type: string
            format: date-time
            description: Timestamp of when the occurrence happened. Must adhere to RFC 3339.
          data:
            type: object
            properties:
              workspace:
                type: object
                properties:
                  cloudId:
                    type: string
                required:
                  - cloudId
              container:
                type: object
                description: Container that the app has been blocked from accessing.
                properties:
                  product: 
                    type: string
                    description: Identifier of the Atlassian app
                  id: 
                    type: string
                    description: Identifier of the container
                required:
                  - product
                  - id
            required:
              - workspace
              - container
      examples:
        - name: AppAccessToObjectsInContainerBlocked
          headers:
            content-type: application/cloudevents+json; charset=utf-8
          payload:
            specversion: "1.0"
            type: "avi:ecosystem.app_policy:blocked:app_access_to_objects_in_container.v2"
            source: "atlassian.com/ecosystem"
            id: "7a6796c0-746d-4504-92cd-819eca234306"
            time: "2023-10-24T08:08:08Z"
            data:
              workspace: 
                cloudId: "abc123"
              container:
                product: "confluence" 
                id: "123456"
    appAccessToObjectsBlocked:
      title: Event - App Access to Objects Blocked
      description: |-
       Published when an App's access to a set of objects such as Confluence pages, blogposts, whiteboards, databases, or Jira issues, has been blocked.

       It could be that the App has been added or removed from a Policy, or the Containers covered by a Policy associated with that App have changed, or some other cause.
      payload:
        type: object
        required:
          - specversion
          - id
          - source
          - type
          - time
          - data
        properties:
          specversion:
            type: string
            description: The version of the CloudEvents specification which the event uses.
            enum:
              - "1.0"
          id:
            type: string
            minLength: 1
            description: Uniquely identifies the event.
          source:
            type: string
            format: uri-reference
            minLength: 1
            description: Identifies the context within which an event occurred.
          type:
            type: string   
            minLength: 1
            description: Describes the type of event related to the originating occurrence. The event type is suffixed by the event type version.
            examples:
              - "avi:ecosystem.app_policy:blocked:app_access_to_objects.v2"
          time:
            type: string
            format: date-time
            description: Timestamp of when the occurrence happened. Must adhere to RFC 3339.
          data:
            type: object
            properties:
              workspace:
                type: object
                properties:
                  cloudId:
                    type: string
                required:
                  - cloudId
              objects:
                type: array
                items:
                  type: object
                  description: Objects the app has been blocked from accessing.
                  properties: 
                    product: 
                      type: string
                      description: Identifier of the Atlassian app
                    type:
                      type: string
                      description: Object type
                    ids:
                      type: array
                      items:
                        type: string
                        description: Object identifier
                  required:
                    - product
                    - type
                    - ids
            required:
              - workspace
              - objects
      examples:
        - name: AppAccessToObjectsBlocked
          headers:
            content-type: application/cloudevents+json; charset=utf-8
          payload:
            specversion: "1.0"
            type: "avi:ecosystem.app_policy:blocked:app_access_to_objects.v2"
            source: "atlassian.com/ecosystem"
            id: "7a6796c0-746d-4504-92cd-819eca234306"
            time: "2023-10-24T08:08:08Z"
            data:
              workspace: 
                cloudId: "abc123"
              objects:
                - product: "confluence"
                  type: "page"
                  ids:
                    - "123456"
                    - "234567"
                    - "345678"
                - product: "confluence"
                  type: "whiteboard"
                  ids:
                    - "45678"
                    - "56789"
                    - "67890"
                - product: "jira"
                  type: "issue"
                  ids:
                    - "123456"
                    - "234567"
                    - "345678"
```
```
