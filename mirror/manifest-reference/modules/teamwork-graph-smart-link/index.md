# Teamwork Graph Smart Link

The `graph:smartLinks` module generates interactive, rich previews that display contextual information and
actions for linked content from supported platforms. Smart Links enhance the user experience by providing
instant access to key details and functionality without leaving the current page.

Smart Links retrieve information from third-party apps in real time as the link is rendered, ensuring
the displayed data is always up to date.

Smart Link requests are executed in the context of the user. Both Atlassian and the app developer share responsibility for respecting user permissions, ensuring that users can only access data they are authorized to view.

By using the [`asUser()`](/platform/forge/runtime-reference/external-fetch-api/) the user Authentication token will automatically be injected in the communication to the remote system. The App should check that the user has a valid token, and if not, trigger the process to authenticate the user.

![](https://dac-static.atlassian.com/platform/forge/snippets/images/graph/screenshot.png?_v=1.5800.1846)

## Manifest structure

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
modules {}
└─ graph:smartLink []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ icon (string) [Mandatory]
   ├─ function (string) [Mandatory]
   ├─ domains [string] [Mandatory]
   ├─ subdomains (boolean) [Optional]
   └─ patterns [string] [Mandatory]
function []
├─ key (string) [Mandatory]
└─ handler (string) [Mandatory]
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the Smart Link module. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | A human-friendly name for the action which will be displayed in the user interface. |
| `icon` | `string` | Yes | An icon displayed within the Smart Card to represent remote system the link is related to. |
| `function` | `string` | Yes | A reference to the hosted Forge function that will parse the URL matching the domains and patterns specified by the module. The function will parse the URL and retrieve the data related to the link and then return the given object information. |
| `domains` | `Array(string)` | Yes | A list of domains that will be used to determine whether the app can resolve a given URL to a Smart Link. |
| `subdomains` | `boolean` | No | Whether sub-domains for the listed domains should be allowed. |
| `patterns` | `Array(string)` | Yes | A list of regular expressions that will be used to determine whether thea app can resolve a given URL to a Smart Link. |

## Manifest example

```
```
1
2
```



```
modules:
  graph:smartLink:
    - key: sl-test-example-hello-world
      icon: https://static.example-hello-world.com/favicon.ico
      name: sl-test
      function: getEntityByUrlFn
      domains:
        - example-hello-world.com
        - www.example-hello-world.com
      subdomains: true
      patterns:
        - https:\/\/([\w\.-]+\.)?example-hello-world\.com\/([0-9a-zA-Z]{4,128})(?:\/.*)?$
  function:
    - key: getEntityByUrlFn
      handler: index.getHelloWorldEntityByUrl
```
```

## Supported object types

All Teamwork Graph object types are supported by the Smart Link module.

## API Contract

### Request

Atlassian will invoke the function specified within the `graph:smartLink` module when it matches one or more domains as well as at least one pattern.
If there are multiple links on a given page for the same App that match, these will all be provided in one single request.

```
```
1
2
```



```
request {}
├─ type (string) [Mandatory]
└─ urls (Array of string) [Mandatory]
```
```

#### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `string` | Yes | Value: `resolve` |
| `urls` | `Array(string)` | Yes | A list of URLs that matched the domains and patterns of the Smart Link module. |

#### Example:

Below is a request to resolve two links.

```
```
1
2
```



```
{
  "type": "resolve";
  "payload": {
    "urls": ["https://www.example-link.com/example1","https://www.example-link.com/example2"];
}
```
```

### Response

```
```
1
2
```



```
response {}
└─ entities [] (Array of EntityResult) [Mandatory]
    ├─ identifier {} (Identifier) [Mandatory]
    │   └─ url (String) [Mandatory]
    ├─ meta {} (Meta) [Mandatory]
    │   ├─ access (String) [Mandatory]
    │   └─ visibility (String) [Mandatory]
    └─ entity [] (Array of Object) [Optional]
```
```

#### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `entities` | `Array(EntityResult)` | Yes | Array of results, one for each URL received in the request. |
| `entities[i].identifier` | `Identifier` | Yes | Object containing identifying information for the entity, including the original URL. |
| `entities[i].identifier.url` | `String` | Yes | The URL that this entity result represents. |
| `entities[i].meta` | `Meta` | Yes | Object containing metadata about the entity, such as access and visibility. |
| `entities[i].meta.access` | `String` | Yes | Access level for the entity.  Supported values: `granted`, `forbidden`, `unauthorized`, `not_found`. |
| `entities[i].meta.visibility` | `String` | Yes | Visibility of the entity.  Supported values: `public`, `restricted`, `other`, `not_found`. |
| `entities[i].entity` | `Object` | No | If the URL could be resolved successfully, return the entity using the Object format that closest matches the object. |

#### Example:

```
```
1
2
```



```
{
  "entities": [
    {
      "identifier": {
        "url": "https://www.example-link.com/example1"
      },
      "meta": {
        "access": "granted",
        "visibility": "restricted"
      },
      "entity": {
        "id" : "my-document",
        "updateSequenceNumber" : 123,
        "displayName" : "My Document",
        "url" : "https://document.com",
        "thumbnail" : {
          "externalUrl" : "https://document-thumbnail.com"
        },
        "createdAt" : "2024-04-16T09:01:32+00:00",
        "atlassian:document" : {
          "type" : {
            "category" : "document",
            "iconUrl" : "http://icon.com"
          },
          "content" : {
            "mimeType" : "text/plain",
            "text" : "Really large content here..."
          },
          "byteSize" : 456,
          "labels" : [ "label1", "label2" ],
          "reactions" : [ {
            "type" : "LIKE",
            "total" : 1
          } ],
          "exportLinks" : [ {
            "mimeType" : "text/plain",
            "url" : "http://localhost"
          } ]
        }
      }
    },
    {
      "identifier": {
        "url": "https://www.example-link.com/example2"
      },
      "meta": {
        "access": "forbidden",
        "visibility": "restricted"
      }
    }
  ]
}
```
```

## Tutorial
