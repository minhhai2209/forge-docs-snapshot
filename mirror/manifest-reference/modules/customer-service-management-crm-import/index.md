# Customer Service Management CRM import (EAP)

Forge’s EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The `customerServiceManagement:crmImport` module adds an item under the **Manage** dropdown on the **Customers**, **Organizations**, and **Products** pages of a Customer Service Management space. When the item is clicked, content is rendered inside a modal dialog. This module is intended for apps that import customer context data from external CRM systems (for example, HubSpot, Zendesk, or Salesforce) into Customer Service Management.

This module can be used in Customer Service Management.

![Item under the Manage dropdown on the Customers page](https://dac-static.atlassian.com/platform/forge/snippets/images/csm-crm-import-demo-dropdown.png?_v=1.5800.2143)

![Modal opened by clicking the item, rendering the Forge app content](https://dac-static.atlassian.com/platform/forge/snippets/images/csm-crm-import-demo-modal.png?_v=1.5800.2143)

For a high-level guide and pointers to product-specific integration patterns, see [Import customer context data with a Forge app](/platform/forge/csm-import-data/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the modal, which is displayed at the top of the modal. The title also appears as an item under the **Manage** dropdown on the **Customers**, **Organizations**, and **Products** pages.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `location` | `string` | The full URL of the host page where this module is displayed. |
