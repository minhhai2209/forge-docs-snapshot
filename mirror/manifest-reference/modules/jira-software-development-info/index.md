# Jira Software Development Information Provider

The `devops:developmentInfoProvider` module allows Forge apps to send development information to Jira and associate it with an issue.

Supplied development information will be presented in the [development panel](https://confluence.atlassian.com/jirasoftwarecloud/viewing-the-development-information-for-an-issue-777002795.html) of the issue it is associated with.

Development information is written and deleted via the [Jira Software REST API](https://developer.atlassian.com/cloud/jira/software/rest/) which can be accessed by Forge apps using the [requestJira](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestjira/) function.

When a user uninstalls an app, all the data that the app sent to Jira is deleted immediately. If the app is reinstalled, this data won't be added back unless the app resends historical information to Jira.

## Example

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
modules:
  devops:developmentInfoProvider:
    - key: my-development-info-provider
      name:
        value: My Development Info Provider
      homeUrl: https://www.my-development-info-provider.com
      logoUrl: https://www.my-development-info-provider.com/logo.svg
      documentationUrl: https://www.my-development-info-provider.com/help
      actions:
        createBranch:
          urlTemplate: https://www.my-development-info-provider/branches/create?issueKey={issue.key}&issueSummary={issue.summary}
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| key | string | Yes | A key to identify this module. |
| name | object | Yes | A human readable name. |
| name.value | string | Yes | *Min length:* 1  *Max length:* 255 |
| homeUrl | string | Yes | URL to the provider's homepage.  *Min length:* 1  *Max length:* 255  *Regex:* `^(http|https):\/\/.*$` |
| logoUrl | string | No | The logo for the provider, will be displayed in an area 16 by 16 pixels.  *Min length:* 1  *Max length:* 255  *Regex:* `^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\\\\?([^#]*))?(#(.*))?` |
| documentationUrl | string | No | Optional URL to documentation about the provider's Jira integration.  *Min length:* 1  *Max length:* 255  *Regex:* `^(http|https):\/\/.*$` |
| actions | Actions | No | Development actions that can be performed by Jira users. Each action is optional (unless indicated otherwise). The absence of an action indicates that the action is not supported by the provider. |

### Actions

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| createBranch | Action | No | Action for creating a new branch.  The given URL will be used on the [Jira issue development panel](https://confluence.atlassian.com/jirasoftwarecloud/viewing-the-development-information-for-an-issue-777002795.html). The "Create branch" button will redirect the user to the URL. |

### Action

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| urlTemplate | string | Yes | Defines the URL template that is used when an action is invoked.  The following context parameters are supported: `{issue.key}`, `{issue.summary}`  *Min length:* 1  *Max length:* 255  *Regex:* `^(http|https):\/\/.*$` |
