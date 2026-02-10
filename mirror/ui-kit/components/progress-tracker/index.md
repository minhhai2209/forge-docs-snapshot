# Progress tracker

To add the `ProgressTracker` component to your app:

```
1
import { ProgressTracker } from '@forge/react';
```

## Description

A progress tracker displays the steps and progress through a journey.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `animated` | `boolean` | No | Turns off transition animations if set to `false`. |
| `items` | `Array<{ id: string; label: string; percentageComplete: number; status: 'unvisited' | 'visited' | 'current' | 'disabled'; onClick?: () => void; }>` | Yes | Ordered list of stage data. |
| `label` | `string` | No | Text to be used as an aria-label of progress tracker. |
| `spacing` | `"comfortable" | "cosy" | "compact"` | No | Margin spacing type between steps. |

## Examples

### Default

The default version of a progress tracker that shows all the steps and states in a journey.

![Example image of a progress tracker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-tracker/progress-tracker-default.png?_v=1.5800.1837)

```
```
1
2
```



```
const ProgressTrackerExample = () => {
  return (
    <ProgressTracker
      items={[
        {
          id: "1",
          label: "Disabled step",
          percentageComplete: 100,
          status: "disabled",
        },
        {
          id: "2",
          label: "Create a space",
          percentageComplete: 100,
          status: "visited",
        },
        {
          id: "3",
          label: "Upload a photo",
          percentageComplete: 0,
          status: "current",
        },
        {
          id: "4",
          label: "Your details",
          percentageComplete: 0,
          status: "unvisited",
        },
        {
          id: "5",
          label: "Invite users",
          percentageComplete: 0,
          status: "unvisited",
        },
        {
          id: "6",
          label: "Confirm",
          percentageComplete: 0,
          status: "unvisited",
        },
      ]}
    />
  );
};
```
```

### Spacing

The margin spacing in between the steps of a progress tracker. Box with width must be used to apply spacing.

#### Comfortable

![Example image of comfortable progress tracker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-tracker/progress-tracker-comfortable.png?_v=1.5800.1837)

```
```
1
2
```



```
const items = [
  {
    id: "1",
    label: "Disabled step",
    percentageComplete: 100,
    status: "disabled",
  },
  {
    id: "2",
    label: "Create a space",
    percentageComplete: 100,
    status: "visited",
  },
  {
    id: "3",
    label: "Upload a photo",
    percentageComplete: 0,
    status: "current",
  },
  {
    id: "4",
    label: "Your details",
    percentageComplete: 0,
    status: "unvisited",
  },
    {
    id: "5",
    label: "Invite users",
    percentageComplete: 0,
    status: "unvisited",
  },
  {
    id: "6",
    label: "Confirm",
    percentageComplete: 0,
    status: "unvisited",
  },
];

const ProgressTrackerSpacingExample = () => (
  <Box xcss={{ width: "320px" }}>
    <ProgressTracker items={items} spacing="comfortable" />
  </Box>
);
```
```

#### Cosy (default)

![Example image of cosy progress tracker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-tracker/progress-tracker-cosy.png?_v=1.5800.1837)

```
```
1
2
```



```
const ProgressTrackerSpacingExample = () => (
  <Box xcss={{ width: "320px" }}>
    <ProgressTracker items={items} spacing="cosy" />
  </Box>
);
```
```

#### Compact

![Example image of compact progress tracker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-tracker/progress-tracker-compact.png?_v=1.5800.1837)

```
```
1
2
```



```
const ProgressTrackerSpacingExample = () => (
  <Box xcss={{ width: "320px" }}>
    <ProgressTracker items={items} spacing="compact" />
  </Box>
);
```
```

### Completed

A progress tracker that shows all steps have been completed.

![Example image of compact progress tracker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-tracker/progress-tracker-completed.png?_v=1.5800.1837)

```
```
1
2
```



```
const ProgressTrackerCompletedExample = () => {
  return ( 
    <ProgressTracker items={[
      {
        id: '1',
        label: 'Disabled step',
        percentageComplete: 100,
        status: 'disabled',
      },
      {
        id: '2',
        label: 'Create a space',
        percentageComplete: 100,
        status: 'visited',
      },
      {
        id: '3',
        label: 'Upload a photo',
        percentageComplete: 100,
        status: 'visited',
      },
      {
        id: '4',
        label: 'Your details',
        percentageComplete: 100,
        status: 'visited',
      },
      {
        id: '5',
        label: 'Invite users',
        percentageComplete: 100,
        status: 'visited',
      },
      {
        id: '6',
        label: 'Confirm',
        percentageComplete: 0,
        status: 'current',
      },
    ]} />
  );
}
```
```

## Accessibility considerations

When using the `ProgressTracker` component, we recommend keeping the following accessibility considerations in mind:

* Use labels that clearly indicate the purpose of the step. When writing, keep options to a single line of text, be short and concise (1-2 words).
* If a task needs more than six steps, consider simplifying the process or breaking it up into multiple tasks.
