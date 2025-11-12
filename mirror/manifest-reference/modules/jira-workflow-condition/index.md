# Jira workflow condition (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:workflowCondition` module creates a workflow condition that can be configured on workflow transitions in
company-managed projects (see: [Advanced workflow configuration](https://confluence.atlassian.com/adminjiracloud/advanced-workflow-configuration-776636620.html)).

Conditions control whether the user can execute a transition. If a condition fails, the user won't be able to execute
the transition. For example, the user won't see the transition button on the *View issue* page.

## Condition based on a Jira expression

You can use [Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/)
to evaluate the condition result.

For example, a condition that checks if the issue is assigned would look like this:

```
1
2
3
4
5
6
modules:
  jira:workflowCondition:
    - key: my-forge-workflow-condition
      name: Issue is assigned condition
      description: This condition allows executing the transition if the issue has an assignee.
      expression: issue.assignee != null
```

A workflow condition only evaluates to true if the provided Jira expression evaluates to true. It will evaluate to false
in all other cases, including when:

* the Jira expression fails to evaluate because of errors or returns anything other than a Boolean value (in this case, an [`avi:jira:failed:expression` event](/platform/forge/events-reference/jira/#expression-evaluation-failed) is sent)
* the app providing the workflow condition has been uninstalled

### Context variables

The following context variables are available to expressions:

* `user` ([User](/cloud/jira/platform/jira-expressions-type-reference#user)): The user the condition is evaluated for.
* `issue` ([Issue](/cloud/jira/platform/jira-expressions-type-reference#issue)): The issue selected for the transition.
* `project` ([Project](/cloud/jira/platform/jira-expressions-type-reference#project)): The project the issue belongs to.
* `transition` ([Transition](/cloud/jiraplatform/jira-expressions-type-reference#transition)): The transition that the condition is being evaluated against.
* `workflow` ([Workflow](/cloud/jira/platform/jira-expressions-type-reference#workflow)): The workflow that contains the condition.
* `config` ([JSON](/cloud/jira/platform/jira-expressions-type-reference#map)): The configuration saved on the configuration page with [Custom UI Jira bridge](/platform/forge/custom-ui-jira-bridge/bridge/).
* `groupOperator` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The logical operator for a group the condition belongs to. Possible results are: `AND`, `OR`, or `null`. The `null` is returned if there is only one condition in the transition.

Additionally, these are available for Jira Service Desk transitions:

* `customerRequest` ([CustomerRequest](/cloud/jira/platform/jira-expressions-type-reference#customerrequest)): The customer request selected for transition.
* `serviceDesk` ([ServiceDesk](/cloud/jira/platform/jira-expressions-type-reference#servicedesk)): The service desk the customer request belongs to.

## Adding condition configuration with Custom UI

Adding condition configuration with [UI Kit](/platform/forge/ui-kit/) is currently not supported.

Expression-based workflow conditions often require some degree of the configuration of their behavior. For example, you may want to
allow a user to transition the issue to a specific state only if the user is in a particular group and you want the project admin to configure
that group. For this purpose, three additional properties in the manifest allow you to declare
the [Custom UI](/platform/forge/custom-ui) resources that will show:

* the form that is shown when a workflow condition is first created
* the form that is shown when a workflow condition is edited
* the read-only view or summary of the configuration

The create and edit pages should present a form with configuration relevant to the condition. In order to persist
this information in Jira, the page needs to use the [workflowRules API](/platform/forge/custom-ui-jira-bridge/workflowRules/#onConfigure).

When evaluating the condition, the configuration saved that way will be available to the Jira expression under the `config` context variable.

The `config` context variable is stored under the `extension.conditionConfig` key in the context object returned from the
[getContext API](/platform/forge/custom-ui-bridge/view/#getcontext) in the Custom UI bridge.

### Example

To create a condition that displays the [Custom UI](/platform/forge/custom-ui), declare it in the manifest as follows:

```
```
1
2
```



```
modules:
  jira:workflowCondition:
    - key: my-forge-workflow-condition
      name: Issue is assigned condition
      description: This condition allows executing the transition if the issue has an assignee.
      expression: issue.assignee != null
      projectTypes: ['company-managed', 'team-managed']
      configurationDescription:
        expression: "config['ruleDescription']"
      edit:
        resource: edit-resource
      create:
        resource: create-resource
      view:
        resource: view-resource
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
```
```

To get the Atlassian app context in the `create`, `edit`, and `view` resources defined in the manifest, use [`view.getContext` function](/platform/forge/custom-ui-bridge/view/#getcontext).

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
      setConfig(ctx.extension.conditionConfig)
    });
  }, []);
}
```
```

To save the user input to the `config` context variable, pass the callback function returning stringified JSON to the [`workflowRules.onConfigure` function](/platform/forge/custom-ui-jira-bridge/workflowRules/#onConfigure).

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

// calling onConfigure from async function
try {
    await workflowRules.onConfigure(onConfigureFn);
} catch (e) {
    // Handle the error.
}

// calling onConfigure from non-async function
workflowRules
    .onConfigure(onConfigureFn)
    .catch(e => {
        // Handle the error.
    });
```
```

### Overriding Jira expression

Additionally, you can override the entire [Jira expression](/cloud/jira/platform/jira-expressions) from the manifest.
To do that, include the `expression` property in the returned JSON. For example:

```
```
1
2
```



```
const onConfigureFn = async () => {
  var config = {
    'expression': 'dynamically built expression'
  };

  return JSON.stringify(config);
};
```
```

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
| `name` | `string` or `i18n object` | Yes | The name of the condition displayed in the workflow configuration.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | The description of the condition displayed when adding the condition to a transition.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `expression` | `string` | Yes | The expression used to evaluate whether the user can execute a transition. The expression should return a Boolean value.  The expression is evaluated with the [context variables](/platform/forge/manifest-reference/modules/jira-workflow-condition/#context-variables). |
| `projectTypes` | `'company-managed'|'team-managed'[]` | No | Specifies which project types can use this workflow rule.  Options:     * `'company-managed'`: Available only in company-managed projects * `'team-managed'`: Available only in team-managed projects * `['company-managed', 'team-managed']`: Available in both project types   By default, workflow rules are enabled only for company-managed projects (i.e. `['company-managed']`) |
| `configurationDescription` | `{ expression: string }` | No | Provides a dynamic summary of the rule's configuration, shown in the workflow editor.  Set this property to an object with an `expression` field containing a Jira expression that returns a string.  The expression can reference the `config` context variable.  If not set, or if the expression returns `null` or an empty string, the static description property is used instead. |
| `create` | `{ resource: string }` | No | A reference to the static `resources` entry that allows you to configure the expression-based workflow condition on creation. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `edit` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to edit the expression-based workflow condition. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `view` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to view the summary of the expression-based condition configuration. See [Resources](/platform/forge/manifest-reference/resources) for more details. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Jira expressions events

Whenever an app-registered [Forge workflow condition](/platform/forge/manifest-reference/modules/jira-workflow-condition)
based on a Jira expression fails while executing, an `avi:jira:failed:expression` event is sent.

You can subscribe to [this event](/platform/forge/events-reference/jira/#expression-evaluation-failed) in Forge apps.
If you want to use this feature you have to include the OAuth scope `manage:jira-configuration` in the app manifest.
