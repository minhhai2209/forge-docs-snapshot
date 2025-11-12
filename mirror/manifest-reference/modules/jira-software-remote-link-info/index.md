# Jira Software Remote Link Information Provider

The `devops:remoteLinkInfoProvider` module allows Forge apps to send remote link information to Jira and associate it with an issue.

Supplied remote link information will be presented in the [development panel](https://confluence.atlassian.com/jirasoftwarecloud/viewing-the-development-information-for-an-issue-777002795.html) of the issue it is associated with.

Remote link information is written and deleted via the [Jira Software REST API](https://developer.atlassian.com/cloud/jira/software/rest/) which can be accessed by Forge apps using the [requestJira](https://developer.atlassian.com/platform/forge/apis-reference/fetch-api-product.requestjira/) function.

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
modules:
  devops:remoteLinkInfoProvider:
    - key: my-remote-link-info-provider
      name:
        value: My Remote Link Info Provider
      homeUrl: https://www.my-remote-link-info.com
      logoUrl: https://www.my-remote-link-info.com/logo.svg
      documentationUrl: https://www.my-remote-link-info.com/help
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
