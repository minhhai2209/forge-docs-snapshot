# Pagination (Preview)

To add the `Pagination` component to your app:

```
1
import { Pagination } from '@forge/react';
```

## Description

Pagination allows you to divide large amounts of content into chunks across multiple pages.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `pages` | `number[]` | Yes | An array of page numbers to display. For example, `[1, 2, 3, 4, 5]`. |
| `defaultSelectedIndex` | `number` | No | The index of the page that is selected by default (uncontrolled). Defaults to `0`. |
| `selectedIndex` | `number` | No | The index of the currently selected page (controlled). Use alongside `onChange` to manage state externally. |
| `onChange` | `(page: number) => void` | No | Called when the user navigates to a different page. Receives the selected page number as an argument. The page number is the **value** of the page in the pages array and not the index. |
| `max` | `number` | No | The maximum number of page buttons to display at once. When there are more pages than the max, pages are truncated with ellipses. |
| `label` | `string` | No | An accessible label for the pagination navigation landmark. |
| `nextLabel` | `string` | No | An accessible label for the next page button. |
| `previousLabel` | `string` | No | An accessible label for the previous page button. |
| `pageLabel` | `string` | No | An accessible label applied to each page button. The page number is appended automatically. |
| `testId` | `string` | No | A unique string that appears as a `data-testid` attribute in the rendered HTML. Used for testing. |

## Examples

### Default

The default pagination with a list of pages.

![Example image of rendered default pagination](https://dac-static.atlassian.com/platform/forge/ui-kit/images/pagination/pagination-default.png?_v=1.5800.2167)

```
```
1
2
```



```
const PaginationDefaultExample = () => {
  return <Pagination pages={[1, 2, 3, 4, 5]} />;
};
```
```

### Selected index

Use `defaultSelectedIndex` to pre-select a page on initial render. The index is zero-based, so `defaultSelectedIndex={2}` selects the third page.

![Example image of rendered pagination with selected index](https://dac-static.atlassian.com/platform/forge/ui-kit/images/pagination/pagination-selected-index.png?_v=1.5800.2167)

```
```
1
2
```



```
const PaginationSelectedIndexExample = () => {
  return <Pagination pages={[1, 2, 3, 4, 5]} defaultSelectedIndex={2} />;
};
```
```

## Accessibility considerations

When using the `Pagination` component, we recommend keeping the following accessibility considerations in mind:

* Use the `label` prop to provide a descriptive name for the pagination navigation region so that assistive technologies can distinguish it from other navigation on the page.
* Use the `nextLabel`, `previousLabel`, and `pageLabel` props to provide meaningful accessible labels for the navigation buttons, especially in non-English apps.
