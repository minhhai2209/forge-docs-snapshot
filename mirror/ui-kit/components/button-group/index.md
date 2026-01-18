# Button group

To add the `ButtonGroup` component to your app:

```
1
import { ButtonGroup } from '@forge/react';
```

## Description

A button group gives users access to frequently performed, related actions.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"default" | "danger" | "link" | "primary" | "subtle" | "subtle-link" | "warning"` | No | The appearance to apply to all buttons. |
| `children` | `Array<Button>` | Yes | The buttons to render inside the button group. |
| `label` | `string` | No | Refers to an aria-label attribute. Sets an accessible name for `ButtonGroup` wrapper to announce it to users of assistive technology. Usage of either this, or the `titleId` attribute is strongly recommended. |
| `titleId` | `string` | No | ID referenced by the `ButtonGroup` wrapper's aria-labelledby attribute. This ID should be assigned to the group-button title element. Usage of either this, or the `label` attribute is strongly recommended. |

## Examples

### Appearance

#### Default

A button group displays multiple buttons together.

![Example image of a rendered default ButtonGroup](https://dac-static.atlassian.com/platform/forge/ui-kit/images/button-group/button-group-examples.png?_v=1.5800.1771)

```
```
1
2
```



```
import { Button, ButtonGroup } from '@forge/react';

const ButtonGroupDefaultExample = () => {
  return (
    <ButtonGroup label="Default button group">
      <Button appearance="primary">Submit</Button>
      <Button>Cancel</Button>
    </ButtonGroup>
  );
};
```
```

#### Primary

The appearance to apply to all buttons.

![Example image of a rendered primary ButtonGroup](https://dac-static.atlassian.com/platform/forge/ui-kit/images/button-group/button-group-appearance.png?_v=1.5800.1771)

```
```
1
2
```



```
import { Button, ButtonGroup } from '@forge/react';

const ButtonGroupAppearanceExample = () => {
  return (
    <ButtonGroup appearance="primary" label="Button group with appearance">
      <Button>Contact HR</Button>
      <Button>Feedback</Button>
      <Button>Request IT Support</Button>
    </ButtonGroup>
  );
};
```
```

For more examples, see the [Button component](/platform/forge/ui-kit/components/button/).
