# useCurrentFilter (EAP)

Hook for accessing the filter represented by the currently open dropdown and its session-only override.

For module configuration and setup instructions, see [Dashboard filter (EAP)](/platform/forge/manifest-reference/modules/dashboard-filter/).

### Installation

Install Forge hooks using the [@forge/hooks](https://www.npmjs.com/package/@forge/hooks) npm package.
Import `@forge/hooks` using a bundler, such as [Webpack](https://webpack.js.org/).

## Usage

To add the `useCurrentFilter` hook to your app:

```
1import { useCurrentFilter } from "@forge/hooks/dashboards";
2
```

Here is an example of accessing the currently open filter and override:

```
1import React from "react";
2import { useCurrentFilter } from "@forge/hooks/dashboards";
3
4function CurrentFilter() {
5  const { filter, override } = useCurrentFilter();
6
7  if (!filter) {
8    return null;
9  }
10
11  const filterLabel = "label" in filter ? filter.label : filter.id;
12
13  return (
14    <div>
15      <p>Filter: {filterLabel}</p>
16      <p>Selected values: {override?.values?.join(", ") ?? "None"}</p>
17    </div>
18  );
19}
20
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
```



```
function useCurrentFilter(): UseCurrentFilterResult;

interface UseCurrentFilterResult {
  filter: FilterExpression | null;
  override: FilterOverride | null;
}
```
```

For the `FilterExpression` and `FilterOverride` types, see the [filter model](/platform/forge/apis-reference/dashboard-bridge-apis/filter/#filter-model).

## Returns

* **filter** (FilterExpression | null): The filter represented by the currently open dropdown, or `null` when no filter dropdown is open.
* **override** (FilterOverride | null): The current session-only override for the filter, or `null` when no override exists.
