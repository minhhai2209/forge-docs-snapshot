# widgetEdit

Use the `widgetEdit` APIs for dashboard widget edit operations and lifecycle management.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

## Handling custom save events

Registers a callback function that executes when the user saves the widget. Since the "Save" button is owned by the platform, you'll need to register this callback if you want to be notified when the user intends to save changes. This allows you to, for example, store the modifications on your own service.

#### Usage

```
1import { widgetEdit } from "@forge/dashboards-bridge";
2
3widgetEdit.onSave(async (config, { widgetId }) => {
4  console.log("Widget saved!", config, widgetId);
5  // Perform custom save logic here
6});
7
```

**Parameters:**

* **callback** (OnSave): Function called on widget save
  * **config** (WidgetConfig): Your widget configuration object
  * **widgetContext** (WidgetContext): Widget-specific context, including widgetId
  * **context** (Context): App context

#### Method signature

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
function onSave(callback: OnSave): void;

type OnSave = (
  config: WidgetConfig,
  widgetContext: Omit<WidgetContext, "widgetId"> & { widgetId: string },
  context: Context,
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
  * **widgetContext** (WidgetContext): Widget-specific context
  * **context** (Context): App context
  * **returns** (WidgetConfig | null | undefined): Config to save, or `null`/`undefined` to skip product save

#### Method signature

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
```



```
function onProductSave(callback: OnProductSave): void;

type OnProductSave = (
  config: WidgetConfig,
  widgetContext: WidgetContext,
  context: Context,
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
3
4
5
6
7
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
  * **widgetContext** (WidgetContext): Widget-specific context
  * **context** (Context): App context

#### Method signature

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
function onSaveError(callback: OnSaveError): void;

type OnSaveError = (
  error: Error,
  widgetContext: WidgetContext,
  context: Context,
) => void;
```
```
