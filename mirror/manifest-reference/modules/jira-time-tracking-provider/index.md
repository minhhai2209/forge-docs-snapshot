# Time tracking provider (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:timeTrackingProvider` module allows an app to replace Jira's native time tracking components with ones defined by the app.
After installing this module, the new time tracking provider will be available as an option on [Jira's time tracking administration page](https://support.atlassian.com/jira-cloud-administration/docs/configure-time-tracking/#Change-the-time-tracking-provider).

When an app is selected as the "time tracking provider" for Jira, the following native Jira time tracking UI elements will be hidden and
the app will be able to provide standard modules to implement custom versions of these features:

| Native component | Forge module |
| --- | --- |
| `Log work` button | `jira:issueAction` |
| `Work log` issue tab panel | `jira:issueActivity` |

Additionally, the native "Log work" action via the time tracking issue field will be disabled. Instead, the field displays and allows entering the time remaining.

## Display conditions

Two conditions related to time tracking providers are available:

| Display condition | Description |
| --- | --- |
| `jiraTimeTrackingProviderEnabled` | The condition is evaluated to `true` if the currently selected time tracking provider is Jira's native time tracking implementation. |
| `timeTrackingProviderEnabled` | The condition is evaluated to `true` if the currently selected time tracking provider matches the one defined in the condition parameters. |

Refer to the [display conditions](/platform/forge/manifest-reference/display-conditions/jira/#time-tracking-conditions) documentation for more information.

## Administration page

An app may provide an administration page that will be shown to the user if that app is selected as the active time tracking provider.
The page should be defined with an [Admin Page](/platform/forge/manifest-reference/modules/jira-admin-page/) module in the app's manifest.
It will be accessible from the System tab on the Administration page in Jira.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The name of the time tracking provider. |
| `adminPage` | `string` | No | If provided, this needs to reference an existing `adminPage` module defined within the app's manifest.  Jira will link the referenced `adminPage` module as the configuration page of this Time tracking provider module. |

## Example

#### Manifest

```
```
1
2
```



```
modules:
  jira:timeTrackingProvider:
    - key: time-tracking-provider
      name: Forge time tracking provider
      adminPage: admin-page-key
  jira:adminPage:
    - key: admin-page-key
      function: main-configure-page
      title: Configure page example
      useAsConfig: true
```
```
