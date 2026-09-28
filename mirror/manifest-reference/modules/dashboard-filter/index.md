# Dashboard filter (EAP)

## Dashboard filter module

The dashboard filter module lets your app add filters to dashboards. Each filter can:

* Be read from your custom widgets across the dashboard
* Provide an edit experience where users configure the filter
* Apply session-only overrides in view mode without changing the persisted definition

### Setup instructions

You can create a dashboard filter app with the following steps:

1. Add a `dashboards:filter` module to your app's `manifest.yml`.
2. Provide a `title`, `icon`, and `edit.resource` for the filter.
3. Add either a `resource` for a dropdown or a `function` for a backend implementation.
4. Use the [`filter`](/platform/forge/apis-reference/dashboard-bridge-apis/filter/) APIs from `@forge/dashboards-bridge` to save filter definitions and update session overrides.
5. Run `forge deploy` to deploy the app.
6. Run `forge install` and follow the prompts to install the app to a product that supports dashboard filters.

## Manifest configuration

### modules.dashboards:filter

A dashboard filter must define exactly one runtime entry point. Use `resource` for a dropdown or `function` for a backend function.
All filters must also define `edit.resource` for configuring the persisted filter group.

#### Example with Custom UI dropdown

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
```



```
modules:
  dashboards:filter:
    - key: status-filter
      title: Status
      icon: resource:icon;icons/status.svg
      resource: filter-dropdown
      edit:
        resource: filter-edit

resources:
  - key: icon
    path: static/icons
  - key: filter-dropdown
    path: static/filter-dropdown/build
  - key: filter-edit
    path: static/filter-edit/build
```
```

#### Example with UI Kit dropdown

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
```



```
modules:
  dashboards:filter:
    - key: status-filter-ui-kit
      title: Status
      icon: resource:icon;icons/status.svg
      resource: filter-dropdown
      render: native
      edit:
        resource: filter-edit
        render: native

resources:
  - key: icon
    path: static/icons
  - key: filter-dropdown
    path: static/filter-dropdown/build
  - key: filter-edit
    path: static/filter-edit/build
```
```

#### Example with backend function

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
```



```
modules:
  dashboards:filter:
    - key: status-filter
      title: Status
      icon: resource:icon;icons/status.svg
      function: status-filter-handler
      edit:
        resource: status-filter-edit

resources:
  - key: icon
    path: static/icons
  - key: status-filter-edit
    path: static/filter-edit/build

functions:
  - key: status-filter-handler
    handler: index.dashboardFilter
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest. |
| `title` | `string` | Yes | The title of the filter as displayed to users. |
| `icon` | `string` | Yes | The icon shown for the filter. This can reference an app resource, for example `resource:icon;icons/status.svg`. |
| `resource` | `string` | Conditional | The key of the static resource that provides the filter dropdown experience. Required for filter dropdowns. |
| `function` | `string` | Conditional | The key of the backend function that provides the filter implementation. Required when the filter is backed by a function. |
| `edit` | `object` | Yes | Configuration for the filter edit experience. |

### edit object properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `resource` | `string` | Yes | The key of a static resource entry that provides the filter edit experience. |

## Runtime behavior

In view mode, a dashboard filter is backed by either a dropdown resource or a backend function.

### Filter dropdown

Use a dropdown when the filter needs an interactive user interface. The dropdown resource renders when a user opens the filter from the dashboard filter top bar.

In the dropdown resource, use `filter.updateOverrides` to apply session-only values, `filter.closeDropdown` to close the dropdown, and the dashboard filter hooks from `@forge/hooks/dashboards` to read the current filter state.

### Filter function

Use a backend function for filters that don't need to render a dropdown. Set `function` on the `dashboards:filter` module; the function runs when a user clicks the filter pill in the top bar.

The function receives the persisted filter group, the currently applied session overrides, and the specific filter represented by the pill that was clicked. Return an overrides map keyed by filter ID to update session-only filter state. Return `null`, `undefined`, or nothing to leave overrides unchanged.

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
import type { FilterFunction } from "@forge/dashboards-bridge";

export const dashboardFilter: FilterFunction = async (event) => {
  const { filter, filterGroup, overrides } = event;

  return {
    [filter.id]: {
      values: ["Done"],
      comparison: "EQUALS",
      metadata: undefined,
    },
  };
};
```
```

The function must follow this shape:

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
type FilterFunction = (event: {
  filterGroup: FilterGroup;
  overrides: Record<string, FilterOverride>;
  filter: Filter;
}) => Promise<Record<string, FilterOverride> | null | undefined | void>;

type FilterOverride = {
  values?: Array<string | null>;
  comparison?: string;
  metadata?: string;
};
```
```

### Filter edit mode

All filters require an edit resource. The edit resource is used when the user configures the filter in the side panel. Register `filter.onProductSave` in the edit resource to return the filter group payload that should be saved to the product.

## Filter definitions

Dashboard filters are saved as a filter tree. For the full data shape, see the [filter model](/platform/forge/apis-reference/dashboard-bridge-apis/filter/#filter-model) in the `filter` bridge API documentation.

## API documentation

For detailed API documentation, see:

* [filter (EAP)](/platform/forge/apis-reference/dashboard-bridge-apis/filter/) - Bridge APIs for filter definitions, save lifecycle events, dropdown lifecycle events, and session overrides
* [useCurrentFilter (EAP)](/platform/forge/ui-kit/hooks/use-current-filter/) - React hook for the filter represented by the currently open dropdown
* [useFilters (EAP)](/platform/forge/ui-kit/hooks/use-filters/) - React hook for persisted filters and session overrides
* [useWidgetContext](/platform/forge/ui-kit/hooks/use-widget-context/) - React hook that lets dashboard widgets read the active dashboard filter expression

## Examples

Use the [Dashboard bridge APIs](/platform/forge/apis-reference/dashboard-bridge-apis/bridge/) and [dashboard hooks](/platform/forge/ui-kit/hooks/hooks-reference/) to build filter dropdown and edit experiences.

### Filter edit resource

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
```



```
import React from "react";
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

function StatusFilterEdit() {
  return <div>Status filter settings</div>;
}

export default StatusFilterEdit;
```
```

### Filter dropdown resource

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
38
39
40
41
42
43
44
45
46
```



```
import React from "react";
import { filter } from "@forge/dashboards-bridge";
import { useCurrentFilter } from "@forge/hooks/dashboards";

const statuses = ["To Do", "In Progress", "Done"];

function StatusFilterDropdown() {
  const { filter: currentFilter, override } = useCurrentFilter();

  if (!currentFilter) {
    return null;
  }

  const selectedValues = override?.values ?? [];

  const toggleStatus = async (status) => {
    const values = selectedValues.includes(status)
      ? selectedValues.filter((value) => value !== status)
      : [...selectedValues, status];

    try {
      await filter.updateOverrides(currentFilter.id, { values });
    } catch (error) {
      console.error("Failed to update filter:", error);
    }
  };

  return (
    <div>
      {statuses.map((status) => (
        <label key={status}>
          <input
            checked={selectedValues.includes(status)}
            onChange={() => toggleStatus(status)}
            type="checkbox"
          />
          {status}
        </label>
      ))}
      <button onClick={() => filter.closeDropdown()}>Apply</button>
    </div>
  );
}

export default StatusFilterDropdown;
```
```

Dashboard widgets can read active dashboard filters through `useWidgetContext()`, where `filters` contains the current dashboard filter expression or `null`.

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
```



```
import React from "react";
import { useWidgetContext } from "@forge/hooks/dashboards";

function FilterAwareWidget() {
  const context = useWidgetContext();

  if (!context) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <p>Dashboard ID: {context.dashboardId}</p>
      <p>Has filters: {context.filters ? "Yes" : "No"}</p>
    </div>
  );
}

export default FilterAwareWidget;
```
```
