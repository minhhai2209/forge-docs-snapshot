# Spinner

To add the `Spinner` component to your app:

```
1
import { Spinner } from '@forge/react';
```

## Description

A spinner is an animated spinning icon that lets users know that content is being loaded.

## Props

| `Name` | `Type` | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"inherit" | "invert"` | No | You can use this to invert the current theme. This is useful when you are displaying a spinner on a background that is not the same background color scheme as the main content. |
| `delay` | `number` | No | Delay the intro animation of the spinner. This is not to be used to avoid quick flickering of the spinner. The spinner will automatically fade in and takes ~200ms to become partially visible. This prop can be helpful for **long delays** such as `500-1000ms` for when you want to not show a spinner until some longer period of time has elapsed. |
| `label` | `string` | No | Describes what the spinner is doing for assistive technologies. For example, "loading", "submitting", or "processing". |
| `size` | `'xsmall' | 'small' | 'medium' | 'large' | 'xlarge' | number` | No | Size of the spinner. The available sizes are `xsmall`, `small`, `medium`, `large`, and `xlarge`. For most use cases, we recommend `medium`. |

## Examples

### Default

The default form of the spinner.

![Example image of a spinner](https://dac-static.atlassian.com/platform/forge/ui-kit/images/spinner/spinner-default.png?_v=1.5800.1783)

```
```
1
2
```



```
const SpinnerExample = () => <Spinner label="loading" />
```
```

### Invert

Use the `invert` appearance when using the spinner on a dark background.

![Example image of a inverted spinner](https://dac-static.atlassian.com/platform/forge/ui-kit/images/spinner/spinner-invert.png?_v=1.5800.1783)

```
```
1
2
```



```
const SpinnerInvertExample = () => <Spinner label="loading" appearance="invert" />
```
```

### Sizes

The spinner can be set to different sizes. `medium` is the default size and is recommended for most use cases.

![Example image of spinner sizes](https://dac-static.atlassian.com/platform/forge/ui-kit/images/spinner/spinner-sizes.png?_v=1.5800.1783)

```
```
1
2
```



```
const SpinnerSizeExample = () => {
  return (
    <Inline>
      <Spinner size="xsmall" />
      <Spinner size="small" />
      <Spinner size="medium" />
      <Spinner size="large" />
      <Spinner size="xlarge" />
      <Spinner size={80} />
    </Inline>
  );
}
```
```

## Accessibility considerations

When using the `Spinner` component, we recommend keeping the following accessibility considerations in mind:

* Always use a label to add context for assistive technologies. Make sure the label accurately describes the type of process that's occurring. For example, "loading", "submitting", or "processing".
