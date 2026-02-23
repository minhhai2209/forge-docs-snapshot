```
{
  "info": {
    "_postman_id": "9adaa327-91e5-427a-a4f6-6989e0f1947e",
    "name": "Forge Containers API",
    "description": "The Forge Containers Public API\n\n**Important:** The API base URL should be read from the `FORGE_EGRESS_PROXY_URL` environment variable.\nThe localhost URL in the servers section is for documentation purposes only.\n",
    "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
  },
  "item": [
    {
      "name": "App Installations",
      "description": "APIs for accessing installations information.",
      "item": [
        {
          "name": "Get app installations",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}v0/installations",
              "query": [],
              "variable": []
            },
            "method": "GET",
            "header": [
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Returns all installations for the given app Id and environment.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Atlassian GraphQL",
      "description": "Atlassian GraphQL API endpoints for accessing cross-product data and relationships.\n\n**API Documentation:** [Atlassian GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/)\n\nThe Atlassian GraphQL API allows you to access all sorts of Atlassian data including Jira projects, Bitbucket repositories, \nOpsgenie teams, and cross-product work activities using one common mechanism through the Atlassian GraphQL Gateway.\nUse the `/atlassian/graphql/{target}` endpoint to proxy requests to the Atlassian GraphQL API.\n",
      "item": [
        {
          "name": "Proxy POST request to Atlassian GraphQL API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/graphql/",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies POST requests to the Atlassian GraphQL API.\n\n**API Documentation:** [Atlassian GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/)\n\n**Examples:**\n\n**Query Example:**\n```json\n{\n  \"query\": \"query GetProjects { projects { id name key } }\"\n}\n```\n\n**Mutation Example:**\n```json\n{\n  \"query\": \"mutation CreateIssue($input: CreateIssueInput!) { createIssue(input: $input) { issue { id key summary } } }\",\n  \"variables\": {\n    \"input\": {\n      \"projectId\": \"10001\",\n      \"summary\": \"New issue from GraphQL\",\n      \"description\": \"Issue description\"\n    }\n  }\n}\n```\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Confluence",
      "description": "Confluence API endpoints for accessing Confluence Cloud platform functionality.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\nThe Confluence API provides comprehensive access to pages, spaces, users, comments, and other Confluence resources.\nUse the `/confluence/{target}` endpoint to proxy requests to the Confluence REST API.\n",
      "item": [
        {
          "name": "Proxy GET request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages/123` - Get page details\n- `api/v2/spaces` - List spaces\n- `api/v2/users/me` - Get current user info\n- `api/v2/pages/123/comments` - Get page comments\n- `api/v2/blogs/123` - Get blog post details\n",
                  "disabled": false
                }
              ]
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies requests to the Confluence Cloud REST API v2.\nThe target parameter specifies the Confluence API endpoint.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\n**Examples:**\n- `/confluence/api/v2/pages/123` - Get page details\n- `/confluence/api/v2/spaces` - List spaces\n- `/confluence/api/v2/users/me` - Get current user info\n- `/confluence/api/v2/pages/123/comments` - Get page comments\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PUT request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages/123` - Update page\n- `api/v2/blogs/123` - Update blog post\n- `api/v2/pages/123/comments/456` - Update comment\n",
                  "disabled": false
                }
              ]
            },
            "method": "PUT",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PUT requests to the Confluence Cloud REST API v2.\nThe target parameter specifies the Confluence API endpoint.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\n**Examples:**\n- `/confluence/api/v2/pages/123` - Update page\n- `/confluence/api/v2/blogs/123` - Update blog post\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy POST request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages` - Create new page\n- `api/v2/pages/123/comments` - Add comment to page\n- `api/v2/blogs` - Create new blog post\n- `api/v2/spaces` - Create new space\n",
                  "disabled": false
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies POST requests to the Confluence Cloud REST API v2.\nThe target parameter specifies the Confluence API endpoint.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\n**Examples:**\n- `/confluence/api/v2/pages` - Create new page\n- `/confluence/api/v2/pages/123/comments` - Add comment to page\n- `/confluence/api/v2/blogs` - Create new blog post\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy DELETE request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages/123` - Delete page\n- `api/v2/pages/123/comments/456` - Delete comment\n- `api/v2/blogs/123` - Delete blog post\n",
                  "disabled": false
                }
              ]
            },
            "method": "DELETE",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies DELETE requests to the Confluence Cloud REST API v2.\nThe target parameter specifies the Confluence API endpoint.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\n**Examples:**\n- `/confluence/api/v2/pages/123` - Delete page\n- `/confluence/api/v2/pages/123/comments/456` - Delete comment\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy OPTIONS request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages` - Discover available methods for pages\n- `api/v2/spaces` - Discover available methods for spaces\n",
                  "disabled": false
                }
              ]
            },
            "method": "OPTIONS",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies OPTIONS requests to the Confluence Cloud REST API v2.\nUsed for CORS preflight requests and method discovery.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy HEAD request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages/123` - Check if page exists\n- `api/v2/spaces/SPACE` - Check if space exists\n",
                  "disabled": false
                }
              ]
            },
            "method": "HEAD",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies HEAD requests to the Confluence Cloud REST API v2.\nReturns headers without response body, useful for checking resource existence.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PATCH request to Confluence API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}confluence/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Confluence API endpoint path\n\n**Format:** `api/v2/{endpoint}`\n\n**Examples:**\n- `api/v2/pages/123` - Partially update page\n- `api/v2/blogs/123` - Partially update blog post\n",
                  "disabled": false
                }
              ]
            },
            "method": "PATCH",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PATCH requests to the Confluence Cloud REST API v2.\nThe target parameter specifies the Confluence API endpoint.\n\n**API Documentation:** [Confluence Cloud REST API v2](https://developer.atlassian.com/cloud/confluence/rest/)\n\n**Examples:**\n- `/confluence/api/v2/pages/123` - Partially update page\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Forge Context",
      "description": "APIs for retrieving Forge invocation Context",
      "item": [
        {
          "name": "Get invocation context",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}invocation/context",
              "query": [],
              "variable": []
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Returns contextual data associated with the invocation. This API retrieves data cached in the proxy and is expected to be low latency.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Forge Dynamic Modules",
      "description": "Forge Dynamic Modules API for managing dynamic modules",
      "item": [
        {
          "name": "List all dynamic modules",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/installation/v1/dynamic/module",
              "query": [
                {
                  "key": "nextPageToken",
                  "value": "{{nextPageToken}}",
                  "disabled": true,
                  "description": "Token for the next page of results"
                },
                {
                  "key": "limit",
                  "value": "{{limit}}",
                  "disabled": true,
                  "description": "Maximum number of items to return"
                }
              ],
              "variable": []
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Update a dynamic module",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/installation/v1/dynamic/module",
              "query": [],
              "variable": []
            },
            "method": "PUT",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Create a dynamic module",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/installation/v1/dynamic/module",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get a dynamic module",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/installation/v1/dynamic/module/:key",
              "query": [],
              "variable": [
                {
                  "key": "key",
                  "value": "{{key}}",
                  "description": "Key of the dynamic module",
                  "disabled": false
                }
              ]
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Delete a dynamic module",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/installation/v1/dynamic/module/:key",
              "query": [],
              "variable": [
                {
                  "key": "key",
                  "value": "{{key}}",
                  "description": "Key of the dynamic module",
                  "disabled": false
                }
              ]
            },
            "method": "DELETE",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              }
            ],
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Forge Events",
      "description": "Forge async events endpoints for submitting events to queues",
      "item": [
        {
          "name": "Publish Async Events to Forge",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}atlassian/forge/events/v1/async-events",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Submit asynchronous events to the Forge events system.\nEvents are queued for processing and will be delivered to the specified queue.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Forge KVS",
      "description": "Forge Key-Value Store (KVS) API endpoints for storing and retrieving data in key-value pairs.\n\nAPI Documentation: Forge REST API - KVS/Custom Entity Store\n\nThe Forge KVS API provides hosted storage capabilities that let you store data in your app installation. Use the /forge/storage/kvs/{target} endpoint to proxy requests to the Forge KVS REST API.",
      "item": [
        {
          "name": "Get value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/kvs/v1/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a value by key. Write conflicts are resolved using a last-write-wins strategy.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/query",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Retrieve key-value pairs matching the provided list of criteria. This method does not return secret values set by [Set secret value](/platform/forge/rest/v1/api-group-key-value-store/#api-v1-secret-set-post).",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Batch set key-value pairs",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/kvs/v1/batch/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/secret/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Gets a value by key, which was stored using [Set secret value by key](/platform/forge/rest/v1/api-group-key-value-store/#api-v1-secret-set-post). The value is decrypted before being returned.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/secret/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Stores sensitive credentials in JSON format, with encryption. \nValues set with this method can only be accessed with [Get secret value by key](/platform/forge/rest/v1/api-group-key-value-store/#api-v1-secret-get-post). \nWrite conflicts are resolved using a last-write-wins strategy by default, but this can be configured via the key policy option.\nOptionally, you can specify a TTL (Time To Live) to automatically expire the data after a specified duration.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/secret/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a secret value by key.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get custom entity value by key",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/kvs/v1/entity/get",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/entity/set",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/entity/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes a value by key, for the selected entity.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
              "path": "{{basePath}}forge/storage/kvs/v1/entity/query",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Execute transaction",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/kvs/v1/transaction",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Lets you perform a series of Key-Value Store and/or Custom Entity Store operations that must all succeed or fail together. This method supports 3 types of operations:\n- create or update data\n- delete data\n- check whether a specific Custom Entity condition is true\n(optionally with TTL for automatic expiration)",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Forge LLM",
      "description": "This API is accessible only from Forge applications and requires platform-provided authentication headers. It enables Forge apps to interact with native Forge-supported LLMs.\nFor more information, see the [Forge LLMs documentation](https://go.atlassian.com/forge-llms-api-reference)",
      "item": [
        {
          "name": "/forge/llm/{model}",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/llm/:model",
              "query": [],
              "variable": [
                {
                  "key": "model",
                  "value": "{{model}}",
                  "description": "The model to use for the request",
                  "disabled": false
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Proxy endpoint to make requests to the native Forge supported LLMs.",
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
      "name": "Forge Object Store",
      "description": "Forge Object Store API for storing and retrieving objects",
      "item": [
        {
          "name": "Delete Object",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/os/v1/delete",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "description": "Deletes an object from the object store.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get Metadata",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/os/v1/metadata",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Get the metadata for the specified object in the payload.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get Upload URL",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/os/v1/upload-url",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Generates a pre-signed URL for uploading an object.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Get Download URL",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/os/v1/download-url",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Generates a pre-signed URL for downloading an object.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Forge Proxy",
      "description": "External service proxying endpoints for forwarding requests to external services.\n\n**Important:** You can only egress to domains that are listed in the Runtime egress permissions in your Forge Manifest.\nSee [Runtime egress permissions](https://developer.atlassian.com/platform/forge/runtime-egress-permissions/#runtime-egress-permissions) for details.\n\nExternal domains must be declared in the `permissions.external.fetch.backend` section of your `manifest.yml` file.\nUse the `/proxy/{target}` endpoint to proxy requests to external services.\n",
      "item": [
        {
          "name": "Proxy GET request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies requests to external services through the Forge Outbound Proxy (FOP).\nThe target parameter specifies the external service to proxy to.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PUT request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "PUT",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PUT requests to external services through the Forge Outbound Proxy (FOP).\nThe target parameter specifies the external service to proxy to.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy POST request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies POST requests to external services through the Forge Outbound Proxy (FOP).\nThe target parameter specifies the external service to proxy to.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy DELETE request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "DELETE",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies DELETE requests to external services through the Forge Outbound Proxy (FOP).\nThe target parameter specifies the external service to proxy to.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy OPTIONS request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "OPTIONS",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies OPTIONS requests to external services through the Forge Outbound Proxy (FOP).\nUsed for CORS preflight requests and method discovery.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy HEAD request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "HEAD",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies HEAD requests to external services through the Forge Outbound Proxy (FOP).\nReturns headers without response body, useful for checking resource existence.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PATCH request to external service",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}proxy/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target external service URL or operation\n\n**Example:** `httpbin.org/status/200`\n",
                  "disabled": false
                }
              ]
            },
            "method": "PATCH",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PATCH requests to external services through the Forge Outbound Proxy (FOP).\nThe target parameter specifies the external service to proxy to.\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "name": "Forge Realtime",
      "description": "Forge realtime service endpoints for publishing events",
      "item": [
        {
          "name": "Publish an event to a realtime channel",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/realtime/v1/publish",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body",
                "disabled": true
              },
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
            "description": "Proxies POST requests to Forge realtime services for publishing events.\nAll clients in the same context as the sender and subscribed to this realtime channel will receive the event.\n\"Publish\" requests only work when the request originated from a UI context invocation. In the `forge-proxy-authorization` header you must specify the `id` of the invocation; you can't perform operations on behalf of an `installationId`.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"forge-container-realtime-channel\",\n  \"payload\": \"Realtime message sent from the container service, id=1\",\n  \"options\": {\n    \"token\": \"example-token\"\n  }\n}"
            }
          },
          "response": []
        },
        {
          "name": "Publish an event to a global realtime channel",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/realtime/v1/publish/global",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body",
                "disabled": true
              },
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
            "description": "Proxies POST requests to Forge realtime services for publishing events.\nAll clients subscribed to this global realtime channel will receive the event.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"forge-container-realtime-channel\",\n  \"payload\": \"Realtime message sent from the container service, id=1\"\n}"
            }
          },
          "response": []
        },
        {
          "name": "Sign a forge realtime token",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/realtime/v1/token",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body",
                "disabled": true
              },
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
            "description": "Signs a forge realtime token that can be used to securely publish events to realtime channels.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"channelName\": \"forge-container-realtime-channel\",\n  \"claims\": {\n    \"allowedUsers\": [\n      \"user1\",\n      \"user2\"\n    ]\n  }\n}"
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Forge SQL",
      "description": "Forge SQL Storage REST API for containers",
      "item": [
        {
          "name": "Execute a DML SQL statement",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/sql/v1/execute",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Executes a SQL statement, and with optional params to be substituted in. This is to be used for DML (Data Manipulation) queries.\n\nDML queries are limited to SELECT, INSERT, UPDATE and DELETE statements.\n\nThis is recommended for all user facing requests, as the restrictive permissions limits the potential impact of a client being able to \nsuccessfully use a query injection attack on your app. Using params will use server side params to further mitigate against these attacks.\n\nThe DDL API is available for all other statements, and should be used sparingly, and avoid usage where client provided parameters are included.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"query\": \"SELECT name, age FROM users WHERE name = ? AND age = ?\",\n  \"params\": [\n    \"Alice\",\n    30\n  ]\n}"
            }
          },
          "response": []
        },
        {
          "name": "Execute a DDL SQL statement",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}forge/storage/sql/v1/execute/ddl",
              "query": [],
              "variable": []
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
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
            "description": "Executes a SQL statement, and with optional params to be substituted in. This is to be used for DDL (Data Definition) queries.\n\nDDL refers to statements like CREATE, ALTER and DROP. This DDL endpoint is your schema management endpoint and is granted all * permissions to your schema.\n\nWe recommended to use this API only when modifying your schema in some way, and doesn’t include user generated params, as there is a \nchance for higher impact on failure to do so. Use the DML based endpoint for user based requests.\nThe API rate and connection limits are more restrictive than the DML endpoint.",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": "{\n  \"query\": \"CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, name TEXT NOT NULL, age INT NOT NULL);\",\n  \"params\": []\n}"
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Jira",
      "description": "Jira API endpoints for accessing Jira Cloud platform functionality.\n\n**API Documentation:** \n- [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n- [Jira Software Cloud REST API](https://developer.atlassian.com/cloud/jira/software/rest/intro)\n- [Jira Service Management Cloud REST API](https://developer.atlassian.com/cloud/jira/service-desk/rest/intro/)\n\nThe Jira API provides comprehensive access to issues, projects, users, workflows, and other Jira resources.\nUse the `/jira/{target}` endpoint to proxy requests to the Jira REST API.\n",
      "item": [
        {
          "name": "Proxy GET request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue/ISSUE-123` - Get issue details\n- `rest/api/3/project` - List projects\n- `rest/api/3/myself` - Get current user info\n- `rest/api/3/search` - Search issues using JQL\n- `rest/api/3/issue/ISSUE-123/comment` - Get issue comments\n",
                  "disabled": false
                }
              ]
            },
            "method": "GET",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies requests to the Jira Cloud Platform REST API v3.\nThe target parameter specifies the Jira API endpoint.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n\n**Examples:**\n- `/jira/rest/api/3/issue/ISSUE-123` - Get issue details\n- `/jira/rest/api/3/project` - List projects\n- `/jira/rest/api/3/myself` - Get current user info\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PUT request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue/ISSUE-123` - Update issue\n- `rest/api/3/project/PROJECT-123` - Update project\n- `rest/api/3/issue/ISSUE-123/comment/123` - Update comment\n",
                  "disabled": false
                }
              ]
            },
            "method": "PUT",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PUT requests to the Jira Cloud Platform REST API v3.\nThe target parameter specifies the Jira API endpoint.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n\n**Examples:**\n- `/jira/rest/api/3/issue/ISSUE-123` - Update issue\n- `/jira/rest/api/3/project/PROJECT-123` - Update project\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy POST request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue` - Create new issue\n- `rest/api/3/issue/ISSUE-123/comment` - Add comment to issue\n- `rest/api/3/search` - Search issues using JQL\n- `rest/api/3/project` - Create new project\n",
                  "disabled": false
                }
              ]
            },
            "method": "POST",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies POST requests to the Jira Cloud Platform REST API v3.\nThe target parameter specifies the Jira API endpoint.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n\n**Examples:**\n- `/jira/rest/api/3/issue` - Create new issue\n- `/jira/rest/api/3/issue/ISSUE-123/comment` - Add comment to issue\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
            "body": {
              "mode": "raw",
              "raw": ""
            }
          },
          "response": []
        },
        {
          "name": "Proxy DELETE request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue/ISSUE-123` - Delete issue\n- `rest/api/3/issue/ISSUE-123/comment/123` - Delete comment\n- `rest/api/3/project/PROJECT-123` - Delete project\n",
                  "disabled": false
                }
              ]
            },
            "method": "DELETE",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies DELETE requests to the Jira Cloud Platform REST API v3.\nThe target parameter specifies the Jira API endpoint.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n\n**Examples:**\n- `/jira/rest/api/3/issue/ISSUE-123` - Delete issue\n- `/jira/rest/api/3/issue/ISSUE-123/comment/123` - Delete comment\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy OPTIONS request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue` - Discover available methods for issues\n- `rest/api/3/project` - Discover available methods for projects\n",
                  "disabled": false
                }
              ]
            },
            "method": "OPTIONS",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies OPTIONS requests to the Jira Cloud Platform REST API v3.\nUsed for CORS preflight requests and method discovery.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy HEAD request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue/ISSUE-123` - Check if issue exists\n- `rest/api/3/project/PROJECT-123` - Check if project exists\n",
                  "disabled": false
                }
              ]
            },
            "method": "HEAD",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "description": "",
                "disabled": false,
                "key": "Accept",
                "value": "application/json"
              }
            ],
            "description": "Proxies HEAD requests to the Jira Cloud Platform REST API v3.\nReturns headers without response body, useful for checking resource existence.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            }
          },
          "response": []
        },
        {
          "name": "Proxy PATCH request to Jira API",
          "request": {
            "url": {
              "protocol": "{{protocol}}",
              "host": "{{host}}",
              "path": "{{basePath}}jira/:target",
              "query": [],
              "variable": [
                {
                  "key": "target",
                  "value": "{{target}}",
                  "description": "Target Jira API endpoint path\n\n**Format:** `rest/api/3/{endpoint}`\n\n**Examples:**\n- `rest/api/3/issue/ISSUE-123` - Partially update issue\n- `rest/api/3/project/PROJECT-123` - Partially update project\n",
                  "disabled": false
                }
              ]
            },
            "method": "PATCH",
            "header": [
              {
                "key": "forge-proxy-authorization",
                "value": "{{forge-proxy-authorization}}",
                "description": "Forge Proxy Authorization header. Must start with \"Forge \" followed by comma-separated key-value pairs.\n\n**Format:** `Forge [field1=value1,field2=value2,...]`\n\n**Required Fields:**\n- `id` - Invocation ID from the corresponding inbound request (x-forge-invocation-id)\n\n**Optional Fields:**\n- `as=` - Specifies whether to call the API using either the app or its user as context\n- `accountId=` - For user impersonation (only supported when as=user)\n\n**Examples:**\n- `Forge as=app,id=invocation-123` - Use app context with invocation ID\n- `Forge as=user,id=invocation-123` - Use user context with invocation ID  \n- `Forge as=user,accountId=user-123,id=invocation-123` - User impersonation\n",
                "disabled": false
              },
              {
                "key": "Content-Type",
                "value": "{{Content-Type}}",
                "description": "Content type of the request body\n\n**Example:** `application/json`\n",
                "disabled": true
              },
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
            "description": "Proxies PATCH requests to the Jira Cloud Platform REST API v3.\nThe target parameter specifies the Jira API endpoint.\n\n**API Documentation:** [Jira Cloud Platform REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/)\n\n**Examples:**\n- `/jira/rest/api/3/issue/ISSUE-123` - Partially update issue\n",
            "auth": {
              "type": "bearer",
              "bearer": {
                "key": "token",
                "type": "string"
              }
            },
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
      "value": "%7BFORGE_EGRESS_PROXY_URL%7D/"
    }
  ]
}
```
