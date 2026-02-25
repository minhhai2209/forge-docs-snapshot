# Confluence page banner

The `confluence:pageBanner` module adds a banner to Confluence pages. The banner
can be used to display information, notifications, or other content relevant to the page.

Confluence page banner is supported on Confluence pages, live docs, and spaces. It is not supported on whiteboards,
databases, smart links, or pages that are embedded within another Confluence page.

![Example of a Confluence page banner](https://dac-static.atlassian.com/platform/forge/snippets/images/confluence-page-banner.png?_v=1.5800.1877)

## Manifest structure

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
modules {}
└─ confluence:pageBanner []
   ├─ key (string) [Mandatory]
   ├─ resource (string) [Mandatory]
   ├─ render (string) [Optional]
   ├─ resolver {} [Optional]
   └─ displayConditions {} [Optional]
   └─ unlicesedAccess (string[]) [Optional]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | Yes | A reference to the static `resources` entry that your context menu app wants to display. See resources for more details. |
| `render` | `'native'` | Yes for UI Kit. | Indicates the module uses UI Kit. |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | No | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `displayConditions` | `object` | No | The object that defines whether or not a page banner is displayed. See [display conditions](/platform/forge/manifest-reference/display-conditions). |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed` (Guests Users), and `anonymous`. For more information, see [Access to Forge apps for unlicensed Confluence users](/platform/forge/access-to-forge-apps-for-unlicensed-users/#confluence-forge-modules). |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
|
| `content.id` | `string` | A string that represents the unique identifier of the `content` object. |
| `content.type` | `string` | A string that represents the type of the `content` object. |
| `content.subtype` | `string` or `null` | A string that represents the subtype of the `content` object. `null` is returned if `subtype` does not apply. |
| `space.id` | `string` | A string that represents the unique identifier of the `space` object. |
| `space.key` | `string` | A string that represents the unique key of the `space` object. |
| `location` | `string` | The full URL of the host page where this action menu item is displayed. |

## Example

This example shows how to create a simple page banner that displays a message and a button to dismiss the banner.

### Manifest

```
```
1
2
```



```
modules:
  confluence:pageBanner:
    - key: hello-world-page-banner
      resource: main
      render: native
```
```

### Page banner

```
```
1
2
```



```
import React, { useState } from 'react';
import ForgeReconciler, { Button, Inline, Box, Text, xcss } from '@forge/react';
import { view } from '@forge/bridge';

const boxStyle = xcss({
  backgroundColor: 'color.background.accent.yellow.subtle',
  padding: 'space.150',
});

const App = () => {
  return (
    <Box xcss={boxStyle}>
      <Inline spread="space-between" alignBlock="center">
        <Text>Welcome to the page banner!</Text>
        <Button onClick={() => view.close()}>Dismiss</Button>
      </Inline>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Usage guidelines

To ensure that banners are accessible and enhance the user experience, we recommend adhering
to the following guidance:

* Use banners sparingly. There should be no more than one banner at a time.
* Banners should be dismissable. Ensure you provide a way for the banner to be dismissed using the [view.close()](/platform/forge/apis-reference/ui-api-bridge/view/#close) method from `@forge/bridge`.
* Closed banners can be re-opened with the [view.open()](/platform/forge/apis-reference/ui-api-bridge/view/#open) method from `@forge/bridge`.
* Banners should be relevant to and enhance the user experience of your app. They must not be used to upsell or
  cross-promote apps. If your app is found to be misusing banners, such as for promotional purposes, you
  may be contacted by the Forge team and risk having your app removed from Marketplace.
* Note that banners are often disruptive for people who use assistive technology, so only use banners
  when necessary.
