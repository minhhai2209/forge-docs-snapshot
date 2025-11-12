# Upgrade from UI Kit 1 to UI Kit latest version

This guide is only applicable for migrating existing UI Kit 1 apps to the latest version of UI Kit.

Not all hooks in UI Kit 1 exist in the latest
version of UI Kit.

In the latest version, implementations of standard `react` library hooks (`useState`, `useEffect` and `useAction`) can now be directly accessed from `react` instead (see [Hooks API Reference – React](https://reactjs.org/docs/hooks-reference.html)). Note that the `react` equivalent of UI kit's `useAction` is `useReducer`, although usage of both is identical.

The `useProductContext`, `useConfig`, `useContentProperty`, `useSpaceProperty` and `useIssueProperty` hooks are available in our `@forge/react` package.

In addition, since the context/configuration/property values outputted by the `@forge/react` hooks take time to load, they will not be immediately available upon app mounting; i.e. these values will initially be `undefined` before they are loaded with actual values.

### useState, useEffect, useAction (useReducer)

**UI Kit 1**

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
import ForgeUI, { useState, useEffect, useAction, Text } from '@forge/ui';

const App = () => {
  const [count, setCount] = useState(0);

  return (
    <Text>Count: {count}</Text>
  );
}
```

**Latest version of UI Kit**

```
```
1
2
```



```
import React, { useState, useEffect, useReducer } from 'react';
import { Text } from '@forge/react';

const App = () => {
  const [count, setCount] = useState(0);

  return (
    <Text>Count: {count}</Text>
  );
};
```
```

The [latest version of UI Kit](https://developer.atlassian.com/platform/forge/changelog/#1590) is now generally available. This version comes with a new major version of `@forge/react` containing 37 updated components.

Use this guide to know what you need to do to move your apps from UI Kit 1 to the latest version
of UI Kit.

## Changes to the manifest

We’re introducing a new manifest structure for UI Kit. In the new structure, you need to make the following changes:

* Add `render: native` to each module.
* Use the `resource` key to point to the frontend, instead of `function`.
* Use the `resolver` key with `function` properties to point to any resolvers.

Your `manifest.yml` file should look like the following:

```
```
1
2
```



```
modules:
    confluence:globalPage:
        - key: hello-world
          resource: main
          route: hello-world
          resolver:
            function: resolver
          render: native
          title: UI Kit App
    function:
        - key: resolver
          handler: index.handler
resources:
    - key: main
      path: src/frontend/index.jsx
```
```

## Changes to existing components

The component APIs in UI Kit are very different to UI Kit 1 components. The breaking changes are:

### Avatar

* The `Avatar` component has been removed. Use the [User](/platform/forge/ui-kit/components/user/) component instead.

### AvatarStack

* The `AvatarStack` component has been removed. Use the [UserGroup](/platform/forge/ui-kit/components/user-group/) component instead.

### Badge

* The `text` prop for `Badge` has been removed. Content is now placed in `children` instead.
* `Badge` has a new `max` prop that defaults to the value of 99. It renders badge content as `99+` for values greater than 99.

### Button

* The `text` prop for `Badge` has been removed. Content is now placed in `children` instead.
* The `appearance` prop no longer accepts `link` and `subtle-link` types, as we now have `LinkButton`.
* The `disabled` prop has been renamed to `isDisabled`.
* `icon` and `iconPosition` have been updated to `iconBefore` and `iconAfter`. `iconBefore` and `iconAfter` take the same values as icon and will position before and after the button children contents accordingly.

### ButtonSet

* The `ButtonSet` component has been replaced by [ButtonGroup](/platform/forge/ui-kit/components/button-group/). There are no other breaking changes outside of the component name change.

### CheckboxGroup

* The `children`, `description` and `label` props have been removed. The `options` prop, `HelperMessage` component, and `Label` component can be used instead.

```
```
1
2
```



```
const CheckboxGroup = () => {
  return (
    <Label labelFor="products">Products</Label>
    <CheckboxGroup name="products" options={[
      { label: 'Jira', value: 'jira' },
      { label: 'Confluence', value: 'confluence' },
    ]} />
    <HelperMessage>Pick a product</HelperMessage>
  )
}
```
```

### Code

* The functionality of `Code` has now been separated into two different components:
  * `Code` should now only be used for inline code.
  * [CodeBlock](/platform/forge/ui-kit/components/code-block/) has been added and should be used for code blocks.
* As the intended use of `Code` is for inline code, the `language` prop has been removed.
* The `text` prop has been removed. Content is now placed in `children` instead.

### DateLozenge

* `DateLozenge` has been removed and can be replaced by using [Lozenge](/platform/forge/ui-kit/components/lozenge/).
* The date value must be formatted to the desired display value.

### DatePicker

* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="start-date">Start date</Label>
<DatePicker id="start-date" />
<HelperMessage>Enter a start date</HelperMessage>
```
```

### Form

* The `submitButtonAppearance`, `submitButtonText` and `actionButtons` props have been removed. A `Button` component with the `type="submit"` prop must be used within your `Form` component to allow for form submissions.
* The `Form` component should now be used with the [useForm](/platform/forge/ui-kit/hooks/use-form/) hook for state management. See [example usage](/platform/forge/ui-kit/components/form/#field-level-validation).

### FormCondition

* The `FormCondition` component has been removed. Use the [useForm](/platform/forge/ui-kit/hooks/use-form/) hook for state management. See [example usage](/platform/forge/ui-kit/components/form/#field-level-validation).

### Heading

* The `size` prop has been removed. The `as` prop is now required instead. Heading [accessibility guidelines](/platform/forge/ui-kit/components/heading/#accessibility-considerations) should be followed.

### Link

* The `appearance` prop has been removed. Use [LinkButton](/platform/forge/ui-kit/components/button/#linkbutton-props) instead for `button` and `primary-button` types.

### ModalDialog

* The `ModalDialog` component has been replaced by [Modal](/platform/forge/ui-kit/components/modal/).
* The `closeButtonText` and `header` props have been removed.
  * A `Button` component will need to be rendered to close `Modal`.
  * The `header` prop has been replaced by `ModalTitle`.

### Radio

* The `defaultChecked` prop has been removed. Use `isChecked` instead.

### RadioGroup

* The `children`, `description` and `label` props have been removed. The `options` prop, `HelperMessage` component, and `Label` component can be used instead.
* `RadioGroup` can now be used regardless of whether it is in a `Form` or in the config for the `macro` extension point.

```
```
1
2
```



```
<Label labelFor="color">Color</Label>
<RadioGroup id="color" options={[
  { name: 'color', value: 'red', label: 'Red' },
  { name: 'color', value: 'blue', label: 'Blue' },
  { name: 'color', value: 'yellow', label: 'Yellow' },
]} />
<HelperMessage>Pick a color</HelperMessage>
```
```

### Range

* `Range` can now be used anywhere, so the `isRequired` prop is will not be checked if it is not in a form
* `Range` spans the full width of its container.
* The `label` prop has been removed. Use the `Label` component instead.

```
```
1
2
```



```
<Label labelFor="range">Range</Label>
<Range id="range" />
```
```

### SectionMessage

* The `appearance` prop now takes different values.
  * `information` replaces `info`.
  * `success` replaces `confirmation`.
  * `discovery` replaces `change`.

### Select

* The `children` prop has been replaced by `options`.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.
* The `defaultSelected` prop in `Option` has been removed. Use `defaultValue` in `Select` instead.

```
```
1
2
```



```
<Label labelFor="fruit">Favourite fruit</Label>
<Select
  inputId="fruit"
  options={[
    { label: 'Apple', value: 'apple' },
    { label: 'Banana', value: 'banana' },
  ]}
/>
<HelperMessage>Pick a fruit</HelperMessage>
```
```

### StatusLozenge

* The `StatusLozenge` component has been replaced by [Lozenge](/platform/forge/ui-kit/components/lozenge/).
* The `text` prop has been removed. Content is now placed in the `children` prop of the `Lozenge` component instead.

### Table

* The `Table` component has been replaced by [DynamicTable](/platform/forge/ui-kit/components/dynamic-table/).
* Individual `Head`, `Row`, and `Cell` components have been removed in favor of data being passed in via arrays and objects.
* Major breaking changes have been made to provide a more powerful table with additional features.

### Tabs

* The code layout of `Tabs` has been updated. See an [example](/platform/forge/ui-kit/components/tabs/) of the new Tabs component.

### Tag

* The color prop values are now camel-cased instead of snake-cased.
  * i.e. `greyLight` replaces `grey-light`.

### Text area

* `Text area` spans the full width of its container.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="message">Message</Label>
<TextArea id="message" />
<HelperMessage>Enter a message</HelperMessage>
```
```

### Text field

* The component has been renamed from `TextField` to `Textfield`.
* `Textfield` spans the full width of its container.
* The `autoComplete` prop has been removed.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="email">Email</Label>
<Textfield id="email" />
<HelperMessage>Enter an email</HelperMessage>
```
```

### Toggle

* The `label` prop has been removed. Use the `Label` component instead.

```
```
1
2
```



```
<Label labelFor="toggle">Toggle</Label>
<Toggle id="toggle" />
```
```

* The `text` prop has been replaced by `content`.

### UserPicker

* `UserPicker` spans the full width of its container.

### AssetsAppImportTypeConfiguration

* `AssetsAppImportTypeConfiguration` should be replaced by `Form` and render action buttons within the `Form` component.

## New components

The following components are available in the latest version of UI Kit:

### Other features

We now have components that support the `xcss` prop. See the [XCSS documentation](/platform/forge/ui-kit/components/xcss/) for more information.

## Changes to extension points

### Top-level components

Each module in UI Kit 1 requires a top-level component at the root of the app. These components
have been removed in UI Kit and do not need to be included in your app anymore. For most modules,
the top-level component has no props and can simply be deleted.

##### UI Kit 1

```
```
1
2
```



```
import ForgeUI, { AdminPage, render, Text} from '@forge/ui';

const App = () => {
    return (
        <AdminPage>
            <Text>Hello, world!</Text>
        </AdminPage>
    );
};

export const run = render(
    <App/>
);
```
```

##### UI Kit

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Text } from '@forge/react';

const App = () => {
    return (
        <Text>Hello, world!</Text>
    );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

Some modules allow a value to be submitted, where the top-level component has an `onSubmit` prop
and the value gets automatically updated when the form is submitted. For example, Jira’s
Custom Field and Dashboard Gadget modules both have `edit` entrypoints.

The removal of the top-level components in UI Kit means field values in these modules now have
to be manually submitted by the developer via the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit)
on `@forge/bridge`.

### Confluence macro configuration

For a complete guide on how to add macro configuration in UI Kit,
see [Add configuration to a macro with UI Kit](/platform/forge/add-configuration-to-a-macro-with-ui-kit/).
The section below highlights some key differences between UI Kit 1 and UI Kit.

The config property in the macro module is a boolean instead of a function reference.

##### UI Kit 1

```
```
1
2
```



```
modules:
  macro:
    - key: pet-facts
      function: main
      title: Pet
      description: Inserts facts about a pet
      config:
        function: config-function-key
  function:
    - key: main
      handler: index.run
    - key: config-function-key
      handler: index.config
```
```

##### UI Kit

```
```
1
2
```



```
modules:
  macro:
    - key: pet-facts
      resource: main
      render: native
      resolver:
        function: resolver
      title: Pet
      config: true
  function:
    - key: resolver
      handler: index.handler
```
```

The allowed form components in config no longer have the `label` prop. To add a label,
a `Label` component must be added as a direct sibling before the form component.

The `MacroConfig` top-level component has also been removed from UI Kit.

##### UI Kit 1

```
```
1
2
```



```
import ForgeUI, { MacroConfig, TextField, render } from '@forge/ui';

const Config = () => {
  return (
    <MacroConfig>
      <Textfield name="age" label="Pet age" />
    </MacroConfig>
  );
};

export const config = render(<Config />);
```
```

##### UI Kit

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Label, Textfield } from '@forge/react';

const Config = () => {
  return (
    <>
      <Label>Pet age</Label>
      <Textfield name="age" />    
    </>
  );
};

ForgeReconciler.addConfig(<Config />);
```
```

## Changes to hooks

## Resolvers

The `@forge/api` package cannot be used in frontend code, so some API calls in UI Kit 1 need to be moved into a [resolver](/platform/forge/runtime-reference/forge-resolver/). For example, to call the Storage API, a function is defined in the resolver to call the API, and the frontend invokes the resolver with the `invoke` function on `@forge/bridge`.

This tutorial uses the legacy `storage` module from the `@forge/api` package.
When using the Key-Value Store and Custom Entity Store capabilities, we recommend that you use the `kvs` module from the `@forge/kvs` package instead
(as all future updates will be added to that package).

**src/resolvers/index.js**

```
```
1
2
```



```
import { storage, startsWith } from '@forge/api';
import Resolver from '@forge/resolver';

const resolver = new Resolver();

resolver.define('getExampleValue', async ({ payload, context }) => {
  return await storage.get('example-key');

});

export const handler = resolver.getDefinitions();
```
```

**src/frontend/index.jsx**

```
```
1
2
```



```
import React, { useEffect, useState } from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const [value, setValue] = useState(undefined);

  useEffect(() => {
    invoke('getExampleValue').then(setValue);
  }, []);

  return (
    <Text>{value}</Text>
  )
};
```
```

You'll notice that the folder structure is now different. The following modifications have been made:

* `src/resolvers/index.js` has been added. This is where you write backend functions for your app, such as the API calls mentioned above.
* `index.jsx` is now at `src/frontend/index.jsx`. This is where you write the application with which the user interacts directly.

**UI Kit**

```
```
1
2
```



```
ui-kit-app
├── README.md
├── manifest.yml
├── package-lock.json
├── package.json
└── src
    ├── frontend
    │   └── index.jsx
    ├── index.js
    └── resolvers
        └── index.js
```
```

**UI Kit 1**

```
```
1
2
```



```
ui-kit-1-app
├── README.md
├── manifest.yml
├── package-lock.json
├── package.json
└── src
    └── index.jsx
```
```

## Changes to Atlassian app requests

Jira and Confluence API requests can be made from the app frontend via `@forge/bridge` instead of `@forge/api`.

##### UI Kit 1

```
```
1
2
```



```
import api, { route } from '@forge/api';

await api.asUser()
  .requestJira(route`/rest/api/3/issue/${issueKey}/watchers`, {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
      },
      body: JSON.stringify(`${accountId}`)
  });
```
```

##### UI Kit

```
```
1
2
```



```
import { requestJira } from '@forge/bridge';

await requestJira(`/rest/api/3/issue/${issueKey}/watchers`, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
    },
    body: JSON.stringify(`${accountId}`)
});
```
```

`@forge/bridge` only performs requests authorized as the user (`asUser`). Requests that need to authorize as the app (`asApp`) still require `@forge/api` and must be called from a resolver. `@forge/bridge` also does not support `requestBitbucket` or `requestGraph` yet, so a resolver is required to call these APIs as well.

## Changes to export view

In order for UI Kit macros to export to word document, page history, or via the REST API, you need to specify an `adfExport` function in your app's `manifest.yml` file. This function should return a representation of the macro in [Atlassian document format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).

Previously on UI Kit 1, macros would export without an `export` function defined. Due to technical limitations, this is not the case for UI Kit. You must define an `adfExport` function in your app's `manifest.yml` file in order for the macro to export successfully for all export types, with the exception of pdf export.

If your app has an `export` property in the manifest, you need to rename it to `adfExport` and update the underlying export function accordingly.

##### UI Kit 1 manifest excerpt

```
```
1
2
```



```
modules:
  macro:
    export:
        function: exportFunction
  function:
    - key: exportFunction
      handler: index.macroExport
```
```

##### UI Kit manifest excerpt

```
```
1
2
```



```
modules:
  macro:
    adfExport:
        function: exportFunction
  function:
    - key: exportFunction
      handler: index.macroExport
```
```

Here is an example of an update to the `export` function that you might make:

##### UI Kit 1 export function

```
```
1
2
```



```
import ForgeUI, { render, Text } from "@forge/ui";

export const macroExport = render(
    <Text>`Hello world! This is the export view for my macro.`</Text>
);
```
```

##### UI Kit adfExport function

```
```
1
2
```



```
import { doc, p } from '@atlaskit/adf-utils/builders';

export const macroExport = async (payload) => {
    return doc(
        p(`Hello world! This is the export view for my macro.`)
    );
}
```
```

## Migration example

Check out this [migration example](/platform/forge/ui-kit/migration-example) where the Issue Translation UI Kit 1 app is transformed into UI Kit.

## Migrating a published UI Kit 1 app

If you are migrating a published UI Kit 1 app, keep the same app ID to retain your license.
