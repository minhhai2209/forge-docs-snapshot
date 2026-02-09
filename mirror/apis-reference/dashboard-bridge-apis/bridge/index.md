# Dashboard UI bridge (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://docs.google.com/forms/d/e/1FAIpQLSfl_TpJ7o160vlOMhvU07u4XfKSnTnMpzi_4Q8d7-ieNhD1vQ/viewform?usp=sharing&ouid=100849039189157529928p).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

The Dashboard UI bridge is a JavaScript API that enables [Forge dashboard widgets](/platform/forge/manifest-reference/modules/dashboard-widget) to securely integrate with dashboards in Atlassian Home.

Install the Dashboard UI bridge using the
[@forge/dashboards-bridge](https://www.npmjs.com/package/@forge/dashboards-bridge) npm package.
Import `@forge/dashboards-bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

You can start by creating a new app from one of the Custom UI templates.
In the `static/hello-world` directory, run `npm install && npm build` to bundle the
static web application template with the Dashboard UI bridge into the `static/hello-world/build`
directory. Use this directory as the resource path in the Forge app's `manifest.yml`.

In the template, use the bridge in `static/hello-world/src/View.js` like this:

```
1
2
3
4
5
6
7
import { widget } from "@forge/dashboards-bridge";

// Set preview configuration for widget picker
widget.setPreviewConfig({
  title: "My Widget Preview",
  description: "Preview description",
});
```

For widget edit functionality, use the bridge in `static/hello-world-edit/src/Edit.js` like this:

```
```
1
2
```



```
import { widgetEdit } from "@forge/dashboards-bridge";

// Handle save events
widgetEdit.onSave(async (config, { widgetId }) => {
  console.log("Widget saved!", config, widgetId);
});

// Handle product save events
widgetEdit.onProductSave(async (config) => {
  return config; // Return config to save in product
});
```
```
