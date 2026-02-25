# Toggle

To add the `Toggle` component to your app:

```
1
import { Toggle } from '@forge/react';
```

## Description

A toggle is used to view or switch between enabled or disabled states.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `defaultChecked` | `boolean` | No | Whether the toggle is initially checked or not. After the initial interaction, whether the component is checked or not is controlled by the component. |
| `id` | `string` | No | Use a pairing label with your toggle using `id` and `labelFor` props to set the relationship. |
| `isChecked` | `boolean` | No | If defined it takes precedence over `defaultChecked` and `Toggle` acts as a controlled component. You can provide an `onChange` function to be notified of checked value changes. |
| `isDisabled` | `boolean` | No | Sets if the toggle is disabled or not. This prevents any interaction. Keep in mind that disabled toggles will not be available to screen readers. |
| `label` | `string` | No | Text to be used as `aria-label` of toggle component. Use this when there is no visible label for the toggle. |
| `name` | `string` | No | Descriptive name for value property to be submitted in a form. |
| `onBlur` | `(event: FocusEvent) => void` | No | Handler to be called when toggle is unfocused. |
| `onChange` | `(event: ChangeEvent) => void` | No | Handler to be called when native 'change' event happens internally. |
| `onFocus` | `(event: FocusEvent) => void` | No | Handler to be called when toggle is focused. |
| `size` | `"regular" | "large"` | No | Toggle size. |
| `value` | `string` | No | Value to be submitted in a form. |

## Examples

### Default

The default form of a toggle.

![Example image of a rendered default toggle](https://dac-static.atlassian.com/platform/forge/ui-kit/images/toggle/toggle-default.png?_v=1.5800.1877)

```
```
1
2
```



```
import { Label, Toggle } from "@forge/react";

export default function ToggleExample() {
  return (
    <Toggle id="toggle-default" />
  );
}
```
```

### Controlled

#### onChange

Manage the checked state of the input by providing the `isChecked` prop. This requires an `onChange` handler to control the state value that you pass into the `isChecked` prop.

![Example image of a rendered controlled toggle](https://dac-static.atlassian.com/platform/forge/ui-kit/images/toggle/toggle-controlled.png?_v=1.5800.1877)

```
```
1
2
```



```
import React, { useState } from "react";
import { Label, Toggle } from "@forge/react";

export default function ToggleControlledExample() {
  const [isChecked, setIsChecked] = useState(false);

  return (
    <>
      <Toggle 
        id="toggle"
        onChange={() => setIsChecked((prev) => !prev)}
        isChecked={isChecked}
       />
      <Label labelFor="toggle">Field label</Label>
    </>
  );
}
```
```

### States

#### Disabled

When a selection has already been made outside of the current context that negates the need for the toggle, you can use the disabled state.

![Example image of a disabled toggle](https://dac-static.atlassian.com/platform/forge/ui-kit/images/toggle/toggle-disabled.png?_v=1.5800.1877)

```
```
1
2
```



```
export default function ToggleDisabledExample() {
  return (
    <Toggle id="toggle-disabled" isDisabled defaultChecked />
  );
}
```
```

### Size

To call attention to a specific action, use a large toggle.

![Example image of a large toggle](https://dac-static.atlassian.com/platform/forge/ui-kit/images/toggle/toggle-size.png?_v=1.5800.1877)

```
```
1
2
```



```
export default function ToggleLargeExample() {
  return (
    <Toggle size="large" />
  );
}
```
```

### Toggle with hidden label

Always use the `label` prop when there isn't a visible label that you can pair the toggle with.

![Example image of a toggle with a hidden label](https://dac-static.atlassian.com/platform/forge/ui-kit/images/toggle/toggle-hidden-label.png?_v=1.5800.1877)

```
```
1
2
```



```
export default function ToggleLabelExample() {
  return (
    <Toggle id="toggle-default" label="This label is hidden" />
  );
}
```
```

## Accessibility considerations

When using the `Toggle` component, we recommend to keep the following accessibility considerations in mind:

* If you're using a disabled toggle, include information explaining why the option isn't available. You can also use visually hidden to tell people who use screen readers that there is an option that isn't available to them.
* Avoid changing the toggle label based on the on or off state. The label should be the same regardless of the current toggle setting.
* Label your toggle using a `Label` component that properly describes your `Toggle` component.
