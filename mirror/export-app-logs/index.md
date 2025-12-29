# Export app logs

App logs, which can be viewed in the [developer console](/console/myapps), help in tracking down
and troubleshooting issues that app users may be experiencing. Forge app owners and
[app contributors](/platform/forge/manage-app-contributors/) can view app logs.

You can also use the **App logs API** to export app logs to several observability tools,
including [Splunk](https://www.splunk.com/), [Datadog](https://www.datadoghq.com/), [Dynatrace](https://www.dynatrace.com/), [New Relic](https://newrelic.com/), and more.
Such tools offer advanced capabilities for analyzing and managing logs.

The App logs API is a REST API that provides logs in
[OTLP log data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) format, which is the format
used in the
[OpenTelemetry framework](/platform/forge/app-metrics-in-third-party-tools/#opentelemetry-framework).

Exporting app logs involves the following steps:

1. [Authenticate with the Atlassian Gateway](#authenticate-with-the-atlassian-gateway/)
2. [Query the App logs API](#query-the-app-logs-api)
3. [Set up your infrastructure](#set-up-your-infrastructure)

Check out
[this repository](https://bitbucket.org/atlassian/forge-observability-consumption-patterns/src/main/logs/)
for example code and resources for configuring observability tools
to consume Forge app logs.

## Authenticate with the Atlassian Gateway

You must first authenticate with the Atlassian Gateway to consume the API and export app logs
to a tool of your choice. For this you need to generate the API tokens to access the App logs API.

Only the owner of the Forge app or an app contributor that has access to logs can make the request.
It is recommended to use a non human account (bot account), instead of an admin account, which has access to the app logs.

To generate the API tokens:

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Select **Create API token**.
3. Enter a label to describe your API token. For example, *export-logs-api-token*.
4. Select **Create**.
5. Select **Copy to clipboard** and close the dialog.
6. Use this token as a Basic Authorization when making request to the API.

## Query the App logs API

You can use the below API Spec and try the App logs API with your Forge app.

### API

The API return logs in the OTLP format, which is the format used in the OpenTelemetry
framework.

#### Endpoint URL

```
```
1
2
```



```
https://api.atlassian.com/v1/app/logs/${appId}?environmentId=${envId}&startDate=${startDate}&endDate=${endDate}&level={level}&message={message}&installationContext={installationContext}&cursor=${cursor}
```
```

#### HTTP method

#### Path parameters

```
```
1
2
```



```
- `appId`: string, Required, Id of the forge App.
```
```

To get the app ID:

1. In the [developer console](/console/myapps/), navigate to your Forge app.
2. Go to the **Overview** page.
3. Find the **app ID** in the App details section.

#### Query parameters

| Name | Required | Description |
| --- | --- | --- |
| `environmentId` | Yes | The environment ID of the Forge app. |
| `startDate` | Yes | Start date and time for the logs (in UTC). This field uses the ISO format `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'` |
| `endDate` | Yes | End date and time for the logs in UTC. This field uses the ISO format `yyyy-MM-dd'T'HH:mm:ss.SSS'Z'` |
| `level` | No | The log level (TRACE, DEBUG, INFO, WARN, ERROR, FATAL) |
| `message` | No | If provided, only logs containing this text will be displayed. |
| `installationContext` | No | The Site Ids for which to fetch logs, with a maximum of 50 allowed. |
| `cursor` | No | The marker retrieved from the previous request, to fetch the next set of logs. |

To get the environment ID:

1. In the [developer console](/console/myapps/), navigate to your Forge app.
2. Go to the **Environments** page.
3. Find the **environment ID** in the Environment ID column.

To get the Site ID:

1. Open the [developer console](/console/myapps/) and navigate to your Forge app.
2. Select the **Installations** page from the menu.
3. Hover over the site in the "Site & ID" column and click the "Copy site ID" button.

#### Responses

```
```
1
2
```



```
- `200 OK`: Successful response. Returns paginated logs.
- `400 Bad Request`: Request failed with status code 400.
- `401 Unauthorized`: Unauthorized.
- `404 Not Found`: Request failed with status code 404.
- `429 Too many requests`: Request has been rate limited.
- `500 Internal Server Error`: Request failed with status code 500.
```
```

* The maximum time difference allowed between `startDate` and `endDate` is 1 hour. This means the
  `endDate` must not exceed 1 hour after the `startDate`.
* Both the `startDate` and `endDate` must be within the last 14 days from the current date and time.
  This means any date-time specified that is more than 14 days in the past will not be accepted.
* We recommend fetching data periodically, for example, every three or five minutes. A rate limit of
  30 calls per minute per `appId` is enforced.
* The API returns logs of approximately 3500 sites on which the app is installed.

#### Sample API request to retrieve app logs

```
```
1
2
```



```
// Please replace `email`, `appId`, `envId` and `<api_token>` with your actual values.
// This code will fetch data for the last 5 minutes and
// if the response contains a cursor, it will do a subsequent fetch with the new cursor.
// This will continue until no more cursors are returned.

// Define necessary variables
const email = "<email>";
const appId = "<appId>";
const envId = "<envId>";
const searchMsg = "example_search_text";
const siteId1 = "<site_id_1>"; // for eg: ari:cloud:confluence::site/089a1455-4ea0-122a-b70c-5b17360f047d
const siteId2 = "<site_id_2>"; // for eg: ari:cloud:jira::site/4eecb4e0-22cc-4e18-bad1-b58a154be343
const api_token = "<api_token>";

// Get current date/time and subtract 5 minutes for startDate
const now = new Date();
const endDate = new Date(now.getTime() - 1 * 60000); // 1 minute ago
const startDate = new Date(now.getTime() - 6 * 60000); // 6 minutes ago
let cursor = null;

// Function to fetch logs
const fetchLogs = async (startDate, endDate, cursor) => {
  try {
    const url = `https://api.atlassian.com/v1/app/logs/${appId}` +
                `?environmentId=${envId}` +
                `&startDate=${startDate.toISOString()}` +
                `&endDate=${endDate.toISOString()}` +
                `&level=INFO&level=ERROR` +
                `&message=${searchMsg}` +
                `&installationContext=${siteId1}&installationContext=${siteId2}` +
                `${cursor ? `&cursor=${cursor}` : ""}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Basic ${Buffer.from(`${email}:${api_token}`).toString("base64")}`,
        Accept: "application/json",
      },
    });

    console.log(`Response: ${response.status} ${response.statusText}`);

    const data = await response.json();
    
    // export your logs to the external monitoring tool
    console.log(data);


    // if data.cursor exists, fetch next data
    if (data.cursor) {
      await fetchLogs(startDate, endDate, data.cursor);
    }
  } catch (err) {
    console.error(err);
  }
};

// Call fetchLogs function
fetchLogs(startDate, endDate, cursor);
```
```

#### Sample API response for a successful request

```
```
1
2
```



```
{
    "appLogs": [
        {
            "timeUnixNano": "1707821444939000000",
            "severityNumber": 30,
            "severityText": "INFO",
            "body": {
                "stringValue": "This is simple log message"
            },
            "traceId": "3e1c350520934cbeb20b7d54d56bee2c",
            "spanId": "6c7f6ad7436700c1",
            "attributes": [
                {
                    "key": "appId",
                    "value": {
                        "stringValue": "yibeb59-d217-58d3-a3a7-0a888b3bc5ef"
                    }
                },
                {
                    "key": "environmentId",
                    "value": {
                        "stringValue": "0129990-850f-1a19-a013-12cdefe2fa19"
                    }
                },
                {
                    "key": "invocationId",
                    "value": {
                        "stringValue": "e1f88a1e-1b59-1511-adfb-e080972d5d89"
                    }
                },
                {
                    "key": "installationContext",
                    "value": {
                        "stringValue": "ari:cloud:confluence::site/089a1455-4ea0-122a-b70c-5b17360f047d"
                    }
                },
                {
                    "key": "appVersion",
                    "value": {
                        "stringValue": "1.206.0"
                    }
                },
                {
                    "key": "functionKey",
                    "value": {
                        "stringValue": "updateStatusTitle"
                    }
                },
                {
                    "key": "moduleType",
                    "value": {
                        "stringValue": "core:function"
                    }
                },
                {
                    "key": "arguments",
                    "value": {
                        "stringValue": "[{\"randomData\":0.6341547823420093}]"
                    }
                },
                {
                    "key": "licenseState",
                    "value": {
                        "stringValue": "Active"
                    }
                },
                {
                    "key": "edition",
                    "value": {
                        "stringValue": "Standard"
                    }
                }
            ]
        }
    ],
    "cursor": "someString"
}
```
```

## Set up your infrastructure

To use the App logs API and ingest logs into observability tools, we recommend fetching logs in
OTLP format from the API, and having the following components in your infrastructure:

![Partner Server View](https://dac-static.atlassian.com/platform/forge/images/partner-server-arch-logs.svg?_v=1.5800.1739)

### CronJob service

The CronJob service periodically polls the exposed REST endpoint for the required logs.
The API returns logs in OTLP format as a response. Logs are then pushed as is to the OTEL Sidecar,
which is running alongside this cron service.

When setting up the service, you can use either a **serverless framework** or **server framework**.

#### Serverless framework

If using Amazon Web Services (AWS) infrastructure, you can configure a Lambda to be executed
every “x” minutes or so. You can also use a similar configuration for Google Cloud Platform (GCP)
, Microsoft Azure infrastructure or any other cloud provider

A sample Lambda configuration should look like the following:

```
```
1
2
```



```
Resources:
  # IAM Role for Lambda execution
  MyLambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: sts:AssumeRole
      Path: "/"
      Policies:
      - PolicyName: S3AccessPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Effect: Allow
            Action:
            - s3:GetObject
            Resource: arn:aws:s3:::my-s3-bucket/*
          - Effect: Allow
            Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
            Resource: arn:aws:logs:*:*:*
  
  # Lambda Function
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: MyLambdaFunction
      Runtime: nodejs16.x
      Handler: index.handler
      Role: !GetAtt MyLambdaExecutionRole.Arn
      Code:
        S3Bucket: my-s3-bucket
        S3Key: my-function-package.zip
      Layers:
        - !Ref OTelLambdaLayer
      Timeout: 60 # Timeout set to 1 minute
      Environment:
        Variables:
          OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/otel-collector-config.yaml

  # Event Rule for Lambda Invocation
  MyLambdaInvocationRule:
    Type: "AWS::Events::Rule"
    Properties:
      Description: Invoke Lambda every 5 minutes
      ScheduleExpression: "rate(5 minutes)"
      State: ENABLED
      Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
          Id: MyLambdaInvoke

  # Permissions for Lambda Invocation
  PermissionForEventsToInvokeLambda:
    Type: "AWS::Lambda::Permission"
    Properties:
      FunctionName: !GetAtt MyLambdaFunction.Arn
      Action: "lambda:InvokeFunction"
      Principal: events.amazonaws.com
      SourceArn: !GetAtt MyLambdaInvocationRule.Arn
```
```

#### Server framework

If using AWS infrastructure, you can set up a dedicated EC2 resource running a server that polls
the REST API every “x” minutes or so. This can be a virtual machine (VM) if running an on-premise
data center.

### OTEL Collector

Next, run an OTEL Collector/Sidecar using the configuration of three components:

1. **Receiver**: A receiver, which can be push- or pull-based, is how data gets into the OTEL Collector.
   An [OTLP receiver](https://github.com/open-telemetry/opentelemetry-collector/blob/main/receiver/otlpreceiver/README.md)
   is used, which can receive export calls via HTTP/JSON. Logs received in the OTLP format
   are compatible with the accepted format for this receiver to work.
2. **Processors**: Processors are run on data between being received and exported. While processors
   are optional, these are some of the
   [recommended ones](https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor#recommended-processors).
3. **Exporters**: An exporter, which can be push- or pull-based, is how you send data to one or more
   backends or destinations. All supported exporters can be found
   [here](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter).

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
Resources:
  # IAM Role for Lambda execution
  MyLambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: sts:AssumeRole
      Path: "/"
      Policies:
      - PolicyName: S3AccessPolicy
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Effect: Allow
            Action:
            - s3:GetObject
            Resource: arn:aws:s3:::my-s3-bucket/*
          - Effect: Allow
            Action:
            - logs:CreateLogGroup
            - logs:CreateLogStream
            - logs:PutLogEvents
            Resource: arn:aws:logs:*:*:*
  
  # Lambda Layer
  OTelLambdaLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: OTelLambdaLayer
      Description: My OTEL Lambda layer
      Content:
        S3Bucket: my-s3-bucket
        S3Key: my-layer-package.zip
      CompatibleRuntimes:
        - nodejs16.x

  # Lambda Function
  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: MyLambdaFunction
      Runtime: nodejs16.x
      Handler: index.handler
      Role: !GetAtt MyLambdaExecutionRole.Arn
      Code:
        S3Bucket: my-s3-bucket
        S3Key: my-function-package.zip
      Layers:
        - !Ref OTelLambdaLayer
      Timeout: 60 # Timeout set to 1 minute
      Environment:
        Variables:
          OPENTELEMETRY_COLLECTOR_CONFIG_FILE: /var/task/otel-collector-config.yaml

  # Event Rule for Lambda Invocation
  MyLambdaInvocationRule:
    Type: "AWS::Events::Rule"
    Properties:
      Description: Invoke Lambda every 5 minutes
      ScheduleExpression: "rate(5 minutes)"
      State: ENABLED
      Targets:
        - Arn: !GetAtt MyLambdaFunction.Arn
          Id: MyLambdaInvoke

  # Permissions for Lambda Invocation
  PermissionForEventsToInvokeLambda:
    Type: "AWS::Lambda::Permission"
    Properties:
      FunctionName: !GetAtt MyLambdaFunction.Arn
      Action: "lambda:InvokeFunction"
      Principal: events.amazonaws.com
      SourceArn: !GetAtt MyLambdaInvocationRule.Arn
```
```

#### Server framework

We recommend you run the OTEL Collector as a sidecar docker container on the same VM/EC2 server
responsible for cron scheduling.

To set up a server framework:

1. Create a sample `otel-collector-config.yaml` file in the repository as needed. The config file
   should look similar to this (we're using **Datadog** as an example third-party monitoring tool here):

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
     datadog:
       api: 
         key: "<API key>"

   service:
     pipelines:
       logs:
         receivers: [otlp]
         exporters: [datadog]
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
4. Make an **HTTP POST** request with the response of the REST API to the sidecar running at path
   `http://localhost:4318/v1/logs` on the same server.

   You need to create a `json` object here
   using the below format. Add the array of `appLogs` in the `logRecords` field. Refer this [example](https://github.com/open-telemetry/opentelemetry-proto/blob/v1.1.0/examples/logs.json)

   ```
   ```
   1
   2
   ```



   ```
   const logs = {
       resourceLogs: [
           {
               "resource": {
                   "attributes": [
                       {
                           "key": "service.name",
                           "value": {
                               "stringValue": "my.service"
                           }
                       }
                   ]
               },
               "scopeLogs": [
                   {
                       "scope": {
                           "name": "my.library",
                           "version": "1.0.0",
                           "attributes": [
                               {
                                   "key": "my.scope.attribute",
                                   "value": {
                                       "stringValue": "some scope attribute"
                                   }
                               }
                           ]
                       },
                       logRecords: "<Place appLogs received from REST API Call>",
                   },
               ],
           },
       ],
   };
   ```
   ```
5. After creating a `json` object, you can use a **HTTP POST** call to send logs to your tool of choice.

   ```
   ```
   1
   2
   ```



   ```
   curl --location --request POST 'localhost:4318/v1/logs' \
   --header 'Content-Type: application/json' \
   --data <logs>'
   ```
   ```

App logs should now be visible in your configured monitoring tool.
