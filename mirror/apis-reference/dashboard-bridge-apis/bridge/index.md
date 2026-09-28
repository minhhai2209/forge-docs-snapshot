# Dashboard UI bridge

The Dashboard UI bridge is a JavaScript API that enables [Forge dashboard widgets](/platform/forge/manifest-reference/modules/dashboard-widget/) to securely integrate with Jira dashboards.
It also exposes the [`filter`](/platform/forge/apis-reference/dashboard-bridge-apis/filter/) APIs for apps that define filters for dashboards.

Install the Dashboard UI bridge using the
[@forge/dashboards-bridge](https://www.npmjs.com/package/@forge/dashboards-bridge) npm package.
Import `@forge/dashboards-bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

You can start by creating a new app from one of the Custom UI templates.
In the `static/hello-world` directory, run `npm install && npm build` to bundle the
static web application template with the Dashboard UI bridge into the `static/hello-world/build`
directory. Use this directory as the resource path in the Forge app's `manifest.yml`.

In the template, use the bridge in `static/hello-world/src/View.js` like this:

```
1import { widget } from "@forge/dashboards-bridge";
2
3// Set preview configuration for widget picker
4widget.setPreviewConfig({
5  title: "My Widget Preview",
6  description: "Preview description",
7});
8
```

For widget edit functionality, use the bridge in `static/hello-world-edit/src/Edit.js` like this:

```
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

For dashboard filter functionality, use the bridge in your filter resource like this:

```
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
13
14
```



```
import { filter } from "@forge/dashboards-bridge";

filter.onProductSave(async () => ({
  operator: "AND",
  groups: [
    {
      label: "Status",
      comparison: "EQUALS",
      defaultValues: ["Done"],
      dimensions: ["status"],
    },
  ],
}));
```
```
