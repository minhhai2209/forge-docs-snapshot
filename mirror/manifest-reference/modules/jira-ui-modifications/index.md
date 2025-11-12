# Jira UI modifications

The `jira:uiModifications` module allows you to change the look and behavior of the *Global issue create* (GIC), *Issue view* and *Issue transition* (the [new experience](https://community.atlassian.com/t5/Jira-articles/Now-GA-try-the-new-issue-transition-experience-in-Jira/ba-p/2734436))
when used in conjunction with the [UI modifications (apps) REST API](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).

**UI modifications** (UIM) is a runtime extension which allows applications to modify the UI on supported screens in a given
**UIM app mounting context** (for example, a combination of a project, an issue type and a view type).
The UI is modified using the **UIM JS API** in Forge applications in the **UIM Forge module**.
You can manage the available **UI modifications** and their contexts using the **UIM REST API**.
Applications can store additional data related to **UI modifications** as **UIM data**, which is also managed by the **UIM REST API**.
Each **UI modification** is backed by a **UIM entity** which represents it on the back-end and is delivered to the front-end in **UIM data**.

To understand the broader context of this module read the [UI modifications guide](/platform/forge/understanding-ui-modifications/).

#### UIM app

An Atlassian Forge application which uses the UIM Forge module. A single UIM app can declare only one UIM Forge module.

#### UIM app invocation context

Provided to the UIM app by Jira. It consists of a project, issueType, and uiModifications (UIM data).

#### UIM app mounting context

A combination of a `project`, `issueType`, and `viewType`.
UIM supports the following view types:

* Global issue create
* Issue view
* Issue transition

#### UIM data

An array of UIM entities for a given UIM app invocation context. The interpretation of UIM data is the responsibility of the UIM app. UIM data can be accessed through the invocation argument within the `initCallback` and the `changeCallback`.

#### UIM entity

A single mapping of custom textual data and a UIM app mounting context. It can be created and obtained using the UIM REST API.

#### UIM Forge bridge API

The API provided to the UIM app through the `@forge/jira-bridge` module. For more details, see the [Jira Bridge uiModifications documentation](/platform/forge/custom-ui-jira-bridge/uiModifications/).

#### UIM Forge module

A UI modifications Forge module (`jira:uiModifications`) declared in the manifest.

#### UIM REST API

The back-end REST API used to assign and retrieve specific data (related to `project`, `issueType`, and `viewType`) to be consumed by the UIM app through the UIM app invocation context. For more details, see the [UI modifications (apps) documentation](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).

## Writing your first UIM app

To write your first UIM app, follow the detailed instructions below or try out the example app at [atlassian/forge-ui-modifications-example](https://bitbucket.org/atlassian/forge-ui-modifications-example).

### Forge manifest

You can build your Forge app following one of our [guides](/platform/forge/). To create an app that will run as a UIM app, make sure to update your manifest.yml file to include:

```
```
1
2
```



```
modules:
  jira:uiModifications:
    - key: ui-modifications-app
      title: Example UI modifications app
      resource: uiModificationsApp
resources:
  - key: uiModificationsApp
    path: static/ui-modifications/dist
```
```

### The application

UIM apps depend on the `@forge/jira-bridge` package which exposes the [uiModifications API](/platform/forge/custom-ui-jira-bridge/uiModifications/) from version 0.6.0 onwards.
Both initialization-triggered and user-triggered phase changes are supported.
This package works on the client side and will be effective only when used within the static resource declared in the `jira:uiModifications` module.

The UIM Forge module will be rendered inside an invisible `iframe` element. The only meaningful part is the script linked in the main HTML file.

```
```
1
2
```



```
//static/hello-world/index.js
import { uiModificationsApi } from '@forge/jira-bridge';

uiModificationsApi.onInit(
  ({ api }) => {
    const { getFieldById, getScreenTabs } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    priority?.setVisible(false);

    // Changing the summary field label
    const summary = getFieldById('summary');
    summary?.setName('Modified summary label');

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');

    // Get value of labels field
    const labels = getFieldById('labels');
    const labelsData = labels?.getValue() || [];
    labels?.setDescription(
      `${labelsData.length} label(s) are currently selected`
    );

    // Hide the last screen tab
    const tabs = getScreenTabs();
    if (tabs.length > 0) {
      tabs.at(-1).setVisible(false);
    }
  },
  () => ['priority', 'summary', 'assignee', 'labels']
);
```
```

Keep in mind that all changes requested during the run of the `onInit` callback will be applied at once after the function completes its execution.

#### Async operations

The execution of changes can be postponed, for example when a UIM needs to perform some async operations before evaluating which modification to apply. For that purpose, our API allows you to return a `promise` object from the callback. The changes will be postponed until the `promise` resolves.

A correct implementation using a `promise`:

```
```
1
2
```



```
import { uiModificationsApi } from '@forge/jira-bridge';

// Below: imaginary import
import { shouldPriorityBeHidden } from '../my-services';

uiModificationsApi.onInit(
  ({ api }) => {
    const { getFieldById } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    // We store the update Promise
    const priorityUpdate = shouldPriorityBeHidden().then((result) => {
      if (result === true) {
        priority?.setVisible(false);
      }
    });

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');

    // We return the promise. In this case even the assignee field description
    // will be updated only after the priorityUpdate promise resolves.
    return priorityUpdate;
  },
  () => ['priority', 'assignee']
);
```
```

Note that `async/await` syntax is supported:

```
```
1
2
```



```
import { uiModificationsApi } from '@forge/jira-bridge';

// Below: imaginary import
import { shouldPriorityBeHidden } from '../my-services';

uiModificationsApi.onInit(
  async ({ api }) => {
    const { getFieldById } = api;

    // Hiding the priority field
    const priority = getFieldById('priority');
    const result = await shouldPriorityBeHidden();
    if (result === true) {
      priority?.setVisible(false);
    }

    // Changing the assignee field description
    const assignee = getFieldById('assignee');
    assignee?.setDescription('Description added by UI modifications');
  },
  () => ['priority', 'assignee']
);
```
```

### Configure the UI modification

The UIM Forge module will only render when configured for a given `projectId` and `issueTypeId` using the [UIM REST API](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/).
For example, there could be an [AdminPage](/platform/forge/ui-kit-components/jira/admin-page/) that creates a UIM using the REST API. Apps can also include Custom UIM data to be passed to the UIM Forge module when it is executed, for example a list of rules that a user has selected:

```
```
1
2
```



```
import api, { route } from '@forge/api';

const createUiModification = async (projectId, issueTypeId) => {
  const result = await api.asApp().requestJira(route`/rest/api/3/uiModifications`, {
    method: "POST",
    body: JSON.stringify({
      name: 'demo-ui-modification',
      data: '["custom data", "for your app"]',
      contexts: [
        { projectId, issueTypeId, viewType: 'GIC' }, 
        { projectId, issueTypeId, viewType: 'IssueView' }
      ],
    }),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  });
  console.log(`Created UI modification with status ${result.status}`);
  return result.status;
}
```
```

This Custom UIM data is available as `uiModifications` within the `onInit` and `onChange` callbacks. It has the following shape:

```
```
1
2
```



```
uiModifications: Array<{
  id: string,
  data?: string,
}>
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

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

UIM Forge modules can retrieve the current `project` and `issueType` by [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI and UI Kit.

The UIM context shape on **GIC** is:

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

The UIM context shape on **Issue view** is:

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
    issue: {
      id: string,
      key: string,
    }
    viewType: 'IssueView'
  }
}
```
```

The UIM context shape on **Issue transition** is:

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
    issue: {
      id: string,
      key: string,
    }
    issueTransition: {
      id: string,
    }
    viewType: 'IssueTransition'
  }
}
```
```

Usage:

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

### Classic scopes

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

### Granular scopes

```
```
1
2
```



```
permissions:
  scopes:
    - 'read:project:jira'
    - 'read:issue-type:jira'
    - 'read:user:jira'
    - 'read:user-configuration:jira'
    - 'read:issue:jira'
    - 'read:issue-status:jira'
    - 'read:priority:jira'
    - 'read:label:jira'
    - 'read:project.component:jira'
    - 'read:project-version:jira'
    - 'read:license:jira'
    - 'read:field:jira'
    - 'read:field-configuration:jira'
    - 'read:screen-tab:jira'
    - 'write:field-configuration:jira'
    - 'write:field.default-value:jira'
    - 'write:field:jira'
    - 'write:screen-tab:jira'
```
```

| Scope | Data exposed | Field | Method |
| --- | --- | --- | --- |
| `read:project:jira` | Project ID, key, and type of the issue being created using the GIC form or presented on the Issue view | n/a | `view.getContext` |
| `read:issue-type:jira` | Issue type ID and issue type name of the issue being created using the GIC form or presented on the Issue view | n/a | `view.getContext` |
| `read:user:jira` | User account ID | n/a | `view.getContext` |
| User account ID | Assignee, Reporter, People, User picker, Multiple user picker | `getValue` |
| `read:user-configuration:jira` | User timezone and locale | n/a | `view.getContext` |
| `read:issue:jira` | Issue data of the issue being created using the GIC form or presented on the Issue view | All supported fields | `getValue` |
| `read:issue-status:jira` | Issue status value | Status | `getValue` |
| `read:priority:jira` | Priority value | Priority | `getValue` |
| `read:label:jira` | Label value | Labels | `getValue` |
| `read:project.component:jira` | Components value | Components | `getValue` |
| `read:project-version:jira` | Versions value | Fix Versions, Affects Versions | `getValue` |
| `read:license:jira` | Atlassian app license status | n/a | `view.getContext` |
| `read:field:jira` | Field name | All supported fields | `getName` |
| `read:field-configuration:jira` | Field description | All supported fields | `getDescription` |
| Field visibility | `isVisible` |
| `read:screen-tab:jira` | Screen tab identifier | All visible screen tabs | `getId` |
| Screen tab visibility | `isVisible` |
| `write:field-configuration:jira` | Field description can be modified | All supported fields | `setDescription` |
| Field visibility can be modified | `setVisible` |
| `write:field.default-value:jira` | Default field value can be modified | All supported fields | `setValue` |
| `write:field:jira` | Field name can be modified | All supported fields | `setName` |
| `write:screen-tab:jira` | Screen tab visibility can be modified | All visible screen tabs | `setVisible` |
| Screen tab focus can be modified | `focus` |

#### Additional granular scopes required for Issue view

| Scope | Data exposed | Field | Method |
| --- | --- | --- | --- |
| `write:issue:jira` | Issue field values can be modified | All supported fields on Issue view | `setValue` |
| `read:issue-field-values:jira` | Issue field values can be read | All supported fields on Issue view | `getValue` |

#### Additional granular scopes required for Issue transition

| Scope | Data exposed | Field | Method |
| --- | --- | --- | --- |
| `read:issue.transition:jira` | Issue transition field values can be read | All supported fields on Issue transition | `getValue` |

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

### Global issue create

### Issue view

### Issue transition

## Multiple UIM apps

If you install and configure multiple UIM apps to run for a given combination of project, issue type, and view type, up to 5 apps can apply changes simultaneously. If more than 5 apps are configured, changes from the remaining apps will be disregarded. Apps apply changes asynchronously, so the order of application is random.

There may be conflicts when multiple apps attempt to modify the same field using the same [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) method. In such cases, app developers will receive conflict errors via the [onError](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#error-handling) handler, and users will see corresponding notifications:

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/multi-app-conflict-notification.png?_v=1.5800.1617)

If the conflict happens, the changes applied by the app which finished running last will override changes from other apps.

## Global issue create

### Supported project types

UIM for Global issue create (GIC) currently support the following project types:

### Supported entry points

The Global issue create (GIC) modal can be opened from many places in the system. We currently support the following entry points:

* the global **Create** button in the top **Navigation bar**
* the `c` keyboard shortcut
* the issue view **Add a child issue** and **Create subtask** buttons
* a Forge app with Custom UI using `CreateIssueModal` from `@forge/jira-bridge`

The Global issue create (GIC) modal with UIM will only open from **Add a child issue** and **Create subtask** if the summary and at least one other field is set as mandatory for the issue type.

### Known limitations

#### Flash of unmodified fields

UI modifications are loaded after the *Create issue dialog* has finished loading. The user is informed about the loading state by a small spinner icon next to the label, which indicates that a UIM is running. Users can still see the fields before the modifications are applied. For example, a field will be visible for a moment before being hidden, or the default field description will be visible before it changes.

#### *Show fields* and *Find your field*

![Global issue create > show fields](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/limitations-show-fields.png?_v=1.5800.1617)

Fields can be hidden by individual users using **Show fields**. Data for these hidden fields is not sent to the UIM app.

**Find your field** does not know about fields being hidden by a UIM app using `setVisible`. Users may not be able to discover why a field is not visible to them.

## Issue view (preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

### Supported project types

UIM for Issue view currently support the following project types:

### Supported entry points

The Issue view can be displayed in many places in Jira. We currently support the following entry points:

* Full page issue view
* Board issue view
* Backlog issue view
* List issue view
* Issues issue view
* Search issue view (global search)

### Using setValue versus other methods

Because by default fields are in read mode, when your app uses the `setValue` method, the changes are automatically committed and persisted to the database. Calling setValue doesn’t enable edit mode. Customizations applied using other methods are only valid for the current user session.

Because many users may be viewing an issue at the same time, `setValue` will normally trigger an issue data refresh and show the new value to all users. However, an issue data refresh doesn’t trigger when only the user making the change is viewing the issue.

### Known limitations

#### Validation fails are not propagated

The issue view updates data optimistically and may process invalid input from the user before rolling back the changes.
If that happens, UIM apps won’t call a second `onChange` and may unsync from the current state of the Issue view.

For example, if a user updates the Summary field to contain 240 characters, and then updates it again to contain 260 characters, this will trigger a validation error and the value will be rolled back to 240 characters. Your UIM app will receive both changes, but won’t receive the rollback.

#### Flash of unmodified fields

UI modifications are loaded after the *Issue view* has finished loading. For example, a field will be visible for a moment before being hidden.

#### Real time updates

There are no callbacks available to react to real time updates in the *Issue view*.

## Issue transition (preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

### Supported project types

UIM for Issue transition currently support the following project types:

### Supported entry points

The Issue transition dialog can be opened from many places in the system. We currently support the following entry points:

* full page Issue view:
  * changing the issue status
  * running **edit status** from the command palette
* all issues page - changing issue status
* **Project** > **Backlog** - changing the issue status
* **Plans** > **Timeline** - changing the issue status
* **Active sprints** - moving card between columns
* **Active sprints** - issue dialog changing the issue status

### Known limitations

#### Issue Transition new experience

UI modifications only run on the new experience of the Issue transition dialog. The legacy dialog isn’t and won’t be supported.

#### Flash of unmodified fields

UI modifications are loaded after the *Issue transition dialog* has finished loading. The user is informed about the loading state by a small spinner icon next to the label, which indicates that a UIM is running. Users can still see the fields before the modifications are applied. For example, a field will be visible for a moment before being hidden, or the default field description will be visible before it changes.
