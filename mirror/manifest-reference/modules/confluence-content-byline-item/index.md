# Confluence content byline item

The `confluence:contentBylineItem` module adds an entry to the content byline section,
which is the part of the content under the title that includes metadata about contributors and more.
The `title`, `icon`, and `tooltip` of the module render together as a list item.

On apps that use Custom UI, module content is displayed inside a [special Forge iframe](/platform/forge/custom-ui/iframe/) which has the [sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox) attribute configured. This means that HTML links (for example, `<a href="https://domain.tld/path">...</a>`) in this iframe won't be clickable. To make them clickable, use the [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate) API from the `@forge/bridge` package.

![Example of a Content byline item](https://dac-static.atlassian.com/platform/forge/images/content-byline-item-demo.gif?_v=1.5800.1771)

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'` or `'fullscreen'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |
| `viewportContainer` | `'popup'` or `'modal'` |  | The display type of the content byline item. Defaults to popup if no option provided |
| `title` | `string` or `i18n object` | Yes | The title of the content byline item, which is displayed as a list item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `icon` | `string` |  | The icon displayed next to the `title`.   For Custom UI and UI Kit apps, the `icon` property accepts a relative path from a declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See [Icons](/platform/forge/custom-ui/#icons) for more information.  If no icon is provided, or if there's an issue preventing the icon from loading, a generic app icon will be displayed. |
| `tooltip` | `string` or `i18n object` |  | The tooltip of the content byline item, which is displayed on hover.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` |  | The description of the content byline item.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `displayConditions` | `object` |  | The object that defines whether or not a module is displayed in the UI of the app. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `dynamicProperties` | `{ function: string }` |  | Contains a `function` property, which references the `function` module that defines the [configuration](/platform/forge/manifest-reference/resources) of `resource`. See [Dynamic properties](#dynamic-properties) for more details. |
| `contentPropertyKey` | `string` |  | The key of the [content property](/cloud/confluence/rest/v2/api-group-content-properties/#api-group-content-properties), which stores the `title`, `icon`, and `tooltip` byline properties. When this key is provided, the byline module renders using the values from the content property instead of executing the [dynamicProperties](#dynamic-properties) function. We strongly recommend making this key unique, like a UUID. See the [Content Properties to store byline properties](#content-properties-to-store-byline-properties) for more details. |
| `keyboardShortcut` | `object` |  | The object that defines a keyboard shortcut to trigger this module. See [keyboard shortcuts](/platform/forge/manifest-reference/keyboard-shortcuts). |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-jsm-users/#confluence-forge-modules). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Content properties to store byline properties

Starting in Forge CLI version `12.6.1`, you can control the `title`, `icon`, or `tooltip` properties of the `confluence:contentBylineItem` module using content properties. If the `contentPropertyKey` is provided in the `manifest.yml` file, Confluence attempts to retrieve the dynamic properties from the value of that `content property` on the initial render of the app. Read more about the [content property API](/cloud/confluence/rest/v2/api-group-content-properties/#api-pages-page-id-properties-property-id-put).

You can also use either the `set` method of the [useContentProperty](/platform/forge/ui-kit/hooks/use-content-property) hook (in `@forge/react` version `11.4.0` and above) or the [updateBylineProperties](/platform/forge/apis-reference/confluence-api-bridge/updateBylineProperties) `@forge/confluence-bridge` (in `@forge/confluence-bridge` version `3.1.0` and above) method to programmatically refresh the associated byline module properties. For example, a `confluence:backgroundScript` module could be used to trigger the re-rendering of byline properties by updating the values in the content property of a page.

In your byline manifest:

```
```
1
2
```



```
confluence:contentBylineItem:
  - key: byline-app
    resource: main
    render: native
    title: Byline App
    contentPropertyKey: byline-properties-unique-key
```
```

In another module, like `confluence:backgroundScript` or `macro`, you can use:

```
```
1
2
```



```
import { useContentProperty } from '@forge/react';

const [properties, setProperties, deleteProperties] = useContentProperty('byline-properties-unique-key', { defaultValues });

const setTestContentProperty = async () => {
  const date = new Date().toTimeString();
  await setProperties({ title: `Updated title at ${date}`, icon: "new-icon-path", tooltip: `Updated tooltip at ${date}`});
}
```
```

You can also use the [updateBylineProperties](/platform/forge/apis-reference/confluence-api-bridge/updateBylineProperties) bridge method for Custom UI apps.

When you use `contentPropertyKey`, we highly recommend keeping this property unique, like a UUID. Multiple content properties with the same key could exist on the same page, and since we don't require you to fetch the `id` of the content property, the byline properties will not update if more than one content property has the same key on that page.

## Dynamic properties

Dynamic properties are used to dynamically update the `title`, `icon`, or `tooltip` properties of the
`confluence:contentBylineItem` module. If provided in the `manifest.yml` file, Confluence attempts
to retrieve the dynamic properties on the initial render of the app. To do this, the `dynamicProperties`
handler function of the app is called. When the content byline item is clicked, the app renders in a
dialog, where it can perform business logic updates. After the dialog is closed, the handler function
is again called to retrieve updates, and then update the `title`, `icon`, or `tooltip`.

The app's handler function is passed two arguments: `payload` and `context`. The `payload` object has the following structure:

```
```
1
2
```



```
interface Payload {
  // The cloudId for your site 
  cloudId: string;
  // A unique id for this instance of this component in the content
  localId: string;
  extension: {
    // The module type included in the manifest.yml file.
    // In this case, it is the "confluence:contentBylineItem" module.
    type: string;
    content: {
      // The unique identifier of the Confluence content
      id: string;
      // The type of Confluence content on which the invocation has occurred
      type: 'page' | 'blogpost' | 'space';
    };
    space: {
      // The id of the originating invocation space
      id: string;
      // The key of the originating invocation space
      key: string;
    }
  };
}
```
```

The `context` object has the following structure:

```
```
1
2
```



```
interface Context {
  principal: {
    accountId: string;
  };
  installContext: string;
}
```
```

The handler function should return (or resolve with) a plain old JavaScript object with a `title`,
`icon`, and `tooltip` as keys. These optional keys are only sent if their
respective values require updating. Failure to provide a key would default to the last used value
or the original values defined within the `manifest.yml` file.

Below is an example of a handler function returning a returned object:

```
```
1
2
```



```
function handlerFunction(payload, context) {
  return {
    "title": "Updated title",
    "icon": "https://mydomain.com/my-icon.png",
    "tooltip": "Updated Tooltip"
  };
}
```
```

When you use an `icon` in your dynamic properties, its source URL is subject to a permission check.

For an example of adding source URL permissions for your `icon` property, see [External Permissions](/platform/forge/manifest-reference/permissions/#images).

Bundled resources in the following formats are allowed by default:

* `resource:<resource key>;<relative path to resource>`
* `data:image` URIs

See [Icons](/platform/forge/custom-ui/#icons) for more information about bundling icons as a resource.

When the source URL does not have the appropriate permissions, the dynamic properties are not loaded. The default configuration is used instead.

Check out the [Page approver app](/platform/forge/example-apps-confluence/#page-approver-app-with-ui-kit) as an example of
an app that updates the title and tooltip on change, and prepopulates a default icon that's missing
from the `manifest.yml` file.

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
|
| `content.id` | `string` | A string that represents the unique identifier of the `content` object. |
| `content.type` | `"page"` or `"blogpost"` | A string that represents the type of the `content` object. |
| `content.subtype` | `string` or `null` | A string that represents the subtype of the `content` object. `null` is returned if `subtype` does not apply. |
| `space.id` | `string` | A string that represents the unique indentifier of the `space` object. |
| `space.key` | `string` | A string that represents the unique key of the `space` object. |
| `location` | `string` | The full URL of the host page where this module is displayed. |
