# useWidgetContext (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://docs.google.com/forms/d/e/1FAIpQLSfl_TpJ7o160vlOMhvU07u4XfKSnTnMpzi_4Q8d7-ieNhD1vQ/viewform?usp=sharing&ouid=100849039189157529928p).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

Hook for accessing widget context information including `widgetId`, `dashboardId` and `layout` information. The context data loads asynchronously, so the output is `undefined` while loading.

For module configuration and setup instructions, see [Dashboard widget](/platform/forge/manifest-reference/modules/dashboard-widget/).

### Installation

Install Forge hooks using the [@forge/hooks](https://www.npmjs.com/package/@forge/hooks) npm package.
Import `@forge/hooks` using a bundler, such as [Webpack](https://webpack.js.org/).

## Usage

To add the `useWidgetContext` hook to your app:

```
1import { useWidgetContext } from "@forge/hooks/dashboards";
2
```

Here is an example of accessing widget context information:

```
1import React from "react";
2import { useWidgetContext } from "@forge/hooks/dashboards";
3
4function MyWidget() {
5  const context = useWidgetContext();
6
7  if (!context) return <div>Loading...</div>;
8
9  const { layout, widgetId, dashboardId } = context;
10
11  return (
12    <div style={{ width: layout.width, height: layout.height }}>
13      <p>Widget ID: {widgetId}</p>
14      <p>Dashboard ID: {dashboardId}</p>
15      <p>
16        Size: {layout.width}x{layout.height}
17      </p>
18    </div>
19  );
20}
21
```

## Function signature

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
15
16
17
18
19
20
21
22
23
24
25
26
27
```



```
function useWidgetContext(): UseWidgetContextType | undefined;

interface UseWidgetContextType {
  layout: Layout;
  widgetId?: string;
  dashboardId: string;
}

interface Layout {
  /**
   * The width of the container of the widget in px.
   */
  width: number;
  /**
   * The height of the container of the widget in px.
   */
  height: number;
  /**
   * The row span of the widget.
   */
  rowSpan?: "xsmall" | "small" | "medium" | "large";
  /**
   * The column span of the widget in a 12 column grid.
   */
  columnSpan?: 3 | 4 | 6 | 8 | 12;
}
```
```

## Returns

* **UseWidgetContextType:** Widget context object containing:
  * **layout** (Layout): Widget dimensions and grid positioning
  * **widgetId** (string | undefined): Unique widget identifier, `undefined` if it's a new widget
  * **dashboardId** (string): Parent dashboard identifier
