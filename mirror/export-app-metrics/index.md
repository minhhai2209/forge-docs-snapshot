# Export app metrics

App metrics, which can be viewed in the [developer console](/platform/forge/view-app-metrics/),
show you how your Forge app is currently performing across all
[sites](/developer-guide/glossary).

You can also use our **App metrics API** to export app metrics to several observability tools,
including [SignalFX](https://www.splunk.com/) and [Datadog](https://www.datadoghq.com/).
Such tools offer capabilities, like grouping and filtering metrics by different attributes
and integrating with incident response tools.

The App metrics API is an [Atlassian GraphQL](/platform/atlassian-graphql-api/graphql/)
metrics API that provides metrics in the
[OTLP protobuf JSON](https://protobuf.dev/programming-guides/proto3/#json) format, which is
the format used in the
[OpenTelemetry framework](/platform/forge/app-metrics-in-third-party-tools/#opentelemetry-framework).

The following app metrics can be exported to monitoring tools via the App metrics API:

Exporting app metrics involves the following steps:

1. [Authenticate with the Atlassian GraphQL Gateway](#authenticate-with-the-atlassian-graphql-gateway/)
2. [Query the App metrics API](#query-the-app-metrics-api)
3. [Set up your infrastructure](#set-up-your-infrastructure)

Check out
[this repository](https://bitbucket.org/atlassian/forge-observability-consumption-patterns/src/main/metrics/)
for example code and resources for configuring observability tools
to consume Forge app metrics.

## Authenticate with the Atlassian GraphQL Gateway

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

## Query the App metrics API

You can use the *sample queries* below and try the App metrics API at
[GraphQL Gateway](https://api.atlassian.com/graphql) for your Forge app. Ensure to input
the corresponding *properties* in your queries.

* You can run a query for up to 14 days in the past. Each API call retrieves a maximum of 15 minutes
  of metrics. This limit is enforced to make sure there aren't too many data points returned
  in the API response.
* We recommend fetching data periodically, for example, every three or five minutes. A rate limit of
  five calls per minute per user is enforced.

### Sample queries

The sample queries return metrics in the
[OTLP protobuf JSON](https://protobuf.dev/programming-guides/proto3/#json) format, which is
the format used in the OpenTelemetry framework.

#### Sample AGG query

```
```
1
2
```



```
query Ecosystem($appId: ID!, $query: ForgeMetricsOtlpQueryInput!) {
  ecosystem {
    forgeMetrics(appId: $appId) {
      appMetrics(query: $query) {
        ... on ForgeMetricsOtlpData {
          resourceMetrics
        }
        ... on QueryError {
          message
          identifier
          extensions {
            statusCode
            errorType
          }
        }
      }
    }
  }
}
```
```

#### Sample AGG query variables

```
```
1
2
```



```
{
  "appId": "ari:cloud:ecosystem::app/8ce114f4-d82c-45e2-b4fb-c6a0751d7d57",
  "query": {
    "filters": {
      "environments": ["8cb293d5-be08-47ae-a75c-95b89da5ad1d"],
      "interval": {
        "start": "2023-06-18T02:55:00.000Z",
        "end": "2023-06-18T02:57:00.000Z"
      },
      "metrics": ["FORGE_API_REQUEST_COUNT", "FORGE_API_REQUEST_LATENCY", "FORGE_BACKEND_INVOCATION_LATENCY", "FORGE_BACKEND_INVOCATION_COUNT", "FORGE_BACKEND_INVOCATION_ERRORS"]
    }
  }
}
```
```

```
```
1
2
```



```
{
  "Authorization": "Basic base64<email:token>",
  "User-Agent": "ForgeMetricsExportServer/1.0.0",
  "X-ExperimentalApi": "ForgeMetricsQuery"
}
```
```

#### Sample AGG query response

```
```
1
2
```



```
{
    "data": {
        "ecosystem": {
            "forgeMetrics": {
                "appMetrics": {
                    "resourceMetrics": [
                        {
                            "resource": {},
                            "schemaUrl": "https://opentelemetry.io/schemas/1.9.0",
                            "scopeMetrics": [
                                {
                                    "metrics": [
                                        {
                                            "name": "forge_api_request_count",
                                            "description": "",
                                            "sum": {
                                                "aggregationTemporality": 1,
                                                "dataPoints": [
                                                    {
                                                        "asInt": 8,
                                                        "attributes": [
                                                            {
                                                                "key": "appId",
                                                                "value": {
                                                                    "stringValue": "a11dfa0b-cf2c-44d1-9080-5c3944961223"
                                                                }
                                                            },
                                                            {
                                                                "key": "contextAri",
                                                                "value": {
                                                                    "stringValue": "ari:cloud:compass::site/04c5a385-0899-4edc-93a8-ada653b7c534"
                                                                }
                                                            },
                                                            {
                                                                "key": "environmentId",
                                                                "value": {
                                                                    "stringValue": "6f5f56e9-55c0-4551-9247-ee1484340f64"
                                                                }
                                                            },
                                                            {
                                                                "key": "provider",
                                                                "value": {
                                                                    "stringValue": "app"
                                                                }
                                                            },
                                                            {
                                                                "key": "remote",
                                                                "value": {
                                                                    "stringValue": "stargate"
                                                                }
                                                            },
                                                            {
                                                                "key": "status",
                                                                "value": {
                                                                    "stringValue": "2xx"
                                                                }
                                                            },
                                                            {
                                                                "key": "url",
                                                                "value": {
                                                                    "stringValue": "/forge/entities/graphql"
                                                                }
                                                            }
                                                        ],
                                                        "startTimeUnixNano": "1698720840000000000",
                                                        "timeUnixNano": "1698720900000000000"
                                                    }
                                                ]
                                            },
                                            "unit": "s"
                                        },
                                        {
                                            "name": "forge_backend_invocation_count",
                                            "description": "",
                                            "sum": {
                                                "aggregationTemporality": 1,
                                                "dataPoints": [
                                                    {
                                                        "asInt": 70,
                                                        "attributes": [
                                                            {
                                                                "key": "appId",
                                                                "value": {
                                                                    "stringValue": "8ce114f4-d82c-45e2-b4fb-c6a0751d7d57"
                                                                }
                                                            },
                                                            {
                                                                "key": "appVersion",
                                                                "value": {
                                                                    "stringValue": "4.64.0"
                                                                }
                                                            },
                                                            {
                                                                "key": "contextAri",
                                                                "value": {
                                                                    "stringValue": "ari:cloud:confluence::site/13095d29-407d-47ec-aa57-76764a470f36"
                                                                }
                                                            },
                                                            {
                                                                "key": "environmentId",
                                                                "value": {
                                                                    "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                                                }
                                                            },
                                                            {
                                                                "key": "functionKey",
                                                                "value": {
                                                                    "stringValue": "updateStatusTitle"
                                                                }
                                                            }
                                                        ],
                                                        "startTimeUnixNano": "1687497375656000000",
                                                        "timeUnixNano": "1687497375662000000"
                                                    }
                                                ]
                                            },
                                            "unit": "s"
                                        },
                                        {
                                            "name": "forge_backend_invocation_errors",
                                            "description": "",
                                            "sum": {
                                                "aggregationTemporality": 1,
                                                "dataPoints": [
                                                    {
                                                        "asInt": 0,
                                                        "attributes": [
                                                            {
                                                                "key": "appId",
                                                                "value": {
                                                                    "stringValue": "8ce114f4-d82c-45e2-b4fb-c6a0751d7d57"
                                                                }
                                                            },
                                                            {
                                                                "key": "appVersion",
                                                                "value": {
                                                                    "stringValue": "5.1.0"
                                                                }
                                                            },
                                                            {
                                                                "key": "contextAri",
                                                                "value": {
                                                                    "stringValue": "ari:cloud:compass::site/6a9ea14f-759d-4f4a-b3ac-11395d8bf519"
                                                                }
                                                            },
                                                            {
                                                                "key": "environmentId",
                                                                "value": {
                                                                    "stringValue": "8cb293d5-be08-47ae-a75c-95b89da5ad1d"
                                                                }
                                                            },
                                                            {
                                                                "key": "errorType",
                                                                "value": {
                                                                    "stringValue": "UNHANDLED_EXCEPTION"
                                                                }
                                                            },
                                                            {
                                                                "key": "functionKey",
                                                                "value": {
                                                                    "stringValue": "process-app-event"
                                                                }
                                                            },
                                                            {
                                                                "key": "moduleKey",
                                                                "value": {
                                                                    "stringValue": "app-event-webtrigger"
                                                                }
                                                            }
                                                        ],
                                                        "startTimeUnixNano": "1687488960000000000",
                                                        "timeUnixNano": "1687489020000000000"
                                                    }
                                                ]
                                            },
                                            "unit": "s"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
}
```
```

### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `appId` | `string` | Yes | A unique identifier for your forge app which can be found in the app's `manifest.yml` file  *Regex:* `ari:cloud:ecosystem::app/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| `filters` | [Filters](#filters) | Yes | Filters to fetch metrics as required. See [Filters](#filters). |

#### Filters

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `environments` | `Array<string>` | Yes | A list of environment UUIDs for which metrics needs to be fetched. *Regex:* `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` |
| `interval` | [Interval](#interval) | Yes | Time range for which metrics needs to be fetched. |
| `metrics` | `Array<enum>` | Yes | A list of enums of metrics to be fetched. Possible values are: `FORGE_API_REQUEST_COUNT` , `FORGE_API_REQUEST_LATENCY` , `FORGE_BACKEND_INVOCATION_COUNT` , `FORGE_BACKEND_INVOCATION_ERRORS`, and `FORGE_BACKEND_INVOCATION_LATENCY` |

#### Interval

Each API call retrieves at most 15 minutes of metrics. You can run a query for up to 14 days in the past.
This limit is enforced to make sure the number of data points returned is not huge in the API response.

We recommend fetching data periodically, for example, every three or five minutes. A rate limit of
five calls per minute per user is enforced.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `start` | `string` | Yes | Start time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format |
| `end` | `string` | Yes | End time in [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) format |

## Set up your infrastructure

To consume the Atlassian GraphQL API and ingest metrics in real-time into observability tools,
we recommend having the following components in your infrastructure:

![Partner Server View](https://dac-static.atlassian.com/platform/forge/images/partner-server-arch.svg?_v=1.5800.1808)

### CronJob service

The CronJob service periodically polls the exposed GraphQL endpoint for the required metrics.
The AGG endpoint returns the OTLP protobuf JSON standard format as a response. The same response
is then pushed as is to the OTEL Sidecar, which is running alongside this cron service.

When setting up the service, you can use either a **serverless framework** or **server framework**.

#### Serverless framework

If using Amazon Web Services (AWS) infrastructure, you can configure Lambda to be executed
every “x” minutes or so. You can also use a similar configuration for Google Cloud Platform (GCP)
or Microsoft Azure infrastructure.

A sample Lambda configuration should look like the following:

```
```
1
2
```



```
```
MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
    FunctionName: MyLambdaFunction
    Runtime: nodejs14.x
    Handler: index.handler
    Code:
        S3Bucket: my-function-bucket
        S3Key: my-function-package.zip
    Layers:
        - !Ref OTelLambdaLayer
    Environment:
        Variables:
        OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/config.yml
MyScheduledRule:
    Type: AWS::Events::Rule
    Properties:
    Description: My scheduled rule
    ScheduleExpression: rate(3 minutes)
    State: ENABLED
    Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
        Id: MyLambdaTarget
```
```
```

#### Server framework

If using AWS infrastructure, you can set up a dedicated EC2 resource running a server that polls
the AGG API every “x” minutes or so. This can be a virtual machine (VM) if running an on-premise
data center.

### OTEL Collector

Next, run an OTEL Collector/Sidecar using the configuration of three components:

1. **Receiver**: A receiver, which can be push- or pull-based, is how data gets into the OTEL Collector.
   An [OTLP receiver](https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md)
   is used, which can receive trace export calls via HTTP/JSON. The AGG response is compatible with
   the accepted format for this receiver to work.
2. **Processors**: Processors are run on data between being received and exported. While processors
   are optional, these are some of the
   [recommended ones](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor#recommended-processors).
3. **Exporters**: An exporter, which can be push- or pull-based, is how you send data to one or more
   backends or destinations. All supported exporters can be found
   [here](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

When setting up the service, you can use either a **serverless framework** or **server framework**.

#### Serverless framework

If using AWS infrastructure, you can leverage the OTEL lambda layer. You can also use a similar
configuration for GCP or Microsoft Azure infrastructure.

A sample configuration should look like the following:

```
```
1
2
```



```
```
Resources:
OTelLambdaLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
    LayerName: OTelLambdaLayer
    Description: My OTEL Lambda layer
    Content:
        S3Bucket: my-layer-bucket
        S3Key: my-layer-package.zip
    CompatibleRuntimes:
        - nodejs14.x
MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
    FunctionName: MyLambdaFunction
    Runtime: nodejs14.x
    Handler: index.handler
    Code:
        S3Bucket: my-function-bucket
        S3Key: my-function-package.zip
    Layers:
        - !Ref OTelLambdaLayer
    Environment:
        Variables:
        OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/config.yml
MyScheduledRule:
    Type: AWS::Events::Rule
    Properties:
    Description: My scheduled rule
    ScheduleExpression: rate(3 minutes)
    State: ENABLED
    Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
        Id: MyLambdaTarget
```
```
```

#### Server framework

We recommend you run the OTEL Collector as a sidecar docker container on the same VM/EC2 server
responsible for cron scheduling.

To set up a server framework:

1. Create a sample `otel-collector-config.yaml` file in the repository as needed. The config file
   should look similar to this (we're using **SignalFX** as an example third-party monitoring tool here):

   ```
   ```
   1
   2
   ```



   ```
   receivers:
     otlp:
       protocols:
         http:
       
   exporters:
     signalfx:
       # Access token to send data to SignalFx.
       access_token: <access_token>
       # SignalFx realm where the data will be received.
       realm: us1
       # Timeout for the send operations.
       timeout: 30s  

   processors:
     batch:

   service:
     pipelines:
       metrics:
         receivers: [otlp]
         processors: [batch]
         exporters: [signalfx]
   ```
   ```
2. Create a Docker image with the open source OTEL collector
   [docker image](https://github.com/open-telemetry/opentelemetry-collector-contrib)
   available using: `docker build . -t otel-sidecar:v1`

   ```
   ```
   1
   2
   ```



   ```
   FROM otel/opentelemetry-collector-contrib:latest

   # Copy the collector configuration file into the container
   COPY otel-collector-config.yaml /etc/otel-collector-config.yaml

   # Start the collector with the specified configuration file
   CMD ["--config=/etc/otel-collector-config.yaml"]
   ```
   ```
3. Run the above Docker image: `docker run -p 4318:4318 otel-sidecar:v1`

   This will spin up the OTEL sidecar at `http://localhost:4318`.
4. Make an **HTTP POST** request with the response of the above AGG API endpoint, for example,
   `response.data.ecosystem.forgeMetrics.appMetrics`, to the sidecar running at path
   `http://localhost:4318/v1/metrics` on the same server.

   ```
   ```
   1
   2
   ```



   ```
   curl --location --request POST 'localhost:4318/v1/metrics' \
   --header 'Content-Type: application/json' \
   --data-raw '<response.data.ecosystem.forgeMetrics.appMetrics>'
   ```
   ```

App metrics should now be visible in your configured monitoring tool.

## Export API metrics

The following metrics are available for all `function` invocations making either
[Fetch API](/platform/forge/runtime-reference/fetch-api/),
[Async events API](/platform/forge/runtime-reference/async-events-api/),
and [Web trigger API](/platform/forge/runtime-reference/web-trigger-api/),
or [hosted storage API](/platform/forge/runtime-reference/storage-api/) HTTP requests
via the [App metrics API](/platform/forge/export-app-metrics/#query-the-app-metrics-api):

* **API request count**: The total number of HTTP requests, grouped by status codes, such as `2xx`,
  `3xx`, `4xx`, and `5xx`.
* **API request latency**: The round trip time it takes for a HTTP request triggered within
  a Forge function.

This doesn’t include code executing in a Custom UI iframe. However, this includes functions
invoked by `@forge/bridge`.

The following tags and dimensions are available with API metrics when using the App metrics API:

1. `remote`: Useful to bifurcate between Atlassian app, external, and GraphQL HTTP requests. This field
   can have one of the following values: `jira`, `confluence`, `bitbucket`, `egress`, or `stargate`.
2. `status`: Represents the HTTP status code received for an API call. This is only available
   for `API request count` metric.
3. `url`: Represents the path of the HTTP request. This field can have one of the following values,
   depending on the type of API call:

   * For non-Atlassian HTTP requests, `url` field will be captured as hostname.
     For example: `api.slack.com` , `api.google.com`
   * For Atlassian app HTTP requests, `url` field will have the templatized path, as such:
     `/rest/api/2/field/{fieldKey}/option` , `/repositories/{workspace}/{repo_slug}/commits`,
     `/rest/api/user/watch/content/{contentId}`
   * For Storage, GraphQL, and Async HTTP requests, the `url` field can have values as
     `/forge/entities/graphql`, `/graphql`,
     `/webhook/queue/publish/{cloudId}/{environmentId}/{appId}/{appVersion}`, and more.
