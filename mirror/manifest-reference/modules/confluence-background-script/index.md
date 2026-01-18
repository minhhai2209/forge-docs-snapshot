# Confluence background script

The `confluence:backgroundScript` module adds an invisible container across various Confluence views. This container lets you run app functions in the background of a page, such as:

* distributing shared data
* making heavy calculations
* running code without UI elements

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | Required if using Custom UI or the latest version of UI Kit. | A reference to the static `resources` entry that your context menu app wants to display. See resources for more details. |
| `render` | `'native'` | Yes for UI Kit. | Indicates the module uses UI Kit. |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `displayConditions` | `object` |  | The object that defines whether or not the background script executes on a page. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-jsm-users/#confluence-forge-modules). |

## Extension context

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `content.id` | `string` | A string that represents the unique identifier of the `content` object.   **Note:** This value only exists on content type pages. |
| `content.type` | `"page"`, `"blogpost"` or `"space"` | A string that represents the type of the `content` object.   **Note:** This value only exists on content type pages. |
| `content.subtype` | `string` or `null` | A string that represents the subtype of the `content` object. `null` is returned if `subtype` does not apply.   **Note:** This value only exists on content type pages. |
| `space.id` | `string` | A string that represents the unique identifier of the `space` object.   **Note:** This value only exists on content type pages. |
| `space.key` | `string` | A string that represents the unique key of the `space` object.   **Note:** This value only exists on content type pages. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Example

You can use the [events](/platform/forge/custom-ui-bridge/events/) API to enable communication between a Confluence background script and [homepage feed module](/platform/forge/manifest-reference/modules/confluence-homepage-feed/). Either script and feed may be rendered first, you'll need to handle both independently:

Background script:

```
```
1
2
```



```
import { events } from '@forge/bridge';

// Emit the data to an already rendered homepage feed
events.emit('app.data-change', 'initial-data');

// Listen to data change requests from homepage feeds
events.on('app.request-data', (payload) => {
  events.emit('app.data-change', 'initial-or-changed-data');
});
```
```

Homepage feed:

```
```
1
2
```



```
import { events } from '@forge/bridge';

// Request data in case the background script is already rendered
events.emit('app.request-data');

// Listen to data change
events.on('app.data-change', (payload) => {
  console.log('The data has changed:', payload)
});
```
```

Manifest:

```
```
1
2
```



```
modules:
  confluence:backgroundScript:
    - key: confluence-background-script
      resource: main
      render: native
  confluence:homepageFeed:
    - key: confluence-background-script-homepage-feed
      title: Hello world!
      description: Homepage feed that talks with a background script
      resource: main
      render: native
```
```
