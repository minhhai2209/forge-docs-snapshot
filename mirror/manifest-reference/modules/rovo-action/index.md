# Action

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

An `action` module lets a Rovo Agent perform a specific task, like calling an API or running predefined code. Actions are implemented as a Forge function and have a plain text name and description, so Rovo Agent can understand what it does and decide when to invoke it.

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
13
14
15
16
modules {}
└─ action []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ function (string) [Mandatory]
   ├─ actionVerb (string) [Mandatory]
   ├─ description (string) [Mandatory]
   ├─ inputs {} [Mandatory]
   │  └─ inputName {}
   │     ├─ title (string) [Mandatory]
   │     ├─ type (string) [Mandatory]
   │     ├─ required (boolean) [Mandatory]
   │     └─ description (string) [Optional]
function []
└─ key (string) [Mandatory]
└─ handler (string) [Mandatory]
```

In this structure:

* The action array includes generic properties such as `key`, `name`, `function`, `actionVerb`, `description`, and `inputs`.
* The inputs object contains input fields, represented generically as `inputName`, with properties `title`, `type`, `required`, and `description`.
* The function array includes properties `key` and `handler`.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the action, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | A human-friendly name for the action which will be displayed in the user interface. |
| `function` or `endpoint` | `string` | Yes | A reference to the hosted Forge function that defines the behavior of this action. If you are using Forge Remote then you can use an endpoint instead. |
| `actionVerb` | `string` | Yes | The verb that best represents your action: `GET`, `CREATE`, `UPDATE`, `DELETE`, `TRIGGER`. [Agents](/platform/forge/manifest-reference/modules/rovo-agent) triggered by automation rules will not invoke actions with actionVerb `CREATE` , `UPDATE` , `DELETE` , and `TRIGGER` . |
| `description` | `string` | Yes | The description that the Agent will use to decide when to invoke this action. |
| `inputs` | [inputs](/platform/forge/manifest-reference/modules/rovo-action/#inputs) | Yes | The inputs for this action. |

The Rovo Agent action module can only handle data up to 5 MB due to a dependency size limit,
which restricts the amount of data that can be processed or fetched. You need to manage data within this
constraint by optimizing or segmenting larger datasets.

### Inputs

Each input must have a unique user-defined name, referred to as `inputName`, which acts as a parent container for the properties listed below.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | `string` | Yes | The name of the input. |
| `type` | `string` | Yes | The data type of the input: `string`, `integer`, `number`, or `boolean`. |
| `required` | `string` | Yes | True if the input is required. |
| `description` | `string` | Yes | A description of what this particular input is intended for. Example: 'ID of the Issue that will be updated as a result of this action' |

### Example using a hosted Forge function:

```
```
1
2
```



```
modules:
  action:
    - key: fetch-timesheet-by-date
      name: Fetch timesheet by date
      function: getTimesheetByDate
      actionVerb: GET
      description: |
        Retrieve a user's timesheet based on a date
      inputs:
        timesheetDate:
          title: Timesheet Date
          type: string
          required: true
          description: "The date that the user wants a timesheet for"
  function:
    - key: getTimesheetByDate
      handler: index.getTimesheetByDate
```
```

### Example using a Forge Remote endpoint

```
```
1
2
```



```
modules:
  action:
    - key: log-time
      endpoint: logTime
      name: Log time
      actionVerb: CREATE
      description: |
        Log some time for the user against a Jira issue
      inputs:
        issueKey:
          title: Jira Issue Key
          type: string
          required: true
          description: "The jira issue to log time against"
        time:
          title: Time to log in minutes
          type: integer
          required: true
          description: "The number of minutes to log"
  endpoint:
  - key: logTime
    remote: timesheetapp
      route:
        path: log-time
      auth:
        appUserToken:
          enabled: true
        appSystemToken:
          enabled: false
remote: 
  - key: timesheetapp
    baseUrl: "https://backend.timesheetapp.com"
```
```

## Writing your action

The business logic for your action is in the referenced Forge function (or remote endpoint if you are using Forge Remote).

The `payload` and `context` are passed into the function as arguments. Please refer to [Function Arguments](/platform/forge/function-reference/arguments/#function-arguments) for more details.

The payload will include the inputs defined for the action. In certain contexts (e.g. viewing a Jira issue, Confluence page) the payload will also include a context object with relevant Atlassian app identifiers (e.g. `issueKey`, `contentId`).

The `context` contains the user's `accountId`.

### Jira issue example

```
```
1
2
```



```
"payload": {
    "input1ToYourAction": 1241,
    "input2ToYourAction": 12412,
    "context": {
        "cloudId":"7607d59e-650b-4c16-adcf-c19d17c915ac",
        "moduleKey":"sum-2-numbers-new-action",
        "jira": {
          "url": "https://mysite.atlassian.com/browse/FAA-1",
          "resourceType": "issue",
          "issueKey": 1,
          "issueId": 123,
          "issueType": "story",
          "issueTypeId": 1234,
          "projectKey": "FAA",
          "projectId": 5678
      }
    }
}
```
```

### Confluence page example

```
```
1
2
```



```
"payload": {
    "input1ToYourAction": 1241,
    "input2ToYourAction": 12412,
    "context": {
        "cloudId":"7607d59e-650b-4c16-adcf-c19d17c915ac",
        "moduleKey":"sum-2-numbers-new-acion",
        "confluence" : {
            "url": "https://mysite.atlassian.com/wiki/spaces/~65536301eb7512314748ebb489aba9d526b0f8/blog/2024/06/27/44662787/Holiday+in+Japan",
            "resourceType": "blog",
            "contentId": "44662787",
            "spaceKey": "~65536301eb7512314748ebb489aba9d526b0f8",
            "spaceId": "2064386"
        }
    }
}
```
```

Understanding input and context

* **Input**: The LMM extracts inputs from the Atlassian app context and user interactions (e.g., chat prompts). This makes it more flexible but also leaves it subject to hallucination.

  Your app should never rely on values passed as inputs to perform critical checks like authorization.
  If you need a user’s `accountId` read it from the `context`.
* **Context**: For certain contexts (e.g., issue view, page view), the Atlassian app context will be included as part of the payload. This is done deterministically in the same way the Atlassian app context is passed to other Forge modules.

Providing both for the early access program is somewhat of an experiment to see what is most useful, or how they might be used in combination. For example, you might run a basic regex on an `issueKey` passed through the inputs, and if it isn’t valid, then fall back to the value in the context if present. We’re keen to get your feedback on how this works in practice. Please provide your input on the [CDAC](https://community.developer.atlassian.com/c/rovo/138) or Slack channels.

## Returning data

Your function can return any string or JSON object, which the Agent will interpret and transform into a natural-language response to the customer.

### Example function

The `logTime` function from the previous example might look like this:

```
```
1
2
```



```
export function logTime (payload, context) {
    console.log(`payload: ${JSON.stringify(payload)}`);
    console.log(`payload: ${JSON.stringify(context)}`);
    
    // Extract necessary information
    const { issueKey, minutes } = payload;
    
    // Code to actually log time to the timesheet
    
    // Construct the success message
    const result = `${minutes} minutes added to issue ${issueKey}`;
    return result;
}
```
```

## Customer created agents

Actions in your Forge app can be made available to customer-built agents by adding the `read:chat:rovo` scope to the permissions in your manifest. This enables agents created by customers to utilize these actions.

```
```
1
2
```



```
permissions:
  scopes:
    - read:chat:rovo
```
```

The additional scope is needed because customer-built agents may access data that your app can't otherwise reach. This data can be provided as input to your action through a Rovo chat.

![Example of adding a Forge action](https://dac-static.atlassian.com/platform/forge/images/rovo/customer-add-action.png?_v=1.5800.1800)
