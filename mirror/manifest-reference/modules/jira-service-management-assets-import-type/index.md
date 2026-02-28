# Jira Service Management assets import type

The `jiraServiceManagement:assetsImportType` module displays a modal that allows users to configure their Forge-based imports with information such as login details or configuration information for their app.

The modal appears when a user selects an object schema within Assets, then selects `Schema configuration`, then selects `Import`, then selects their import type, then selects `Configure App` in the dropdown.

The module also contains functions for optional use - onDeleteImport, startImport, stopImport, importStatus.

The content of the module is rendered below the text `Configure {Import Structure Name}` and above the `Save Configuration` and `Cancel` buttons.

This module can be used in Jira Service Management.

Unlicensed user access: This module does not support interaction with anonymous users, customer accounts, or unlicensed accounts.

![Example of an Assets Import Type](https://dac-static.atlassian.com/platform/forge/snippets/images/assets-import-type-demo.png?_v=1.5800.1881)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
|
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `description` | `string` or `i18n object` |  | A description of the Assets Import Type that displays under it.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `title` | `string` or `i18n object` | Yes | The name of an Assets Import Type, which is displayed on each of the import structure cards. They live on the `Imports` tab of each Object Schema in `Assets`.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` | Yes | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `onDeleteImport` | `{ function: string }` |  | Contains a `function` property, which is executed on deletion of an Assets Import Type. *Regex:* `^[a-zA-Z0-9_-]+$` |
| `startImport` | `{ function: string }` | Yes | Contains a `function` property, which is executed when an import of this Assets Import Type is started. *Regex:* `^[a-zA-Z0-9_-]+$` |
| `stopImport` | `{ function: string }` | Yes | Contains a `function` property, which is executed when an import of this Assets Import Type is cancelled. *Regex:* `^[a-zA-Z0-9_-]+$` |
| `importStatus` | `{ function: string }` | Yes | Contains a `function` property, which is executed when Imports UI is loaded to display the status of the import. There are two status enums that can be returned currently,`{ status: "NOT_CONFIGURED" }` or `{ status: "READY" }`  *Regex:* `^[a-zA-Z0-9_-]+$` |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `importId` | `string` | The id of the Assets Import Type. |
| `workspaceId` | `string` | The id of the Assets workspace. |
| `schemaId` | `string` | The id of the schema. |
| `location` | `string` | The full URL of the host page where this module is displayed. |
