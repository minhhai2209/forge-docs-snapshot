# Empty state

To add the `EmptyState` component to your app:

```
1
import { EmptyState } from "@forge/react";
```

## Description

An empty state appears when there is no data to display and describes what the user can do next.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `buttonGroupLabel` | `string` | No | Accessible name for the action buttons group. |
| `description` | `string` | No | The main block of text that holds additional supporting information. |
| `header` | `string` | Yes | Title that briefly describes the page to the user. |
| `headingLevel` | `number` | No | The value used to set the heading level of the header element. Must be in the range of `1` to `6`. Defaults to `4`. |
| `isLoading` | `boolean` | No | Used to indicate a loading state. Will show a spinner next to the action buttons when `true`. |
| `primaryAction` | `ForgeElement` | No | Primary action button for the page. |
| `secondaryAction` | `ForgeElement` | No | Secondary action button for the page. |
| `tertiaryAction` | `ForgeElement` | No | Tertiary action button for the page. |
| `width` | `"narrow"` | `"wide"` | No | Controls how much horizontal space the component fills. Defaults to `wide`. |

## Examples

### Default

The only required property of an empty state is the header.

![Example image of empty state](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-default.png?_v=1.5800.1834)

```
```
1
2
```



```
export const EmptyStateExample = () => {
  return <EmptyState header="You don't have access to this issue" />;
};
```
```

The `headingLevel` rendered by default is `4`. To make sure that the empty state is accessible, headers must follow a logical order. If the empty state does not follow a `h3` or `h4` in the reading order, then you will need to modify the heading order to the next logical heading level.

![Example image of empty state with custom heading level](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-custom-heading-level.png?_v=1.5800.1834)

```
```
1
2
```



```
export const CustomHeadingLevelEmptyStateExample = () => {
  return (
    <EmptyState header="You don't have access to this issue" headingLevel={1} />
  );
};
```
```

### Description

Descriptions should add useful and relevant additional information.

![Example image of empty state with description](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-description.png?_v=1.5800.1834)

```
```
1
2
```



```
export const EmptyStateWithDescriptionExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      description="Make sure the issue exists in this project. If it does, ask a project admin for permission to see the project's issues."
    />
  );
};
```
```

### Actions

#### Primary

Use a primary action button to recommend the best next step that people can take.

![Example image of empty state one action](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-actions-primary.png?_v=1.5800.1834)

```
```
1
2
```



```
export const EmptyStateWithOneActionExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      primaryAction={<Button appearance="primary">Request access</Button>}
    />
  );
};
```
```

#### Secondary

Use a secondary action button to recommend an alternate step that people could take. This will render on the left side of the primary action button.

![Example image of empty state with two actions](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-actions-secondary.png?_v=1.5800.1834)

```
```
1
2
```



```
export const EmptyStateWithTwoActionsExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      primaryAction={<Button appearance="primary">Request access</Button>}
      secondaryAction={<Button>View permissions</Button>}
    />
  );
};
```
```

#### Tertiary

Use tertiary action buttons to link to external resources or documentation to further explain how to resolve the empty state. This will render below the primary and secondary action buttons.

![Example image of empty state with all actions](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-actions-tertiary.png?_v=1.5800.1834)

```
```
1
2
```



```
export const EmptyStateWithAllActionsExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      primaryAction={<Button appearance="primary">Request access</Button>}
      secondaryAction={<Button>View permissions</Button>}
      tertiaryAction={
        <LinkButton appearance="link" href="/">
          About permissions
        </LinkButton>
      }
    />
  );
};
```
```

### Loading State

Use the `isLoading` prop to indicate a loading state. This will show a spinner next to the action buttons when true.

![Example image of loading state empty state](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-loading-state.png?_v=1.5800.1834)

```
```
1
2
```



```
export const LoadingStateEmptyStateExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      primaryAction={<Button appearance="primary">Request access</Button>}
      isLoading={true}
    />
  );
};
```
```

### Width

#### Narrow

The horizontal space that an empty state takes up can be controlled with the `width` prop. It can be set to either `narrow` or `wide`, where the default is `wide`.

![Example image of narrow empty state](https://dac-static.atlassian.com/platform/forge/ui-kit/images/empty-state/empty-state-width-narrow.png?_v=1.5800.1834)

```
```
1
2
```



```
export const NarrowEmptyStateExample = () => {
  return (
    <EmptyState
      header="You don't have access to this issue"
      description="Make sure the issue exists in this project. If it does, ask a project admin for permission to see the project's issues."
      primaryAction={<Button appearance="primary">Request access</Button>}
      width="narrow"
    />
  );
};
```
```
