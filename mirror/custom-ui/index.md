# Extend UI with custom options

When building with UI Kit, you can use the [Frame component](/platform/forge/ui-kit/components/frame/) to render static content, such as HTML, CSS, and JavaScript within a container. This allows you to extend your app's the capabilities beyond the existing UI Kit feature set while still seamlessly integrating with UI Kit capabilities.

Alternatively, if you are looking for full customization, you can use Custom UI to build interfaces from scratch using any front-end framework.

## Resources

A resource is a collection of static assets, which is hosted on and distributed by
Atlassian cloud infrastructure.

`Frame` is supported for any module that supports Custom UI. They both require an eligible module with the resource property. See [Modules](/platform/forge/manifest-reference/modules/) to see which modules are eligible for Custom UI and `Frame`.

Consider the following example `manifest.yml` file:

```
1
2
3
4
5
6
7
8
modules:
  jira:issuePanel:
    - key: hello-world-panel
      resource: example-resource
      title: Hello world!
resources:
  - key: example-resource
    path: static/hello-world/build
```

This is the manifest declaration for a basic Jira issue panel using Frame or Custom UI. In this example:

* `resource` is a reference to a defined key in the `resources` object.
* `path` is the relative path from the top-level directory of your Forge app to the directory of
  the static assets for the resource. It should contain the `index.html` entry point for the
  Custom UI app; in this case, `static/hello-world/build/index.html`.

Consider an example `index.html` file saved in the root of the resource path:

```
```
1
2
```



```
<!DOCTYPE html>
<html>
  <body>
    <div>Hello, world!</div>
  </body>
</html>
```
```

In this example, `index.html` contains some text that's displayed to the user when they view
the issue panel. The `index.html` file can include any valid HTML, JavaScript, and CSS, subject
to [security constraints](/platform/forge/custom-ui/#security).

The `index.html` file can also include other files from the same resource directory using relative URLs,
such as JavaScript and CSS files, and images.

For example, to include an image at `static/hello-world/build/images/image.png`, the `index.html` looks
like this:

```
```
1
2
```



```
<!DOCTYPE html>
<html>
  <body>
    <div>Hello, world!</div>
    <img src="./images/image.png"></img>
  </body>
</html>
```
```

## Frame

Using `Frame` involves importing the component into your UI Kit app and specifying a resource on the `resource` prop. This will render your specified resource within a container in your UI Kit app. This will provide flexibility in implementing desired user interfaces and supports communication with the main app through the Events API, allowing bidirectional and broadcast communication.

```
```
1
2
```



```
// This is the UI Kit part of the app, e.g., `src/frontend/index.jsx` for a Forge app

import React, { useEffect } from 'react';
import ForgeReconciler, { Frame } from '@forge/react';
import { events } from '@forge/bridge';

const App = () => {
  // add your resource to the Frame component
  return <Frame resource="example-resource" />;
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

### Communication between UI Kit and Frame

Communication between UI Kit and Frame is done through the Events API communication, which is both **bidirectional** and **broadcast**:

* **Bidirectional**: Events can be sent from both the UI Kit and `Frame` component using `events.emit`.
* **Broadcast**: A single event can be received by multiple targets (e.g., different instances or extensions of the same app) through the `events.on` mechanism, as the Events API design enables communication among Custom UI extensions.

The primary mechanism for communication between the Forge UI Kit (main app) and the `Frame` component is the [Events API](/platform/forge/apis-reference/ui-api-bridge/events/) within `@forge/bridge`.

#### Example of using events.emit

The following example demonstrates how you can use the `event.emit` function to send data from UI Kit to the `Frame` component:

```
```
1
2
```



```
// This is the UI Kit part of the app, e.g., `src/frontend/index.jsx` for a Forge app

import React, { useEffect } from 'react';
import ForgeReconciler, { Frame } from '@forge/react';
import { events } from '@forge/bridge';

const App = () => {
  useEffect(() => {
    // Send a message to the Frame component
    setTimeout(() => {
      events.emit('MY_FRAME_RESOURCE_DATA', { msg: 'hello' });
    }, 2000);
  }, []);
  return <Frame resource="example-frame-resource" />;
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

#### Example of using events.on

The following example shows how you can use the `event.on` function to receive data from UI Kit in the `Frame` component:

```
```
1
2
```



```
// This is the Frame resource part of the app, e.g., `resources/frame-app/src/App.jsx` for a Forge app

import React, {useEffect, useState } from 'react';
import { events } from "@forge/bridge";

function App() {
  const [msg, setMsg] = useState('');

  useEffect(() => {
    let subscription = null;
    const registerMessage = async () => {
      subscription = await events.on('MY_FRAME_RESOURCE_DATA', ({ msg }) => {
        // This will be called whenever the message is sent from UI Kit
        setMsg(msg);
      });
    };
    registerMessage();
    return () => {
      if (subscription) {
        subscription.then(({ unsubscribe }) => unsubscribe());
      }
    };
  }, [setMsg]);

  return <b>{msg}</b>;
}
```
```

## Custom UI

Custom UI provides a means of building the user interface of an app from scratch. [Custom UI runs within an iframe](/platform/forge/custom-ui/iframe/), providing an isolated environment for the app's interface to be displayed.
Using Custom UI, you can define your own user interface using static resources, such as HTML, CSS, JavaScript, and images. The Forge
platform hosts your static resources, enabling your app to display Custom UI on Atlassian apps.
Custom UI apps inherit modern security features to ensure high trust between Atlassian, developers,
and users.

This page describes the main concepts behind Custom UI and how these concepts are applied in a
sample Forge app.

### Related pages

* [Custom UI iframe](/platform/forge/custom-ui/iframe/): Reference documentation for Custom UI iframe that describes required permissions of the iframe.
* [Shared responsibility model](/platform/forge/shared-responsibility-model/): Understand your responsibilities when building and supporting a Forge app, and what responsibilities Atlassian takes care of.

### Resource quotas

Static resources bundled with your app count against your
[Forge quotas](https://developer.atlassian.com/platform/forge/platform-quotas-and-limits/#platform-quotas-and-limits).
Resource quotas are consumed per deployment to your production environment;
deployments to development and staging environments are unmetered. These quotas are
refreshed weekly.

|  | Paid apps | Free apps | Distributed apps |
| --- | --- | --- | --- |
|  | Per app | Per app | Per app |
| File capacity (weekly) | 150 MB | 75 MB | 75 MB |
| Files uploaded (weekly) | 500 files | 250 files | 250 files |

### Icons

You can set an icon for any module that features an `icon` property.
On both UI kit and Custom UI implementations,
you can bundle your icon files with other [resources](#resources):

1. Store your icon images in a location declared as a resource.
2. Use the following syntax to reference the icon:

   ```
   ```
   1
   2
   ```



   ```
         icon: resource:<resource key>;<relative path to resource>
   ```
   ```

Icon files bundled with your code will count against your Forge [resource quotas](#resource-quotas).

Consider the following `manifest.yml` excerpt. Here, we use the `issue-panel.svg` file located
in `static/hello-world/build/icons/` as our icon for the Jira issue panel:

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: hello-world-panel
      title: Hello world!
      icon: resource:example-resource;icons/issue-panel.svg
resources:
  - key: example-resource
    path: static/hello-world/build
```
```

Alternatively, the `icon` property also supports an absolute URL to any self-hosted image file:

```
```
1
2
```



```
icon: https://example.com/icon.png
```
```

You can do this for either UI kit or Custom UI apps.

### Bridge

The Custom UI bridge is a JavaScript API that enables UI Kit and Custom UI apps to securely integrate with
Atlassian apps.

**Option - 1**:

To install the Custom UI bridge using the
[@forge/bridge](https://www.npmjs.com/package/@forge/bridge) npm package:

* Under `static/<module-name>` folder, run `npm install -s @forge/bridge`.

This installs the `@forge/bridge` dependency and saves it in `package.json`, which will allow importing `@forge/bridge` in the source using a bundler, such as [Webpack](https://webpack.js.org/).

**Option - 2**:

Start by creating a new app from one of the Custom UI templates.

After you create a Custom UI template:

1. Go to `static/<module-name>` directory.

   Custom UI template can either create a folder with the `module-name` or `hello-world`.
2. Run `npm install && npm run build`.

This will install [@forge/bridge](https://www.npmjs.com/package/@forge/bridge) npm package and bundle the template static web application together with the Custom UI bridge, into the `static/<module-name>/build`
directory, which is used as the resource path in the Forge app's `manifest.yml`.

In the template, the bridge is used in `static/<module-name>/src/App.js`:

```
```
1
2
```



```
import { invoke } from "@forge/bridge";

invoke("exampleFunctionKey", { example: "my-invoke-variable" }).then(setData);
```
```

See [Custom UI bridge](/platform/forge/custom-ui-bridge/bridge/) reference documentation
for the available bridge API methods.

### Security

Custom UI apps are hosted by Atlassian. To help mitigate some common classes of security vulnerabilities,
such as cross-site scripting (XSS) and data injection, all Custom UI apps are served with a *content security policy (CSP)*.
For your Custom UI app to work as expected, your users must be on a
[CSP-compatible browser](https://confluence.atlassian.com/cloud/supported-browsers-744721663.html).

#### Default limitations

By default, the CSP used in Custom UI apps restricts some behavior. For example:

* All scripts and assets used in your Custom UI app must come from the same resource directory as
  your Custom UI app. This means that you cannot use scripts or images from external sources, such
  as Google Analytics or Sentry, in your static assets. This is to help mitigate cross-site scripting
  vulnerabilities.
* In a similar way, you cannot fetch APIs from your static assets. Instead, you must use the
  [invoke method](/platform/forge/custom-ui-bridge/invoke/) from the Custom UI bridge
  to run an Atlassian-hosted backend FaaS function, where you may fetch from your desired APIs,
  and return the required data to the frontend.

If there is code in your Custom UI app that violates the CSP, the app will not behave as
expected, and an error will be shown in the browser console.

#### Custom content security and egress controls

Having visibility and control over the external systems that your app communicates and shares data
with helps maintain the security of your app and your app users.

To enable this, we're providing a way to add `permissions` to share data with external resources,
as well as to use custom Content Security Policies (CSP).

See [add content security and egress controls](/platform/forge/add-content-security-and-egress-controls/)
to know how to set this up for your Forge app.

### Inline styles

To include inline CSS in your app, follow the instructions on how to
[use custom content security policies](/platform/forge/add-content-security-and-egress-controls/#use-custom-content-security-policies).

### Accessing static assets

Since the static assets of a Custom UI app are distributed via a URL with a particular path that
identifies your app, you should use relative paths when accessing these assets from your Custom UI app.
For example, instead of including an image at `"/assets/image.png"`,
you should use `"./assets/image.png"`.

#### Errors and troubleshooting

When working with static assets in your Custom UI app, you may encounter certain errors. Here are some common errors and their troubleshooting steps:

##### 403 forbidden error

**Description:**
A 403 forbidden error indicates that the server is refusing to fulfill the request to access a resource. This often occurs when static assets are not served correctly.

**Troubleshooting steps:**

1. **Check relative paths:** Ensure all static files use relative paths, like `./assets/image.png`.
2. **React apps:** When using [create-react-app](https://create-react-app.dev/) to generate your
   static assets (by creating a single-page React app), set `"homepage": "./"` in your `package.json` for relative paths when bundling.
3. **Vue.js and Vite:** Add `base: './'` to your `vite.config.js` to convert absolute paths to relative paths.

##### 422 unprocessable entity error

**Description:**
A 422 unprocessable entity error means the server can't process the request instructions.

**Troubleshooting steps:**

1. **Check asset paths:** Ensure paths are correct and assets exist.
2. **Inspect network requests:** Use developer tools to check for failed loads and response details.

See the following [step-by-step tutorial](/platform/forge/build-a-custom-ui-app-in-jira/)
to start building a Custom UI app in Jira.

### Viewport size

Custom UI apps in certain module types can be displayed in various sizes. You can configure the
`viewportSize` property of a module in the app's `manifest.yml` file. See
[Modules](/platform/forge/manifest-reference/modules/) to see which modules can be displayed in
various sizes.

### Look and feel

Your app's user experience is most effective when you keep its interface consistent with
Atlassian's apps. For guidance on doing so when using Custom UI, refer to the
[Atlassian Design System](https://atlassian.design/foundations/).
