# The Forge REST API

POST

## Proxy POST request to Atlassian GraphQL API

Proxies POST requests to the Atlassian GraphQL API.

**API Documentation:** [Atlassian GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/)

**Examples:**

**Query Example:**

```
1{
2  "query": "query GetProjects { projects { id name key } }"
3}
4
```

**Mutation Example:**

```
1{
2  "query": "mutation CreateIssue($input: CreateIssueInput!) { createIssue(input: $input) { issue { id key summary } } }",
3  "variables": {
4    "input": {
5      "projectId": "10001",
6      "summary": "New issue from GraphQL",
7      "description": "Issue description"
8    }
9  }
10}
11
```

### Request

Expand all

**forge-proxy-authorization**

string

Required

#### Request bodyapplication/json

Generic request body

object

### Responses

200OK

Request successfully proxied to Atlassian GraphQL API

400Bad Request429Too Many Requests500Internal Server Error
