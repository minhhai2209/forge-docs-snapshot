# Router (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

To add the `Router` and `Route` components to your app:

```
1
import { Router, Route } from '@forge/react/router';
```

## Description

The `Router` component provides client-side routing for Forge UI Kit full page apps. It initializes a
history instance using the Forge bridge and manages navigation state, allowing you to define routes and
navigate between different views within your app without full page reloads.

`Router` works together with the [Route](#route) component to render content based on the current URL path,
and with the [useNavigate](/platform/forge/ui-kit/hooks/use-navigate/),
[useLocation](/platform/forge/ui-kit/hooks/use-location/), and
[useParams](/platform/forge/ui-kit/hooks/use-params/) hooks to programmatically navigate and read
routing information.

## Supported modules

The `Router` component can be used in the following modules:

## Router props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeChildren` | Yes | The child elements to render within the router. Typically contains one or more `Route` components. |
| `fallback` | `ForgeNode` | No | Content to display while the router is initializing, or if an error occurs during initialization. Defaults to `null`. |

## Route

The `Route` component conditionally renders its children when the current URL path matches its `path`
prop. It must be used within a `Router` component.

When multiple `Route` components are placed as siblings inside a `Router`, only the first matching route
is rendered.

Route paths support three types of segments:

* **Static segments** — Match a path segment exactly (e.g. `/settings`).
* **Dynamic parameters** — Segments prefixed with `:` capture a value from the URL (e.g. `/posts/:id`).
  Use the [`useParams`](/platform/forge/ui-kit/hooks/use-params/) hook to read captured values.
* **Catch-all (`*`)** — Matches any remaining path segments. The matched remainder is available as `*`
  in the params object.

### Route props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | Yes | The URL path pattern to match against the current location. Supports static segments, dynamic parameters (e.g. `:id`), and a catch-all wildcard (`*`). |
| `children` | `ForgeChildren` | Yes | The content to render when the path matches the current location. |

## Examples

### Basic routing

Define multiple routes within a `Router`. Only the first matching `Route` is rendered.

```
```
1
2
```



```
import ForgeReconciler, { Text, Heading } from '@forge/react';
import { Router, Route } from '@forge/react/router';

const HomePage = () => (
  <>
    <Heading as="h1">Home</Heading>
    <Text>Welcome to the app!</Text>
  </>
);

const SettingsPage = () => (
  <>
    <Heading as="h1">Settings</Heading>
    <Text>Manage your preferences here.</Text>
  </>
);

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
```

### With a fallback

Use the `fallback` prop to show a loading indicator while the router initializes.

```
```
1
2
```



```
import ForgeReconciler, { Text, Spinner } from '@forge/react';
import { Router, Route } from '@forge/react/router';

const App = () => (
  <>
    <Route path="/">
      <Text>Home Page</Text>
    </Route>
  </>
);

ForgeReconciler.render(
  <Router fallback={<Spinner label="Loading..." />}>
    <App />
  </Router>
);
```
```

### Dynamic parameters

Use `:paramName` segments to capture dynamic values from the URL.

```
```
1
2
```



```
import ForgeReconciler, { Text } from '@forge/react';
import { Router, Route, useParams } from '@forge/react/router';

const PostDetail = () => {
  const { postId } = useParams();
  return <Text>Viewing post {postId}</Text>;
};

const App = () => (
  <>
    <Route path="/posts/:postId">
      <PostDetail />
    </Route>
  </>
);

ForgeReconciler.render(
  <Router>
    <App />
  </Router>
);
```
```

### Multiple dynamic parameters

Capture multiple values from the URL.

```
```
1
2
```



```
import ForgeReconciler, { Text } from '@forge/react';
import { Router, Route, useParams } from '@forge/react/router';

const CommentDetail = () => {
  const { postId, commentId } = useParams();
  return <Text>Post {postId}, Comment {commentId}</Text>;
};

const App = () => (
  <>
    <Route path="/posts/:postId/comments/:commentId">
      <CommentDetail />
    </Route>
  </>
);

ForgeReconciler.render(
  <Router>
    <App />
  </Router>
);
```
```

### Catch-all route (404 page)

Use a `*` path to catch any unmatched routes. Place it after all other routes. If a route path pattern ends with `/*`, it matches any characters following the `/`, including other `/` characters.

```
```
1
2
```



```
import ForgeReconciler, { Text } from '@forge/react';
import { Router, Route } from '@forge/react/router';

const App = () => (
  <>
    <Route path="/">
      <Text>Home</Text>
    </Route>
    <Route path="/settings">
      <Text>Settings</Text>
    </Route>
    <Route path="/*">
      <Text>Page not found</Text>
    </Route>
  </>
);

ForgeReconciler.render(
  <Router>
    <App />
  </Router>
);
```
```
