# view

The `view` object refers to the context in which a resource is loaded. For example, a modal.

## close

The `close` method enables you to request the closure of the current view. For example, close a modal.

### Function signature

```
1
function close(): Promise<void>;
```

### Example

```
1
2
3
import { view } from "@forge/bridge";

view.close();
```

## submit

The `submit` method enables you to request form submission on the
[Jira custom field edit](/platform/forge/manifest-reference/modules/jira-custom-field/#editing),
[Jira custom field type edit](/platform/forge/manifest-reference/modules/jira-custom-field-type/#editing), and
[Jira context configuration](/platform/forge/manifest-reference/modules/jira-custom-field-type/#configuration) views.

The `submit` method throws an error if the submission fails.

### Function signature

```
1
function submit(payload: mixed): Promise<void>;
```

Where the `payload` shape is defined by the requirements of the views.

### Example

This example shows how to request form submission on a Jira custom field edit.

```
```
1
2
```



```
import { view } from "@forge/bridge";

const onSubmit = async () => {
  const fieldValue = "new-value";
  try {
    return await view.submit(fieldValue);
  } catch (e) {
    // Handle the error
  }
};
```
```

## getContext

The `getContext` method enables you to retrieve contextual information for your Custom UI app.

### Function signature

```
```
1
2
```



```
function getContext(): Promise<Context>;

interface Context {
  accountId?: string;
  cloudId?: string;
  extension: ExtensionData;
  license?: LicenseDetails;
  localId: string;
  locale: string;
  moduleKey: string;
  siteUrl: string;
  timezone: string;
}

interface ExtensionData {
  [k: string]: any;
}

interface LicenseDetails {
  active: boolean;
  billingPeriod: string;
  ccpEntitlementId: string;
  ccpEntitlementSlug: string;
  isEvaluation: boolean;
  subscriptionEndDate: string | null;
  supportEntitlementNumber: string | null;
  trialEndDate: string | null;
  type: string;
}
```
```

### Returns

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";

const context = await view.getContext();
```
```

## createHistory

The `createHistory` method enables your UI Kit and Custom UI app to manipulate the current page URL for routing
within full page apps.

When using this API, the `path` and `location` properties are always relative to your app's URL.

The `createHistory` method is only available in the following modules:

[Learn how to add routing to a full page app with React Router](/platform/forge/add-routing-to-a-full-page-app/).

### Function signature

```
```
1
2
```



```
type LocationDescriptor = {
  pathname: string;
  search?: string;
  hash?: string;
  state?: any;
};
type UnlistenCallback = () => void;
type Action = "POP" | "PUSH" | "REPLACE";

function createHistory(): Promise<{
  action: Action;
  location: LocationDescriptor;
  push(path: string, state?: any): void;
  push(location: LocationDescriptor): void;
  replace(path: string, state?: any): void;
  replace(location: LocationDescriptor): void;
  go(n: number): void;
  goBack(): void;
  goForward(): void;
  listen(
    listener: (location: LocationDescriptor, action: Action) => void
  ): UnlistenCallback;
}>;
```
```

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";

const history = await view.createHistory();

// e.g. URL begins as http://example.atlassian.net/example/apps/abc/123

history.push("/page-1");
// this updates the URL to http://example.atlassian.net/example/apps/abc/123/page-1

history.push("/page-2");
// this updates the URL to http://example.atlassian.net/example/apps/abc/123/page-2

history.go(-2);
// this updates the URL to http://example.atlassian.net/example/apps/abc/123
```
```

## refresh

The `refresh` method enables you to fetch the data for the parent page again,
without performing a full-page reload.

The `refresh` method is only available for certain Atlassian apps. You will see the error
*this resource's view is not refreshable* if the `refresh` method is not available.

At the moment, it can be used by the following modules:

### Function signature

```
```
1
2
```



```
function refresh(): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";

view.refresh();
```
```

## theme

The `theme` object includes the method to enable theming. View the [Design Tokens and Theming page](/platform/forge/design-tokens-and-theming/) for more details.

### enable

The `theme.enable` method enables theming in the Forge app. This will fetch the current active theme from the host environment (e.g. Jira) and apply it in your app. It will also reactively apply theme changes that occur in the host environment so that your app and the host are always in sync.

### Function signature

```
```
1
2
```



```
function enable(): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";

await view.theme.enable();
```
```

```
```
1
2
```



```
// Example usage in a React app
// Make sure to call enable() before the app is mounted for tokens to be available before the first render
view.theme.enable().then(() => {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById("root")
  );
});
```
```

## changeWindowTitle

The `changeWindowTitle` method enables you to change the title of the current document in the following Jira modules: global page, admin page, project settings page, and project page.

### Function signature

```
```
1
2
```



```
function changeWindowTitle(newTitle: string): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";

await view.changeWindowTitle("New title");
```
```

## emitReadyEvent

The `emitReadyEvent` function notifies Confluence that a Forge macro has completed loading and is ready for export or further processing. This enables Confluence or other consumers, such as our PDF export service, to reliably detect when macros are fully loaded, rather than relying on DOM scanning or timing heuristics.

This function is part of the `@forge/bridge` library and leverages the [Forge Events API](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/events/#events) to emit an `EXTENSION_READY` event, including contextual information about the macro or extension that triggered it.

### Function signature

```
```
1
2
```



```
function emitReadyEvent(): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { view } from "@forge/bridge";
import { useEffect, useState } from "react";

const MyMacro = () => {
  const [data, setData] = useState();

  useEffect(() => {
    const loadData = async () => {
      const result = await fetchData();
      setData(result);
      // Perform any other operations your macro requires
      await view.emitReadyEvent(); // Notify that the macro is ready
    };

    loadData();
  }, []);

  return <div>{data ? "Macro content loaded" : "Loading..."}</div>;
};

export default MyMacro;
```
```
