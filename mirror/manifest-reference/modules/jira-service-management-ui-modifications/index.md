# Jira Service Management UI modifications

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:uiModifications` module is shared between Jira and Jira Service Management. It allows you to change the look and behavior of:

* **Jira:** *Jira global issue create*, *Jira issue view* (Preview), and *Jira issue transition* (Preview) (the [new experience](https://community.atlassian.com/t5/Jira-articles/Now-GA-try-the-new-issue-transition-experience-in-Jira/ba-p/2734436))
* **Jira Service Management:**
  * *Jira Service Management request create portal* (Preview) – the request create form your customers use in the help center or portal.
  * *Jira Service Management agent view* (Preview) – the views your agents use inside a service project. This covers three separate views: *global issue create* (GIC), *issue view*, and *issue transition*.

The agent view shares the same views as Jira, but runs in service projects. Because of this, its extension context also
exposes the request type of the work item, and the set of supported fields differs from the request create portal.
For each agent view, the `viewType` in the extension context tells you which view your app is running in:
`GICAgentView`, `IssueViewAgentView`, or `IssueTransitionAgentView`.

This page documents how `jira:uiModifications` works for Jira Service Management-specific views. The module itself is the same but for Jira, see [Jira UI modifications](/platform/forge/manifest-reference/modules/jira-ui-modifications/).

The module is designed to be used in conjunction with the [UI modifications (apps) REST API](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).

## Get started

## Manifest structure

```
```
1
2
```



```
modules {}
└─ jira:uiModifications []
   ├─ key (string) [Mandatory]
   ├─ title (string | i18n) [Mandatory]
   ├─ resource (string) [Mandatory]
   └─ unlicensedAccess (List<string>)

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `resource` | `string` | Required if using [Custom UI](/platform/forge/custom-ui/) or the latest version of [UI Kit.](/platform/forge/ui-kit/) | A reference to the static `resources` entry that your context menu app wants to display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `title` | `string` or `i18n object` | Yes | A title for the module.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed`, `customer`, and `anonymous`. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

UIM Forge modules can retrieve the current context using the [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI and UI Kit.

The shape of the context depends on the view your app is running in:

* On the **request create portal**, the context exposes the current `portalId` and `request` type.
* On the **agent view**, the context exposes the current `project`, `issueType`, and `requestTypeId`, plus `issue` and
  `issueTransition` where relevant to the view. Use the `viewType` property to detect which agent view your app is
  running in.

JSM request create portal context shape

JSM agent view context shape

```
```
1
2
```



```
{
  extension: {
    type: 'jira:uiModifications',
    portalId: {
      id: string,
    },
    request: {
      typeId: string
    },
    viewType: 'JSMRequestCreate'
  }
}
```
```

## Example

The same app can run on both the request create portal and the agent view. Read the `viewType` from the extension
context to work out which view your app is running in, then read only the properties available in that view.

JSM request create portal

JSM agent view

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

  const { portalId, request } = context.extension;

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

The same scopes cover both the request create portal and the agent view. The agent view supports more fields, so it
needs a few extra scopes on top of the portal ones. These are marked as **agent view only** in the examples below. If
your app runs in both views, declare all of the scopes listed.

# Warning

Before general availability, we may add a few more scopes specific to Jira Service Management.

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
    # Agent view only (Preview)
    - 'manage:jira-project'
```
```

| Scope | Data exposed | Field | Method |  |  |
| --- | --- | --- | --- | --- | --- |
| `read:jira-user` | User timezone and account ID | n/a | `view.getContext` |  |  |
| User display name, account ID, and avatar | User Picker | `getValue` |  |  |
| `read:jira-work` | Portal ID; request type ID of the request being created using portal | n/a | `view.getContext` |  |  |
| Data of the request being created using portal | All supported fields | `getValue` |  |  |
| Field name | All supported fields | `getName` |  |  |
| Field visibility | All supported fields | `isVisible` |  |  |
| `manage:jira-configuration` | Field description | All supported fields | `getDescription` |  |  |
| User locale | n/a | `view.getContext` |  |  |
| Atlassian app license status | n/a | `view.getContext` |  |  |
| The following values can be modified:  * name * description * visibility | All supported fields | * `setName` * `setDescription` * `setVisible` |  |  |
| `write:jira-work` | Default field value can be modified | All supported fields | `setValue` |  |  |

#### Additional data exposed in the agent view

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The agent view runs the same views as Jira (*global issue create*, *issue view*, and *issue transition*), so the scopes
above expose the same data as they do in Jira. For the full per-field breakdown, see
[Jira UI modifications: Scopes](/platform/forge/manifest-reference/modules/jira-ui-modifications/#scopes). The following
data is specific to Jira Service Management.

| Scope | Data exposed | Field | Method |
| --- | --- | --- | --- |
| `read:jira-work` | Project ID, key and type; issue type ID and name; work item ID and key; issue transition ID | n/a | `view.getContext` |
| Request type ARI of the work item (`requestTypeId`) | n/a | `view.getContext` |

## Required user permissions

In case a required permission isn't assigned, the user will see the following error:

```
```
1
2
```



```
We couldn't load the UI modifications configuration for this form
```
```

Permissions are evaluated per view. The request create portal is used by customers, while the agent view runs inside a
service project and is used by agents, so each has different requirements.

| View | Product access | Required project permission |
| --- | --- | --- |
| JSM request create portal | To make UI modifications load the user needs to have an access to Jira and JSM products. | n/a – the user needs to be able to raise a request for the request type they've selected. |
| JSM agent view – global issue create (Preview) | The user needs a licensed Jira Service Management agent seat and access to the service project. | [“Create issues” permission](https://support.atlassian.com/jira-cloud-administration/docs/permissions-for-company-managed-projects/#Issue-permissions) |
| JSM agent view – issue view (Preview) | [“Browse projects” permission](https://support.atlassian.com/jira-cloud-administration/docs/permissions-for-company-managed-projects/#Project-permissions) |
| JSM agent view – issue transition (Preview) | [“Transition issues” permission](https://support.atlassian.com/jira-cloud-administration/docs/permissions-for-company-managed-projects/#Issue-permissions) |

## View-specific requirements and limitations

JSM request create portal (Preview)

JSM agent view (Preview)

| Category | Details |
| --- | --- |
| **Supported entry points** | * Portal Request create form |
| **Known limitations** | * **Flash of unmodified fields** – UI modifications are loaded after the *Portal Request create view* has finished loading. For example, a field will be visible for a moment before being hidden. * Anonymous account types are not supported yet. [Read more](/platform/forge/access-to-forge-apps-for-unlicensed-users/). * Embeded request create forms are not supported yet. |

## Other known limitations

### Multiple UIM apps

If you install and configure multiple UIM apps to run for a given combination of project, issue type, and view type, up to 5 apps can apply changes simultaneously. If more than 5 apps are configured, changes from the remaining apps will be disregarded. Apps apply changes asynchronously, so the order of application is random.

There may be conflicts when multiple apps attempt to modify the same field using the same [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) method. In such cases, app developers will receive conflict errors via the [onError](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#error-handling) handler, and users will see corresponding notifications:

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/multi-app-conflict-notification.png?_v=1.5800.2272)

If the conflict happens, the changes applied by the app which finished running last will override changes from other apps.

### Image previews unavailable until issue is created

The [Atlassian Document Format (ADF)](/platform/forge/ui-kit/components/adf-renderer/) supports rich content
when using the UIM to add media content (like images) to Jira description, text area, or rich text custom fields.

However, when adding an image through the UIM during issue creation (for example, throught the GIC modal) the image
preview might display a `Preview unavailable` message. This is because the necessary permissions to display the image
aren't available yet; they'll be available after the issue is created and/or the page is refreshed.
