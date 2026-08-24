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
1import { useNavigate } from '@forge/react/router';
2
```

Here is an example of an app that uses `useNavigate` to navigate between pages.

```
1import ForgeReconciler, { Button, Text, Heading } from '@forge/react';
2import { Router, Route, useNavigate } from '@forge/react/router';
3
4const HomePage = () => {
5  const navigate = useNavigate();
6  return (
7    <>
8      <Heading as="h1">Home</Heading>
9      <Text>Welcome to the app!</Text>
10      <Button appearance="primary" onClick={() => navigate('/settings')}>
11        Go to Settings
12      </Button>
13    </>
14  );
15};
16
17const SettingsPage = () => {
18  const navigate = useNavigate();
19  return (
20    <>
21      <Heading as="h1">Settings</Heading>
22      <Button onClick={() => navigate('/')}>Back to Home</Button>
23    </>
24  );
25};
26
27const App = () => (
28  <>
29    <Route path="/">
30      <HomePage />
31    </Route>
32    <Route path="/settings">
33      <SettingsPage />
34    </Route>
35  </>
36);
37
38ForgeReconciler.render(
39  <Router>
40    <App />
41  </Router>
42);
43
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
3
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
3
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
3
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
3
4
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
3
4
```



```
// Current path: /settings/general
const navigate = useNavigate();
navigate('../advanced'); // Navigates to /settings/advanced
```
```
