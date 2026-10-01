# useParams (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

This hook returns an object containing the dynamic parameters extracted from the current URL, as
defined by the matching [Route](/platform/forge/ui-kit/components/router/#route) component's `path` prop.

It must be used within a [Route](/platform/forge/ui-kit/components/router/#route) component.

## Usage

To add the `useParams` hook to your app:

```
1import { useParams } from '@forge/react/router';
2
```

Here is an example of an app that uses `useParams` to display a post by its ID.

```
1import ForgeReconciler, { Text, Heading } from '@forge/react';
2import { Router, Route, useParams } from '@forge/react/router';
3
4const PostPage = () => {
5  const { id } = useParams();
6  return (
7    <>
8      <Heading as="h2">Post Detail</Heading>
9      <Text>Viewing post with ID: {id}</Text>
10    </>
11  );
12};
13
14const App = () => (
15  <>
16    <Route path="/">
17      <Text>Home Page</Text>
18    </Route>
19    <Route path="/posts/:id">
20      <PostPage />
21    </Route>
22  </>
23);
24
25ForgeReconciler.render(
26  <Router>
27    <App />
28  </Router>
29);
30
```

### Function signature

```
```
1
2
```



```
function useParams(): Record<string, string>;
```
```

### Arguments

None.

### Returns

* **Record<string, string>:** An object containing key-value pairs of the dynamic parameters from the
  matched route path. The keys correspond to the parameter names defined in the
  [Route](/platform/forge/ui-kit/components/router/#route) component's `path` prop (without the `:` prefix).

  For example, if the route path is `/posts/:postId/comments/:commentId` and the current URL is
  `/posts/42/comments/7`, the returned object will be `{ postId: '42', commentId: '7' }`.

  If the route uses a catch-all pattern (`*`), the matched remainder is available under the `*` key.
  For example, if the route path is `/files/*` and the current URL is `/files/docs/report.pdf`, the
  returned object will be `{ '*': 'docs/report.pdf' }`.
