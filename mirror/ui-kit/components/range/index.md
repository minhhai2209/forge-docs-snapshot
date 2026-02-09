# Range

To add the `Range` component to your app:

```
1
import { Range } from "@forge/react";
```

## Description

A range lets users choose an approximate value on a slider.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `defaultValue` | `number` | No | Sets the default value if range is not set. |
| `max` | `number` | No | Sets the maximum value of the range. |
| `min` | `number` | No | Sets the minimum value of the range. |
| `step` | `number` | No | Sets the step value for the range. |
| `onChange` | `(value: number) => void;` | No | Hook to be invoked on change of the range. |
| `id` | `string` | No | Unique identifier. |
| `isDisabled` | `boolean` | No | Sets whether field range is disabled. |
| `value` | `number` | No | Current value of range. |

## Examples

### Default

The default form of a range.

![Example image of range](https://dac-static.atlassian.com/platform/forge/ui-kit/images/range/range-default.png?_v=1.5800.1834)

```
```
1
2
```



```
const RangeExample = () => {
  return (
    <Range value={50} />
  );
};
```
```

### Controlled

In a `controlled` range, the state is managed by the React component. Use the `onChange` handler to set the value.

![Example image of a controlled range](https://dac-static.atlassian.com/platform/forge/ui-kit/images/range/range-controlled.png?_v=1.5800.1834)

```
```
1
2
```



```
import { useState } from "react";
import { Range } from "@forge/react";

const RangeControlledExample = () => {
  const [value, setValue] = useState(50);

  return (
    <>
      <Range value={value} onChange={(value) => setValue(value)} />
      <Text>The current value is: {value}</Text>
    </>
  );
};
```
```

### States

#### Disabled

Set `isDisabled` to disable a range when another action has to be completed before the range is usable.

Avoid using disabled UI where possible. This can cause accessibility problems because disabled UI does not give enough information about what went wrong and how to proceed.

![Example image of a disabled range](https://dac-static.atlassian.com/platform/forge/ui-kit/images/range/range-disabled.png?_v=1.5800.1834)

```
```
1
2
```



```
const RangeDisabledExample = () => {
  return (
    <Range value={50} isDisabled />
  );
};
```
```

### Range in a Form component

A range can be used within a Form to collect user input.

![Example image of range in a form](https://dac-static.atlassian.com/platform/forge/ui-kit/images/range/range-form.png?_v=1.5800.1834)

```
```
1
2
```



```
import { Form, FormSection, FormFooter, HelperMessage, Range, Button, useForm } from "@forge/react";

const RangeFormExample = () => {
  const { register, getFieldId, handleSubmit } = useForm();

  return (
    <Form onSubmit={handleSubmit((value) => console.log(value))}>
      <FormSection>
        <Label labelFor={getFieldId("brightness")}>Adjust brightness</Label>
        <Range {...register("brightness")} />
        <HelperMessage>Move the slider to set your preferred brightness level, then press submit.</HelperMessage>
      </FormSection>
      <FormFooter align="start">
        <Button type="submit">Submit</Button>
      </FormFooter>
    </Form>
  );
};
```
```
