# Jira workflow post function (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:workflowPostFunction` module creates a workflow post function that can be configured on workflow transitions
in company-managed projects (
see: [Advanced workflow configuration](https://confluence.atlassian.com/adminjiracloud/advanced-workflow-configuration-776636620.html)).

Post functions carry out any additional processing required after a Jira workflow transition is executed, such as:

* updating an issue's fields
* adding a comment to an issue

A function must be declared in the manifest and configured for a given post function module. It is then invoked after
every transition to which the post function has been added, with the [post function event](/platform/forge/events-reference/jira/#run-post-function-event) as an
argument.
If multiple post functions are added to a transition, the execution order is not guaranteed.

## Lambda function

Whenever an issue is transitioned and an app-registered Forge workflow post function is assigned to the transition,
the function declared in the manifest is executed.

A function must be declared in the manifest and configured for a given post function. It is then invoked after every
transition to which the post function has been added. When the function is invoked, an argument is passed to it with the
following information about the transition.

Retries for post functions work in the same way
as [product event retries](/platform/forge/events-reference/product_events/#retry-product-events). You can request
a retry for a function invocation by returning an `InvocationError` object, defined in the `@forge/events` package.

### Payload

The payload is the same payload included in [post function event](/platform/forge/events-reference/jira/#run-post-function-event).
Due to the data sent to the function from Jira, it is necessary to include OAuth scopes in the app manifest: `read:jira-work` and `manage:jira-configuration`.

## Fetching additional data

You can fetch additional data not included in the argument passed to the lambda function using
the [Product Fetch API](/platform/forge/apis-reference/fetch-api-product.requestjira/) from the `@forge/api` package.

Sample resources:

## Adding post function configuration with Custom UI

Adding post function configuration with [UI Kit](/platform/forge/ui-kit/) is currently not supported.

Workflow post function behavior often requires some configuration. For example, you
may want to react to a state transition only if the issue has a particular label, and you want the project administrator
to configure that label. For this purpose, three additional properties in the manifest allow you to declare
[Custom UI](/platform/forge/custom-ui) resources that will show:

* the form that is shown when a post function is first created
* the form that is shown when a post function is edited
* the read-only view or summary of the configuration

The create and edit pages should present a form with configuration items relevant to the post function. In order to
persist this information in Jira, the page needs to use
the [workflowRules API](/platform/forge/custom-ui-jira-bridge/workflowRules/#onConfigure).

Note: the maximum size of post function configuration is 100 kB.

The `config` context variable is stored under the `extension.postFunctionConfig` key in the context object returned from
the [getContext API](/platform/forge/custom-ui-bridge/view/#getcontext) in the Custom UI bridge.

Post function configuration is also included in the [post function event](/platform/forge/events-reference/jira/#run-post-function-event).

### Example

To create a post function that displays a [Custom UI](/platform/forge/custom-ui), declare it in the manifest as
follows:

```
```
1
2
```



```
modules:
  jira:workflowPostFunction:
    - key: my-forge-workflow-post-function
      name: Jira workflow post function example
      description: This post function will be executed after issue transition.
      function: my-postfunction
      projectTypes: ['company-managed', 'team-managed']
      configurationDescription:
        expression: "'Update the issue summary to \"' + config['key'] + '\".'"
      edit:
        resource: edit-resource
      create:
        resource: create-resource
      view:
        resource: view-resource
  function:
  - key: my-postfunction
    handler: index.postfunction
resources:
  - key: create-resource
    path: static/create/build
  - key: edit-resource
    path: static/edit/build
  - key: view-resource
    path: static/view/build
permissions:
  scopes:
    - manage:jira-configuration
    - read:jira-work
```
```

To get Atlassian app context in the `create`, `edit`, and `view` resources defined in the manifest,
use the [`view.getContext` function](/platform/forge/custom-ui-bridge/view/#getcontext).

```
```
1
2
```



```
import { view } from '@forge/bridge';

function App() {
    const [context, setContext] = useState();
    const [config, setConfig] = useState();

    useEffect(() => {
        view.getContext().then(ctx => {
            setContext(ctx);
            setConfig(ctx.extension.postFunctionConfig)
        });
    }, []);
}
```
```

To save user input to the `config` context variable, pass the callback function returning stringified JSON to
the [`workflowRules.onConfigure` function](/platform/forge/custom-ui-jira-bridge/workflowRules/#onConfigure).

```
```
1
2
```



```
import { workflowRules } from '@forge/jira-bridge';

const onConfigureFn = async () => {
    var config = {
        'key': 'value'
    };

    return JSON.stringify(config);
};

// calling onConfigure from an async function
try {
    await workflowRules.onConfigure(onConfigureFn);
} catch (e) {
    // Handle the error.
}

// calling onConfigure from a non-async function
workflowRules
    .onConfigure(onConfigureFn)
    .catch(e => {
        // Handle the error.
    });
```
```

To implement the actual post function logic in the `src/index.js` file, declare the function that will be invoked:

```
```
1
2
```



```
import api, { route } from '@forge/api';

export const postfunction = async event => {
    console.log(`Running post function for issue ${event.issue.key}`);

    if (event.comment) {
        const response = await api
            .asApp()
            .requestJira(route`/rest/api/latest/issue/${event.issue.id}/comment/${event.comment.id}`);
        const commentData = await response.json();
        console.log('Comment data', commentData);
    } else {
        console.log('Comment absent');
    }

    if (event.changelog) {
        const response = await api
            .asApp()
            .requestJira(
                route`/rest/api/latest/issue/${event.issue.id}/changelog/list`,
                {
                    method: 'POST',
                    body: JSON.stringify({'changelogIds': [parseInt(event.changelog.id)]})
                }
            );
        const changelogData = await response.json();
        console.log('Changelog data', changelogData);
    } else {
        console.log('Changelog absent');
    }
}
```
```

Requests here can be made with `api.asUser()` construct subject to conditions outlined in [offline user impersonation](/platform/forge/remote/calling-product-apis/#offline-user-impersonation).

## New workflow editor

The new workflow editor supports this module in the same way. You can use same Custom UI resources and the same functions for managing configuration.

If you want to detect whether the new editor is being used, check for whether the key `extension.isNewEditor` is `true` in the object returned from the [`view.getContext` function](/platform/forge/custom-ui-bridge/view/#getcontext). This key will be unset in the old workflow editor.

The context will also include the workflow ID and project ID for team-managed workflows in the new editor.

The maximum length of configuration saved via the new editor is limited to 32KB.

```
```
1
2
```



```
import { view } from '@forge/bridge';

const context = await view.getContext();
const isNewEditor = context.extension.isNewEditor || false;
const workflowId = context.extension.workflowId;
const projectId = context.extension.scopedProjectId;
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the post function displayed in the workflow configuration.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | The description of the post function displayed when adding the post function to a transition.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `projectTypes` | `'company-managed'|'team-managed'[]` | No | Specifies which project types can use this workflow rule.  Options:     * `'company-managed'`: Available only in company-managed projects * `'team-managed'`: Available only in team-managed projects * `['company-managed', 'team-managed']`: Available in both project types   By default, workflow rules are enabled only for company-managed projects (i.e. `['company-managed']`) |
| `configurationDescription` | `{ expression: string }` | No | Provides a dynamic summary of the rule's configuration, shown in the workflow editor.  Set this property to an object with an `expression` field containing a Jira expression that returns a string.  The expression can reference the `config` context variable.  If not set, or if the expression returns `null` or an empty string, the static description property is used instead. |
| `create` | `{ resource: string }` | No | A reference to the static `resources` entry that allows you to configure the post function on creation. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `edit` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to edit the post function. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `view` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to view the summary of the post function configuration. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Known issues

* [FRGE-709](https://ecosystem.atlassian.net/browse/FRGE-709): if the comment has been added on the transition with
  restricted visibility, the post function won't be able to fetch it using
  the [Product Fetch API](/platform/forge/apis-reference/fetch-api-product.requestjira/).
