# Action

We recommend limiting Forge custom actions to 500 for optimal performance.

## Overview

The action module adds custom actions to Atlassian Automation rules. This allows you to extend Automation with app-specific functionality that can be selected, configured, and executed as part of any automation rule. Users select your action from the component picker, configure its inputs through a form you provide, and when the rule executes, your Forge function is invoked with the configured values.

The `core:action` module is also used by Rovo. To make your action available in Automation, you must add it to an `actionProvider` module (see below).

### Action lifecycle

When a user adds your action to a rule, they configure it through your custom form. When the rule executes, Automation invokes your Forge function with the configured inputs. Your action can then:

* Process the inputs and perform the intended operation
* Return errors if the configuration is invalid, which stops rule execution and notifies the rule owner
* Return successfully, allowing the rule to continue execution

If your action ran successfully, control will be passed back to Automation, and the rule will continue execution.

## Manifest

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
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
modules {}
└─ automation:actionProvider []
   ├─ key (string) [Mandatory]
   └─ actions (array) [Mandatory]
└─ action []
   ├─ key (string) [Mandatory]
   ├─ name (string) [Mandatory]
   ├─ function (string) [Mandatory]
   ├─ actionVerb (string) [Mandatory]
   ├─ description (string) [Mandatory]
   ├─ config {} [Optional]
   │  └─ resource (string) [Mandatory]
   │  └─ render (default | native) [Optional]
   ├─ inputs {} [Mandatory]
   │  └─ inputName {}
   │     ├─ title (string) [Mandatory]
   │     ├─ type (string) [Mandatory]
   │     ├─ required (boolean) [Mandatory]
   │     └─ description (string) [Optional]
   ├─ outputs {} [Optional]
   │  └─ outputName {}
   │     ├─ description (string) [Optional]
   │     ├─ type (string) [Mandatory]
   │     ├─ nullable (boolean) [Mandatory]
   ├─ outputContext {} [Optional]
   │  └─ entityName (string) [Mandatory]
   │  └─ outputType (string) [Mandatory]
   │  └─ outputDomain (string) [Mandatory]
   ├─ resolver {} [Optional]
   │  └─ function (string) [Mandatory]
function []
└─ key (string) [Mandatory]
└─ handler (string) [Mandatory]
resources []
└─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

### The actionProvider module

Automation will only show actions that are referenced by an `actionProvider`.

To make your actions visible in Automation, you must add them to an `actionProvider` module.

The `action` module supports both Automation and Rovo.
To control where the action should be shown, you need to opt into Automation explicitly by adding your `action` to an `actionProvider`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the action provider. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `actions` | `string[]` | Yes | A list of references to `action` modules (defined next) |

A single app is allowed to define up to 20 Automation actions.

### The action module

The `action` module allows you to configure an action.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the action, which other modules can refer to. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | A human-friendly name for the action which will be displayed in the user interface. |
| `function` or `endpoint` | `string` | Yes | A reference to the Forge function that defines the behavior of this action. If you are using [Forge remote](/platform/forge/remote/) then you can use an external API endpoint here. |
| `actionVerb` | `string` | Yes | The verb that best represents your action: `GET`, `CREATE`, `UPDATE`, `DELETE`, `TRIGGER`. |
| `description` | `string` | Yes | Textual representation of the component's configuration state. |
| `config` | [config](/platform/forge/manifest-reference/modules/automation-action/#the-config-property) | Yes | Form to provide additional context during action invocation. |
| `inputs` | [inputs](/platform/forge/manifest-reference/modules/automation-action/#the-inputs-property) | Yes | The inputs for this action. |
| `outputs` | [outputs](/platform/forge/manifest-reference/modules/automation-action/#the-outputs-property) | No | The outputs for this action. |
| `outputContext` | [outputContext](/platform/forge/manifest-reference/modules/automation-action/#the-outputcontext-property) | No | The output context for this action. |
| `resolver` | [resolver](/platform/forge/manifest-reference/modules/automation-action/#the-resolver-property) | No | The resolver for this action. |

### Example module

#### Using a Forge app with output

```
```
1
2
```



```
modules:
  automation:actionProvider:
    - key: action-provider-module-key
      actions:
        - add-comment-ui-kit
  action:
    - key: add-comment-ui-kit
      name: Add Comment on an Issue (UI Kit) - Event Test
      function: addCommentToIssue
      description: adds comment on an issue.
      config:
        resource: main-resource
        render: native
      inputs:
        projectKey:
          title: Project Key
          type: string
          description: Jira project key
          required: true
        issueKey:
          title: Issue Id
          type: string
          description: The issue id for the Jira issue id where a comments needs to be added
          required: true
        comment:
          title: Comment
          type: string
          description: The comment that needs to be added to the issue
          required: true
      actionVerb: CREATE
      resolver:
        function: automation-resolver
      outputs:
        message:
          description: The message that was created
          type: string
          nullable: false
      outputContext:
        entityName: comment
        outputType: OBJECT
        outputDomain: jira
  function:
    - key: addCommentToIssue
      handler: index.addComment
    - key: automation-resolver
      handler: resolver.handler
app:
  runtime:
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/1ac1c9df-ed96-4b89-b874-256479040a5a
resources:
  - key: main-resource
    path: src/frontend/fui.tsx
  - key: main-resource-custom-ui
    path: static/automation-actions-app/build
permissions:
  scopes:
    - write:jira-work
    - read:jira-work
  content:
    styles:
      - "unsafe-inline"
    scripts:
      - "unsafe-inline"
```
```

### The `config` property

After adding an app action to a rule, users can configure it.
This is done via a configuration form controlled by your app.
See [Action configuration](/platform/forge/manifest-reference/modules/automation-action/#action-configuration) below for more details.

The `config` property allows you to choose between UI Kit and Custom UI.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | Required if using the latest version of [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/extend-ui-with-custom-options/#custom-ui) | A reference to the static resources entry that your context menu app wants to display. See resources |
| `render` | `native` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |

### The `inputs` property

When your action is invoked, it receives a set of inputs, each of which is configured via the `inputs` property.

Each input must have a unique user-defined name, referred to as `inputName`, which acts as a parent container for the following properties: `title`, `type`, `required`, and `description`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `title` | `string` | Yes | The name of the input. |
| `type` | `string` | Yes | The data type of the input: `string`, `integer`, `number`, or `boolean`. |
| `required` | `string` | Yes | True if the input is required. |
| `description` | `string` | No | A short description of your action. |

### The `outputs` property

If your action when invoked, can return an output then each of those outputs can be configured via the `outputs` property.

Each output must have a unique user-defined name, referred to as `outputName`, which acts as a parent container for the following properties: `description`, `type`, and `nullable`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
|
| `description` | `string` | No | A short description of your output. |
| `type` | `string` | Yes | The data type of the output: `string`, `integer`, `number`, or `boolean`. |
| `nullable` | `boolean` | Yes | True if it is nullable. |

### The `outputContext` property

If your action on execution returns any `output`, then we need to provide a few more details around the output with the `outputContext` property.

We use the data from this property mainly for smart value processing.

This property is mandatory to be provided if you have any defined outputs.

Each outputContext must have the following properties: `entityName`, `outputType`, and `outputDomain`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `entityName` | `string` | Yes | The name of the operation which you wish to make with the returned output. Can only be alphanumeric characters and not exceeding 12 characters in length. |
| `outputType` | `string` | Yes | The type of output being returned. Supported output types are `OBJECT` or `LIST`. |
| `outputDomain` | `string` | Yes | The domain on which the output entity would operate on. Can only be lower case alphabets not exceeding 12 characters in length. Use of `-` separator allowed if you wish to have multiple words. |

### The `resolver` property

You can refer to this page [resolver](/platform/forge/runtime-reference/forge-resolver/#forge-resolver) for more details.

### Scopes

Automation action module doesn't require any additional scopes to be added to the manifest.

Keep in mind that if your action communicates with the Atlassian app API, it might need additional scopes.
See [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api) for more details.

### Example modules

#### Using a Forge function

```
```
1
2
```



```
modules:
  action:
    - key: log-time
      function: logTime
      name: Fetch timesheet by date
      actionVerb: CREATE
      description: |
        Retrieve a user's timesheet based on a date
      config:
        render: native
        resource: main-resource
      inputs:
        timesheetDate:
          title: Timesheet Date
          type: string
          required: true
          description: "The date that the user wants a timesheet for"
  function:
    - key: logTime
      handler: index.logTime
    - key: summary
      handler: index.summary
resources:
  - key: main-resource
    path: src/frontend/fui.tsx
```
```

#### Using a Forge remote endpoint

```
```
1
2
```



```
modules:
  action:
    - key: log-time
      endpoint: logTime
      name: Log time
      actionVerb: CREATE
      description: |
        Log some time for the user against a Jira issue
      config:
        render: native
        resource: main-resource
      inputs:
        issueKey:
          title: Jira Issue Key
          type: string
          required: true
          description: "The jira issue to log time against"
        time:
          title: Time to log in minutes
          type: integer
          required: true
          description: "The number of minutes to log"
  endpoint:
    - key: logTime
      remote: timesheetapp
      route:
        path: log-time
      auth:
        appUserToken:
          enabled: true
        appSystemToken:
          enabled: false
remote:
  - key: timesheetapp
    baseUrl: "https://backend.timesheetapp.com"
```
```

## Action configuration

Users can configure your action after they have added it to a rule.
They do that by providing inputs via a configuration form.

That configuration form is built by you, using either UI Kit or Custom UI.

We recommend choosing UI Kit due to its simplicity and efficiency in capturing user inputs.

![configuration-example](https://dac-static.atlassian.com/platform/forge/images/automation/action-configuration-example.png?_v=1.5800.1863)

For a great user experience, it is important for the configuration form to interact properly with Automation.
There are two areas to take care of:

* Maintaining configuration state
* Validation

### Maintaining configuration state

Users should be able to make changes to your action, navigate to another one, and then get back to yours.
**Changes they have made should not be lost along the way.**

Configuration state can be maintained in multiple ways prior to saving the rule:

* A user submits the configuration form with the `Next` button
* An app has `onChange` or `onBlur` handlers implemented per input in the configuration form that will call `view.submit(payload)` on each such event triggered.

* The configuration form loads in a pristine state with the `Next` button disabled. This prevents users from saving incomplete or unchanged configurations. To enable the `Next` button, implement `onChange` or `onBlur` handlers that call `view.submit()` to pass the input state, which marks the form as dirty.
* Clicking the `Back` button does not maintain the form state. This is intentional—the `Back` button is designed to discard unsaved changes and reset the form to its pristine state.

#### Maintaining state example in UI Kit

When the user clicks the `Next` button during rule creation/update, the Form’s `onSubmit` will be triggered, allowing you to handle the form's validation and submission.

More information about the form can be found under [Form](/platform/forge/ui-kit/components/form/) component.

```
```
1
2
```



```
import { view } from '@forge/bridge';
import ForgeReconciler, {
    Form,
    useForm,
    Text,
    useProductContext,
    ErrorMessage,
    TextArea,
} from '@forge/react';

export const CommentForm = ({ context }) => {
  const formInstance = useForm({
    defaultValues: context.extension.data.inputs,
  });
  const { handleSubmit, register, getValues } = formInstance;

  const onSubmit = (data) => {
    view.submit(data);
  };

  const onChangeHandler = (value) => {
    view.submit({ ...getValues(), ...value });
  };

  const { onChange: onCommentChange, ...commentRegisterProps } = register(
    "comment",
    {
      required: { value: true, message: "Comment is required" },
    }
  );

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Text>Comment</Text>
      <TextArea
        {...commentRegisterProps}
        onChange={(e) => {
          onCommentChange(e);
          onChangeHandler({ comment: e.target.value });
        }}
      />
      {formInstance.formState.errors.comment?.message && (
        <ErrorMessage>
          {formInstance.formState.errors.comment?.message}
        </ErrorMessage>
      )}
    </Form>
  );
};

export const App = () => {
  const context = useProductContext();

  return !context ? <Text>Loading...</Text> : <CommentForm context={context} />;
};

ForgeReconciler.render(<App />);
```
```

#### Maintaining state example in Custom UI

Custom UI necessitates additional setup.
The code must be either bundled into your Forge app or served from an external CDN, ensuring appropriate Content Security Policy (CSP) configurations are in place.

To be able to submit the configuration form with the native `Next` button - a subscription to an event is required, where the event listener callback should call the `view.submit`.

The event is called `AUTOMATION_ACTION_SUBMIT`.
It will notifies your app that a configuration form was submitted.
This event is only available for Custom UI modules.

```
```
1
2
```



```
import ReactDOM from 'react-dom/client';
import { useEffect, useRef, useState } from 'react';

import Form, { Field } from '@atlaskit/form';
import Textfield from '@atlaskit/textfield';

import { view, events } from '@forge/bridge';

export const App = () => {
  const [formData, setFormData] = useState(null);
  const formRef = useRef(null);

  useEffect(() => {
    view.getContext().then(({ extension }) => {
      setFormData(extension.data.inputs);
    });

    const subscription = events.on("AUTOMATION_ACTION_SUBMIT", () => {
      formRef.current?.onSubmit();
    });

    return () => {
      subscription.then((sub) => sub.unsubscribe());
    };
  }, []);

  const onChangeHandler = (value) => {
    const updatedFormData = { ...formData, ...value };

    view.submit(updatedFormData);
    setFormData(updatedFormData);
  };

  const onSubmit = (data) => {
    view.submit(data);
  };

  return (
    <Form onSubmit={onSubmit}>
      {({ formProps }) => {
        formRef.current = formProps;

        return (
          <form {...formProps}>
            <Field
              name="issueKey"
              label="Issue key"
              defaultValue={formData.issueKey}
            >
              {({ fieldProps: { onChange, ...restFieldProps } }) => (
                <Textfield
                  {...restFieldProps}
                  onChange={(e) => {
                    onChangeHandler({ [restFieldProps.name]: e.target.value });
                    onChange(e);
                  }}
                />
              )}
            </Field>
          </form>
        );
      }}
    </Form>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(<App />);
```
```

### Rule Validation

In order to be able **to save the rule in the Automation platform**, the configuration needs to pass some basic validation checks.

* The total size of the configuration, as a JSON, should not exceed 100 kilobytes
* The configuration should contain fields corresponding to the `inputs` declared in the manifest module
  * Every field type and size is validated against the input declaration
  * Fields present in the configuration but not declared as `inputs` in the manifest will be rejected

Additionally, we provide information to the action configuration about any invalid fields, enabling it to highlight those fields on initial load. This information can be retrieved from the `extension` object.

```
```
1
2
```



```
{
  // ...
  errors: {
    invalidInputs: {
      issueKey: {
        message: "issueKey is required",
      },
      comment: {
        message: "comment is required",
      },
    },
  }
}
```
```

Additionally, you can listen to the `AUTOMATION_ACTION_VALIDATE_RULE_EVENT` to receive notifications when rule validation is in progress.
This event passes an object with an `isValidating` boolean property that indicates whether validation is currently in progress.
This allows you to update your form's UI state, such as disabling inputs during validation.

#### For UI Kit

```
```
1
2
```



```
import { view, events } from '@forge/bridge';
// ... same as above ...

export const CommentForm = ({ context, isValidating }) => {
  const formInstance = useForm({
    defaultValues: context.extension.data.inputs,
    disabled: isValidating
  });
  const { handleSubmit, register, getValues } = formInstance;

  // ... same as above ...

  const { onChange: onCommentChange, ...commentRegisterProps } = register(
    "comment",
    {
      required: { value: true, message: "Comment is required" },
      disabled: isValidating,
    }
  );

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      {/* ... same as above ... */}
    </Form>
  );
};

export const App = () => {
  const context = useProductContext();
  const [isValidating, setIsValidating] = useState(false);

  useEffect(() => {
    const handleValidateRuleEvent = ({ isValidating }) => {
      setIsValidating(isValidating);
    };
    const subscription = events.on('AUTOMATION_ACTION_VALIDATE_RULE_EVENT', handleValidateRuleEvent);
    return () => subscription.then(sub => sub.unsubscribe());
  }, []);

  return !context ? <Text>Loading...</Text> : <CommentForm context={context} isValidating={isValidating} />;
};

ForgeReconciler.render(<App />);
```
```

#### For Custom UI

```
```
1
2
```



```
// ... same as above ...
import { view, events } from '@forge/bridge';

export const App = () => {
  const [formData, setFormData] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const formRef = useRef(null);

  // ... same as above ...

  useEffect(() => {
    const handleValidateRuleEvent = ({ isValidating }) => {
      setIsValidating(isValidating);
    };
    const subscription = events.on('AUTOMATION_ACTION_VALIDATE_RULE_EVENT', handleValidateRuleEvent);
    return () => subscription.then(sub => sub.unsubscribe());
  }, []);

  // ... same as above ...

  return (
    <Form onSubmit={onSubmit} isDisabled={isValidating}>
      {/* ... same as above ... */}
    </Form>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(<App />);
```
```

#### Trigger form validation in UI Kit

`trigger` method can be called from the `form` on initial render

```
```
1
2
```



```
// ...
const form = useForm({
  defaultValues: context.extension.data.inputs,
});

useEffect(() => {
  if (Object.keys(context.extension.errors.invalidInputs).length) {
    form.trigger();
  }
}, []);
// ...
```
```

#### Trigger form validation in Custom UI

Triggering form validation depends on which form library is used and its corresponding API for validation.

For libraries without manual validation triggers, store `context.extension.errors.invalidInputs` in local state to display field-level error messages. Clear each field's error state when the user begins editing to remove stale messages.

### Accepting Smart Values

If you want to use Smart Values to pass dynamic configuration to your action, you can add a hidden input field to your form (make sure to declare it in the manifest).

Then set the value of the input field to the smart value, e.g. `“{{version.name}}"`.

When Automation executes your action, it will pass on the resolved value.

#### Smart values output with Forge apps

We can now leverage smart value processing with Forge apps, this allows us to use the output of the defined Forge actions within our rule builder, to create more dynamic automation rules.

For every Forge automation action that produces outputs, we construct something called as the smart value operator.
The smart value operator name is derived by combining the values specified for the fields `actionVerb`, `outputDomain` and `entityName` in the apps `manifest` file.
Finally what you see on the UI is in the format `{smartValueOperator}.{outputs}` which can be used across rules.

Kindly refer [outputs](/platform/forge/manifest-reference/modules/automation-action/#the-outputs-property) and [outputContext](/platform/forge/manifest-reference/modules/automation-action/#the-outputcontext-property) sections to thoroughly understand how to define outputs for Forge actions.

Below section gives a glimpse of what to expect when working with Forge actions and smart values.
Defining a rule with a Forge action that has defined outputs mentioned in the example here: [Forge Action](/platform/forge/manifest-reference/modules/automation-action/#using-a-forge-app-with-output)

![automation-action-configuration](https://dac-static.atlassian.com/platform/forge/images/automation/automation-action-smart-value-configuration.png?_v=1.5800.1863)

We can now select the smart value operator which is created as explained above. This operator can than be used in the subsequent rule executions.

![automation-action-smart-value-operator](https://dac-static.atlassian.com/platform/forge/images/automation/automation-action-smart-value-operator.png?_v=1.5800.1863)

## Action execution

When Automation executes your action, it invokes the referenced Forge function (or remote endpoint if you are using Forge remote).
A `payload` object is passed into the function as an argument.
It includes the inputs defined for the action during the configuration inside the UI.

Here’s an example of a payload object, and how it can be accessed.

```
```
1
2
```



```
"payload": {
  "projectKey": "CP",
  "issueKey": "CP-16",
  "comment": "hello world"
}
```
```

The `addComment` function from the previous example might look like this:

```
```
1
2
```



```
export async function addComment(payload) {

  // Extract necessary information
  const projectKey = payload?.projectKey;
  const issueKey = payload?.issueKey;
  const comment = payload.comment || "This is a comment";

  // Your code goes here ...
}
```
```

### Permissions: `asApp()` vs `asUser()`

Automation will always invoke your action as a particular user associated with the connection in action configuration.
Therefore, you should always use `asUser()` when making outbound requests.
Quoting from [Forge’s Shared Responsibility Model](/platform/forge/shared-responsibility-model/#authorization-of-requests-to-the-app):

> You must use `asUser()` whenever you are performing an operation on behalf of a user.
> This ensures your app has at most the permissions of the calling user.

Note that configuring a connection for an action is not sufficient on its own.

The user associated with the connection must also have an app consent entry in their [Connected apps](https://id.atlassian.com/manage-profile/apps) to ensure reliable action execution when `asUser()` is used.

### Communicating errors

If the user hasn’t provided valid inputs to your action, you can return a list of error messages.
The rule will stop execution, the action will be marked as failed, and the rule owner will be notified by email.
The rule owner can then navigate to the Audit Log, where they can then see the error messages you have provided.

*Note: if your app throws an exception, the execution will be marked as failed too, but only a generic error message will be shown.*

```
```
1
2
```



```
export async function addCommentWithUsageError(payload) {
  const issueKey = payload?.issueKey;

  if (!issueKey) {
    return {
      errors: [
        {
          message: `Payload provided with invalid issue key: ${issueKey}`,
        },
      ],
    };
  }

  // continue execution
}
```
```

## Icons

An app icon will be used as an action icon visible in the automation flow configuration.
If the app defines multiple actions, they will have the same icon.

An app icon can be configured in the Developer console:

![app-icon](https://dac-static.atlassian.com/platform/forge/images/automation/action-configuration-icon.png?_v=1.5800.1863)

## Design guidelines

Refer to the [design guidelines](/platform/forge/action-components-guidelines) for best practices on designing action icons, naming them, and writing clear descriptions. This will help ensure that your action is consistent with others in Atlassian Automation.

## Known issues

### Behaviour on app installation

When a user uninstalls your app, there might still be references to your app actions in their rules.
These references will continue to exist (together with the documentation).

However, the action will be shown as an “unknown component”.

If the user chooses to reinstall the app, all the actions will appear again together with the previous configuration.

### Internationalization

If your action appends error messages to Automation’s Audit log, these will be persisted in the Audit Log.
There is no support for internationalization / translating these strings.

### Forge tunnel

Note that `forge tunnel` will only work if the automation rule action is set up with a Connection linked to your personal user account.
Code reloading and the action execution logs should work as usual after running `forge tunnel`.
