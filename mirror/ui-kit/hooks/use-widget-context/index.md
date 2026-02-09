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
1
import { useWidgetContext } from "@forge/hooks/dashboards";
```

Here is an example of accessing widget context information:

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
import React from "react";
import { useWidgetContext } from "@forge/hooks/dashboards";

function MyWidget() {
  const context = useWidgetContext();

  if (!context) return <div>Loading...</div>;

  const { layout, widgetId, dashboardId } = context;

  return (
    <div style={{ width: layout.width, height: layout.height }}>
      <p>Widget ID: {widgetId}</p>
      <p>Dashboard ID: {dashboardId}</p>
      <p>
        Size: {layout.width}x{layout.height}
      </p>
    </div>
  );
}
```

## Function signature

```
```
1
2
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
