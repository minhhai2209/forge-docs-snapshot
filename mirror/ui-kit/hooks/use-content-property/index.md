# useContentProperty

This hook reads, writes, or updates the
[content properties](https://developer.atlassian.com/cloud/confluence/confluence-entity-properties/)
in the Confluence page where the app is installed. Note that this hook is only for use on pages; to manage content properties on blog posts and other entities, use `@forge/bridge`'s [requestConfluence](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/requestConfluence/) function to connect to the [Confluence REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-content-properties/#api-blogposts-blogpost-id-properties-get).

When using this event, your Forge app must have permission from the site admin to access the data
it provides within the event payload. The OAuth scope required are: `read:page:confluence`, `write:page:confluence`

Running the `forge lint` command picks up these required scopes.

### Usage

To add the `useContentProperty` hook to your app:

```
1
import { useContentProperty } from "@forge/react";
```

Avoid calling `useContentProperty` multiple times in the same app, since their outputs are not synced.

Here is an example of an app that stores information in a content property with `useContentProperty`.

![The app display on a Confluence page](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/usecontentproperty-concrete-value-update.png?_v=1.5800.1779)

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
import React from 'react';
import ForgeReconciler, { Button, Heading, Inline, useContentProperty } from '@forge/react';

const App = () => {
  const [number, setNumber, deleteNumber] = useContentProperty('number', '<Click me>');
  const setRandomInt = async () => {
    const randomInt = Math.floor(Math.random() * 10);
    await setNumber(randomInt);
  };
  return (
    <>
      <Heading as='h3'>Content Property</Heading>
      <Inline>
        <Button onClick={setRandomInt}>{`Random number: ${number}`}</Button>
        <Button onClick={async () => await deleteNumber()}>Delete</Button>
      </Inline>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

Here's another example that updates the content property based on the current value stored in the
property.

![The app display on a Confluence page](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/usecontentproperty-setter-function-update.png?_v=1.5800.1779)

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Button, Heading, Inline, useContentProperty } from '@forge/react';

const App = () => {
  const [count, setCount, deleteCount] = useContentProperty('count', 0);
  const increaseCount = async () => await setCount((c) => (c+1));

  return (
    <>
      <Heading as='h3'>Content Property</Heading>
      <Inline>
        <Button onClick={increaseCount}>{`Clicks: ${count}`}</Button>
        <Button onClick={async () => await deleteCount()}>Delete</Button>
      </Inline>
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

### Function signature

```
```
1
2
```



```
function useContentProperty<V>(
  key: string,
  defaultValue: V
): [
  V,
  ((value: V | ((prevValue: unknown) => V), retries?: number) => Promise<V>),
  () => Promise<void>
];
```
```

### Arguments

* **key:** The key for the content property. The key is namespaced automatically and stored with
  a key of form `forge-${localId}-${key}`. Note that keys of the same name are not shared across different apps.
* **defaultValue:** The default value to use if the content property does not exist yet.

### Returns

* An array of three elements:
  * The first element is the current value of the property (or default value if the property does not exist). Note that this value takes time to load, so it will initially be `undefined` before its actual value is loaded into this variable.
  * The second element is an asychronous function used to update the property. The update may run for multiple times per function call if the previous attempts fail (due to other updates). A second optional value specifies the number of retries to attempt (default is 2). There are two ways to use this:

    * Provide a new value, which will create or replace the property.
    * Provide an updater function, which takes the current value stored in the property and returns an updated value to store.

    When updating a property based on its previous state, make sure to pass in the calculation as an updater function. This ensures that its new value is calculated based on the most recent value in the cloud, rather than the cached value on the users' device.
  * The third element is an asychronous function that can be used to delete the property.
