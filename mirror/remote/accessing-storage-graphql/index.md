# Accessing Forge storage from a remote via GraphQL

We’ve implemented a REST API gateway for accessing Forge’s Key-Value Store (KVS) and Custom Entity Store. This gateway provides an interface that is simpler and more performant than the GraphQL API.

We will continue supporting the GraphQL API gateway. However, all future KVS and Custom Entity Store updates will be only be available through the REST API. If you are planning to integrate Forge hosted storage into a remote service, we recommend that you use the REST API gateway instead.

See [Accessing Forge storage from a remote via REST API](/platform/forge/remote/accessing-storage/) for details.

Once your remote backend has received a request from Forge, you can access storage GraphQL APIs.

## Prerequisites

To communicate with Forge’s back end via GraphQL or REST API from a remote endpoint you've invoked using Forge Remote,
you'll need to configure your app to call a remote backend (from a Custom UI or UI Kit 2 frontend) in a specific way.
To do this, you’ll need need to configure the following properties in your `manifest.yml` file:

| Property | Setting | Description |
| --- | --- | --- |
| `endpoint.auth.appSystemToken` | Set to `true` | This setting ensures that requests to your remote contain an `x-forge-oauth-system header`. This header contains a token (valid for at least 55 minutes) that you can use to call this REST API. See [Endpoint](/platform/forge/manifest-reference/endpoint/) for reference. |
| permissions.scopes | Must contain:  * storage:app * read:app-system-token | Forge requires these scopes to allow access to this REST API from remotes. See [Forge scopes](/platform/forge/manifest-reference/scopes-forge/) for reference. |

## Calling the Forge Storage GraphQL APIs

Access to Forge storage is provided to remote backends through GraphQL. You can get, set, update, and delete information in your app's Forge storage with GraphQL queries.

### Authentication

Atlassian GraphQL APIs only accept OAuth bearer tokens as authentication. Your app must supply this token in the `Authorization: Bearer {bearerToken}` header of the request.

### Requests

All Forge Storage GraphQL requests should be HTTP `POST` requests to the endpoint: `https://api.atlassian.com/graphql`.

The request body should be JSON encoded and of the format:

```
```
1
2
```



```
{
  "query": "...",
  "operationName": "...",
  "variables": { "myVariable": "someValue", ... }
}
```
```

Where:

* `query` is the GraphQL query, in string format.
* `operationName` is an optional field and is used to define the operation that is executed if the query contains multiple operations. See the [GraphQL documentation](https://graphql.org/learn/queries/#variables) for more information.
* variables is an optional JSON field, which allows the defining of variables that can be used in the query. See the [GraphQL documentation](https://graphql.org/learn/queries/#variables) for more information.

### Responses

The response will be in JSON format and of the shape:

```
```
1
2
```



```
{
  "data": { ... },
  "errors": [ ... ]
}
```
```

Where:

* `data` contains the field requested in the GraphQL query.
* `errors` is a list of errors that occurred. The field is only included if there was an error when executing the request.

### Error handling for Forge Storage requests

For GraphQL requests, the HTTP status code may be 200 even if there was an error. Please make sure that your implementation takes into consideration the errors field in the response body, in addition to HTTP errors. Here are some links on error handling with GraphQL for more information:

#### Example response for a query that attempts to get an invalid key

```
```
1
2
```



```
query badGet {
  appStoredEntity(
    key: "",
    encrypted: false
  ) {
    value
  }
}
```
```

The app receives the response:

```
```
1
2
```



```
{
    "errors": [
        {
            "path": [
                "appStoredEntity"
            ],
            "locations": [
                {
                    "line": 2,
                    "column": 3
                }
            ],
            "message": "Key was 0 characters, but should be at least 1 characters",
            "extensions": {
                "statusCode": 400,
                "errorType": "KEY_TOO_SHORT"
            }
        }
    ],
    "data": {
        "appStoredEntity": null
    }
}
```
```

### HTTP errors for GraphQL operations

Your app may also encounter HTTP errors in the event of some severe issues. For instance:

* HTTP 401 is returned if the OAuth token provided as authorization for the request was invalid or missing.
* HTTP 400 is returned if the query was malformed (e.g - requesting for a field that doesn't exist or using invalid GraphQL syntax).
* HTTP 500 is returned if the GraphQL Gateway is down.

## GraphQL query examples

The examples on this page are provided in the following format.

**GraphQL query**

```
```
1
2
```



```
query nameOfQuery($variable: VariableType) {
  fieldRequiringArgs(variable: $variable) {
    fieldA
    fieldB
  }
}
```
```

**GraphQL variables, to be used in the query**

```
```
1
2
```



```
{
  "variable" : {
    "nestedVariable": "value"
  }
}
```
```

This is the equivalent of:

```
```
1
2
```



```
query nameOfQuery {
  fieldRequiringArgs(variable: {
    nestedVariable: "value"
  }) {
    fieldA
    fieldB
  }
}
```
```

With GraphQL queries, you will get back the fields you asked for in your query. The response to the query provided may look something like this:

```
```
1
2
```



```
{
  "data": {
    "fieldRequiringArgs": {
      "fieldA": "valueA",
      "fieldB": "valueB"
    }
  }
}
```
```

## Set storage key

Sets the `value` for a given `key`.

If the key already exists, its value is updated. If the key does not exist, the key-value pair is added.

You cannot set a key's `value` property to `null`. If your app attempts this, GraphQL returns a validation error.

### GraphQL query

```
```
1
2
```



```
mutation forge_app_setExample($input: SetAppStoredEntityMutationInput!) {
  appStorage {
    setAppStoredEntity(input: $input) {
      success
      errors {
        message
        extensions {
          errorType
          statusCode
        }
      }
    }
  }
}
```
```

| Property | Description |
| --- | --- |
| `success` | A boolean indicating whether the query succeeded. If `false`, see `errors` for more information. |
| `errors.message` | A descriptive error message to assist in troubleshooting. |
| `errors.extensions.errorType` | The type of error that occurred. For example, `"INVALID_KEY"`. |
| `errors.extensions.statusCode` | The status code returned by the error. For example, `400`. |

**GraphQL variables**

The `encrypted` field is how you would store secrets in Forge storage. Setting it to `true` is the equivalent of the `kvs.setSecret` from the
[Key-Value Store](/platform/forge/runtime-reference/storage-api-secret/).

```
```
1
2
```



```
{
  "input": {
    "contextAri": "contextAri associated with the request",
    "key": "example key",
    "value": "example value",
    "encrypted": true | false
  }
}
```
```

| Variable | Description |
| --- | --- |
| `contextAri` | The unique identifier for the context in which the GraphQL query is invoked. |
| `key` | The key to set. |
| `value` | The value to set for the key. |
| `encrypted` | A boolean indicating whether this storage entry should be encrypted. |

### GraphQL response

**GraphQL response (Successfully sets a value)**

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "setAppStoredEntity": {
        "success": true,
        "errors": null
      }
    }
  }
}
```
```

**GraphQL response (Fails to set a value due to an invalid key provided in the request)**

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "setAppStoredEntity": {
        "success": false,
        "errors": [
          {
            "message": "Key \"test-key@\" should match the pattern \"/^(?!\\s+$)[a-zA-Z0-9:._\\s-#]+$/\"",
            "extensions": {
              "errorType": "INVALID_KEY"
            }
          }
        ]
      }
    }
  }
}
```
```

### Example

Set the key "example-key" with the non-encrypted string value of "hello world".

#### Query

**GraphQL variables**

```
```
1
2
```



```
{
  "input": {
    "key": "example-key",
    "value": "hello world",
    "encrypted": false
  }
}
```
```

#### Response

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "setAppStoredEntity": {
        "success": true,
        "errors": null
      }
    }
  }
}
```
```

## Get storage key

Gets a `value` by `key`.

If the requested `key` is not found, the `value` is returned as `null`.

### GraphQL query

```
```
1
2
```



```
query forge_app_getExample($key: ID!, $encrypted: Boolean!) {
  appStoredEntity(
    key: $key,
    encrypted: $encrypted
  ) {
    value
  }
}
```
```

**GraphQL variables**

```
```
1
2
```



```
{
  "key": "example-key",
  "encrypted": true | false
}
```
```

| Variable | Description |
| --- | --- |
| `key` | The key for which to retrieve a value from Forge Storage. |
| `encrypted` | A boolean indicating whether this Forge Storage entry is encrypted. |

### GraphQL response

**GraphQL response (Successfully retrieved the key's value)**

```
```
1
2
```



```
{
  "data": {
    "appStoredEntity": {
      "value": "example-value"
    }
  }
}
```
```

**GraphQL response (Key not found)**

```
```
1
2
```



```
{
  "data": {
    "appStoredEntity": {
      "value": null
    }
  }
}
```
```

### Example

Get the value of the key "example-key".

#### Query

**GraphQL variables**

```
```
1
2
```



```
{
  "key": "example-key",
  "encrypted": false
}
```
```

#### Response

```
```
1
2
```



```
{
  "data": {
    "appStoredEntity": {
      "value": "example-value"
    }
  }
}
```
```

## Query storage keys

Builds a query that returns a list of entities (key and value).

### GraphQL query

```
```
1
2
```



```
query forge_app_queryExample($where: [AppStoredEntityFilter!]!, $first: Int!, $after: String) {
  appStoredEntities(where: $where, first: $first, after: $after) {
    edges {
      node {
        value
        key
      }
      cursor
    }
    pageInfo {
      hasNextPage
    }
  }
}
```
```

| Property | Description |
| --- | --- |
| `edges` | An array of returned key-value pairs and cursors. |
| `edges.node` | The requested contents of Forge Storage, returned as a key-value pair. |
| `edges.cursor` | A string value that can be supplied in the `after` field of a subsequent query, to fetch the next page of data. |
| `pageInfo.hasNextPage` | A boolean indicating whether there is still more data that can be returned if the query is invoked again with `after` set to the cursor value. |

**GraphQL variables**

```
```
1
2
```



```
{
    "where": {
        "field": "key",
        "condition": "STARTS_WITH",
        "value": "example key"
    },
    "first": 10,
    "encrypted": true | false,
    "after": "Optional, used for paginated requests. Use the cursor field from the previous query to fetch the next page."
}
```
```

| Variable | Description |
| --- | --- |
| `where` | The selection criteria for query results. |
| `where.field` | The field on which to query. This must be set to `"key"`. |
| `where.condition` | The query operator to use. This must be set to `"STARTS_WITH"`. |
| `where.value` | The key for which to retrieve values. |
| `first` | The maximum number of entries this query can return. This can be set to at most 20. |
| `encrypted` | A boolean indicating whether the data is encrypted or not. |
| `after` | An optional cursor value used to retrieve subsequent pages of data for a query that has more than one page of matching results. |

### GraphQL response

**GraphQL response (Successfully retrieved 2 entries)**

```
```
1
2
```



```
{
  "data": {
    "appStoredEntities": {
      "edges": [
        {
          "node": {
            "value": "test-value-1",
            "key": "test-key-1"
          },
          "cursor": "FAJ0ZXN0LWtleS0xAA=="
        },
        {
          "node": {
            "value": "test-value-2",
            "key": "test-key-2"
          },
          "cursor": "FAJ0ZXN0LWtleS0yAA=="
        }
      ],
      "pageInfo": {
        "hasNextPage": true
      }
    }
  }
}
```
```

### Example

Get up to 10 results where the key begins with “example”. Start from the cursor location `FAJ0ZXN0LWtleS0yAA==`.

Set the maximum number of responses to return using the `first` property. The maximum number of responses you can request is 20.

You can retrieve the value of the `cursor` from the response of your previous query. If there are more pages to fetch, the `hasNextPage` field will be `true`.

#### Query

**GraphQL variables**

```
```
1
2
```



```
{
    "where": {
        "field": "key",
        "condition": "STARTS_WITH",
        "value": "example"
    },
    "first": 10,
    "encrypted": false,
    "after": "FAJ0ZXN0LWtleS0yAA=="
}
```
```

#### Response

```
```
1
2
```



```
{
    "data": {
        "appStoredEntities": {
            "edges": [
                {
                    "node": {
                        "value": "test-value-2",
                        "key": "example-2"
                    },
                    "cursor": "FAJ0ZXN0LWtleS0yAA=="
                },
                {
                    "node": {
                        "value": "test-value-3",
                        "key": "example-3"
                    },
                    "cursor": "FAJ0ZXN0LWtleS0zAA=="
                }
            ]
        }
    }
}
```
```

## Delete storage key

Deletes a `value` by `key`.

### GraphQL query

```
```
1
2
```



```
mutation forge_app_deleteExample($input: DeleteAppStoredEntityMutationInput!) {
  appStorage {
    deleteAppStoredEntity(input: $input) {
      success
      errors {
        message
        extensions {
          errorType
          statusCode
        }
      }
    }
  }
}
```
```

**GraphQL variables**

```
```
1
2
```



```
{
  "input": {
    "key": "example key",
    "encrypted" true | false
  }
}
```
```

| Variable | Description |
| --- | --- |
| `key` | The key for which to retrieve a value from Forge Storage. |
| `encrypted` | A boolean indicating whether this Forge Storage entry is encrypted. |

### GraphQL response

**GraphQL response (Successfully deletes the key)**

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "deleteAppStoredEntity": {
        "success": true,
        "errors": null
      }
    }
  }
}
```
```

**GraphQL response (Fails to delete the key due to an invalid key provided in the request)**

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "deleteAppStoredEntity": {
        "success": false,
        "errors": [
          {
            "message": "Key \"test-key-@\" should match the pattern \"/^(?!\\s+$)[a-zA-Z0-9:._\\s-#]+$/\"",
            "extensions": {
              "errorType": "INVALID_KEY",
              "statusCode": 400
            }
          }
        ]
      }
    }
  }
}
```
```

### Example

Delete the value associated with the key "example-key".

#### Query

**GraphQL variables**

```
```
1
2
```



```
{
  "input": {
    "key": "example key",
    "encrypted" false
  }
}
```
```

#### Response

```
```
1
2
```



```
{
  "data": {
    "appStorage": {
      "deleteAppStoredEntity": {
        "success": true,
        "errors": null
      }
    }
  }
}
```
```

## Next steps

For further help, see how you can:
