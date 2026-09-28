# filter (EAP)

Use the `filter` APIs to define filters for dashboards, persist filter definitions, and apply session-only filter overrides.

For module configuration and setup instructions, see [Dashboard filter (EAP)](/platform/forge/manifest-reference/modules/dashboard-filter/).

## Installation

Install the Dashboard UI bridge using the [@forge/dashboards-bridge](https://www.npmjs.com/package/@forge/dashboards-bridge) npm package.
Import `@forge/dashboards-bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

```
1import { filter } from "@forge/dashboards-bridge";
2
```

## Filter model

Dashboard filters are represented as a filter tree.

* `FilterGroup`: a group with an `id`, an `operator` of `AND` or `OR`, and child filter expressions.
* `AvpStoredFilter`: a product-managed filter. Use this type if you want the product to save your filter data to the dashboard.
* `AppStoredFilter`: an app-managed filter. Use this type if you are managing your own filter data.
* `FilterOverride`: session-only values for a filter, such as `values`, `comparison`, or `metadata`.

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
29
30
31
32
33
34
35
36
37
```



```
type FilterExpression = FilterGroup | Filter;

interface FilterGroup {
  id: string;
  operator: "AND" | "OR";
  groups: FilterExpression[];
}

type Filter = AvpStoredFilter | AppStoredFilter;

interface AvpStoredFilter {
  id: string;
  label: string;
  comparison: string;
  defaultValues: Array<string | null>;
  metadata?: string;
  dimensions: FilterDimension[];
}

interface AppStoredFilter {
  id: string;
  label: string;
}

interface FilterDimension {
  name: string;
  product?: string;
  subProduct?: string | null;
  dynamicDimensionKey?: string; // The key for any custom fields
}

interface FilterOverride {
  values?: Array<string | null>;
  comparison?: string;
  metadata?: string;
}
```
```

## Handling product save events

### filter.onProductSave

Registers a callback that executes when the user saves the filter in edit mode. The callback must return a filter group payload. Use `AvpStoredFilterPayload` if you are saving filter data to the dashboard, or `AppStoredFilterPayload` if you are managing your own filter data.

Child filters with an `id` update the existing filter with that ID. Child filters without an `id` are created as new filters.

#### Usage

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

**Parameters:**

* **callback** (OnProductSave): Function called when the filter is saved in edit mode.
  * **returns** (FilterGroupPayload): Filter group payload to save to the product.

#### Method signature

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
29
```



```
function onProductSave(callback: OnProductSave): void;

type OnProductSave = () => Promise<FilterGroupPayload> | FilterGroupPayload;

interface FilterGroupPayload {
  id?: string;
  operator: "AND" | "OR";
  groups: FilterPayload[];
}

type FilterPayload =
  | FilterGroupPayload
  | AvpStoredFilterPayload
  | AppStoredFilterPayload;

interface AvpStoredFilterPayload {
  id?: string;
  label: string;
  comparison: string;
  defaultValues: Array<string | null>;
  metadata?: string;
  dimensions: string[];
}

interface AppStoredFilterPayload {
  id?: string;
  label: string;
}
```
```

## Handling saved filters

### filter.onSave

Registers a callback that executes after the filter group has been saved to the product.

#### Usage

```
```
1
2
3
4
5
6
```



```
import { filter } from "@forge/dashboards-bridge";

filter.onSave(async () => {
  console.log("Filter saved");
});
```
```

**Parameters:**

* **callback** (OnSave): Function called after the filter group is saved.

#### Method signature

```
```
1
2
3
4
```



```
function onSave(callback: OnSave): void;

type OnSave = () => Promise<void> | void;
```
```

## Updating session overrides

### filter.updateOverrides

Applies session-only overrides for a filter and returns the saved override. Use overrides to change the active values, comparison, or metadata for a filter during the current dashboard session without changing the persisted filter definition.

#### Usage

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
```



```
import { filter } from "@forge/dashboards-bridge";

try {
  const savedOverride = await filter.updateOverrides("filter-id", {
    values: ["In Progress", "Done"],
  });
} catch (error) {
  console.error("Failed to update filter:", error);
}
```
```

**Parameters:**

* **filterId** (string): ID of the filter to override. This should represent a single filter, not a filter group.
* **override** (FilterOverride): Session-only override values.

#### Method signature

```
```
1
2
3
4
5
```



```
function updateOverrides(
  filterId: string,
  override: FilterOverride,
): Promise<FilterOverride>;
```
```

## Handling dropdown close events

### filter.onDropdownClose

Registers a callback that executes when the view mode filter dropdown closes, including programmatic closes triggered by `filter.closeDropdown()`.

#### Usage

```
```
1
2
3
4
5
6
```



```
import { filter } from "@forge/dashboards-bridge";

filter.onDropdownClose(() => {
  console.log("Filter dropdown closed");
});
```
```

**Parameters:**

* **callback** (OnDropdownClose): Function called when the filter dropdown closes.

#### Method signature

```
```
1
2
3
4
```



```
function onDropdownClose(callback: OnDropdownClose): void;

type OnDropdownClose = () => void;
```
```

## Closing the dropdown

### filter.closeDropdown

Closes the currently open filter dropdown.

#### Usage

```
```
1
2
3
4
```



```
import { filter } from "@forge/dashboards-bridge";

filter.closeDropdown();
```
```

#### Method signature

```
```
1
2
```



```
function closeDropdown(): void;
```
```
