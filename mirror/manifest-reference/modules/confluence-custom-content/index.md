# Confluence custom content

The `confluence:customContent` module registers a new custom content type in Confluence that behaves like
built-in content types, such as `page`, `blog post` or `comment`.
After registering a new type, the corresponding custom content can be created by one user then listed, indexed
and displayed in quick and advanced search results.

Custom content must respect the content type hierarchy by providing container and child types.
For example, custom content can be created under a page container and have a comment child or an attachment child. Custom content can even be a parent or child to another piece of custom content,
although in this case, both custom content types must be registered in the same app.
See the `supportedContainerTypes` and `supportedChildTypes` parameters in the manifest description.

To retrieve, create, update, and delete custom content, use the corresponding [REST API](/cloud/confluence/rest/intro/).
As an input parameter for these requests, the content type key should be structured as follows:

`forge:[APP_ID]:[ENVIRONMENT_ID]:[MODULE_KEY]`.

Where:

* `forge`: The prefix for content type created with Forge.
* `APP_ID`: The identifier for your Forge app. To get the app ID, use the [useProductContext](/platform/forge/ui-kit-hooks-reference/#useproductcontext) hook.
  The app ID is a part of the `localId` attribute.
* `ENVIRONMENT_ID`: The environment identifier where the app was deployed.
  For more details, see [Environments and versions](/platform/forge/environments-and-versions/). To get the environment ID,
  use the [useProductContext](/platform/forge/ui-kit-hooks-reference/#useproductcontext) hook.
* `MODULE_KEY`: Unique `confluence:customContent` module key.

For example:

`forge:b44c55b2-251f-45e3-8ea4-b56762f82e8a:f7522737-117c-46e7-a7ca-03a73c99afcf:customer`

For more complex user interfaces, you can create a custom list component.
Regardless, all custom content created within a page is available under **Page -> Action Menu -> Attachments -> Custom Contents**.
On this page, each type of custom content is grouped within a separate tab.

The `confluence:customContent` module defines the app that is rendered to display custom content.
This app is rendered under `/display/:spaceKey/customcontent/:customContentId` url inside the main content area of the Confluence.

On apps that use Custom UI, module content is displayed inside a [special Forge iframe](/platform/forge/custom-ui/iframe/) which has the [sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox) attribute configured. This means that HTML links (for example, `<a href="https://domain.tld/path">...</a>`) in this iframe won't be clickable. To make them clickable, use the [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate) API from the `@forge/bridge` package.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `title` | `string` or `i18n object` | Yes | The title of the custom content.    This title appears on the Confluence page, which shows all custom content created within a page, and on the advanced search page in the `type` dropdown list  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` |  | The description of the content action.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | An absolute URL to the icon that represent the custom content. Relative URLs aren't supported. A generic app icon is displayed if no icon is provided. |
| `bodyType` | `string` |  | Defines the content body type of this custom content. Currently, supported content body types are:  * `storage`: This is Confluence's default storage representation which can be rendered using the [Content Body Conversion API](/cloud/confluence/rest/api-group-content-body/#api-wiki-rest-api-contentbody-convert-to-post) * `raw`: This representation is used for storing raw data in the body that is not storage format. This format is opaque to Confluence.  If `bodyType` is not defined, `storage` format is used by default |
| `supportedContainerTypes` | `string[]` | Yes | Defines types that this custom content can be contained in. Currently, supported content types:  * `space`: For this content type a custom content can be created directly in a space. * `page`: This custom content can be contained in a page. * `blogpost`: This custom content can be contained in a blog post. * Other custom content type registered in this manifest, in the form of `this:[OTHER_MODULE_KEY]` |
| `supportedChildTypes` | `string[]` |  | Defines types that can be contained in this custom content. Currently, supported content types:  * `attachment`: This custom content can contain attachments. * `comment`: This custom content can contain comments. * Other custom content type registered in this manifest, in the form of `this:[OTHER_MODULE_KEY]` |
| `supportedSpacePermissions` | `string[]` |  | Defines the space permissions that this custom content supports. Allowable values are : `read`, `create` and `delete`. These permissions must be granted through the space permissions UI in order to perform the given operation.    If no space permissions are defined, the default permissions are used. |
| `indexing` | `boolean` |  | Defines whether this content type is indexed and displayed in search results. |
| `preventDuplicateTitle` | `boolean` |  | Defines whether Confluence should prevent content with duplicate titles from being created in the same space or container. |
| `migratedFromConnect` | `boolean` |  | When set to `true`, new content for this module will use the Connect type format (`ac:[ADDON_KEY]:[MODULE_KEY]`) instead of the Forge format (`forge:[APP_ID]:[ENVIRONMENT_ID]:[MODULE_KEY]`). This ensures compatibility with existing custom content when migrating from Connect to Forge. See [Migrate custom content from Connect to Forge](/platform/adopting-forge-from-connect/migrate-custom-content/) for more details. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-users/#confluence-forge-modules). |

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
| `location` | `string` | The full URL of the host page where this module is displayed. |
