# widgetEdit (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://developer.atlassian.com/platform/forge/eap-preview-ga/#early-access-program-eap).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

Use the `widgetEdit` APIs for dashboard widget edit operations and lifecycle management.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

## Handling custom save events

Registers a callback function that executes when the user saves the widget. Since the "Save" button is owned by the platform, you'll need to register this callback if you want to be notified when the user intends to save changes. This allows you to, for example, store the modifications on your own service.

#### Usage

```
1
2
3
4
5
6
import { widgetEdit } from "@forge/dashboards-bridge";

widgetEdit.onSave(async (config, { widgetId }) => {
  console.log("Widget saved!", config, widgetId);
  // Perform custom save logic here
});
```

**Parameters:**

* **callback** (OnSave): Function called on widget save
  * **config** (WidgetConfig): Your widget configuration object
  * **widgetContext** (WidgetContext) Widget-specific context, including widgetId
  * **context**: (Context): App context

#### Method signature

```
```
1
2
```



```
function onSave(callback: OnSave): void;

type OnSave = (
  config: WidgetConfig,
  widgetContext: Omit<WidgetContext, "widgetId"> & { widgetId: string },
  context: Context
) => Promise<void>;
```
```

## Handling in-product save events

Registers a callback that executes before the widget is saved in the product. Use this to transform config data or prevent product-level saves. Since the "Save" button is owned by the platform, you'll need to register this callback if you want to save the changes made by the user (or other relevant information) in the product dashboard itself. By default, no data is saved.

#### Usage

```
```
1
2
```



```
import { widgetEdit } from "@forge/dashboards-bridge";

// Transform config before saving
widgetEdit.onProductSave(async (config) => {
  return {
    ...config,
    timestamp: Date.now(),
  };
});

// Prevent product save by returning null
widgetEdit.onProductSave((config) => {
  return null;
});
```
```

**Parameters:**

* **callback** (OnProductSave): Function called before product save
  * **config** (WidgetConfig): Your widget configuration object
  * **widgetContext** (WidgetContext) Widget-specific context
  * **context**: (Context): App context
  * returns **WidgetConfig | null | undefined**: Return the config to save, or `null`/`undefined` to skip product save

#### Method signature

```
```
1
2
```



```
function onProductSave(callback: OnProductSave): void;

type OnProductSave = (
  config: WidgetConfig,
  widgetContext: WidgetContext,
  context: Context
) => Promise<WidgetConfig | null | undefined>;
type WidgetConfig = Record<string, unknown>;
```
```

## Error handling

Registers a callback for handling save errors of the widget to the dashboard.

#### Usage

```
```
1
2
```



```
import { widgetEdit } from "@forge/dashboards-bridge";

widgetEdit.onSaveError((error, widgetContext, context) => {
  console.error("Save failed:", error.message);
  // Handle error appropriately
});
```
```

**Parameters:**

* **callback** (OnSaveError): Error handling function
  * **error** (Error): Error object
  * **widgetContext** (WidgetContext) Widget-specific context
  * **context**: (Context): App context

#### Method signature

```
```
1
2
```



```
function onSaveError(callback: OnSaveError): void;

type OnSaveError = (
  error: Error,
  widgetContext: WidgetContext,
  context: Context
) => void;
```
```
