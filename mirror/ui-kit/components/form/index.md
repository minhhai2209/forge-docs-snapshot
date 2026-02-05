# Form

To add the `Form` component to your app:

```
1
import { Form } from '@forge/react';
```

## Description

A form allows users to input information.

To use the `Form` component, make sure to also import and use the [useForm](/platform/forge/ui-kit/hooks/use-form/) hook which helps in managing `Form` state.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `onSubmit` | `() => (Promise<void | boolean> | void)` | No | Event handler called when the form is submitted. Fields must be free of validation errors.  All modules except for `jiraServiceManagement:assetsImportType` must use `() => Promise<void>|void`.  For the `jiraServiceManagement:assetsImportType` module, the onSubmit event handler returns a boolean value indicating if the form is valid (`true`) or invalid (`false`). If you use `() => Promise<void>|void` for this module, it will default to `true`. |

Use a form header to describe the contents of the form. This is the title and description of the form. If your form contains required fields, the form header is also where you should include a legend for sighted users to know that \* indicates a required field.

```
```
1
2
```



```
import { FormHeader } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `ForgeElement` | No | Child content to render in the form below the title and description. |
| `description` | `string` | No | Description or subtitle of the form. |
| `title` | `string` | No | Title of the form. This is a header. |

Use a form footer to set the content at the end of the form. This is used for a button that submits the form.

This is positioned after the last field in the form.

```
```
1
2
```



```
import { FormFooter } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `align` | `"start" | "end"` | No | Sets the alignment of the footer contents. This is often a button. Defaults to `end`. |
| `children` | `Forge Element` | No | Content to render in the footer of the form. |

### Form section

Use a form section to group related information together, so that longer forms are easier to understand. There can be multiple form sections in one form.

```
```
1
2
```



```
import { FormSection } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `Forge Element` | No | Content or components to render after the description. |
| `description` | `string` | No | Description of the contents of the section. |
| `title` | `string` | No | Title of the form section. |

### Helper message

A helper message tells the user what kind of input the field takes. For example, a helper message could be "Password should be more than 4 characters".

```
```
1
2
```



```
import { HelperMessage } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `string` | No | The content of the message. |

### Error message

An error message is used to tell a user that the field input is invalid. For example, an error message could be "Invalid username, needs to be more than 4 characters".

```
```
1
2
```



```
import { ErrorMessage } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `string | ForgeElement` | No | The content of the error message. |

### Label

A label represents a caption for an item in a user interface.

```
```
1
2
```



```
import { Label } from '@forge/react';
```
```

| Name | Type | Required | Available in macro config | Description |
| --- | --- | --- | --- | --- |
| `children` | `string` | No | Yes | Content of the label. |
| `id` | `string` | No | No | The unique identifier for the label. |
| `labelFor` | `string` | Yes | No | The unique identifier to match the label to the field component `id`. |

### Required asterisk

Use a required asterisk to specify that a form field must not be empty.

```
```
1
2
```



```
import { RequiredAsterisk } from '@forge/react';
```
```

### Validation message

A valid message is used to tell a user that the field input is valid. For example, a helper message could be "Nice one, this username is available".

```
```
1
2
```



```
import { ValidMessage } from '@forge/react';
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `string` | No | The content of the message. |

## Examples

### Default

A form is a group of related fields. You can customize the fields with components such as text field, range field, and checkbox field. You can also pass in default values. Submitting the form calls a callback function. To manage state, validation and submissions, use the component together with the provided [useForm](/platform/forge/ui-kit/hooks/use-form/) hook.

![Example image of a form](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-default.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Form,
  FormHeader,
  FormSection,
  FormFooter,
  HelperMessage,
  Label,
  RequiredAsterisk,
  Textfield,
  Button,
  useForm
} from "@forge/react";

export const FormDefaultExample = () => {
  const { handleSubmit, register, getFieldId } = useForm();

  const login = (data) => {
    // handle data inputs
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(login)}>
      <FormHeader title="Login">
        Required fields are marked with an asterisk <RequiredAsterisk />
      </FormHeader>
      <FormSection>
        <Label labelFor={getFieldId("username")}>
          Username
          <RequiredAsterisk />
        </Label>
        <Textfield {...register("username", { required: true })} />
        <HelperMessage>
          You can use your username, email or phone number.
        </HelperMessage>

        <Label labelFor={getFieldId("password")}>
          Password
          <RequiredAsterisk />
        </Label>
        <Textfield {...register("password", { required: true })} />
      </FormSection>
      <FormFooter>
        <Button appearance="primary" type="submit">
          Submit
        </Button>
      </FormFooter>
    </Form>
  );
}
```
```

### Layout

Use a form header to describe the contents of the form. This is the title and description of the form. If your form contains required fields, the form header is also where you should include a legend for sighted users to know that \* indicates a required field.

#### Form section

Use a form section to group related information together, so that longer forms are easier to understand. There can be multiple form sections in one form.

Use a form footer to set the content at the end of the form. This is used for a button that submits the form. Content should be left-aligned in single-page forms, flags, cards, and section messages with the primary button on the left. See the button positioning for more details.

This is positioned after the last field in the form. It can also be fixed to the bottom of viewport for longer forms.

![Example image of form layout components](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-layout.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Form,
  FormHeader,
  FormSection,
  FormFooter,
  Stack,
  Box,
  Label,
  RequiredAsterisk,
  Textfield,
  Checkbox,
  Select,
  RadioGroup,
  Button,
  useForm
} from "@forge/react";

export const FormLayoutExample = () => {
  const { handleSubmit, register, getFieldId } = useForm();

  const handleCancel = () => {
    // handle cancel button
  };

  const createRepository = (data) => {
    // handle data inputs
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(createRepository)}>
      <FormHeader title="Create a new repository">
        Required fields are marked with an asterisk <RequiredAsterisk />
      </FormHeader>
      <FormSection>
        <Stack space="space.100">
          <Box>
            <Label labelFor={getFieldId("project")}>
              Choose a project
              <RequiredAsterisk />
            </Label>
            <Select
              {...register("project", { required: true })}
              options={[
                { label: "Project A", value: "A" },
                { label: "Project B", value: "B" },
              ]}
            />
          </Box>
          <Box>
            <Label labelFor={getFieldId("repository")}>Repository name</Label>
            <Textfield {...register("repository")} />
          </Box>

          <Box>
            <Label labelFor={getFieldId("access-level")}>Access level</Label>
            <Checkbox
              {...register("access-level")}
              label="This is a private repository"
            />
          </Box>

          <Box>
            <Label labelFor={getFieldId("color")}>Pick a color</Label>
            <RadioGroup
              {...register("color")}
              options={[
                { name: "color", value: "red", label: "Red" },
                { name: "color", value: "blue", label: "Blue" },
                { name: "color", value: "green", label: "Green" },
              ]}
            />
          </Box>
        </Stack>
      </FormSection>
      <FormFooter>
        <Button onClick={handleCancel} appearance="subtle">Cancel</Button>
        <Button appearance="primary" type="submit">
          Create
        </Button>
      </FormFooter>
    </Form>
  );
}
```
```

### Field label and helper message

Always use a label component for each field and associate the label to the field properly. Use the `HelperMessage` component for any optional field related message.

#### Required field label

For required fields, always add the `RequiredAsterisk` component next to the label.

![Example image of form label and helper message](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-label.png?_v=1.5800.1824)

```
```
1
2
```



```
const LabelExample = () => {
  return (
    <>
      <Label labelFor="field">Field label<RequiredAsterisk /></Label>
      <Textfield id="field" placeholder="Placeholder" />
      <HelperMessage>Helper message</HelperMessage>
    <>
  )
}
```
```

### Validation

#### Error and valid message

Use `ErrorMessage` and `ValidMessage` components to indicate when a form submission fails or requires more information. Keep helper text as short as possible. For complex information, provide a link to more information in a new browser tab.

When validating text fields in real-time, messaging can be updated to provide the user feedback on whether a criteria has been met. These error and warning messages disappear when the criteria is met.

#### Field-level validation

Validate a field’s value using the validation properties supplied by the [register](/platform/forge/ui-kit/hooks/use-form/#register) from `useForm` function.

![Example image of form with validation messages](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-validation-messages.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Form,
  FormHeader,
  FormSection,
  FormFooter,
  Label,
  RequiredAsterisk,
  ValidMessage,
  Textfield,
  Button,
  useForm,
  ErrorMessage,
  HelperMessage,
  LinkButton,
  Stack,
  Box,
} from "@forge/react";

export const FieldValidationExample = () => {
  const { handleSubmit, register, getFieldId, formState } = useForm();

  const { errors, touchedFields } = formState;

  const login = (data: any) => {
    // handle data inputs
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(login)}>
      <FormHeader title="Login">
        Required fields are marked with an asterisk <RequiredAsterisk />
      </FormHeader>
      <FormSection>
        <Stack space="space.100">
          <Box>
            <Label labelFor={getFieldId("username")}>
              Username
              <RequiredAsterisk />
            </Label>
            <Textfield
              {...register("username", {
                required: true,
                pattern: /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/,
              })}
            />
            {errors["username"] && (
              <ErrorMessage>Please enter a valid email</ErrorMessage>
            )}
            {!touchedFields["username"] && !errors["username"] && (
              <HelperMessage>
                You can use your username, email or phone number
              </HelperMessage>
            )}
            {touchedFields["username"] && !errors["username"] && (
              <ValidMessage>Nice, this is a valid email</ValidMessage>
            )}
          </Box>

          <Box>
            <Label labelFor={getFieldId("password")}>
              Password
              <RequiredAsterisk />
            </Label>
            <Textfield
              type="password"
              {...register("password", { required: true })}
            />
            {errors["password"] && (
              <ErrorMessage>Password required</ErrorMessage>
            )}
          </Box>
        </Stack>
      </FormSection>
      <FormFooter>
        <LinkButton appearance="subtle" href="/">
          Create an account
        </LinkButton>
        <Button appearance="primary" type="submit">
          Login
        </Button>
      </FormFooter>
    </Form>
  );
};
```
```

#### Submission validation

On submission, the current state gets passed onto the `onSubmit` handler. This state can be validated in the event handler and render an appropriate error message if the validation fails.

The `onSubmit` handler can return synchronously or return a promise that resolves to the result. Note that the promise should resolve with the error, rather than reject with the error.

![Example image of form with submission validation](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-submission-validation.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Form,
  FormHeader,
  FormSection,
  FormFooter,
  Label,
  RequiredAsterisk,
  Textfield,
  Button,
  useForm,
  ErrorMessage,
  HelperMessage,
  ValidMessage,
  LinkButton,
  Stack,
  Box,
  SectionMessage,
  LoadingButton
} from "@forge/react";

export const SubmissionValidationExample = () => {
  const { handleSubmit, register, getFieldId, formState } = useForm();
  const [isLoginError, setIsLoginError] = React.useState(false);

  const { errors, isSubmitting, touchedFields } = formState;

  const login = async (data) => {
    setIsLoginError(false);
    sleep(2000);
    // isSubmitting from useForm will be set to true if this as this is an async function
    // validate data here and if there's an error, set isLoginError to true
    setIsLoginError(true);
  };

  return (
    <Form onSubmit={handleSubmit(login)}>
      <FormHeader title="Login">
        Required fields are marked with an asterisk <RequiredAsterisk />
      </FormHeader>
      <FormSection>
        {isLoginError && (
          <SectionMessage appearance="error">
            Incorrect username or password. Try again.
          </SectionMessage>
        )}
        <Stack space="space.100">
          <Box>
            <Label labelFor={getFieldId("username")}>
              Username
              <RequiredAsterisk />
            </Label>
            <Textfield
              {...register("username", {
                required: true,
                pattern: /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/,
              })}
            />
            {errors["username"] && (
              <ErrorMessage>Please enter a valid email</ErrorMessage>
            )}
            {!touchedFields["username"] && !errors["username"] && (
              <HelperMessage>
                You can use your username, email or phone number
              </HelperMessage>
            )}
            {touchedFields["username"] && !errors["username"] && (
              <ValidMessage>Nice, this is a valid email</ValidMessage>
            )}
          </Box>

          <Box>
            <Label labelFor={getFieldId("password")}>
              Password
              <RequiredAsterisk />
            </Label>
            <Textfield
              type="password"
              {...register("password", { required: true })}
            />
            {errors["password"] && (
              <ErrorMessage>Password required</ErrorMessage>
            )}
          </Box>
        </Stack>
      </FormSection>
      <FormFooter>
        <LinkButton appearance="subtle" href="/">
          Create an account
        </LinkButton>
        <LoadingButton
          isLoading={isSubmitting}
          appearance="primary"
          type="submit"
        >
          Login
        </LoadingButton>
      </FormFooter>
    </Form>
  );
};
```
```

### Form in a modal

When using Form in a modal, use the [Modal layout](/platform/forge/ui-kit/components/modal/#modal-body-props) components instead of the Form layout components.

![Example image of form in a modal](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-modal.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader,
  ModalTitle,
  ModalTransition,
  Form,
  Label,
  Textfield,
  Button,
  Stack,
  Box,
  useForm
} from "@forge/react";

export const FormModalExample = () => {
  const { handleSubmit, register, getFieldId } = useForm();
  const [isOpen, setIsOpen] = React.useState(false);

  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);
  const submit = (data: any) => {
    // handle data inputs
    console.log(data);
  };

  return (
    <>
      <Button onClick={open}>Open Modal</Button>

      <ModalTransition>
        {isOpen && (
          <Modal onClose={close}>
            <Form onSubmit={handleSubmit(submit)}>
              <ModalHeader>
                <ModalTitle>Modal dialog with form</ModalTitle>
              </ModalHeader>
              <ModalBody>
                <Stack space="space.100">
                  <Box>
                    <Label labelFor={getFieldId("name")}>Name</Label>
                    <Textfield {...register("name")} />
                  </Box>
                  <Box>
                    <Label labelFor={getFieldId("email")}>Email</Label>
                    <Textfield {...register("email")} />
                  </Box>
                </Stack>
              </ModalBody>
              <ModalFooter>
                <Button onClick={close} appearance="subtle">
                  Cancel
                </Button>
                <Button appearance="primary" type="submit">
                  Submit
                </Button>
              </ModalFooter>
            </Form>
          </Modal>
        )}
      </ModalTransition>
    </>
  );
};
```
```

### Form with all fields

Example of a form with all possible input components.

![Example image of form with all field components](https://dac-static.atlassian.com/platform/forge/ui-kit/images/form/form-all-fields.png?_v=1.5800.1824)

```
```
1
2
```



```
import {
  Box,
  Button,
  ButtonGroup,
  Checkbox,
  DatePicker,
  Form,
  FormFooter,
  FormHeader,
  FormSection,
  HelperMessage,
  Label,
  RadioGroup,
  Range,
  RequiredAsterisk,
  Select,
  Stack,
  TextArea,
  Textfield,
  Toggle,
  UserPicker,
  useForm
} from "@forge/react";

export const FormAllFieldsExample = () => {
  const { getFieldId, register, handleSubmit } = useForm();

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormHeader title="Form header">
        <Text>
          Required fields are marked with an asterisk. <RequiredAsterisk />
        </Text>
      </FormHeader>

      <FormSection>
        <Stack space="space.200">
          <Box>
            <UserPicker
              {...register("userPicker")}
              label='User Picker'
              placeholder='Select a user'
            />
          </Box>
          <Box>
            <Label labelFor={getFieldId("textfield")}>
              Textfield <RequiredAsterisk />
            </Label>
            <Textfield
              {...register("textfield", {
                required: true,
                maxLength: 5,
              })}
            />
            <HelperMessage>Helper message.</HelperMessage>
          </Box>

          <Box>
            <Label labelFor={getFieldId("textarea")}>Text area</Label>
            <TextArea placeholder="Long form text" {...register("textarea")} />
          </Box>

          <Box>
            <Label labelFor={getFieldId("datepicker")}>Date picker</Label>
            <DatePicker {...register("datepicker")} />
          </Box>

          <Box>
            <Label labelFor={getFieldId("select")}>Select</Label>
            <Select
              options={[
                { label: "Apple", value: "apple" },
                { label: "Banana", value: "banana" },
              ]}
              {...register("select")}
            />
          </Box>

          <Box>
            <Label labelFor={getFieldId("range")}>Range</Label>
            <Range {...register("range")} />
          </Box>

          <Box>
            <Label labelFor={getFieldId("checkbox")}>Checkbox</Label>
            <Checkbox label="Label" {...register("checkbox.A")} />
            <Checkbox label="Label" {...register("checkbox.B")} />
            <Checkbox label="Label" {...register("checkbox.C")} />
          </Box>

          <Box>
            <Label labelFor={getFieldId("radio")}>Radio group</Label>
            <RadioGroup
              options={[
                { name: "radio", value: "A", label: "Label" },
                { name: "radio", value: "B", label: "Label" },
                { name: "radio", value: "C", label: "Label" },
              ]}
              {...register("radio")}
            />
          </Box>

          <Box>
            <Label labelFor="toggle">Toggle label</Label>
            <Toggle {...register("toggle")} />
          </Box>
        </Stack>
      </FormSection>

      <FormFooter>
        <ButtonGroup>
          <Button appearance="subtle">Cancel</Button>
          <Button type="submit" appearance="primary">
            Submit
          </Button>
        </ButtonGroup>
      </FormFooter>
    </Form>
  );
};
```
```
