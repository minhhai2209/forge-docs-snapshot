# Add custom configuration to a macro

With the [release of](/platform/forge/changelog/#CHANGE-2381) `@forge/react` version 11.0.0, enhancements have been made
to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook to improve performance in [macro config](/platform/forge/manifest-reference/modules/macro/) apps when receiving configuration value changes.

Confluence macro config apps relying on the **[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/)**
hook or **[view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext)** need to
transition to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook before upgrading to
`@forge/react` version 11.0.0 or higher in order to properly access the latest values after the configuration updates.

Confluence macro config apps using the **[useConfig](/platform/forge/ui-kit/hooks/use-config/)** hook
should upgrade to `@forge/react` version 11.0.0 for improved performance.

Configuration allows you to customize what the macro displays by adjusting settings in a form.
To access these settings, you need to go into the edit mode for the macro, as demonstrated below.
This gives you the ability to customize the macro's output according to your preferences.

Custom configuration can be used for more complex use cases, such as when you need to use
specialised input components, or want more control over the rendering experience of configuring a macro.
It also allows saving arbitrary configuration at runtime, instead of requiring you to predefine all possible configuration fields.

Custom configuration supports both UI Kit and Custom UI.

You can add simple configuration to a macro using UI Kit components,
[as described here](https://developer.atlassian.com/platform/forge/add-configuration-to-a-macro-with-ui-kit/).

You can use rich text bodied macros,
[as described here](/platform/forge/using-rich-text-bodied-macros/).

You can also see a sample implementation of a macro with custom configuration in the [rich-text-custom-config-macro sample app](https://bitbucket.org/atlassian/forge-rich-text-custom-config-macro).

## Before you begin

Make sure you have the following:

* A Forge app with a Confluence macro created using [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/).
* The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.

## Step 1: Configure the manifest

First, set the `config` property to the [config object](/platform/forge/manifest-reference/modules/macro/#config-object)
in the `manifest.yml` file.

### For existing apps

If you already have a macro in your `manifest.yml`, add the `config` section to your existing macro definition:

**Before:**

```
```
1
2
```



```
modules:
  macro:
    - key: my-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: My Macro
```
```

**After:**

```
```
1
2
```



```
modules:
  macro:
    - key: my-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: My Macro
      config:
        resource: macro-config
        render: native # Only for UI Kit
        viewportSize: max # Optional
        title: Config # Optional
```
```

### For new apps

If you're creating a new macro, use this complete structure:

```
```
1
2
```



```
modules:
  macro:
    - key: my-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: My Macro
      config:
        resource: macro-config
        render: native
        viewportSize: max # Optional
        title: Config # Optional
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
  - key: macro-config
    path: src/frontend/config.jsx
app:
  runtime:
    name: nodejs20.x
  id: ari:cloud:ecosystem::app/YOUR_APP_ID
```
```

**Important differences:**

* **UI Kit** uses `render: native` on both the macro and config
* **Custom UI** does NOT use `render: native` (Custom UI is auto-detected from the build path)
* Both require the `runtime` property in the `app` section

## Step 2: Declare resources for the custom editor

Next, define the `resources` property in the `manifest.yml` file according to the
[Resources](/platform/forge/manifest-reference/resources/) page.
The `key` prop should match the `resource` name in the `config` object, and the `path` prop
should point to the `config` resource file that we will create in [step 3](#step-3--create-the-configuration-resource).

Add the `macro-config` resource to your existing `resources` section:

```
```
1
2
```



```
resources:
  - key: main
    path: src/frontend/index.jsx
  - key: macro-config
    path: src/frontend/config.jsx
```
```

The `key` value `macro-config` must match the `resource` value in the `config` object from Step 1.

## Step 3: Create the configuration resource

Define the `config` resource at the path specified in [step 2](#step-2--declare-resources-for-the-custom-editor).

Create the file `src/frontend/config.jsx` with the following complete code:

```
```
1
2
```



```
import React, { useState, useEffect } from 'react';
import ForgeReconciler, { Button, Label, SectionMessage, Stack, Textfield } from '@forge/react';
import { view } from "@forge/bridge";

// Submit functionality - handles configuration persistence
const useSubmit = () => {
  const [error, setError] = useState();
  const [message, setMessage] = useState('');

  const submit = async (fields) => {
    const payload = { config: fields };

    try {
      await view.submit(payload);
      setError(false);
      setMessage(`Submitted successfully.`);
    } catch (error) {
      setError(true);
      setMessage(`${error.code}: ${error.message}`);
    }
  };

  return {
    error,
    message,
    submit
  };
};

// Main configuration component
const Config = () => {
  const [value, setValue] = useState('');
  const [loading, setLoading] = useState(true);

  const {
    error,
    message,
    submit
  } = useSubmit();

  useEffect(() => {
    // Get the existing config from the bridge context
    view.getContext().then((context) => {
      if (context.extension?.config?.myField) {
        setValue(context.extension.config.myField);
      }
      setLoading(false);
    });
  }, []);

  if (loading) {
    return <Label>Loading...</Label>;
  }

  return (
    <Stack space="space.200">
      <Label labelFor="myField">Config field:</Label>
      <Textfield id="myField" value={value} onChange={(e) => setValue(e.target.value)} />
      <Button appearance="subtle" onClick={() => view.close()}>
        Close
      </Button>
      <Button appearance="primary" onClick={() => submit({ myField: value })}>
        Submit
      </Button>
      {typeof error !== 'undefined' && (
        <SectionMessage appearance={error ? 'error' : 'success'}>{message}</SectionMessage>
      )}
    </Stack>
  );
};

// Render the configuration modal
ForgeReconciler.render(
  <React.StrictMode>
    <Config />
  </React.StrictMode>
);
```
```

**Important**: `useConfig()` from `@forge/react` does not work for custom macro config. It is exclusively for sidebar macro config. For custom macro config, you must use `view.getContext()` from `@forge/bridge` to access the existing configuration, as shown above.

You will not be able to close the configuration modal by pressing `Escape` or by clicking outside the modal.

In UI Kit, we provide a modal header that contains a close button, and users will be able to close the configuration modal that way. The close button does not call `view.submit()` - you should provide submit functionality in the configuration resource as shown above.

## Step 4: Understanding configuration persistence

The configuration persistence functionality is already included in the complete `config.jsx` file from [Step 3](#step-3--create-the-configuration-resource).

The `useSubmit` function handles configuration persistence using the [view.submit()](/platform/forge/apis-reference/ui-api-bridge/view/#submit) method. Here's how it works:

### Configuration submission process:

1. **User input**: User enters data in the configuration form
2. **Submit button**: User clicks the "Submit" button
3. **Payload creation**: The `submit` function creates a payload with `{ config: fields }`
4. **Persistence**: `view.submit(payload)` saves the configuration
5. **Feedback**: Success or error message is displayed to the user

### Key functions:

* **`view.submit(payload)`**: Saves configuration and closes the modal
* **`view.close()`**: Closes the modal without saving (cancels macro insert)

### Error handling:

The function includes comprehensive error handling that:

* Shows success messages when configuration is saved
* Displays error codes and messages when submission fails
* Provides user feedback through the `SectionMessage` component

## Validation: Test your configuration

Before proceeding to Step 5, validate that your configuration is working correctly:

1. **Deploy your app**: Run `forge deploy` to deploy your changes
2. **Install/upgrade**: Run `forge install --upgrade` if you've changed permissions
3. **Test in Confluence**:
   * Edit a Confluence page
   * Insert your macro using `/` command
   * Click the configuration button to open the config modal
   * Enter test data and click "Submit"
   * Verify the macro displays your configuration data

If you encounter errors during testing, check the browser console for detailed error messages and refer to the [Troubleshooting](#troubleshooting) section below.

## Step 5: Show changes on app

Finally, we can show the changes submitted from the `config` on our app.

Place the following code into the `src/frontend/index.jsx` file.
For UI Kit, at the bottom of the file, use `ForgeReconciler` to render the modal.

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { useConfig, CodeBlock, Text } from '@forge/react';

const App = () => {
  const config = useConfig();

  return (
    <>
      <Text>Macro configuration data:</Text>
      <CodeBlock language="json" text={JSON.stringify(config, null, 2)} />
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Custom macro editor does not launch | Check if the custom macro editor resource is defined correctly in the manifest. |
| Custom macro editor closes automatically | Check the custom macro editor resource for any `view.close()` calls. You may need to provide the `keepEditing` parameter in `view.submit()`, which will then keep the editor open on submit. |
| Payload does not save | Check `view.submit()` [error codes](/platform/forge/manifest-reference/modules/macro/#error-code-guide). Ensure that the payload abides by the [supported payload format](/platform/forge/manifest-reference/modules/macro/#supported-config-payload-format). |
| Editor modal does not close when overlay is clicked | Clicking the modal background once the resource has loaded will not close the modal. However, if the resource is still loading, the user is able to click the background to close the modal. For a Custom UI editor resource, the developer must provide a UI element that calls `view.close()` to allow the user to close the modal. |
| Error in browser console: `ForgeReconciler.addConfig() cannot be called from within a custom config resource` | Check the custom editor resource for `ForgeReconciler.addConfig()` call(s) and remove them. Adding classic UI Kit config is not supported in custom configuration resources. |
| Macro is not inserted onto page after I close the custom macro editor | Make sure you use `view.submit()` to close the macro editor if you want the macro inserted onto the page. Using `view.close()` will cancel the macro insert. |
