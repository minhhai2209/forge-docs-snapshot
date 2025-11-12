# workflowRules (preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

If your app uses the [`jira:workflowValidator`](/platform/forge/manifest-reference/modules/jira-workflow-validator),
[`jira:workflowCondition`](/platform/forge/manifest-reference/modules/jira-workflow-condition) or
[`jira:workflowPostFunction`](/platform/forge/manifest-reference/modules/jira-workflow-post-function) module
with Custom UI, you can use the `workflowRules` object to pass additional configuration data. This data will be
available when evaluating the Forge function.

## onConfigure

The `onConfigure` method enables you to pass a callback function that should return a stringified JSON value based on
your input elements. This will be saved as workflow module configuration. When evaluating the validator, condition or
post function, this configuration will be available under the `config` context variable.

Note: the maximum size of the post function configuration is 100 kB.

The `onConfigure` callback is invoked in two cases:

* when the user clicks the `Add` button on the `create` view displayed when adding a new validator, condition or post
  function
* when the user clicks the `Update` button on the `edit` view displayed when editing an existing validator, condition or
  post function

If you want to prevent users from submitting the form and don't want to save the current configuration,
return an `undefined` value from this callback.

### Function signature

```
```
1
2
```



```
type OnConfigureResponse = string;
type OnConfigureFn = () => Promise<OnConfigureResponse> | OnConfigureResponse;

function onConfigure(onConfigureFn: OnConfigureFn): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { workflowRules } from '@forge/jira-bridge';

// When the configuration is saved, this method is called. Return the configuration based on your input elements.
const onConfigureFn = async () => {
    const config = {
        'key': 'val'
    };

    // If you want to skip form submission, return undefined value.
    /*
    const isFormDataValid = await validateForm(config);
    if (!isFormDataValid) {
      return undefined;
    }
    */

    return JSON.stringify(config); // The string returned here will be available under the `config` context variable.
}

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

The saved configuration will appear under the `extension.validatorConfig`, `extension.conditionConfig`
or `extension.postFunctionConfig` key in the context object returned from
the [getContext API](/platform/forge/custom-ui-bridge/view/#getcontext) in the Custom UI bridge.

```
```
1
2
```



```
import { view } from '@forge/bridge';

const context = await view.getContext();
const savedValidatorConfig = context.extension.validatorConfig;
const savedConditionConfig = context.extension.conditionConfig;
const savedPostFunctionConfig = context.extension.postFunctionConfig;
```
```
