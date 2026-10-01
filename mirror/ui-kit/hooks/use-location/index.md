# useLocation (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

This hook returns the current location object, which contains information about the current URL. It
updates automatically when the user navigates to a different route.

It must be used within a [Router](/platform/forge/ui-kit/components/router/) component.

## Usage

To add the `useLocation` hook to your app:

```
1import { useLocation } from '@forge/react/router';
2
```

Here is an example of an app that displays the current path using `useLocation`.

```
1import ForgeReconciler, { Text, Code } from '@forge/react';
2import { Router, Route, useLocation } from '@forge/react/router';
3
4const CurrentPath = () => {
5  const location = useLocation();
6  return (
7    <Text>
8      Current path: <Code>{location.pathname}</Code>
9    </Text>
10  );
11};
12
13const App = () => (
14  <>
15    <Route path="*">
16      <CurrentPath />
17    </Route>
18  </>
19);
20
21ForgeReconciler.render(
22  <Router>
23    <App />
24  </Router>
25);
26
```

### Function signature

```
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
```



```
import type { Location } from 'history';

function useLocation(): Location;

interface Location {
  pathname: string;
  search: string;
  hash: string;
  key: string;
}
```
```

### Arguments

None.

### Returns

* **Location:** An object representing the current URL location with the following properties:
  * **pathname** (`string`): The current URL path (e.g. `/settings`).
  * **search** (`string`): The query string portion of the URL, including the leading `?`
    (e.g. `?filter=active`). Empty string if there is no query string.
  * **hash** (`string`): The hash portion of the URL, including the leading `#` (e.g. `#section`).
    Empty string if there is no hash.
  * **key** (`string`): A unique key identifying this location.
