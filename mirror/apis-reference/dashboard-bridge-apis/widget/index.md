# widget

Use the `widget` APIs for dashboard widget view operations.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

## Setting preview configuration

Sets the preview configuration for the widget that appears when selected in the [widget list](/platform/forge/manifest-reference/modules/dashboard-widget/#widget-list). The configuration object replaces `config` in [useWidgetConfig](/platform/forge/ui-kit/hooks/use-widget-config/) when the widget is rendered as a preview.

#### Usage

```
1import { widget } from "@forge/dashboards-bridge";
2
3widget.setPreviewConfig({
4  title: "Preview Title",
5  description: "This is a preview configuration",
6});
7
```

**Parameters:**

* **previewConfig** (WidgetConfig): The preview configuration object

#### Method signature

```
```
1
2
3
4
```



```
function setPreviewConfig(previewConfig: WidgetConfig): void;

type WidgetConfig = Record<string, unknown>;
```
```
