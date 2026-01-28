# User picker

To add the `UserPicker` component to your app:

```
1
import { UserPicker } from "@forge/react";
```

## Description

A dropdown field that allows users to search and select users from a list.

## Props

| Name | Type | Required | Available in macro config | Description |
| --- | --- | --- | --- | --- |
| `isMulti` | `boolean` | No | Yes | Whether the user can select multiple users from the list. Defaults to `false`. |
| `isRequired` | `boolean` | No | Yes | Indicates to the user whether or not a value is required in this field to submit the form. If a field is required, an asterisk appears at the end of that field’s label. |
| `label` | `string` | Yes | No | The label text to display. |
| `name` | `string` | Yes | Yes | The key to which the input value is assigned in the returned form object. If `isMulti` is `true`, the submitted value is an array of strings; otherwise, it is a string. |
| `defaultValue` | `string` | No | Yes | The initial user to display. The value should be an Atlassian account ID. |
| `description` | `string` | No | Yes | The text description of the user picker field. |
| `placeholder` | `string` | No | Yes | The placeholder helper text. |
| `onChange` | ```  ``` 1 2 ```    ``` (user: {   id: string;   type: string;   avatarUrl: string;   name: string;   email: string; }) => void ``` ``` | No | No | An event handler that can be asynchronous. Allows you to read values from the component without having to submit as part of a `Form`. |

## Examples

### Default

A field for selecting a user.

![Example image of rendered User picker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/user-picker/user-picker-single.png?_v=1.5800.1801)

```
```
1
2
```



```
const App = () => {
  return (
    <UserPicker
      label="Assignee"
      placeholder="Select a user"
      name="user"
      description="The selected user will be assigned to this task"
      onChange={(user) => console.log(user)}
    />
  );
};
```
```

The returned object from `onChange` contains the Atlassian account ID and various other information of the selected user.

```
```
1
2
```



```
{
    "id": "1a2345bc6789012d3e45f67",
    "type": "user",
    "avatarUrl": "...",
}
```
```

### Multi

Multiple users can be selected when the `isMulti` prop is applied.

![Example image of rendered User picker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/user-picker/user-picker-multi.png?_v=1.5800.1801)

```
```
1
2
```



```
const App = () => {
  return (
    <UserPicker
      isMulti
      label="Project owner(s)"
      placeholder="Select people or teams"
      name="project-owners"
      description="The selected people or teams will be the project owner"
      onChange={(users) => console.log(users)}
    />
  );
};
```
```
