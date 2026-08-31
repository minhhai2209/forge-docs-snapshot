# Checkbox group

To add the `CheckboxGroup` component to your app:

```
1import { CheckboxGroup } from "@forge/react";
2
```

## Description

A Checkbox group is a list of options where one or more choices can be selected.

## Props

| Name | Type | Required | Available in macro config | Description |
| --- | --- | --- | --- | --- |
| `name` | `string` | Yes | Yes | Sets the name prop on each of the Checkbox elements in the group. |
| `options` | `Array<{ label: string; value: string; isDisabled?: boolean; }>` | Yes | Yes | An array of objects, each object is mapped onto a Checkbox element within the group. |
| `value` | `Array<string>` | No | No | Once set, controls the selected value on the `CheckboxGroup`. |
| `defaultValue` | `Array<string>` | No | Yes | Sets the initial selected value on the `CheckboxGroup`. |
| `isDisabled` | `boolean` | No | No | Sets the disabled state of all Checkbox elements in the group. |
| `isRequired` | `boolean` | Only available for macro configuration, cannot be used for other extension points | Yes | Set if the picker is disabled. |
| `onChange` | `(e: ChangeEvent) => void` | No | No | Function that gets fired after each change event. |

## Examples

### Default

The default form of a Checkbox group.

![Example image of a Checkbox group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/checkbox-group/checkbox-group-default.png?_v=1.5800.2300)

```
```
1
2
3
4
5
6
7
8
9
10
11
```



```
import { CheckboxGroup } from "@forge/react";

const options = [
  { value: "jira", label: "Jira" },
  { value: "confluence", label: "Confluence" },
];

const CheckboxGroupDefaultExample = () => {
  return <CheckboxGroup name="Products" options={options} />;
};
```
```

### CheckboxGroup with Form

For required fields, use the `ErrorMessage` or `ValidMessage` components for displaying a validation message.

![Example image of a required Checkbox group in a Form](https://dac-static.atlassian.com/platform/forge/ui-kit/images/checkbox-group/checkbox-group-with-form.png?_v=1.5800.2300)

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
```



```
import {
  Form,
  useForm,
  FormSection,
  FormFooter,
  Label,
  RequiredAsterisk,
  ErrorMessage,
  CheckboxGroup,
  Button,
} from "@forge/react";

const options = [
  { value: "jira", label: "Jira" },
  { value: "confluence", label: "Confluence" },
];

const CheckboxGroupRequiredExample = () => {
  const { handleSubmit, register, getFieldId, formState } = useForm();
  const login = (data) => {
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(login)}>
      <FormSection>
        <Label labelFor={getFieldId("myCheckbox")}>
          Products
          <RequiredAsterisk />
        </Label>
        <CheckboxGroup
          {...register("myCheckbox", { required: true })}
          name="myCheckbox"
          options={options}
        />
        {formState.errors.myCheckbox && (
          <ErrorMessage>
            One of these options needs to be selected.
          </ErrorMessage>
        )}
      </FormSection>
      <FormFooter align="start">
        <Button appearance="primary" type="submit">
          Submit
        </Button>
      </FormFooter>
    </Form>
  );
};
```
```

### States

#### Disabled

`isDisabled` can be used to disable the entire Checkbox group.

![Example image of a disabled Checkbox group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/checkbox-group/checkbox-group-disabled.png?_v=1.5800.2300)

```
```
1
2
3
4
5
6
7
8
9
10
11
```



```
import { CheckboxGroup } from "@forge/react";

const options = [
  { value: "jira", label: "Jira" },
  { value: "confluence", label: "Confluence" },
];

const CheckboxGroupisDisabledExample = () => {
  return <CheckboxGroup name="Products" options={options} isDisabled />;
};
```
```

### Controlled

#### onChange

In a `controlled` checkbox, the checked state is managed by the React component. Set `value` to select the checkbox(es) and use the`onChange` handler to change the value.

![Example image of a controlled Checkbox group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/checkbox-group/checkbox-group-controlled.png?_v=1.5800.2300)

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
```



```
import { CheckboxGroup } from "@forge/react";

const options = [
  { value: "jira", label: "Jira" },
  { value: "confluence", label: "Confluence" },
];

const CheckboxGroupControlledExample = () => {
  const [value, setValue] = useState(["jira"]);

  return (
    <CheckboxGroup
      name="Products"
      options={options}
      value={value}
      onChange={setValue}
    />
  );
};
```
```
