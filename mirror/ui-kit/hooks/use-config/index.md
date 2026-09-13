# useConfig

With the [release of](/platform/forge/changelog/#CHANGE-2381) `@forge/react` version 11.0.0, enhancements have been made
to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook to improve performance in [macro config](/platform/forge/manifest-reference/modules/macro/) apps when receiving configuration value changes.

Confluence macro config apps relying on the **[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/)**
hook or **[view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext)** need to
transition to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook before upgrading to
`@forge/react` version 11.0.0 or higher in order to properly access the latest values after the configuration updates.

Confluence macro config apps using the **[useConfig](/platform/forge/ui-kit/hooks/use-config/)** hook
should upgrade to `@forge/react` version 11.0.0 for improved performance.

This hook retrieves the [configuration values for a macro](/platform/forge/add-configuration-to-a-macro-with-ui-kit-2/). Note that the configuration data is loaded asynchronously, so its output will be `undefined` while it is still loading.

Use configuration to store general data, but not sensitive information. The configuration data is
stored in plaintext, so other users and apps can access and modify the values.

### Usage

To add the `useConfig` hook to your app:

```
1import { useConfig } from "@forge/react";
2
```

Here is an example of accessing configuration for a Forge macro. Note that you'll need to [add configuration to the Confluence macro module](/platform/forge/add-configuration-to-a-macro-with-ui-kit-2/#add-configuration-to-the-confluence-macro-module) in order to configure the displayed values.

![The app display on a Confluence page](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/useconfig.png?_v=1.5800.2330)

```
1import React from 'react';
2import ForgeReconciler, { Heading, Text, Textfield, useConfig } from '@forge/react';
3
4const defaultConfig = { name: 'Unnamed Pet', age: '0' };
5
6const App = () => {
7  const config = useConfig() || defaultConfig;
8  // Displaying a pet's name and age using the configuration values.
9  return (
10    <>
11      <Heading as="h1">Content with configured values</Heading>
12      <Text>"{config.name}" is "{config.age}" years old.</Text>
13    </>
14  );
15};
16
17// Function that defines the configuration UI for the pet's name and age
18const Config = () => {
19  return (
20    <>
21      <Textfield name="name" label="Pet name" defaultValue={defaultConfig.name} />
22      <Textfield name="age" label="Pet age" defaultValue={defaultConfig.age} />
23    </>
24  );
25};
26
27ForgeReconciler.render(
28  <React.StrictMode>
29    <App />
30  </React.StrictMode>
31);
32
33// Adding the Config function to the ForgeReconciler to allow for configuration changes
34ForgeReconciler.addConfig(<Config />);
35
```

### Function Signature

```
```
1
2
3
4
5
6
```



```
interface ExtensionConfiguration {
  [key: string]: any;
}

function useConfig(): ExtensionConfiguration | undefined;
```
```

### Arguments

None.

### Returns

* **ExtensionConfiguration:** If the macro has been configured, this hook returns a dictionary containing the configuration key-value pairs. The keys are the name props given to the child components of the `MacroConfig` component. If the macro has not yet been configured, this hook returns `undefined`.
