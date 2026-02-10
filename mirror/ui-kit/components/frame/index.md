# Frame

Frame component acts as a container for rendering static frontend applications, such as HTML, CSS, and JavaScript, ensuring seamless integration with the UI Kit. It provides flexibility in implementing desired user interfaces and supports communication with the main app through the Events API, allowing bidirectional and broadcast communication.

## Using Frame

To add the `Frame` component to your app:

```
1
import { Frame } from "@forge/react";
```

### Props

The `Frame` component has the following properties that need to be considered:

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | Yes | This is the key of the resource to be loaded in the `Frame`. The resource must be defined in the app’s `manifest.yml` file. If the resource key is missing or cannot be located in the `manifest.yml`, a `Not Found` message will appear within the `Frame` component.   For more information on defining a resource, see [here](/platform/forge/extend-ui-with-custom-options/#resources). |
| `height` | `string` | No | Sets the height of the `Frame` component. By default, the `Frame` component will resize according to the size of its contents. When `height` is set, the automatic resizing of the `Frame` component is disabled. Accepted units are `px` and `%`. |
| `width` | `string` | No | Sets the width of the `Frame` component. By default, the `Frame` component will resize according to the size of its contents. When `width` is set, the automatic resizing of the `Frame` component is disabled. Accepted units are `px` and `%`. |

### Example

```
```
1
2
```



```
import React from "react";
import ForgeReconciler, { Text, Frame } from "@forge/react";

const App = () => {
  return (
    <>
      <Text>[UI Kit] Hello world!</Text>
      <Frame resource="example-frame-resource" />
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Get started

## Custom content security policies

By default, Atlassian blocks any policies that may be considered unsafe when rendering `Frame`. To include capabilities, such as inline CSS, you will need to declare these permissions in the `manifest.yml` file of your app in the `permissions.content` section.

For example, to allow inline CSS in your app, use the following configuration:

```
```
1
2
```



```
permissions:
  content:
    styles:
      - "unsafe-inline"
```
```

Here’s an another example for allowing scripts from specific sources using a script-src style configuration in your manifest.yml:

```
```
1
2
```



```
permissions:
  external:
    scripts:
      - "https://www.example-dev.com/script.js"
```
```

See [content security policies and egress controls](/platform/forge/add-content-security-and-egress-controls/) for other permissions that can be added to `Frame`.

## Known limitations and issues

### Limitations

* Only a **single** `Frame` component can be rendered per module to minimize potential performance impact.
* Only modules that currently support Custom UI will support `Frame`.
* If the `Frame` component does not resize correctly within the application upon layout updates, we recommend checking and confirming that the sizing properties of the root container are defined using non-viewport-related units such as `%`, `px`, `em`, and so on. This limitation is because the `Frame` component's root container does not well support viewport-based relative sizing units like `vh` and `vw`.
* Jira custom fields can’t render the Frame component in view mode.
