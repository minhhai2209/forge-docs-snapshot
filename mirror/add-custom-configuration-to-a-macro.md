```
---
source: https://bitbucket.org/atlassian-developers/forge-docs/src/master/content/platform/forge/add-custom-configuration-to-a-macro.md?at=master&mode=edit&fileviewer=file-view-default&spa=0
title: "Add custom configuration to a macro"
description: "How to add custom configuration to a macro."
platform: platform
product: forge
category: devguide
subcategory: platform-concepts
date: "2025-03-03"
---

# Add custom configuration to a macro

{{% warning %}}
With the [release of](/platform/forge/changelog/#CHANGE-2381) `@forge/react` version 11.0.0, enhancements have been made
to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook to improve performance in [macro config](/platform/forge/manifest-reference/modules/macro/) apps when receiving configuration value changes.

Confluence macro config apps relying on the **[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/)**
hook or **[view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext)** need to
transition to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook before upgrading to
`@forge/react` version 11.0.0 or higher in order to properly access the latest values after the configuration updates.

Confluence macro config apps using the **[useConfig](/platform/forge/ui-kit/hooks/use-config/)** hook
should upgrade to `@forge/react` version 11.0.0 for improved performance.
{{% /warning %}}

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

- A Forge app with a Confluence macro created using [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/).
- The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.

## Step 1: Configure the manifest
First, set the `config` property to the [config object](/platform/forge/manifest-reference/modules/macro/#config-object)
in the `manifest.yml` file.

### For existing apps
If you already have a macro in your `manifest.yml`, add the `config` section to your existing macro definition:

**Before:**
```yaml
modules:
  macro:
    - key: my-macro
      resource: main
      render: native
      resolver:
        function: resolver
      title: My Macro
```

**After:**
```yaml
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

### For new apps
If you're creating a new macro, use this complete structure:

{{% tabs %}}{{% tab title="UI Kit" %}}
```yaml
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
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/YOUR_APP_ID
```
  {{% /tab %}}
{{% tab title="Custom UI" %}}
```yaml
modules:
  macro:
    - key: my-macro
      resource: main
      resolver:
        function: resolver
      title: My Macro
      config:
        resource: macro-config
        viewportSize: max # Optional
        title: Config # Optional
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: static/hello-world/build
  - key: macro-config
    path: static/config/build
app:
  runtime:
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/YOUR_APP_ID
```
  {{% /tab %}}{{% /tabs %}}

{{% note %}}
**Important differences:**
- **UI Kit** uses `render: native` on both the macro and config
- **Custom UI** does NOT use `render: native` (Custom UI is auto-detected from the build path)
- Both require the `runtime` property in the `app` section
{{% /note %}}

## Step 2: Declare resources for the custom editor
Next, define the `resources` property in the `manifest.yml` file according to the
[Resources](/platform/forge/manifest-reference/resources/) page.
The `key` prop should match the `resource` name in the `config` object, and the `path` prop
should point to the `config` resource file that we will create in [step 3](#step-3--create-the-configuration-resource).

{{% tabs %}}{{% tab title="UI Kit" %}}
  Add the `macro-config` resource to your existing `resources` section:

```yaml
resources:
  - key: main
    path: src/frontend/index.jsx
  - key: macro-config
    path: src/frontend/config.jsx
```
  {{% /tab %}}
{{% tab title="Custom UI" %}}
  Add the `macro-config` resource to your existing `resources` section:

```yaml
resources:
  - key: main
    path: static/hello-world/build
  - key: macro-config
    path: static/config/build
```
  {{% /tab %}}{{% /tabs %}}

{{% note %}}
The `key` value `macro-config` must match the `resource` value in the `config` object from Step 1.
{{% /note %}}

## Step 3: Create the configuration resource
Define the `config` resource at the path specified in [step 2](#step-2--declare-resources-for-the-custom-editor).

{{% tabs %}}{{% tab title="UI Kit" %}}
  Create the file `src/frontend/config.jsx` with the following complete code:

  ```javascript
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

  ,{{% note %}}
  **Important**: `useConfig()` from `@forge/react` does not work for custom macro config. It is exclusively for sidebar macro config. For custom macro config, you must use `view.getContext()` from `@forge/bridge` to access the existing configuration, as shown above.

  You will not be able to close the configuration modal by pressing `Escape` or by clicking outside the modal.

  In UI Kit, we provide a modal header that contains a close button, and users will be able to close the configuration modal that way. The close button does not call `view.submit()` - you should provide submit functionality in the configuration resource as shown above.
  {{% /note %}},
  {{% /tab %}}
{{% tab title="Custom UI" %}}
  For Custom UI, we recommend creating your `config` resource files in the directory `static/config/`.
  Please refer to the [Custom UI](/platform/forge/custom-ui/) page for more information on the structure of your resource directory.

  Create the file `static/config/src/App.jsx` with the following complete code:

  ```javascript
  import React, { useState, useEffect } from 'react';
  import { view } from '@forge/bridge';

  function App() {
    const [value, setValue] = useState('');
    const [error, setError] = useState();
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Get the existing config from the bridge context
      view.getContext().then((context) => {
        if (context.extension?.config?.myField) {
          setValue(context.extension.config.myField);
        }
        setLoading(false);
      });
    }, []);

    const handleSubmit = async () => {
      const payload = { config: { myField: value } };

      try {
        await view.submit(payload);
        setError(false);
        setMessage('Submitted successfully.');
      } catch (err) {
        setError(true);
        setMessage(`${err.code}: ${err.message}`);
      }
    };

    const handleClose = async () => {
      await view.close();
    };

    if (loading) {
      return <div style={{ padding: '20px' }}>Loading...</div>;
    }

    return (
      <div style={{ padding: '20px' }}>
        <h2>Macro Configuration</h2>
        <div style={{ marginBottom: '20px' }}>
          <label htmlFor="myField">Config field:</label>
          <br />
          <input
            id="myField"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={handleClose} style={{ padding: '8px 16px' }}>
            Close
          </button>
          <button
            onClick={handleSubmit}
            style={{
              padding: '8px 16px',
              backgroundColor: '#0052CC',
              color: 'white',
              border: 'none',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            Submit
          </button>
        </div>
        {typeof error !== 'undefined' && (
          <div
            style={{
              marginTop: '20px',
              padding: '10px',
              backgroundColor: error ? '#FFEBE6' : '#E3FCEF',
              color: error ? '#DE350B' : '#006644',
              borderRadius: '3px'
            }}
          >
            {message}
          </div>
        )}
      </div>
    );
  }

  export default App;
  ```

  You'll also need to create `static/config/src/index.jsx`:
  ```javascript
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import App from './App';

  import '@atlaskit/css-reset';

  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  ```

  ,{{% note %}}
  **Important**: `useConfig()` from `@forge/react` does not work for custom macro config. It is exclusively for sidebar macro config. For custom macro config, you must use `view.getContext()` from `@forge/bridge` to access the existing configuration, as shown above.

  When `view.submit()` is successful, the modal closes automatically. The success message will only display briefly if there's a network delay.
  {{% /note %}},
  {{% /tab %}}{{% /tabs %}}

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
- **`view.submit(payload)`**: Saves configuration and closes the modal
- **`view.close()`**: Closes the modal without saving (cancels macro insert)

### Error handling:
The function includes comprehensive error handling that:
- Shows success messages when configuration is saved
- Displays error codes and messages when submission fails
- Provides user feedback through the `SectionMessage` component

{{% note %}}
`view.submit()` supports more options than just config for updating the configuration. See
[Options for submitting the configuration](/platform/forge/manifest-reference/modules/macro/#options-for-submitting-the-configuration)
for the full list of options.

To interpret the different error codes returned from `view.submit()`, see [Error code guide](/platform/forge/manifest-reference/modules/macro/#parameters-available-in-the-macro-editor) for the full list.
{{% /note %}}

## Validation: Test your configuration

Before proceeding to Step 5, validate that your configuration is working correctly:

1. **Deploy your app**: Run `forge deploy` to deploy your changes
2. **Install/upgrade**: Run `forge install --upgrade` if you've changed permissions
3. **Test in Confluence**: 
   - Edit a Confluence page
   - Insert your macro using `/` command
   - Click the configuration button to open the config modal
   - Enter test data and click "Submit"
   - Verify the macro displays your configuration data

{{% note %}}
If you encounter errors during testing, check the browser console for detailed error messages and refer to the [Troubleshooting](#troubleshooting) section below.
{{% /note %}}

## Step 5: Show changes on app
Finally, we can show the changes submitted from the `config` on our app.

{{% tabs %}}{{% tab title="UI Kit" %}}

  Place the following code into the `src/frontend/index.jsx` file.
  For UI Kit, at the bottom of the file, use `ForgeReconciler` to render the modal.
  ```javascript
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
  {{% /tab %}}
{{% tab title="Custom UI" %}}

  Place the following code into the `static/hello-world/src/App.jsx` file.
  ```javascript
  import React, { useState, useEffect } from 'react';
  import { view } from '@forge/bridge';

  function App() {
    const [configData, setConfigData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      // Get config from bridge context
      view.getContext().then((context) => {
        setConfigData(context.extension?.config || {});
        setLoading(false);
      });
    }, []);

    if (loading) {
      return <div>Loading...</div>;
    }

    return (
      <div>
        <p>Macro configuration data:</p>
        <pre>{JSON.stringify(configData, null, 2)}</pre>
      </div>
    );
  }

  export default App;
  ```

  For Custom UI, use [ReactDOM.createRoot](https://react.dev/reference/react-dom/client/createRoot) to render the app
  in `static/hello-world/src/index.jsx`.
  ```javascript
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import App from './App';

  import '@atlaskit/css-reset';

  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
  ```

  ,{{% note %}}
  **Important**: When displaying configuration in the macro view, Custom UI apps must use `view.getContext()` from `@forge/bridge` to access the configuration data, as shown above. `useConfig()` from `@forge/react` only works with UI Kit for the main macro display.

  Also note the use of `ReactDOM.createRoot()` instead of the deprecated `ReactDOM.render()` for React 18 compatibility.
  {{% /note %}},
  {{% /tab %}}{{% /tabs %}}

## Troubleshooting

<table>
    <thead>
        <tr>
            <th>Issue</th>
            <th>Solution</th>
      </tr>
    </thead>
    <tbody>
        <tr>
          <td>Custom macro editor does not launch</td>
          <td>Check if the custom macro editor resource is defined correctly in the manifest.</td>
        </tr>
        <tr>
          <td>Custom macro editor closes automatically</td>
          <td>Check the custom macro editor resource for any <code>view.close()</code> calls. You may need to provide the <code>keepEditing</code> parameter in <code>view.submit()</code>, which will then keep the editor open on submit.</td>
        </tr>
        <tr>
          <td>Payload does not save</td>
          <td>Check <code>view.submit()</code> <a href="/platform/forge/manifest-reference/modules/macro/#error-code-guide">error codes</a>. Ensure that the payload abides by the <a href="/platform/forge/manifest-reference/modules/macro/#supported-config-payload-format">supported payload format</a>.</td>
        </tr>
        <tr>
          <td>Editor modal does not close when overlay is clicked</td>
          <td>Clicking the modal background once the resource has loaded will not close the modal. However, if the resource is still loading, the user is able to click the background to close the modal. For a Custom UI editor resource, the developer must provide a UI element that calls <code>view.close()</code> to allow the user to close the modal. </td>
        </tr>
        <tr>
          <td>Error in browser console: <code>ForgeReconciler.addConfig() cannot be called from within a custom config resource</code></td>
          <td>Check the custom editor resource for <code>ForgeReconciler.addConfig()</code> call(s) and remove them. Adding classic UI Kit config is not supported in custom configuration resources. </td>
        </tr>
        <tr>
          <td>Macro is not inserted onto page after I close the custom macro editor</td>
          <td>Make sure you use <code>view.submit()</code> to close the macro editor if you want the macro inserted onto the page. Using <code>view.close()</code> will cancel the macro insert.</td>
        </tr>
    </tbody>
</table>
```
