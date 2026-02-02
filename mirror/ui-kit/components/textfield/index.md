# Text field

To add the `Textfield` component to your app:

```
1
import { Textfield } from "@forge/react";
```

## Description

A text field is an input that allows a user to write or edit text.

## Props

| Name | Type | Required | Available in macro config | Description |
| --- | --- | --- | --- | --- |
| `appearance` | `"subtle" | "standard" | "none"` | No | No | Affects the visual style of the text field. |
| `aria-invalid` | `boolean | "false" | "true" | "grammar" | "spelling"` | No | No | Indicates the entered value does not conform to the format expected by the application. |
| `aria-labelledby` | `string` | No | No | Identifies the element (or elements) that labels the current element. |
| `defaultValue` | `string | number` | No | Yes | The default value of the text field. |
| `elemAfterInput` | `ForgeElement` | No | No | Element after input in text field. |
| `elemBeforeInput` | `ForgeElement` | No | No | Element before input in text field. |
| `id` | `string` | No | No | Used to specify a unique ID for the current element. |
| `isCompact` | `boolean` | No | No | Applies compact styling, making the field smaller. |
| `isDisabled` | `boolean` | No | No | Sets the field as to appear disabled. Users will not be able to interact with the text field. |
| `isInvalid` | `boolean` | No | No | Changes the text field to have a border indicating that its value is invalid. |
| `isMonospaced` | `boolean` | No | No | Sets content text value to appear monospaced. |
| `isReadOnly` | `boolean` | No | No | If `true`, prevents the value of the input from being edited. |
| `isRequired` | `boolean` | No | Yes | Set required for form that the field is part of. |
| `max` | `string | number` | No | No | Specifies the maximum value for the text field. |
| `maxLength` | `number` | No | No | Specifies the maximum number of characters allowed in the input area. |
| `min` | `string | number` | No | No | Specifies the minimum value for the text field. |
| `minLength` | `number` | No | No | Specifies the minimum number of characters required in the input area. |
| `name` | `string` | Required for macro configuration, not required for other extension points | Yes | Name of the input element. |
| `onBlur` | `(e: FocusEvent) => void` | No | No | Handler called when the text field looses focus. |
| `onChange` | `(e: FormEvent) => void` | No | No | Handler called when the input value changes. |
| `onFocus` | `(e: FocusEvent) => void` | No | No | Handler called when the text field gets focused. |
| `placeholder` | `string` | No | Yes | Placeholder text to display in the text field whenever it is empty. |
| `type` | `string` | No | No | Specifies the type of input element to display. |
| `value` | `string | number` | No | No | The value of the text field. |
| `width` | `string | number` | No | No | Sets maximum width of input. |

## Examples

### Basic

A basic text field. Use the `Label` component to describe what the user should enter in the text field.

![Example image of a rendered basic text field](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-basic.png?_v=1.5800.1808)

```
```
1
2
```



```
import { Label, Textfield } from "@forge/react";

export default function TextfieldBasicExample() {
  return (
    <>
      <Label labelFor="textfield">Field label</Label>
      <Textfield name="basic" id="textfield" />
    </>
  );
}
```
```

### Field label and message

Always use a label component for each field and associate the label to the field properly. Use the `HelperMessage` component for any optional field-related message.

#### Required field label

For required fields, always add `RequiredAsterisk` component next to the label.

#### Validation

Use `ErrorMessage` or `ValidMessage` components to display validation-related messages.

![Example image of a validation message](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-field-label.png?_v=1.5800.1808)

```
```
1
2
```



```
import React, { useState } from "react";
import { ErrorMessage, Label, RequiredAsterisk, Textfield } from "@forge/react";

export default function TextfieldValidation() {
  const [error, setError] = useState(undefined);

  const validate = (event) => {
  
    const value = event.target.value;
    
    if (value.length === 0) {
      setError('This field is required');
    } else {
      setError(undefined);
    }
  };

  return (
    <>
      <Label labelFor="textfield">
        Field label
        <RequiredAsterisk />
      </Label>
      <Textfield
        appearance="standard"
        placeholder="Placeholder"
        onChange={validate}
      />
      {error && <ErrorMessage>{error}</ErrorMessage>}
    </>
  );
}
```
```

### Appearance

#### Standard

The default text field appearance.

![Example image of a rendered standard appearance text field](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-standard.png?_v=1.5800.1808)

```
```
1
2
```



```
export default function TextfieldAppearanceStandard() {
  return (
    <Textfield
      appearance="standard"
      placeholder="Enter project name"
    />
  );
}
```
```

#### Subtle

A text field that's transparent until focused.

![Example image of a rendered subtle appearance text field](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-subtle.png?_v=1.5800.1808)

```
```
1
2
```



```
export default function TextfieldAppearanceSubtle() {
  return (
    <Textfield
      appearance="subtle"
      placeholder="Enter project name"
    />
  );
}
```
```

### Spacing

#### Compact

A text field with compact spacing.

![Example image of a rendered text field with compact spacing](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-spacing.png?_v=1.5800.1808)

```
```
1
2
```



```
import { Label, Textfield } from "@forge/react";

export default function TextfieldCompact() {
  return (
    <>
      <Label labelFor="textfield">Field label</Label>
      <Textfield
        id="textfield"
        spacing="compact"
        defaultValue="Compact text field"
      />
    </>
  );
}
```
```

### States

The different states a text field can be in.

![Example image of text field states](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-states.png?_v=1.5800.1808)

```
```
1
2
```



```
import { Label, Textfield } from "@forge/react";

export default function TextfieldStates() {
  return (
    <Stack space="space.300">
      <Box>
        <Label labelFor="textfield">Field label</Label>
        <Textfield
          id="textfield"
          defaultValue="Disabled"
          isDisabled
        />
      </Box>
      <Box>
        <Label labelFor="textfield">Field label</Label>
        <Textfield
          id="textfield"
          defaultValue="Invalid"
          isInvalid
        />
      </Box>
      <Box>
        <Label labelFor="textfield">Field label</Label>
        <Textfield
          id="textfield"
          defaultValue="Read-only"
          isReadOnly
        />
      </Box>
      <Box>
        <Label labelFor="textfield" isRequired>Field label</Label>
        <Textfield
          id="textfield"
          defaultValue="Invalid"
          isRequired
        />
      </Box>
    </Stack>
  );
}
```
```

### Elements before and after

#### Standard

Elements can be added before and after the input.

![Example image of a rendered text field with elements before and after](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-before-after-elements.png?_v=1.5800.1808)

```
```
1
2
```



```
import { Textfield, Icon } from "@forge/react";

export default function TextfieldElements() {
  return (
    <Stack space="space.300">
      <Textfield
        elemBeforeInput={
          <Box xcss={{ marginTop: "space.050", marginLeft: "space.100" }}>
            <Icon glyph="user-avatar-circle" label="User" />
          </Box>
        }
        placeholder="Before input"
      />
      <Textfield
        elemAfterInput={
          <Box xcss={{ marginTop: "space.050", marginRight: "space.100" }}>
            <Icon glyph="error" label="error" />
          </Box>
        }
        placeholder="After input"
      />
    </Stack>
  );
}
```
```

### Text field in a form component

Validation can be applied to a text field when used in a `Form` component along with the `useForm` hook.

![Example image of a rendered text field in a form](https://dac-static.atlassian.com/platform/forge/ui-kit/images/textfield/text-field-form-validation.png?_v=1.5800.1808)

```
```
1
2
```



```
import { Form, Field, Label, Textfield, Button, ErrorMessage, useForm } from "@forge/react";

export default function TextfieldFormExample() {

  const { handleSubmit, register, getFieldId, formState } = useForm();

  return (
    <Form onSubmit={handleSubmit((data) => console.log(data))}>
      <Button onClick={() => console.log(formState)}>Log form state</Button>
      <FormHeader title="Form header" />
      <FormSection>
        <Label labelFor={getFieldId("textfield")}>Field label</Label>
        <Textfield {...register("textfield", { minLength: 10 })} />
        {formState.errors.textfield && (
          <ErrorMessage>Minimum 10 characters required</ErrorMessage>
        )}
      </FormSection>
      <FormFooter align="start">
        <Button appearance="primary" type="submit">
          Submit
        </Button>
      </FormFooter>
    </Form>
  );
}
```
```

## Accessibility considerations

When using the `Textfield` component, we recommend keeping the following accessibility considerations in mind:

* Make sure all fields have a visible label. If you're not using the provided field `Label` component, make sure the label is associated properly to the field for accessibility.
* Avoid using placeholder text whenever possible. Make sure any critical information is communicated either in the field label or using helper text below the field. Search fields or brief examples are the only exceptions where placeholder text is okay.
