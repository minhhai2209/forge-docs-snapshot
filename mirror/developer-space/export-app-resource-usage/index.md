# Export app resource usage

App resource usage, which can be viewed in the [developer console](https://developer.atlassian.com/console/myapps/), shows you your Forge app resource usage across all sites.

You can also use our **App resource usage API** to export app usage metrics to several observability tools. Such tools offer capabilities, like grouping and filtering metrics by different attributes and integrating with incident response tools.

Exporting app resource usage involves the following steps:

1. [Authenticate with the Atlassian Gateway](#authenticate-with-the-atlassian-gateway)
2. [Query the app resource usage API](#query-the-app-resource-usage-api)

## Authenticate with the Atlassian Gateway

You must first
[authenticate with the Atlassian GraphQL Gateway (AGG)](/platform/atlassian-graphql-api/graphql/#authentication)
to consume the API and export app metrics to a tool of your choice.

The Atlassian account making the request must be the same account that owns the Forge app.

To get started using basic authentication:

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Select **Create API token**.
3. Enter a label to describe your API token. For example, *export-metrics-api-token*.
4. Select **Create**.
5. Select **Copy to clipboard** and close the dialog.
6. Include the token and your email in the header of your GraphQL request.
7. Pass the `X-ExperimentalAPI` header. This is because the API is still in the experimental phase
   and is subject to change.
8. Provide a custom `User-Agent` header. This helps differentiate traffic coming from
   the developer console and your own export service. We recommend using this value:
   `ForgeMetricsExportServer/1.0.0`

## Query the app resource usage API

You can use the *sample queries* below and try the app resource usage API at [GraphQL Gateway](https://api.atlassian.com/graphql) for your Forge app. Ensure to input the corresponding *properties* in your queries.

* Single `usageKey` per request
* Supports groupBy `ENVIRONMENT_ID` and pagination
* Rate limits of 5 requests/minute
* Automatic groupBy is applied if `contextAris` are specified without groupBy

### Sample queries

**Sample query (Flat):**

```
```
1
2
```



```
query AppResourceUsageFlat(
  $appId: ID!
  $filters: DevConsoleAppResourceUsageFiltersInput!
) {
  ecosystem {
    devConsole {
      appResourceUsage(
        appId: $appId
        filters: $filters
      ) {
        ... on DevConsoleAppResourceUsageFlatResponse {
          resourceUsage {
            period
            resolution
            tokensConsumed
            tokenUnit
          }
          pagination {
            page
            pageSize
          }
          error {
            message
            identifier
            extensions {
              errorType
              statusCode
            }
          }
        }
      }
    }
  }
}
```
```

**Variables:**

```
```
1
2
```



```
{
  "appId": "<your app id>",
  "filters": {
    "resource": "FUNCTION_COMPUTE",
    "interval": {
      "start": "2025-09-01T00:00:00Z",
      "end": "2025-09-30T23:59:59Z"
    },
    "contextAris": ["ari:cloud:jira::site/12345"],
    "page": 1
  }
}
```
```

**Sample response:**

```
```
1
2
```



```
{
  "resourceUsage": [
    {
      "period": "2025-09-01",
      "resolution": "ONE_DAY",
      "tokensConsumed": "1.024000",
      "tokenUnit": "GB-seconds"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 100
  },
  "error": null
}
```
```

**Sample query (Grouped):**

```
```
1
2
```



```
query AppResourceUsageGroupedByContext(
  $appId: ID!
  $filters: DevConsoleAppResourceUsageFiltersInput!
  $groupBy: DevConsoleGroupBy!
) {
  ecosystem {
    devConsole {
      appResourceUsage(
        appId: $appId
        filters: $filters
        groupBy: $groupBy
      ) {
        ... on DevConsoleAppResourceUsageGroupedResponse {
          resourceUsage {
            period
            resolution
            groups {
              groupBy
              groupValue
              tokensConsumed
              tokenUnit
            }
          }
          pagination {
            page
            pageSize
          }
          error {
            message
            identifier
            extensions {
              errorType
              statusCode
            }
          }
        }
      }
    }
  }
}
```
```

**Variables:**

```
```
1
2
```



```
{
  "appId": "<your app id>",
  "filters": {
    "resource": "FUNCTION_COMPUTE",
    "interval": {
      "start": "2025-09-01T00:00:00Z",
      "end": "2025-09-30T23:59:59Z"
    },
    "contextAris": ["ari:cloud:jira::site/12345"],
    "page": 1
  },
  "groupBy": "CONTEXT_ARI"
}
```
```
