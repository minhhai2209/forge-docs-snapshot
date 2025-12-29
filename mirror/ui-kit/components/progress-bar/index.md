# Progress bar

To add the `ProgressBar` component to your app:

```
1
import { ProgressBar } from '@forge/react';
```

## Description

A progress bar communicates the status of a system process.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"default" | "success" | "inverse"` | No | Visual style of the progress bar. |
| `ariaLabel` | `string` | No | Label associated with the progress bar, read by screen readers. |
| `isIndeterminate` | `boolean` | No | Shows the progress bar in an indeterminate state when true. |
| `value` | `number` | No | Sets the value of the progress bar, between 0 and 1 inclusive. |

## Examples

### Appearance

#### Default

The default appearance of a progress bar.

![Example image of a progress bar with default appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-bar/progress-bar-default.png?_v=1.5800.1739)

```
```
1
2
```



```
const ProgressBarDefaultExample = () => {
  return <ProgressBar ariaLabel="Done: 3 of 10 issues" value={0.3} />;
};
```
```

#### Inverse

![Example image of a progress bar with inverse appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-bar/progress-bar-inverse.png?_v=1.5800.1739)

```
```
1
2
```



```
const ProgressBarInverseExample = () => {
  return (
    <Box backgroundColor="color.background.information.bold">
      <ProgressBar
        appearance="inverse"
        ariaLabel="Done: 6 of 10 issues"
        value={0.6}
      />
    </Box>
  );
};
```
```

#### Success

Success indicates the completion of a process.

![Example image of a progress bar with success appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-bar/progress-bar-success.png?_v=1.5800.1739)

```
```
1
2
```



```
const ProgressBarSuccessExample = () => {
  return (
    <ProgressBar
      appearance="success"
      ariaLabel="Done: 10 of 10 issues"
      value={1}
    />
  );
};
```
```

### Indeterminate

`Indeterminate` progress bars display movement along the container until the process is finished.

![Example image of a progress bar with indeterminate appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/progress-bar/progress-bar-indeterminate.png?_v=1.5800.1739)

```
```
1
2
```



```
const ProgressBarIndeterminateExample = () => {
  return <ProgressBar ariaLabel="Loading issues" isIndeterminate />;
};
```
```

## Accessibility considerations

When using the `ProgressBar` component, we recommend keeping the following accessibility considerations in mind:

* Use the progress bar component as a loading indicator or to communicate the status of a system process.
* Use helper text with a progress bar if the process is complex or has a long wait time. This lets users know what sub-processes are taking place.
* Use a success state when the actions required to continue have been fulfilled.
