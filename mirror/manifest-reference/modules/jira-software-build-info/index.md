# Jira Software Build Information Provider

The `devops:buildInfoProvider` module allows Forge apps to send build information to Jira and associate it with an issue.

Supplied build information will be presented in the [development panel](https://confluence.atlassian.com/jirasoftwarecloud/viewing-the-development-information-for-an-issue-777002795.html) of the issue it is associated with.

Build information is written and deleted via the [Jira Software REST API](https://developer.atlassian.com/cloud/jira/software/rest/) which can be accessed by Forge apps using the [requestJira](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestjira/) function.

When a user uninstalls an app, all the data that the app sent to Jira is deleted immediately. If the app is reinstalled, this data won't be added back unless the app resends historical information to Jira.

## Example

```
1modules:
2  devops:buildInfoProvider:
3    - key: my-build-info-provider
4      name:
5        value: My Build Info Provider
6      homeUrl: https://www.my-build-info.com
7      logoUrl: https://www.my-build-info.com/logo.svg
8      documentationUrl: https://www.my-build-info.com/help
9
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
