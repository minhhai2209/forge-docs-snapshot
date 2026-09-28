# useFilters (EAP)

Hook for accessing the persisted dashboard filter group and any session-only overrides.

For module configuration and setup instructions, see [Dashboard filter (EAP)](/platform/forge/manifest-reference/modules/dashboard-filter/).

### Installation

Install Forge hooks using the [@forge/hooks](https://www.npmjs.com/package/@forge/hooks) npm package.
Import `@forge/hooks` using a bundler, such as [Webpack](https://webpack.js.org/).

## Usage

To add the `useFilters` hook to your app:

```
1import { useFilters } from "@forge/hooks/dashboards";
2
```

Here is an example of accessing persisted filters and overrides:

```
1import React from "react";
2import { useFilters } from "@forge/hooks/dashboards";
3
4function FilterSummary() {
5  const { filterGroup, overrides } = useFilters();
6
7  return (
8    <div>
9      <p>Root operator: {filterGroup?.operator}</p>
10      <p>Active overrides: {Object.keys(overrides).length}</p>
11    </div>
12  );
13}
14
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
function useFilters(): UseFiltersResult;

interface UseFiltersResult {
  filterGroup: FilterGroup | null;
  overrides: Record<string, FilterOverride>;
}
```
```

For the `FilterGroup` and `FilterOverride` types, see the [filter model](/platform/forge/apis-reference/dashboard-bridge-apis/filter/#filter-model).

## Returns

* **filterGroup** (FilterGroup | null): The persisted filter group for the dashboard filter.
* **overrides** (Record<string, FilterOverride>): Session-only overrides keyed by filter ID.
