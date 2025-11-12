# Forge resolver

The Forge resolver enables you to define backend functions, and handle asynchronous events
for your UI Kit and Custom UI apps.
Your backend functions must be defined in the `src` directory of your Forge app. You must then refer to your resolver in the manifest.

Invoke your resolver functions in your frontend assets using
the [invoke Forge UI bridge](/platform/forge/custom-ui-bridge/invoke/) method.

The `@forge/resolver` package is included in both Custom UI and UI Kit templates, so you don’t need to install it separately.

## Usage - UI Kit

Consider the following example `manifest.yml` file:

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
modules:
  jira:issuePanel:
    - key: hello-world-panel
      resource: example-resource
      resolver:
        function: issue-panel-resolver
      render: native
      title: Hello world!
      icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  function:
    - key: issue-panel-resolver
      handler: index.handler
resources:
  - key: example-resource
    path: src/frontend/index.jsx
```

This is the manifest declaration for a basic Jira issue panel using Forge resolver for UI Kit.

In this example:

* `resource` is a reference to a defined key in the resources object.
* `resolver` contains a function property, which references the function module that contains the handler for the resolver to use in your UI app.
* `render`: native to instruct the platform to render the app's UI from the components you've defined.
* `path` refers to the handler function specified in the `manifest.yml` file. This function serves as the entry point for the application, where the UI components are defined, and the app logic is executed.

Consider an example `src/frontend/index.jsx` file that contains the resolver function definitions:

```
```
1
2
```



```
import Resolver from '@forge/resolver';

const resolver = new Resolver();

resolver.define('getText', (req) => {
  console.log(req);
  return 'Hello, world!';
});

export const handler = resolver.getDefinitions();
```
```

In this example:

* A single resolver function is defined, with the string identifier "`getText`".
  * This function can be invoked from the UI app's frontend assets contained in `src/frontend/index.jsx`, by using the [invoke](/platform/forge/apis-reference/ui-api-bridge/invoke/) Forge bridge method.

Continuing this example, the following code invokes the "`getText`" function defined above:

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
  const [data, setData] = useState(null);
  useEffect(() => {
    invoke('getText', { example: 'my-invoke-variable' }).then(setData);
  }, []);
  return (
    <>
      <Text>Hello world!</Text>
      <Text>{data ? data : 'Loading...'}</Text>
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

Including this code in an appropriate location in your frontend assets would result in `"Hello, World!"` appearing in your browser console.

## Usage - Custom UI

Consider the following example `manifest.yml` file:

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: hello-world-panel
      resource: example-resource
      resolver:
        function: issue-panel-resolver
      title: Hello world!
      icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  function:
    - key: issue-panel-resolver
      handler: index.handler
resources:
  - key: example-resource
    path: static/hello-world/build
```
```

This is the manifest declaration for a basic Jira issue panel using Custom UI and
the Custom UI resolver. In this example:

* `resource` is a reference to a defined key in the `resources` object.
* `resolver` contains a function property, which references the function module that contains the handler for the resolver to use in your UI app.
* `path` relative path to the directory of static assets for the resource. It must contain the `index.html` entry point for the Custom UI app; in this case, `static/hello-world/build/index.html`.

Consider an example `src/index.js` file that contains the resolver function definitions:

```
```
1
2
```



```
import Resolver from "@forge/resolver";

const resolver = new Resolver();

resolver.define("exampleFunctionKey", ({ payload, context }) => {
  return { example: `Hello, ${payload.name}!` };
});

export const handler = resolver.getDefinitions();
```
```

In this example:

* A single resolver function is defined, with the string identifier `"exampleFunctionKey"`.
  * This function can be invoked from the Custom UI app's frontend assets contained in
    `static/hello-world`, by using the [invoke](/platform/forge/apis-reference/ui-api-bridge/invoke/) Forge bridge method.

Continuing this example, the following code invokes the `"exampleFunctionKey"` function defined above:

```
```
1
2
```



```
import { invoke } from "@forge/bridge";

invoke("exampleFunctionKey", { name: "World" }).then((returnedData) =>
  console.log(returnedData.example);
);
```
```

Including this code in an appropriate location in your frontend assets would result in `"Hello, World!"`
appearing in your browser console.

## Type-safe invocations

When using TypeScript, you can reuse the types between the backend and frontend
code to make invocations type-safe.

Type safety prevents accidental mistakes when developing the application. It is
not a security mechanism: if another part of the application or a third-party
library uses type overrides like `any`, the error will not be caught at runtime.
Sensitive data should be validated separately.

### Definitions

To create a type-safe interface between the resolver and
[bridge](/platform/forge/apis-reference/ui-api-bridge/invoke), create a shared
type definition file and use it in both the UI and backend code.

In the shared definition file, declare a type with all the operations the UI can
perform, for example, `src/shared/types.ts`:

```
```
1
2
```



```
export type Defs = {
  getPrice: (args: { product: string; }) => { price: number };
  setPrice: (args: { product: string; price: number; }) => void;
  listProducts: () => { products: string[] };
};
```
```

Do not add the arguments for `payload`, `context` or `Promise` in the result
type. The correct types will be derived automatically when defining the
resolver.

Since the shared definitions file will be imported in both the UI and backend
code, you cannot import backend-only or frontend-only modules there (e.g.
`@forge/api` or `@forge/bridge`). We recommend only keeping the type definitions
in the shared file, and keeping the complex logic in the respective backend or
frontend files.

### Resolver

Now you can define the resolver:

```
```
1
2
```



```
import { makeResolver } from '@forge/resolver';

import { Defs } from './shared/types';

export const handler = makeResolver<Defs>({
  async getPrice(request) {
    const { product } = request.payload;
    return { price: 100 };
  },
  async setPrice(request) {
    const { product, price } = request.payload;
  },
  async listProducts() {
    return { products: ['product1', 'product2'] };
  }
});
```
```

For each function, the expected handler type is:

```
```
1
2
```



```
type Handler<Args, Return> = (request: { payload: Args; context: Context }) => Promise<Return>;
```
```

The definition will fail to compile if not all the functions described in the
shared definition are implemented, or their arguments or return values are
incorrect. When using an IDE, autocomplete will suggest possible function names
to define, members for `payload` parameters, and return types.

### UI

Now the same definition can be used to invoke the resolver functions from the
UI:

```
```
1
2
```



```
import { makeInvoke } from '@forge/bridge';

import { Defs } from '../shared/types';

const invoke = makeInvoke<Defs>();

const { products } = await invoke('listProducts');
const result = await invoke('getPrice', { product: products[0]});
console.log(result.price);
```
```

Just like on the backend, invoking the wrong functions, providing incorrect
arguments or expecting a different return types will result in a compilation
error. The function names, parameters and return value will be autocompleted in
an IDE too.

## Methods

### Resolver

The `Resolver` class is the default export of `@forge/resolver` that contains two methods.

#### define

The `define` method is used to define individual resolver functions, identified by a `functionKey`.

##### Function signature

```
```
1
2
```



```
type Context = {
  accountId?: string;
  accountType?: 'licensed' | 'unlicensed' | 'customer' | 'anonymous';
  cloudId?: string;
  workspaceId?: string;
  localId: string;
  installContext: string;
  environmentId: string;
  environmentType: string;
  extension: {
    config?: { [key: string]: any } // defined for macro extensions
    [key: string]: any;
  },
  installation?: {
    ari: {
      installationId: string;
      toString: () => string;
    },
    contexts: [
      {
        cloudId?: string,
        workspaceId?: string,
        toString: () => string
      }
    ]
  }
};

function define(
  functionKey: string,
  cb: (request: {
    payload: { [key in number | string]: any;},
    context: Context
  }) => Promise<{ [key: string]: any } | string | void> | { [key: string]: any } | string | void,
): this
```
```

##### Arguments

* **functionKey**: A string identifier for the resolver function. This string must exactly match the
  `functionKey` used to [invoke](/platform/forge/apis-reference/ui-api-bridge/invoke/) this
  function in your frontend assets.
* **cb**: The callback to be run when the invoke function is called with the matching `functionKey`.
  The return value of this callback will be returned from the invoke function in your frontend assets.
  This callback will have the following data passed into its first argument:
  * **payload**: Data passed in from the `payload` parameter of the invoke function.
  * **context**:
    * **accountId:** The Atlassian ID or JSM Customer ID of the user that interacted with the component.
    * **accountType:** The account type of the user that interacted with the component, one of: `licensed`, `unlicensed`, `customer`, or `anonymous`.
      Note, this field is mainly intended to be used in components that permit access by users without corresponding Atlassian app license.
    * **cloudId:** The ID of the application on which the extension is working, for example the ID of a Jira or Confluence instance.
    * **workspaceId:** The ID of the workspace on which the extension is working.
    * **localId:** The unique ID for this instance of this component in the content.
    * **environmentId:** The unique ID of the [environment](/platform/forge/environments-and-versions/) where the component is deployed.
    * **environmentType:** The name of the [environment](/platform/forge/environments-and-versions/) where the component is deployed.
    * **installContext**: The ARI identifying the cloud or Atlassian app context of this component installation.
    * **installation**: A summary of the app installation, including the installation ARI and the contexts where the app is installed.

Additional contextual information for your Custom UI app. The data available in the `extension` property depends on the module in which your Custom UI resolver is used. Note that **context** is similar to [Platform Context](/platform/forge/ui-kit-hooks-reference/#returns-3), although it's not a 1-to-1 mapping.

* Not all of the values in the `context` parameter are guaranteed to be secure, unalterable, and valid to be used for authorization. See
  [App context security](/platform/forge/app-context-security/) for more information.

#### getDefinitions

The `getDefinitions` method returns the invocation function handler that can be used as the handler
for the function referenced by the `resolver` key in eligible modules.

##### Function signature

```
```
1
2
```



```
  function getDefinitions(): InvocationHandler
```
```

### makeResolver

The `makeResolver` function defines a resolver in one step using type-safe
definitions. It accepts a type parameter describing the interface with the
bridge and an object defining the functions corresponding to that interface.

#### Function signature

```
```
1
2
```



```
function makeResolver<D extends Definitions>(handlers: Handlers<D>): DefinitionsHandler;
```
```

The `Definitions`, `Handlers` and associated types ensure the provided functions
correctly implement the interface.
