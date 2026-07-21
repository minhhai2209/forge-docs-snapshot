# Breadcrumbs (Preview)

To add the `Breadcrumbs` and `BreadcrumbsItem` components to your app:

```
1
import { Breadcrumbs, BreadcrumbsItem } from '@forge/react';
```

## Description

Breadcrumbs are a navigation system used to show a user's location in a site or app.

## Props

### Breadcrumbs

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `BreadcrumbsItem[]` | Yes | One or more `BreadcrumbsItem` elements that make up the breadcrumb trail. |
| `defaultExpanded` | `boolean` | No | If `true`, the breadcrumbs will be expanded by default when the number of items exceeds `maxItems`. |
| `isExpanded` | `boolean` | No | Controls whether the breadcrumbs are expanded (controlled mode). When set, use alongside an `onExpand` handler to manage state externally. |
| `maxItems` | `number` | No | The maximum number of breadcrumb items to display before collapsing. Defaults to `8`. |
| `itemsBeforeCollapse` | `number` | No | The number of items to show before the ellipsis when the breadcrumbs are collapsed. Defaults to `1`. |
| `itemsAfterCollapse` | `number` | No | The number of items to show after the ellipsis when the breadcrumbs are collapsed. Defaults to `1`. |
| `label` | `string` | No | A label to describe the breadcrumbs navigation landmark to assistive technologies. |
| `onExpand` | `(e: MouseEvent ) => void` | No | Called when the user expands the collapsed breadcrumbs by clicking the ellipsis button. Use this to respond to the expand event when controlling state externally with `isExpanded`. |
| `ellipsisLabel` | `string` | No | A label for the ellipsis button shown when breadcrumbs are collapsed, used by assistive technologies. |
| `testId` | `string` | No | A unique string that appears as a `data-testid` attribute in the rendered HTML. Used for testing. |

### BreadcrumbsItem

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | `string` | Yes | The text label for the breadcrumb item. |
| `href` | `string` | No | The URL the breadcrumb item links to. If omitted, the item renders as plain text. |
| `iconBefore` | `string` | No | Places an icon before the breadcrumb item's text. Use the `glyph` segment of the icon name from the [Atlassian Design System Icon Library](https://atlassian.design/components/icon/icon-explorer). For example, use `"home"` for a home icon. |
| `iconAfter` | `string` | No | Places an icon after the breadcrumb item's text. Use the `glyph` segment of the icon name from the [Atlassian Design System Icon Library](https://atlassian.design/components/icon/icon-explorer). |
| `testId` | `string` | No | A unique string that appears as a `data-testid` attribute in the rendered HTML. Used for testing. |

## Examples

### Default

The default breadcrumbs with a series of linked items.

![Example image of rendered default breadcrumbs](https://dac-static.atlassian.com/platform/forge/ui-kit/images/breadcrumbs/breadcrumbs-default.png?_v=1.5800.2211)

```
```
1
2
```



```
const BreadcrumbsDefaultExample = () => {
  return (
    <Breadcrumbs>
      <BreadcrumbsItem href="https://www.atlassian.com" text="Atlassian" />
      <BreadcrumbsItem href="https://www.atlassian.com/software/jira" text="Jira" />
      <BreadcrumbsItem text="Project" />
    </Breadcrumbs>
  );
};
```
```

### Max items

Use the `maxItems` prop to limit the number of visible breadcrumb items. When the number of items exceeds `maxItems`, the middle items collapse into an ellipsis that can be expanded.

![Example image of rendered breadcrumbs with max items](https://dac-static.atlassian.com/platform/forge/ui-kit/images/breadcrumbs/breadcrumbs-max-items.png?_v=1.5800.2211)

```
```
1
2
```



```
const BreadcrumbsMaxItemsExample = () => {
  return (
    <Breadcrumbs maxItems={3}>
      <BreadcrumbsItem href="https://www.atlassian.com" text="Atlassian" />
      <BreadcrumbsItem href="https://www.atlassian.com/software" text="Software" />
      <BreadcrumbsItem href="https://www.atlassian.com/software/jira" text="Jira" />
      <BreadcrumbsItem href="https://www.atlassian.com/software/jira/projects" text="Projects" />
      <BreadcrumbsItem text="My Project" />
    </Breadcrumbs>
  );
};
```
```

### With icons

Use `iconBefore` and `iconAfter` on `BreadcrumbsItem` to add icons to individual breadcrumb items.

![Example image of rendered breadcrumbs with icons](https://dac-static.atlassian.com/platform/forge/ui-kit/images/breadcrumbs/breadcrumbs-with-icons.png?_v=1.5800.2211)

```
```
1
2
```



```
const BreadcrumbsWithIconsExample = () => {
  return (
    <Breadcrumbs>
      <BreadcrumbsItem
        href="https://www.atlassian.com"
        text="Home"
        iconBefore="home"
      />
      <BreadcrumbsItem
        href="https://www.atlassian.com/software/jira"
        text="Jira"
      />
      <BreadcrumbsItem text="Project" iconAfter="chevron-right" />
    </Breadcrumbs>
  );
};
```
```

### Default expanded

Use `defaultExpanded` to show all breadcrumb items expanded on initial render, even when the number of items exceeds `maxItems`.

![Example image of rendered breadcrumbs default expanded](https://dac-static.atlassian.com/platform/forge/ui-kit/images/breadcrumbs/breadcrumbs-default-expanded.png?_v=1.5800.2211)

```
```
1
2
```



```
const BreadcrumbsDefaultExpandedExample = () => {
  return (
    <Breadcrumbs maxItems={2} defaultExpanded>
      <BreadcrumbsItem href="https://www.atlassian.com" text="Atlassian" />
      <BreadcrumbsItem href="https://www.atlassian.com/software/jira" text="Jira" />
      <BreadcrumbsItem text="Project" />
    </Breadcrumbs>
  );
};
```
```

## Usage guidelines

Breadcrumbs are a navigation component and work best in large, full-page app experiences where users move between hierarchical views. We recommend using `Breadcrumbs` only in the following extension points:

* `globalPage`: Global page apps accessible from the side navigation.
* `fullPage`: Full page Confluence and Jira app experiences

Using breadcrumbs in smaller embedded contexts (e.g. macros or content bylines) can result in a poor user experience. Navigation patterns in compact embedded surfaces typically conflict with the parent app’s navigation.

## Accessibility considerations

When using the `Breadcrumbs` and `BreadcrumbsItem` components, we recommend keeping the following accessibility considerations in mind:

* Use the `label` prop to provide a descriptive name for the breadcrumb navigation region so that assistive technologies can distinguish it from other navigation landmarks on the page.
* Use the `ellipsisLabel` prop to provide a meaningful label for the collapse/expand button so that screen reader users understand its purpose.
* Ensure each breadcrumb item's `text` clearly describes the page or location it links to. Avoid generic labels like "Click here".
* The last item in a breadcrumb trail typically represents the current page and should not have an `href`.
