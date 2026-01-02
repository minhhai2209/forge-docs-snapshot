# Jira UI modifications

The `jira:uiModifications` module is shared between Jira and Jira Service Management. It allows you to change the look and behavior of:

* **Jira:** *Jira global issue create*, *Jira issue view* (Preview), and *Jira issue transition* (Preview)(the [new experience](https://community.atlassian.com/t5/Jira-articles/Now-GA-try-the-new-issue-transition-experience-in-Jira/ba-p/2734436))
* **Jira Service Management:** *Jira Service Management request create portal* (Preview)

This page documents how `jira:uiModifications` works for Jira. The module itself is the same but for Jira Service Management-specific views, see [Jira Service Management UI modifications](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/).

The module is designed to be used in conjunction with the [UI modifications (apps) REST API](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).

## Get started

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
modules {}
└─ jira:uiModifications []
   ├─ key (string) [Mandatory]
   ├─ title (string | i18n) [Mandatory]
   └─ resource (string) [Mandatory]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `resource` | `string` | Required if using [Custom UI](/platform/forge/custom-ui/) or the latest version of [UI Kit.](/platform/forge/ui-kit/) | A reference to the static `resources` entry that your context menu app wants to display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `title` | `string` or `i18n object` | Yes | A title for the module.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

UIM Forge modules can retrieve the current `project` and `issueType` using the [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI and UI Kit.

Global issue create context shape

Issue view context shape

Issue transition context shape

```
```
1
2
```



```
{
  extension: {
    type: 'jira:uiModifications',
    project: {
      id: string,
      key: string,
      type: string,
    },
    issueType: {
      id: string,
      name: string,
    },
    viewType: 'GIC'
  }
}
```
```

## Example

```
```
1
2
```



```
import { view } from '@forge/bridge';
import { uiModificationsApi } from '@forge/jira-bridge';

uiModificationsApi.onInit(async ({ api, uiModifications }) => {
  const { getFieldById } = api;
  const context = await view.getContext();

  const { project, issueType } = context.extension;
  
  uiModifications.forEach(({ data: customDataConfiguredUsingRestApi }) => {
    // ...
  });
}, ({ uiModifications }) => [
  // ...
])
```
```

## Scopes

UI modifications expose customer data to the app that provides them. Therefore, you must declare either classic (recommended) or granular scopes in your manifest. Note that you always have to declare all scopes from your chosen group.

Classic scopes

Granular scopes

```
```
1
2
```



```
permissions:
  scopes:
    - 'read:jira-user'
    - 'read:jira-work'
    - 'manage:jira-configuration'
    - 'write:jira-work'
    - 'manage:jira-project'
```
```

| Scope | Data exposed | Field | Method |  |  |
| --- | --- | --- | --- | --- | --- |
| `read:jira-user` | User timezone and account ID | n/a | `view.getContext` |  |  |
| User display name, account ID, and avatar | Assignee | `getValue` |  |  |
| `read:jira-work` | Project ID, key, and type; issue type ID and issue type name of the issue being created using the GIC form or presented on the Issue view | n/a | `view.getContext` |  |  |
| Issue data of the issue being created using the GIC form or presented on the Issue view | All supported fields | `getValue` |  |  |
| Field name | All supported fields | `getName` |  |  |
| Field visibility | All supported fields | `isVisible` |  |  |
| `manage:jira-configuration` | Field description | All supported fields | `getDescription` |  |  |
| User locale | n/a | `view.getContext` |  |  |
| Atlassian app license status | n/a | `view.getContext` |  |  |
| The following values can be modified:  * name * description * visibility | All supported fields | * `setName` * `setDescription` * `setVisible` |  |  |
| `write:jira-work` | Default field value can be modified | All supported fields | `setValue` |  |  |
| `manage:jira-project` | Screen tabs can be modified | All visible screen tabs |  |  |  |

## Required user permissions

In case a required permission isn’t assigned, the user will see the following error:

```
```
1
2
```



```
We couldn't load the UI modifications configuration for this form
```
```

## View-specific requirements and limitations

Each supported view type has its own known limitations:

Jira global issue create

Jira issue view (Preview)

Jira issue transition (Preview)

| Category | Details |
| --- | --- |
| **Supported project types** |  |
| **Supported entry points** | * Global **Create** button in the top navigation bar * `c` keyboard shortcut * Issue view **Add a child issue** and **Create subtask** buttons\* * Forge app with Custom UI using `CreateIssueModal` from `@forge/jira-bridge`   *\*The Global issue create modal with UIM will only open from **Add a child issue** and **Create subtask** if the summary and at least one other field is set as mandatory for the issue type.* |
| **Known limitations** | * **Flash of unmodified fields** – UI modifications are loaded after the *Create issue dialog* has finished loading. The user is informed about the loading state by a small spinner icon next to the label, which indicates that a UIM is running. Users can still see the fields before the modifications are applied. For example, a field will be visible for a moment before being hidden, or the default field description will be visible before it changes. * **Show fields and Find your field** – Fields can be hidden by individual users using **Show fields**. Data for these hidden fields is not sent to the UIM app. **Find your field** does not know about fields being hidden by a UIM app using `setVisible`. Users may not be able to discover why a field is not visible to them.        Global issue create > show fields |

## Other known limitations

### Multiple UIM apps

If you install and configure multiple UIM apps to run for a given combination of project, issue type, and view type, up to 5 apps can apply changes simultaneously. If more than 5 apps are configured, changes from the remaining apps will be disregarded. Apps apply changes asynchronously, so the order of application is random.

There may be conflicts when multiple apps attempt to modify the same field using the same [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) method. In such cases, app developers will receive conflict errors via the [onError](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#error-handling) handler, and users will see corresponding notifications:

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/multi-app-conflict-notification.png?_v=1.5800.1741)

If the conflict happens, the changes applied by the app which finished running last will override changes from other apps.

### Image previews unavailable until issue is created

The [Atlassian Document Format (ADF)](/platform/forge/ui-kit/components/adf-renderer/) supports rich content
when using the UIM to add media content (like images) to Jira description, text area, or rich text custom fields.

However, when adding an image through the UIM during issue creation (for example, throught the GIC modal) the image
preview might display a `Preview unavailable` message. This is because the necessary permissions to display the image
aren't available yet; they'll be available after the issue is created and/or the page is refreshed.
