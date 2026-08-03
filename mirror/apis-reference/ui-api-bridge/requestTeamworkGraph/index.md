# requestTeamworkGraph (EAP)

The `requestTeamworkGraph` bridge method enables Forge apps to call the
[Teamwork Graph GraphQL API](/platform/teamwork-graph/api-reference/overview/) **on behalf of the user who is currently interacting with the app** in the browser. Unlike back-end functions, front-end calls always run as the current user — there is no `asApp()` equivalent.

This means that, in addition to the app declaring the correct [scopes](/platform/forge/manifest-reference/permissions/) in its manifest, the current user must have the Teamwork Graph permissions required by the GraphQL operation being called.

If you need to call the Teamwork Graph API as the app itself, use the [`requestTeamworkGraph`](/platform/forge/runtime-reference/product-fetch-api/#contextual-methods) method from the `@forge/api` package in a back-end function, and call it with `api.asApp()`. See [Contextual methods](/platform/forge/runtime-reference/product-fetch-api/#contextual-methods) for more information on the differences between `asUser()` and `asApp()`.

## Function signature

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
type TeamworkGraphResult = {
  data?: Record<string, unknown> | null;
  errors?: Array<Record<string, unknown>>;
};

const requestTeamworkGraph = (
  query: string,
  variables?: Record<string, unknown>,
): Promise<TeamworkGraphResult>
```

## Arguments

Unlike other Atlassian app APIs, the Teamwork Graph API is a GraphQL API. If you're not familiar with GraphQL, we recommend following the [Teamwork Graph API tutorial](/platform/teamwork-graph/call-the-teamwork-graph-api/) and using the GraphQL explorer at `https://<your-site>.atlassian.net/gateway/api/graphql/twg` to learn how to form queries.

* **query**: The GraphQL query. See the
  [Teamwork Graph API reference](/platform/teamwork-graph/api-reference/overview/) for more information.
* **variables** *(optional)*: The GraphQL variables to provide to the query.

## Returns

* `TeamworkGraphResult`: An object containing the response data from the GraphQL query.
  * **data**: the GraphQL response payload. The shape of this object mirrors the TWG query;
    each key corresponds to a queried field, with nested structure reflecting the Cypher-backed
    graph traversal. May be `null` if a top-level error prevented execution, or partially
    populated alongside `errors` in the case of field-level failures.
  * **errors**: The errors array returned from the API response.

## Example

The following example shows a Jira full-page app that retrieves all Confluence pages and Jira work items created by the currently logged-in user.

### Manifest example

The following manifest declares the `read:graph:jira` scope to enable access to the Teamwork Graph API:

```
```
1
2
```



```
# manifest.yml
modules:
  jira:fullPage:
    - key: jira-full-page
      resource: custom-ui-resource
      title: "My Teamwork Graph App"
resources:
  - key: custom-ui-resource
    path: static/hello-world/build
permissions:
  scopes:
    - 'read:graph:jira'
```
```

If you are installing your app onto Confluence, you will also need to add the `read:graph:confluence` scope.

### Frontend example

The following component calls `requestTeamworkGraph` with the user's account ID to fetch graph data, and render the result:

```
```
1
2
```



```
// src/frontend/index.jsx
import React, { useEffect, useState } from 'react';
import { requestTeamworkGraph, view } from '@forge/bridge';
import { GQL_QUERY, CYPHER_QUERY } from './getConfluencePagesAndJiraIssues';

function App() {
  const [teamworkGraphData, setTeamworkGraphData] = useState(null);
  const [isTeamworkGraphLoading, setIsTeamworkGraphLoading] = useState(true);
  const [isTeamworkGraphError, setIsTeamworkGraphError] = useState(false);
  const [accountId, setAccountId] = useState(null);

  useEffect(() => {
    view.getContext().then((context) => setAccountId(context.accountId));
  }, []);

  useEffect(() => {
    if (!accountId) return;

    requestTeamworkGraph(GQL_QUERY, {
      cypherQuery: CYPHER_QUERY,
      params: { id: `ari:cloud:identity::user/${accountId}` },
    })
      .then(({ data, errors }) => {
        if (errors?.length > 0) {
          setIsTeamworkGraphError(true);
          for (const error of errors) {
            console.error('Error requesting teamwork graph:', error.message);
          }
        } else {
          setIsTeamworkGraphError(false);
          setTeamworkGraphData(data);
        }
      })
      .catch((error) => {
        setIsTeamworkGraphError(true);
        console.error('Error requesting teamwork graph:', error);
      })
      .finally(() => setIsTeamworkGraphLoading(false));
  }, [accountId]);

  return (
    <div>
      {isTeamworkGraphLoading && (
        <p>Loading Teamwork Graph data...</p>
      )}
      {isTeamworkGraphError && (
        <p>Error requesting Teamwork Graph data. Check the console for details.</p>
      )}
      {teamworkGraphData && !isTeamworkGraphError && (
        <>
          <p>Teamwork Graph data loaded successfully</p>
          <p>{JSON.stringify(teamworkGraphData, null, 2)}</p>
        </>
      )}
    </div>
  );
}
```
```

### Query example

The following defines the Cypher query and the wrapping GraphQL query used to retrieve pages and work items for a given user ARI:

```
```
1
2
```



```
export const CYPHER_QUERY = `
MATCH (user:IdentityUser {ari: $id})-[:atlassian_user_created_confluence_page|atlassian_user_created_jira_work_item]->(target)
RETURN user, target`
export const GQL_QUERY = `
query Atlassian_GetAllPagesAndIssues($cypherQuery: String!, $params: CypherRequestParams) {
  cypherQuery(query: $cypherQuery, params: $params) {
    edges {
      node {
        columns {
          key
          value {
            __typename
            ... on CypherQueryResultNode {
                id
                data {
                  __typename
                  ... on ConfluencePage {
                    title
                    webUrl
                  }
                  ... on JiraWorkItem {
                    summary
                  }
                }
            }
          }
        }
      }
    }
  }
}
`;
```
```
