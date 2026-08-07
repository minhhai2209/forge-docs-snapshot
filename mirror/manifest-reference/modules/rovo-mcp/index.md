# Rovo MCP (EAP)

Rovo MCP is available through Forge's Early Access Program (EAP). The EAP allows all Forge developers for testing and feedback. APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production use.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

The `rovo:mcp` module lets you expose actions as tools in Rovo Studio for custom agents. An app can have at most one `rovo:mcp` module.

## Data access

App-based tools can access only the data in the workspace where the app is installed. For example, a Confluence page at yourtenant.atlassian.net that describes your team's CI/CD process is not automatically accessible to an app installed in Jira at yourtenant.atlassian.net.

To enable your tools to access data from multiple Atlassian apps, configure your app to support multiple Atlassian apps. See [App compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility--preview-).

When multiple products have different versions of the same app installed, the exposed tools reflect those from the latest app version.

## Manifest structure

```
```
1
2
```



```
modules {}
└─ rovo:mcp []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ tools [] [Mandatory]
   │  └─ action (string)

resources []
└─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```
```

In this structure:

* The `rovo:mcp` array includes properties such as `key`, `name`, and `tools`.
* The `resources` array includes properties `key` and `path`.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The name of your MCP server. Must not exceed 30 characters. |
| `tools` | `string[]` | Yes | A list of action keys to expose as tools. Each referenced action must have a unique key under 64 characters, and there can be at most 20 actions. |

## Manifest example

Here is an example manifest file that exposes tools for a timesheet app:

```
```
1
2
```



```
modules:
  rovo:mcp:
    - key: timesheet-mcp
      name: "Timesheet MCP"
      tools:
        - fetch-timesheet-by-date
        - update-timesheet
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
    - key: update-timesheet
      name: Update timesheet
      function: updateTimesheet
      actionVerb: UPDATE
      description: |
        Update a user's timesheet entry for a specific date
      inputs:
        timesheetDate:
          title: Timesheet Date
          type: string
          required: true
          description: "The date of the timesheet entry to update"
        hoursWorked:
          title: Hours Worked
          type: number
          required: true
          description: "The number of hours worked to record for the given date"
        projectKey:
          title: Project Key
          type: string
          required: false
          description: "The project or task the hours are attributed to"
        notes:
          title: Notes
          type: string
          required: false
          description: "Optional notes or comments about the timesheet entry"
  function:
    - key: getTimesheetByDate
      handler: index.getTimesheetByDate
    - key: updateTimesheet
      handler: index.updateTimesheet
```
```

## Tutorials

Hands-on, step-by-step guides for building with the `rovo:mcp` module:

The `rovo:mcp` module integrates with other manifest configurations to expose tools in Rovo Studio.
