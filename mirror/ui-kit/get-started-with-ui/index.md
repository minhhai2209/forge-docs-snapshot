# User interface overview

Forge offers two ways to build user interfaces for your apps:

1. [UI Kit](/platform/forge/ui-kit/) is a React-based framework that allows you to enhance Atlassian apps on Forge. By using React primitives to natively render app components within our Atlassian apps, UI Kit allows your app to use many of the same platform components, and APIs that are used by internal teams.
2. [Custom UI](/platform/forge/custom-ui/) allows you full control in building the app’s user interface. Custom UI runs
   within an iframe, providing an isolated environment for the app's interface to be displayed.

Let's look at the fundamental elements of building user interfaces with Forge, namely the [Atlassian app APIs](#atlassian-app-apis) and [components](#components). We'll also explore how to declare and use [resources](#resource) and [resolvers](#resolver), which are the key concepts in UI development.

UI Kit relies only on the `@forge/react` components and does not directly rely on React DOM. Therefore, functionalities dependent on standard browser DOM elements, like custom HTML, portals, and forwarding refs, may not work as expected.

## Atlassian app APIs

API requests to Atlassian apps can be made in the frontend using `@forge/bridge`, typically in your
`App.js` file. For more information, see
[Forge bridge APIs](/platform/forge/apis-reference/ui-api-bridge/bridge/).

## Components

User interfaces can be built using [components](/platform/forge/ui-kit/components/).
These are native and reusable building blocks created to streamline the development of user interfaces.

## Resource

[Resource](/platform/forge/manifest-reference/resources/) allows you to define your own user interface using static resources, such as HTML, CSS, JavaScript, and images.

UI Kit allows only images. However, in the case of Custom UI, there are no restrictions on loading any of the previously mentioned resources.

### Dependencies

UI Kit expects your app to have the following dependencies installed at the top-level directory:

```
```
1
2
```



```
npm i react@18
npm i @forge/react@latest
```
```

### File structure

In UI Kit, the following directory and UI entry point file should be added to your app `/src` folder:

```
```
1
2
```



```
/src
  /frontend
    /index.jsx
```
```

In Custom UI, the following directory and UI entry point file should be added to your app `/src` folder:

The specified folder structure `/static/src/index.js` is not mandatory; instead, ensure that the `index.html` file is located at the path specified in your resource's configuration.

```
```
1
2
```



```
/static
  /src
    /index.js
```
```

### React app

In UI Kit, the React dependencies should be imported, and the Forge render method should be called in the
`/src/frontend/index.jsx` file of your app.

```
```
1
2
```



```
import React, { useEffect } from  'react';
import ForgeReconciler, { Box, Text } from  '@forge/react';

const App = () => (
  <Box>
    <Text>Hello, world!</Text>
  </Box>
)

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

In Custom UI, the React dependencies should be imported, and the `ReactDOM` render method should be called in the `/static/src/index.js` file of your app.

```
```
1
2
```



```
import React from 'react';
import ReactDOM from 'react-dom';

const App = () => (
  <div>
    Hello, world!
  </div>
)

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
```
```

### Manifest definition

A [resource](/platform/forge/manifest-reference/resources/) should be declared in the
[app manifest](/platform/forge/manifest-reference/).

```
```
1
2
```



```
resources:
- key: frontend
  path: src/frontend/index.tsx
```
```

## Resolver

[Resolver](/platform/forge/runtime-reference/forge-resolver/) enables you to define backend functions for your UI Kit and Custom UI apps.

The following dependency should be installed at the top-level directory of your app:

### Dependencies

```
```
1
2
```



```
npm i @forge/resolver@latest
```
```

### File structure

The following directory and UI entry point file should be added to your app `/src` folder:

```
```
1
2
```



```
/src
  /backend
    /index.js
```
```

### Handler

The resolver dependency should be imported, and your resolvers defined in your app `/src/backend/index.js` file.

```
```
1
2
```



```
import Resolver from '@forge/resolver';
const resolver = new Resolver();

resolver.define('my-example', async (req) => {
  return {
    data: 'Hello, world',
  }
});

export  const  handler  =  resolver.getDefinitions();
```
```

### Manifest definition

A [function](/platform/forge/manifest-reference/modules/function/) should be declared in the
[app manifest](/platform/forge/manifest-reference/).

```
```
1
2
```



```
modules:
  function:
    - key: backend
      handler: index.handler
```
```

## Attach a UI resource and resolver to an extension point

To integrate your app, it needs to be declared in a
[module](/platform/forge/manifest-reference/modules/). Modules necessitate a `resource`, `resolver`,
and a `render` mode to display UI in a Atlassian app.

```
```
1
2
```



```
modules:
  macro:
  - key: example
    title: Example Macro
    resource: frontend
    resolver:
      function: backend
```
```

## Next steps

Explore [example apps](/platform/forge/user-interface/#example-apps)
and [tutorials](/platform/forge/user-interface/#tutorials) for various Atlassian apps
to start creating apps using UI Kit.
