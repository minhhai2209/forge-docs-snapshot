# useNavigate (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

This hook returns a function that lets you programmatically navigate to different routes in your app.
It must be used within a [Router](/platform/forge/ui-kit/components/router/) component.

## Usage

To add the `useNavigate` hook to your app:

```
1
import { useNavigate } from '@forge/react/router';
```

Here is an example of an app that uses `useNavigate` to navigate between pages.

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
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
import ForgeReconciler, { Button, Text, Heading } from '@forge/react';
import { Router, Route, useNavigate } from '@forge/react/router';

const HomePage = () => {
  const navigate = useNavigate();
  return (
    <>
      <Heading as="h1">Home</Heading>
      <Text>Welcome to the app!</Text>
      <Button appearance="primary" onClick={() => navigate('/settings')}>
        Go to Settings
      </Button>
    </>
  );
};

const SettingsPage = () => {
  const navigate = useNavigate();
  return (
    <>
      <Heading as="h1">Settings</Heading>
      <Button onClick={() => navigate('/')}>Back to Home</Button>
    </>
  );
};

const App = () => (
  <>
    <Route path="/">
      <HomePage />
    </Route>
    <Route path="/settings">
      <SettingsPage />
    </Route>
  </>
);

ForgeReconciler.render(
  <Router>
    <App />
  </Router>
);
```

### Function signature

```
```
1
2
```



```
function useNavigate(): NavigateFunction;

type NavigateFunction = (to: string | number, options?: NavigateOptions) => void;

interface NavigateOptions {
  replace?: boolean;
}
```
```

### Arguments

None.

### Returns

* **NavigateFunction:** A function you can call to navigate to a different route. It accepts:
  * **to** (`string | number`): The destination to navigate to.
    * If a `string`, it is treated as a path. Absolute paths (starting with `/`) navigate directly
      from the base path of the app.
      Relative paths are resolved against the current location (e.g. `settings` appends to the
      current path, `../other` navigates up one level).
    * If a `number`, it navigates through the history stack (e.g. `-1` goes back one entry, `1` goes forward).
  * **options** (`NavigateOptions`, optional): An object with the following properties:
    * **replace** (`boolean`): If `true`, the current entry in the history stack is replaced instead of
      adding a new entry. Defaults to `false`.

### Examples

#### Navigate to an absolute path

```
```
1
2
```



```
const navigate = useNavigate();
navigate('/settings');
```
```

#### Navigate with replace

Replace the current history entry instead of pushing a new one.

```
```
1
2
```



```
const navigate = useNavigate();
navigate('/login', { replace: true });
```
```

#### Navigate back in history

```
```
1
2
```



```
const navigate = useNavigate();
navigate(-1); // Go back one step
```
```

#### Navigate with a relative path

When the path does not start with `/`, it is treated as relative to the current path. A plain segment
is appended to the current path, while `..` navigates up one level.

```
```
1
2
```



```
// Current path: /settings
const navigate = useNavigate();
navigate('general'); // Navigates to /settings/general
```
```

```
```
1
2
```



```
// Current path: /settings/general
const navigate = useNavigate();
navigate('../advanced'); // Navigates to /settings/advanced
```
```
