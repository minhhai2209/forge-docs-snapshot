# useWidgetConfig (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://docs.google.com/forms/d/e/1FAIpQLSfl_TpJ7o160vlOMhvU07u4XfKSnTnMpzi_4Q8d7-ieNhD1vQ/viewform?usp=sharing&ouid=100849039189157529928p).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

Hook for accessing and updating widget configuration. You can call the hook anywhere in your code, as it subscribes to configuration updates. The configuration data loads asynchronously, so the output is `undefined` while loading.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

### Installation

Install Forge hooks using the [@forge/hooks](https://www.npmjs.com/package/@forge/hooks) npm package.
Import `@forge/hooks` using a bundler, such as [Webpack](https://webpack.js.org/).

## Usage

To add the `useWidgetConfig` hook to your app:

```
1import { useWidgetConfig } from "@forge/hooks/dashboards";
2
```

Here is an example of accessing and updating widget configuration:

```
1import React from "react";
2import { useWidgetConfig } from "@forge/hooks/dashboards";
3
4function MyWidget() {
5  const { config, updateConfig } = useWidgetConfig();
6
7  const handleUpdate = async () => {
8    await updateConfig({
9      title: "New Title",
10    });
11  };
12
13  return (
14    <div>
15      <h1>{config?.title}</h1>
16      <button onClick={handleUpdate}>Update Title</button>
17    </div>
18  );
19}
20
```

## Returns

* **config** (Record<string, unknown> | undefined): Current widget configuration object. Returns `undefined` while loading or if no configuration is set.
* **updateConfig** (function): Function to update configuration. It will also trigger an update of the live editing view.
