# The Forge REST API

POST

## Proxy POST request to Atlassian GraphQL API

Proxies POST requests to the Atlassian GraphQL API.

**API Documentation:** [Atlassian GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/)

**Examples:**

**Query Example:**

```
1
2
3
{
  "query": "query GetProjects { projects { id name key } }"
}
```

**Mutation Example:**

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
{
  "query": "mutation CreateIssue($input: CreateIssueInput!) { createIssue(input: $input) { issue { id key summary } } }",
  "variables": {
    "input": {
      "projectId": "10001",
      "summary": "New issue from GraphQL",
      "description": "Issue description"
    }
  }
}
```

Forge and OAuth2 apps cannot access this REST resource.

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
