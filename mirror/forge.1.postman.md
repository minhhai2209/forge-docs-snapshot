```
{
  "info": {
    "_postman_id": "cd7fe866-81ff-46d9-91b9-36e34ccdd0aa",
    "name": "Key-Value Store/Custom Entity Store REST API",
    "description": "Forge provides hosted storage capabilities for storing your app's data:\n- **Key-Value Store** - stores data as key-value pairs\n- **Custom Entity Store** - stores data within custom data structures (entities)\nBoth capabilities have resources that can be used natively, or accessed by remote resources via REST API. For more information about both capabilities,\nsee [storage-api](https://developer.atlassian.com/platform/forge/runtime-reference/storage-api/).",
    "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
  },
  "item": [
    {
      "name": "Key-Value Store",
      "description": "The Key-Value Store provides simple storage for key/value pairs.\nUse this to persistently store data that you'd like to retrieve through the\n[Query](#api-v1-query-post) operation.\n",
      "item": [
        {
          "name": "Get value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Gets a value by key.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Set value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Stores a JSON value with a specified key. Forge resolves write conflicts using a last-write-wins strategy by default, but this can be configured via the key policy option.\nOptionally, you can specify a TTL (Time To Live) to automatically expire the data after a specified duration.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Delete value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a value by key. Write conflicts are resolved using a last-write-wins strategy.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Query key-value pairs",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/query",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Retrieve key-value pairs matching the provided list of criteria. This method does not return secret values set by [Set secret value](/platform/forge/rest/api-group-key-value-store/#api-v1-secret-set-post).",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get secret value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/secret/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Gets a value by key, which was stored using [Set secret value by key](/platform/forge/rest/api-group-key-value-store/#api-v1-secret-set-post). The value is decrypted before being returned.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Set secret value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/secret/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Stores sensitive credentials in JSON format, with encryption. \nValues set with this method can only be accessed with [Get secret value by key](/platform/forge/rest/api-group-key-value-store/#api-v1-secret-get-post). \nWrite conflicts are resolved using a last-write-wins strategy by default, but this can be configured via the key policy option.\nOptionally, you can specify a TTL (Time To Live) to automatically expire the data after a specified duration.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Delete secret value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/secret/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a secret value by key.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Custom Entity Store",
      "description": "The Custom Entity Store lets you store data in [custom entities](/platform/forge/runtime-reference/custom-entities/), which are data structures\nyou can define according to your app's needs. Custom entities let you assign multiple values\n(or \"attributes\") to a single key (or \"entity\") and define indexes to optimize queries against\nthese values.\n",
      "item": [
        {
          "name": "Get custom entity value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/entity/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Gets a custom entity value by key.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Set custom entity value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/entity/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Stores a JSON value with a specified key, for the selected entity.\nOptionally, you can specify a TTL (Time To Live) to automatically expire the data after a specified duration.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Delete custom entity value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/entity/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a value by key, for the selected entity.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Query custom entities",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/entity/query",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Retrieves custom entities matching the provided list of criteria using query conditions. See [Querying the Custom Entity Store](https://developer.atlassian.com/platform/forge/runtime-reference/storage-api-query-complex/) for more information about building complex queries.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Transaction",
      "description": "The Transaction API allows you to perform multiple operations on key-value pairs and/or custom entities in a single atomic transaction.\nThis ensures that either all operations succeed or none do, maintaining data integrity.\n",
      "item": [
        {
          "name": "Execute transaction",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/transaction",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Lets you perform a series of Key-Value Store and/or Custom Entity Store operations that must all succeed or fail together. This method supports 3 types of operations:\n- create or update data\n- delete data\n- check whether a specific Custom Entity condition is true\n(optionally with TTL for automatic expiration)",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Batch",
      "description": "The Batch API allows you to perform multiple operations on key-value pairs and/or custom entities in a single request.\nThis can improve performance by reducing the number of network calls.\n",
      "item": [
        {
          "name": "Batch set key-value pairs",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v1/batch/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Sets multiple Key-Value Store and/or Custom Entity Store values in a single operation. \nReturns a type ```BatchResponse``` which contains ```successfulKeys``` and ```failedKeys```.\nOptionally, you can specify a TTL (Time To Live) for each item to automatically expire the data after a specified duration.",
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "protocol",
      "name": "Protocol",
      "description": "The HTTP Protocol that should be used for this REST API.",
      "type": "string",
      "value": "https"
    },
    {
      "key": "host",
      "name": "Host",
      "description": "The HTTP host that should be used for this REST API.",
      "type": "string",
      "value": "api.atlassian.com"
    },
    {
      "key": "basePath",
      "name": "Base Path",
      "description": "The path, after the host, of the base of the REST API.",
      "type": "string",
      "value": "forge/storage/kvs/"
    }
  ]
}
```
