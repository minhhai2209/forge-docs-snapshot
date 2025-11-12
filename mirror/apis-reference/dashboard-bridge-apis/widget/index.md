# widget (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://developer.atlassian.com/platform/forge/eap-preview-ga/#early-access-program-eap).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

Use the `widget` APIs for dashboard widget view operations.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

## Setting preview configuration

Sets the preview configuration for the widget that appears when selected in the [widget list](/platform/forge/manifest-reference/modules/dashboard-widget/#widget-list). The configuration object replaces `config` in [useWidgetConfig](/platform/forge/ui-kit/hooks/use-widget-config/) when the widget is rendered as a preview.

#### Usage

```
1
2
3
4
5
6
import { widget } from "@forge/dashboards-bridge";

widget.setPreviewConfig({
  title: "Preview Title",
  description: "This is a preview configuration",
});
```

**Parameters:**

* **previewConfig** (WidgetConfig): The preview configuration object

#### Method signature

```
```
1
2
```



```
function setPreviewConfig(previewConfig: WidgetConfig): void;

type WidgetConfig = Record<string, unknown>;
```
```
