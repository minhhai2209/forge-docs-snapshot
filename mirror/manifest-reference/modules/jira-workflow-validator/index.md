# Jira workflow validator (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:workflowValidator` module defines a validator that can be added to workflow transitions in company-managed
projects (see: [Advanced workflow configuration](https://confluence.atlassian.com/adminjiracloud/advanced-workflow-configuration-776636620.html)).

Validators check that any input made to the transition is valid before the transition is performed. In this case,
input also refers to data entered by the user on the transition screen. If a validator fails, the work item does not progress
to the destination status of the transition, the transition's post functions are not executed, and the error message
of the failed validator is shown.

Validators added by Forge apps are implemented with:

* [Jira expressions](/cloud/jira/platform/jira-expressions) that are provided
  upfront in the manifest or built dynamically on the configuration page
* lambda functions

## Validating with Jira expressions

The work item validated by the [Jira expression](/cloud/jira/platform/jira-expressions) includes changes made on the transition screen, which makes this way
of defining validators particularly suitable for cases where the state to validate can be modified during the transition.

A workflow validator only evaluates to true if the provided Jira expression evaluates to true. It will evaluate
to false in all other cases, including:

* the Jira expression fails to evaluate because of errors or returns anything other than a Boolean value (in this case, an [`avi:jira:failed:expression` event](/platform/forge/events-reference/jira/#expression-evaluation-failed) is sent)
* the app providing the workflow validator is uninstalled

If the expression returns a string value, that value will be shown as the error message on the transition.

### Example

A validator that checks if the work item is assigned would look like this:

```
```
1
2
```



```
modules:
  jira:workflowValidator:
    - key: my-forge-workflow-validator
      name: Work item is assigned validator
      description: This validator allows the transition where the work item has an assignee.
      expression: issue.assignee != null
      errorMessage: "The transition failed because no one is assigned to the task. Assign the task to a user and try again."
```
```

### Context variables

The following context variables are available to expressions:

* `user` ([User](/cloud/jira/platform/jira-expressions-type-reference#user)): The user who performs the transition.
* `issue` ([Work item](/cloud/jira/platform/jira-expressions-type-reference#issue)): The work item that is about to be transitioned. Includes changes made on the transition screen.
* `originalIssue` ([Work item](/cloud/jira/platform/jira-expressions-type-reference#issue)): The work item *before* changes were made on the transition screen. This variable is not available when validator is defined for the [initial transition](https://support.atlassian.com/jira-cloud-administration/docs/configure-the-initial-status/).
* `project` ([Project](/cloud/jira/platform/jira-expressions-type-reference#project)): The project the work item belongs to.
* `transition` ([Transition](/cloud/jira/platform/jira-expressions-type-reference#transition)): The transition that the validator is being evaluated against.
* `workflow` ([Workflow](/cloud/jira/platform/jira-expressions-type-reference#workflow)): The workflow that contains the validator.
* `config` ([JSON](/cloud/jira/platform/jira-expressions-type-reference#map)): The configuration saved on the configuration page with [Custom UI Jira bridge](/platform/forge/custom-ui-jira-bridge/bridge/).

Additionally, these are available for Jira Service Desk transitions:

* `customerRequest` ([CustomerRequest](/cloud/jira/platform/jira-expressions-type-reference#customerrequest)): The customer request that is about to be transitioned.
* `serviceDesk` ([ServiceDesk](/cloud/jira/platform/jira-expressions-type-reference#servicedesk)): The service desk the customer request belongs to.

## Adding validator configuration with Custom UI

Adding validator configuration with [UI Kit](/platform/forge/ui-kit/) is currently not supported.

Expression-based workflow validators often require some degree of the configuration of their behavior. For example, you may want to
allow a state transition only if the work item has a particular label, and you want the project administrator to configure
that label. For this purpose, three additional properties in the manifest allow you to declare
the [Custom UI](/platform/forge/custom-ui) resources that will show:

* the form that is shown when a workflow validator is first created
* the form that is shown when a workflow validator is edited
* the read-only view or summary of the configuration

The create and edit pages should present a form with configuration relevant to the validator. Create and edit for lambda function validators are only supported via new workflow editor.
In order to persist this information in Jira, the page needs to use the [workflowRules API](/platform/forge/custom-ui-jira-bridge/workflowRules/#onConfigure).

When evaluating the validator, the configuration saved that way will be available to the Jira expression under the `config` context variable and will be available to the lambda function under the `configuration` node.

The `config` context variable is stored under the `extension.validatorConfig` key in the context object returned from the
[getContext API](/platform/forge/custom-ui-bridge/view/#getcontext) in the Custom UI bridge.

### Example

To create a validator that displays the [Custom UI](/platform/forge/custom-ui), declare it in the manifest as follows:

```
```
1
2
```



```
modules:
  jira:workflowValidator:
    - key: my-forge-workflow-validator
      name: Work item summary contains text validator
      description: This validator allows the transition where the summary of an work item contains the text defined on the workflow validator configuration page.
      expression: "issue.summary.includes(config['key']) == true"
      projectTypes: ['company-managed', 'team-managed']
      configurationDescription:
        expression: "'The issue summary must contain \"' + config['key'] + '\".'"
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
      setConfig(ctx.extension.validatorConfig)
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
    "expression": "dynamically built expression"
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

## Validating with lambda functions

A function must be declared in the manifest and configured for a given validator. It is then invoked on every transition
to which the validator has been added. When the function is invoked, an argument it passed to it with the following
information about the transition:

```
```
1
2
```



```
{
  "issue": {
    "key": "work item key"
  },
  "configuration": {
  },
  "transition": {
    "from": {
      "id": "status id"
    },
    "to": {
      "id": "status id"
    },
    "modifiedFields": {
      "labels": null,
      "customfield_10020": "Text input",
      "customfield_10021": {
        "self": "https://your-domain.atlassian.net/jira/rest/api/3/customFieldOption/10001",
        "value": "Single select option",
        "id": "10001"
      },
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "Completely new description"
              }
            ]
          }
        ]
      }
    }
  }
}
```
```

The function returns an object containing two properties:

* `result` - a Boolean value indicating whether the transition is allowed
* `errorMessage` - the error message to show if the `result` is `false`. Otherwise, this property is ignored
  and doesn't have to be included

### Modified Fields

The `modifiedFields` section contains the updated values of fields that were changed during the work item transition. These fields are presented in the same format as those in the [REST API v3: Get issue](/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get).

Specific details about certain fields include:

* Array-type fields set to empty or `null` during the transition will be represented as `null` in `modifiedFields`.
* For fields that contain user information, only the `accountId` is returned:

```
```
1
2
```



```
{
  "modifiedFields": {
    "assignee": {
      "accountId": "0000-0000-0000-0000"
    }
  }
}
```
```

#### Supported field types

Modified fields are available for field types listed below.

**System fields**:

* Affects Version
* Fix Version
* Component
* Description
* Assignee
* Resolution
* Priority
* Work Type
* Labels
* Linked Issues
* Comment

**System custom fields**:

* Team
* Sprint
* Parent
* Text Field
* Text Area
* User Picker
* Multi-User Picker
* Date Picker
* Date-Time
* Labels
* Select
* Multi-Select
* Cascading Select
* Multi-Checkboxes
* Radio Buttons
* URL
* Float

**All [Forge custom fields](/platform/forge/manifest-reference/modules/jira-custom-field/#jira-custom-field)**

#### Scopes

The [OAuth 2.0 scope](/cloud/jira/platform/scopes-for-oauth-2-3LO-and-forge-apps/) `read:jira-work` must be granted to the app to ensure that `modifiedFields` are attached; otherwise, they won't be included.

### Example

To create a validator that allows transitions only for work items in the project with key `PRO`,
declare it like this in the manifest:

```
```
1
2
```



```
modules:
  jira:workflowValidator:
    - key: my-forge-workflow-validator
      name: Project is PRO validator
      description: This validator will allow the transition only if the project is PRO.
      function: validate
  function:
    - key: validate
      handler: status.validate
```
```

To implement the actual logic in the `src/status.js` file:

```
```
1
2
```



```
export const validate = args => {
  const issueKey = args.issue.key;

  return {
    result: issueKey.startsWith('PRO'),
    errorMessage: 'Only PRO project can use this flow'
  };
}
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the validator displayed in the workflow configuration.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | The description of the validator displayed when adding the validator to a transition.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `function` | `string` | The validator requires either the `function` or the `expression` in your Forge app. Only one of the two properties must be present in your Forge app. | A reference to the function module that defines the module. |
| `expression` | `string` | The expression used to validate whether the transition should be allowed. The expression can return either a boolean value or a string. Returning a string overrides the error message defined in the manifest – the returned string is shown to the user as the error message instead.  The expression is evaluated with the [context variables](/platform/forge/manifest-reference/modules/jira-workflow-validator/#context-variables).  This expression can be overridden using the configuration page. If you return configuration with the `expression` property, then that expression will be used to evaluate the validator instead of the expression defined here. |
| `errorMessage` | `string` or `i18n object` or  `{ expression: string }` | No | The error message to show when the validation in Jira expression validator fails. If `errorMessage` is not provided, the default error message will be displayed. This can be a static message, an `i18n object` or an object containing the `expression` property, with a Jira expression that returns the error message dynamically, based on the current transition or configuration.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `projectTypes` | `'company-managed'|'team-managed'[]` | No | Specifies which project types can use this workflow rule.  Options:     * `'company-managed'`: Available only in company-managed projects * `'team-managed'`: Available only in team-managed projects * `['company-managed', 'team-managed']`: Available in both project types   By default, workflow rules are enabled only for company-managed projects (i.e. `['company-managed']`) |
| `configurationDescription` | `{ expression: string }` | No | Provides a dynamic summary of the rule's configuration, shown in the workflow editor.  Set this property to an object with an `expression` field containing a Jira expression that returns a string.  The expression can reference the `config` context variable.  If not set, or if the expression returns `null` or an empty string, the static description property is used instead. |
| `create` | `{ resource: string }` | No | A reference to the static `resources` entry that allows you to configure the expression-based workflow validator on creation. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `edit` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to edit the expression-based workflow validator. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `view` | `{ resource: string }` | No | A reference to the static `resources` entry that allows to view the summary of the expression-based validator configuration. See [Resources](/platform/forge/manifest-reference/resources) for more details. |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Jira expressions events

Whenever an app-registered [Forge workflow validator](/platform/forge/manifest-reference/modules/jira-workflow-validator)
based on a Jira expression fails while executing, an `avi:jira:failed:expression` event is sent.

You can subscribe to [this event](/platform/forge/events-reference/jira/#expression-evaluation-failed) in Forge apps.
If you want to use this feature you have to include the OAuth scope `manage:jira-configuration` in the app manifest.
