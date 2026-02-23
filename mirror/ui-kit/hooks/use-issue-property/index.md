# useIssueProperty

This hook reads, writes, or updates the
[issue properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/)
in the Jira issue where the app is installed.

When using this event, your Forge app must have permission from the site admin to access the data
it provides within the event payload. The OAuth scope required are: `read:jira-work`, `write:jira-work`

Running the `forge lint` command picks up these required scopes.

### Usage

To add the `useIssueProperty` hook to your app:

```
1
import { useIssueProperty } from "@forge/react";
```

Avoid calling `useIssueProperty` multiple times in the same app, since their outputs are not synced.

Here is an example of an app that stores information in an issue property with `useIssueProperty`.

![The app display on a Jira issue](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/useissueproperty-concrete-value-update.png?_v=1.5800.1875)

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
import ForgeReconciler, { Button, Heading, Inline, useIssueProperty } from '@forge/react';

const App = () => {
  const [number, setNumber, deleteNumber] = useIssueProperty('number', '<Click me>');
  const setRandomInt = async () => {
    const randomInt = Math.floor(Math.random() * 10);
    await setNumber(randomInt);
  };
  return (
    <>
      <Heading as='h3'>Issue Property</Heading>
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

Here's another example that updates the issue property based on the current value stored in the
property.

![The app display on a Jira issue](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/useissueproperty-setter-function-update.png?_v=1.5800.1875)

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Button, Heading, Inline, useIssueProperty } from '@forge/react';

const App = () => {
  const [count, setCount, deleteCount] = useIssueProperty('count', 0);
  const increaseCount = async () => await setCount((c) => (c+1));

  return (
    <>
      <Heading as='h3'>Issue Property</Heading>
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
function useIssueProperty<V>(
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

* **key:** The key for the issue property. The key is namespaced automatically and stored with
  a key of form `forge-${key}`.
* **defaultValue:** The default value to use if the issue property does not exist yet.

### Returns

* An array of three elements:
  * The first element is the current value of the property (or default value if the property does not exist). Note that this value takes time to load, so it will initially be `undefined` before its actual value is loaded into this variable.
  * The second element is an asychronous function used to update the property. The update may run for multiple times per function call if the previous attempts fail (due to other updates). A second optional value specifies the number of retries to attempt (default is 2). There are two ways to use this:

    * Provide a new value, which will create or replace the property.
    * Provide an updater function, which takes the current value stored in the property and returns an updated value to store.

    When updating a property based on its previous state, make sure to pass in the calculation as an updater function. This ensures that its new value is calculated based on the most recent value in the cloud, rather than the cached value on the users' device.
  * The third element is an asychronous function that can be used to delete the property.

##
