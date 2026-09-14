# useWidgetContext (EAP)

Forge's EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.
For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To participate, you can [sign up for the EAP here](https://docs.google.com/forms/d/e/1FAIpQLSfl_TpJ7o160vlOMhvU07u4XfKSnTnMpzi_4Q8d7-ieNhD1vQ/viewform?usp=sharing&ouid=100849039189157529928p).

**Note:** You must also opt-in to the open beta of Dashboards in Atlassian Home. See the [guide on how to opt-in](https://community.atlassian.com/forums/Atlassian-Home-articles/Home-Dashboards-available-in-open-beta/ba-p/3009544).

Hook for accessing widget context information, including `widgetId`, `dashboardId`, `layout` and dashboard filters. Context data loads asynchronously, so the output is `undefined` while loading.

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
4const getFilterLabels = (expression) => {
5  if (!expression) {
6    return [];
7  }
8
9  if ("groups" in expression) {
10    return expression.groups.flatMap(getFilterLabels);
11  }
12
13  return expression.label ? [expression.label] : [];
14};
15
16function MyWidget() {
17  const context = useWidgetContext();
18
19  if (!context) return <div>Loading...</div>;
20
21  const { layout, widgetId, dashboardId, filters } = context;
22  const filterLabels = getFilterLabels(filters);
23
24  return (
25    <div style={{ width: layout.width, height: layout.height }}>
26      <p>Widget ID: {widgetId}</p>
27      <p>Dashboard ID: {dashboardId}</p>
28      <p>
29        Size: {layout.width}x{layout.height}
30      </p>
31      <p>Dashboard filters: {filterLabels.join(", ") || "None"}</p>
32    </div>
33  );
34}
35
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
28
```



```
function useWidgetContext(): UseWidgetContextType | undefined;

interface UseWidgetContextType {
  layout: Layout;
  widgetId?: string;
  dashboardId: string;
  filters: FilterExpression | null;
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
  * **filters** (FilterExpression | null): Dashboard filters available to the widget. Returns `null` when there is no active filter expression.

## Dashboard filters

Dashboard widgets can receive dashboard filters through the `filters` property. This is typed as a `FilterExpression` tree. Typically on the dashboard, `FilterExpression`s are nested as a root dashboard-level `FilterGroup` containing product-specific `FilterGroup`s, which themselves contain individual leaf node `Filter`s.

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
```



```
type FilterExpression = FilterGroup | Filter;

interface FilterGroup {
  id: string;
  operator: "AND" | "OR";
  groups: FilterExpression[];
}

interface Filter {
  id: string;
  label?: string | null;
  comparison: string;
  defaultValues?: Array<string | null> | null;
  metadata?: string;
  dimensions: FilterDimension[];
}

interface FilterDimension {
  name: string;
  product?: string;
  subProduct?: string | null;
  dynamicDimensionKey?: string; // The key for any custom field dimensions
}
```
```
