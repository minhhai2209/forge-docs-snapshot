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

## createAdfRendererIframeProps (EAP)

The `createAdfRendererIframeProps` method is now available as an Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18979).

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge embedded macros is governed by the Atlassian Developer Terms. Forge embedded macros are considered “Early Access Materials”, as set forth in Section 12 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

APIs and features under EAP are unsupported and subject to change without notice. APIs and features under EAP are not recommended for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Use `createAdfRendererIframeProps` when building a Custom UI bodied macro that needs to display its rich-text body content, including embedded Forge apps. This function generates the properties needed for an iframe element to render the ADF document type content of a Custom UI bodied macro.

### Prerequisites

### Function signature

```
```
1
2
```



```
interface FullContext {
  accountId?: string;
  cloudId?: string;
  workspaceId?: string;
  extension: ExtensionData;
  environmentId: string;
  environmentType: EnvironmentType;
  license?: LicenseDetails;
  localId: string;
}

function createAdfRendererIframeProps(
  context: FullContext,
  iframeId?: string
): Promise<{
  id: string;
  src: string;
  onLoad: () => void;
}>;
```
```

#### Arguments

* **context**: Contextual information for your Custom UI app taken from the [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) method or the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/#useproductcontext) hook. The ADF document is extracted from `context.extension.macro.body`.
* **iframeId**: You can optionally pass an iframe id. Otherwise, an iframe id will be created by default.

#### Returns

Returns an object with the following properties:

* **id**: id of the adf renderer wrapper iframe. The value of `id` will be the same as `iframeId` if `iframeId` was provided as an argument.
* **src**: src of the adf renderer wrapper iframe.
* **onLoad**: the onLoad function of the adf renderer wrapper iframe which will send the ADF document contents to the iframe once the iframe has initialised.

### Example

![Example rendered Custom UI bodied macro contents](https://dac-static.atlassian.com/platform/forge/apis-reference/ui-api-bridge/images/view/view-createAdfRendererIframeProps-custom-ui-bodied-macro.svg?_v=1.5800.1794)

```
```
1
2
```



```
import { view } from "@forge/bridge";

function App() {
  // Get the contents of the bodied macro
  const [context, setContext] = useState(null);
  const [iframe, setIframe] = useState(null);

  useEffect(() => {
    view.getContext().then(setContext);
  }, []);

  useEffect(() => {
    if (!context) return;
    // Generate properties for embedded content wrapper
    // Pass in the embedded contents to the function
    // macroBody - any Valid ADF document can be passed in.
    view.createAdfRendererIframeProps(context).then(({ id, src, onLoad }) =>
      // Required iframe props
      // id - id of the iframe so the wrapper knows where to send the embedded macro contents
      // src - src of the embedded content renderer
      // onLoad - sends embedded macro contents once iframe has initialised
      // You can apply any styling you like to the iframe
      setIframe(<iframe id={id} src={src} onLoad={onLoad} />)
    );
  }, [context]);
  return (
    <div>
      <h1>Embedded content</h1>
      {/* Render the embedded content where you want in your app */}
      {iframe || "Loading embedded content..."}
    </div>
  );
}
export default App;
```
```

You can split up the ADF document object inside `context.extension.macro.body` and use `view.createAdfRendererIframeProps` more than once in your Custom UI bodied macro app. However this will affect performance as an additional iframe will be created.

### Limitations

* **Confluence live pages**: This method is not supported in Confluence live pages (also known as whiteboards or live docs).
* **Connect macros**: Macros built with Atlassian Connect cannot be embedded.
* **Modals**: Modals in Custom UI embedded macros are not supported.

### Supported bridge methods

| Bridge methods | Supported in Forge embedded macros |
| --- | --- |
| events | yes |
| i18n | yes |
| invoke | yes |
| invokeRemote | yes |
| modal | yes |
| objectStore (EAP) | no |
| realtime (Preview) | no |
| requestBitbucket | N/A |
| requestConfluence | yes |
| requestJira | yes |
| requestRemote | no |
| router | yes |
| rovo (Preview) | yes |
| showFlag | yes |
| view | yes |
| getEditorContent | no |
| getMacroContent | no |
| updateMacroContent | no |
| updateBylineProperties | yes |
| Jira bridge APIs | N/A |
| Dashboard bridge APIs | N/A |
