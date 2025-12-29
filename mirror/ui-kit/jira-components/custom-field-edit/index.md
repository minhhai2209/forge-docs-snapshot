# Custom field edit (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

To add the `CustomFieldEdit` component to your app:

```
1
import { CustomFieldEdit } from '@forge/react/jira';
```

## Description

A `CustomFieldEdit` is a wrapper component that provides inline edit features for Forge custom fields in edit mode for apps with `isInline` property defined in app's manifest. The wrapper replicates the behavior of all other Jira fields.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `onSubmit` | `() => void` | Yes | Event handler called when the field is submitted. |
| `hideActionButtons` | `boolean` | No | Sets whether the confirm and cancel action buttons are displayed in the bottom right of the field in the issue view render context. Defaults to `false`. |
| `disableSubmitOnBlur` | `boolean` | No | Disables field submission on blur event. Defaults to `false`. |
| `disableSubmitOnEnter` | `boolean` | No | Disables field submission on "Enter" key press. It is recommended to use this property when `CustomFieldEdit` wraps components such as [Text Area](/platform/forge/ui-kit/components/text-area/) that uses the "Enter" key to break a line in a text editor. Defaults to `false`. |
| `children` | `Forge Element` | Yes | The content of the component. |

## Examples

### Default

`CustomFieldEdit` is a wrapper around a custom edit implementation for Forge custom fields. Create this implementation using [UI Kit components](/platform/forge/ui-kit/components/).

#### Text field

![Example image of an Custom field edit with text field](https://dac-static.atlassian.com/platform/forge/ui-kit/images/jira/custom-field-edit/custom-field-edit-textfield.png?_v=1.5800.1739)

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import { Textfield } from "@forge/react";
import { CustomFieldEdit } from "@forge/react/jira";
import { view } from "@forge/bridge";

const Edit = () => {
  const [value, setValue] = useState("");

  const onSubmit = useCallback(() => {
    view.submit(value);
  }, [view, value]);

  return (
    <CustomFieldEdit onSubmit={onSubmit}>
      <Textfield
        onChange={(e) => {
          setValue(e.target.value);
        }}
      />
    </CustomFieldEdit>
  );
};
```
```

#### Select

![Example image of an Custom field edit with select](https://dac-static.atlassian.com/platform/forge/ui-kit/images/jira/custom-field-edit/custom-field-edit-select.png?_v=1.5800.1739)

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import { Select } from "@forge/react";
import { CustomFieldEdit } from "@forge/react/jira";
import { view } from "@forge/bridge";

const Edit = () => {
  const [value, setValue] = useState("apple");

  const onSubmit = useCallback(() => {
    view.submit(value);
  }, [view, value]);

  const selectOptions = [
    { label: "Apple", value: "apple" },
    { label: "Banana", value: "banana" },
  ];

  return (
    <CustomFieldEdit hideActionButtons onSubmit={onSubmit}>
      <Select
        appearance="default"
        options={selectOptions}
        onChange={(e) => {
          setValue(e.value);
        }}
      />
    </CustomFieldEdit>
  );
};
```
```

#### Multiple components

![Example image of an Custom field edit with select open](https://dac-static.atlassian.com/platform/forge/ui-kit/images/jira/custom-field-edit/custom-field-edit-multiple-components-select.png?_v=1.5800.1739)

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import { Select, Textfield, Box, Stack } from "@forge/react";
import { CustomFieldEdit } from "@forge/react/jira";
import { view } from "@forge/bridge";

const Edit = () => {
  const [textValue, setTextValue] = useState("defaultValue");
  const [selectValue, setSelectValue] = useState("");

  const onSubmit = useCallback(() => {
    view.submit(`Text: ${textValue} | Select: ${selectValue}`);
  }, [view, textValue, selectValue]);

  return (
    <CustomFieldEdit onSubmit={onSubmit}>
      <Box>
        <Stack space="space.100">
          <Select
            appearance="default"
            options={[
              { label: "Apple", value: "apple" },
              { label: "Banana", value: "banana" },
            ]}
            onChange={(e) => {
              setSelectValue(e.value);
            }}
          />
          <Textfield
            defaultValue="defaultValue"
            onChange={(e) => {
              setTextValue(e.target.value);
            }}
          />
          <Textfield />
          <Textfield />
        </Stack>
      </Box>
    </CustomFieldEdit>
  );
};
```
```

### No action buttons

On the Issue view, contextual action buttons are rendered next to each field by default. These are a checkmark (confirm edit) and a cross (cancel edit). You can use `hideActionButtons` to hide them, but we don’t recommend doing so if you want to maintain consistency with the overall Jira experience.

![Example image of an Custom field edit with no action buttons](https://dac-static.atlassian.com/platform/forge/ui-kit/images/jira/custom-field-edit/custom-field-edit-no-action-buttons.png?_v=1.5800.1739)

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import { Textfield } from "@forge/react";
import { CustomFieldEdit } from "@forge/react/jira";
import { view } from "@forge/bridge";

const Edit = () => {
  const [value, setValue] = useState("");

  const onSubmit = useCallback(() => {
    view.submit(value);
  }, [view, value]);

  return (
    <CustomFieldEdit onSubmit={onSubmit} hideActionButtons>
      <Textfield
        defaultValue="press enter or click outside to submit the value"
        onChange={(e) => {
          setValue(e.target.value);
        }}
      />
    </CustomFieldEdit>
  );
};
```
```
