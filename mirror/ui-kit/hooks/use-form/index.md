# useForm

`useForm` is a React hook that returns several properties to validate and manage the state of form fields in UI Kit. For full examples on how to use this hook with UI Kit components,
see the [Form](/platform/forge/ui-kit/components/form) component.

To import `useForm` into your app:

```
1
import { useForm } from '@forge/react';
```

**Props**

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `defaultValues` | `FieldValues` | No | Default values for the form. |

## defaultValues

The `defaultValues` prop populates the entire form with default values. It is recommended to use `defaultValues` for the entire form.

### Example

```
1
2
3
4
5
6
useForm({
  defaultValues: {
    firstName: '',
    lastName: ''
  }
})
```

### Note

* Avoid providing `undefined` as a default value, as it conflicts with the default state of controlled components.
* `defaultValues` will be included in the submission result by default.

**Return Props**

| Name | Type | Description |
| --- | --- | --- |
| `register` | `(name: string, RegisterOptions?) => RegisterReturnProps` | This method allows you to register an input or select element and apply validation rules to Form. |
| `formState` | `Object` | This object contains information about the entire form state. |
| `getFieldId` | `(fieldName: string) => string` | Gets the id of a form field. |
| `getValues` | `(payload?: string | string[]) => Object` | An optimized helper for reading form values |
| `handleSubmit` | `((data: Object, e?: Event) => Promise<void>, (errors: Object, e?: Event) => void) => Promise<void>` | This function will receive the form data if form validation is successful. |
| `trigger` | `(name?: string | string[]) => Promise<boolean>` | Manually triggers form or input validation. |
| `clearErrors` | `(name?: string | string[]) => void` | This function can manually clear errors in the form. |

## register

This method allows you to register an input or select element and apply validation rules to Form.

By invoking the register function and supplying an input's name, you will receive the following properties:

**Props**

| Name | Type | Description |
| --- | --- | --- |
| `name` | `string` | Name of the input field |
| `RegisterOptions` | `Object` | Additional options that can be passed into the `register` function |

**Return Props**

| Name | Type | Description |
| --- | --- | --- |
| `onChange` | `ChangeHandler` | `onChange` prop to subscribe the input change event. |
| `onBlur` | `ChangeHandler` | `onBlur` prop to subscribe the input blur event. |
| `id` | `string` | Input's id containing randomly generated string to avoid clashes. Use `getFieldId(name)` |
| `isInvalid` | `boolean` | Whether a field is invalid. |
| `isDisabled` | `boolean` | Whether a field is disabled. |

### RegisterOptions

| Name | Type | Description | Example |
| --- | --- | --- | --- |
| `required` | `boolean` | A `boolean` which, if `true`, indicates that the input must have a value before the form can be submitted. You can assign a string to return an error message in the `errors` object. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {     required: true   })} /> ``` ``` |
| `disabled` | `boolean` | Set disabled to `true` will lead input value to be `undefined` and input control to be disabled.  `disabled` prop will also omit built-in validation rules.    For schema validation, you can leverage the `undefined` value returned from input or context object. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {     disabled: true   })} /> ``` ``` |
| `max` | `number` | The maximum value to accept for this input. | ```  ``` 1 2 ```    ``` <Textfield   type="number"   {...register('test', {     max: 3   })} /> ``` ``` |
| `maxLength` | `number` | The maximum length of the value to accept for this input. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {       maxLength: 2   })} /> ``` ``` |
| `min` | `number` | The minimum value to accept for this input. | ```  ``` 1 2 ```    ``` <Textfield   type="number"   {...register("test", {     min: 3   })} /> ``` ``` |
| `minLength` | `number` | The minimum length of the value to accept for this input. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {     minLength: 1   })} /> ``` ``` |
| `pattern` | `RegExp` | The regex pattern for the input.  **Note**: A RegExp object with the `/g` flag keeps track of the lastIndex where a match occurred. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {     pattern: /[A-Za-z]{3}/   })} /> ``` ``` |
| `validate` | `Function | Object` | You can pass a callback function as the argument to validate, or you can pass an object of callback functions to validate all of them. This function will be executed on its own without depending on other validation rules included in the `required` attribute.  Note: for `object` or `array` input data, it's recommended to use the `validate` function for validation as the other rules mostly apply to `string`, `string[]`, `number` and `boolean` data types. | ```  ``` 1 2 ```    ``` <Textfield   {...register("test", {     validate: (value, formValue) => {       return value === '1'     }   })} /> ``` ```  ```  ``` 1 2 ```    ``` // object of callback functions <Textfield   {...register("test1", {     validate: {       positive: v => parseInt(v) > 0,       lessThanTen: v => parseInt(v) < 10,       checkUrl: async () => await fetch(),     }   })} /> ``` ``` |

### Example

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Button, Textfield, Label } from "@forge/react";

export default function App() {
  const { register, handleSubmit, getFieldId, Button } = useForm({
    defaultValues: {
      firstName: '',
      lastName: '',
    }
  });

  return (
    <Form onSubmit={handleSubmit(console.log)}>
      <Label labelFor={getFieldId("firstName")}>First Name</Label>
      <Textfield {...register("firstName", { required: true })}/>

      <Label labelFor={getFieldId("lastName")}>Last Name</Label>
      <Textfield {...register("lastName", { minLength: 2 })}/>

      <Button type="submit">Submit</Button>
    </Form>
  );
}
```
```

### Note

* `name` is **required** and **unique**. Input name supports dot syntax to allow for nested form fields.

```
```
1
2
```



```
register('user.firstname'); // returns {user: {firstname: ''}}
```
```

* `name` can neither start with a number nor use number as key name. Please avoid special characters as well.
* `disabled` input will result in an `undefined` form value. If you want to prevent users from updating the input, use `isReadOnly`.
* To produce an array of fields, input names should be followed by a dot and number. For example: `test.0.data`
* Changing the name on each render will result in new inputs being registered. It's recommended to keep static names for each registered input.
* spreading `register` sets the `onChange`, `onBlur`, `id`, `isInvalid`, and `isDisabled` props for a component. If you would like to add your own actions to be triggered on `onChange` or `onBlur`, these props should be passed separately.

```
```
1
2
```



```
const { onChange: formOnChange, ...textfieldProps } = register('endpoint');

<Textfield {...textfieldProps}  onChange={(e) => {
    // `onChange` from `register` to update form state
    formOnChange(e);
    // handle other actions here
    // * trigger action *
 }} 
/>
```
```

## formState

This object contains information about the entire form state. It helps you to keep on track with the user's interaction with your form application.

**Return Props**

| Name | Type | Description |
| --- | --- | --- |
| `dirtyFields` | `Object` | An object with the user-modified fields. Make sure to provide all inputs' defaultValues via useForm, so the library can compare against the `defaultValues`.  **Important**: Make sure to provide `defaultValues` at the useForm, so hook form can have a single source of truth to compare each field's dirtiness. |
| `touchedFields` | `Object` | An object containing all the inputs the user has interacted with. |
| `errors` | `Object` | An object with field errors. |
| `isSubmitted` | `boolean` | Set to `true` after the form is submitted. |
| `isSubmitting` | `boolean` | `true` if the form is currently being submitted. `false` otherwise. |
| `isSubmitSuccessful` | `boolean` | Indicate the form was successfully submitted without any runtime error. |
| `isValid` | `boolean` | Set to `true` if the form doesn't have any errors. |
| `submitCount` | `number` | Number of times the form was submitted. |

### Note

* `formState` is wrapped with a [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) to improve render performance and skip extra logic if specific state is not subscribed to. Therefore make sure to invoke or read it before a render in order to enable the state update.

```
```
1
2
```



```
const { isValid } = formState;
return <Button disabled={!isValid} type="submit">Submit</Button>;
```
```

## getFieldId

Retrieves the `id` of a registered form field. This should be used to retrieve the correct `id` to pass into the `Label` component.

**Props**

| Type | Description | Example |
| --- | --- | --- |
| `string` | returns the registered form field id. | `getFieldId("firstName")` |

### Example

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Button, Textfield, Label } from "@forge/react";

export default function App() {
  const {
    getFieldId,
    register,
    handleSubmit,
    // Read the formState before render to subscribe the form state through the Proxy
    formState: { errors, isSubmitting, submitCount },
  } = useForm();

  const onSubmit = (data) => console.log(data);

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Label labelFor={getFieldId("firstName")}>First Name</Label>
      <Textfield {...register("firstName")} />
      <Button type="submit">Submit</Button>
    </Form>
  );
}
```
```

### Note

* UI Kit uses a randomly generated `id` to prevent conflicts with other components on the page. Use the `getFieldId` to retrieve the correct `id` of a registered form field.

## getValues

An optimized helper for reading form values, `getValues` will not trigger re-renders or subscribe to input changes.

**Props**

| Type | Description | Example |
| --- | --- | --- |
| `undefined` | Returns the entire form values. | `getValues()` |
| `string` | Gets the value at path of the form values. | `getValues("person.firstName")` |
| `array` | Returns an array of the value at path of the form values. | `getValues(["person.firstName", "person.lastName"])` |

### Example

The example below shows what to expect when you invoke `getValues` method.

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Label, Textfield, Button } from "@forge/react"

export default function App() {
  const { register, getValues, getFieldId } = useForm()

  return (
    <Form>
      <Label labelFor={getFieldId("firstname")}>First name</Label>
      <Textfield {...register("firstname")} />

      <Label labelFor={getFieldId("lastname")}>Last name</Label>
      <Textfield {...register("lastname")} />

      <Button
        onClick={() => {
          const values = getValues(); // gets all form values { firstname: '', lastname: ''}
          const singleValue = getValues("firstname");  // gets single form value { firstname: ''}
          const multipleValues = getValues(["firstname", "lastname"]); // gets multiple form values { firstname: '', lastname: ''}

          console.log({ values, singleValue, multipleValues });
        }}
      >
        Get Values
      </Button>
    </Form>
  )
}
```
```

### Note

* Disabled inputs will be returned as `undefined`. If you want to prevent users from updating the input and still retain the field value, you can use `readOnly`.
* It will return `defaultValues` from useForm before the initial render.

## handleSubmit

This function will receive the form data if form validation is successful.

**Props**

| Name | Type | Description |
| --- | --- | --- |
| `onSubmit` | `(data: Object) => Promise<void>` | A successful callback. |
| `onError` | `(errors: Object) => Promise<void>` | An error callback. |

### Example

#### Sync

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Label, Textfield, Button } from "@forge/react"

export default function App() {
  const { register, handleSubmit, getFieldId } = useForm()
  const onSubmit = (data) => console.log(data)
  const onError = (errors) => console.log(errors)

  return (
    <Form onSubmit={handleSubmit(onSubmit, onError)}>
      <Label labelFor={getFieldId('firstName')}>First Name</Label>
      <Textfield {...register("firstName")} />

      <Label labelFor={getFieldId('lastName')}>First Name</Label>
      <Textfield {...register("lastName")} />

      <Button type="submit">Submit</Button>
    </Form>
  )
}
```
```

#### Async

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Label, Textfield, Button } from "@forge/react"

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

function App() {
  const { register, handleSubmit, formState, formState, getFieldId } = useForm();

  const { errors, isSubmitting } = formState;

  const onSubmit = async data => {
    await sleep(2000);
    if (data.username === "bill") {
      console.log(JSON.stringify(data));
    } else {
      console.log("There is an error");
    }
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Label labelFor={getFieldId('username')}>First Name</Label>
      <Textfield {...register("username")} placeholder="Bill"/>
      <LoadingButton isLoading={isSubmitting} type="submit">Submit</LoadingButton>
    </Form>
  );
}
```
```

### Note

* You can easily submit form asynchronously with `handleSubmit`.

```
```
1
2
```



```
handleSubmit(onSubmit)()

// You can pass an async function for asynchronous validation.
handleSubmit(async (data) => await fetchAPI(data))
```
```

* `handleSubmit` function will not ignore errors that occurred inside your `onSubmit` callback, so we recommend you to try and catch inside async request and handle those errors gracefully for your customers.

```
```
1
2
```



```
const onSubmit = async () => {
  // async request which may result error
  try {
    // await fetch()
  } catch (e) {
    // handle your error
  }
};

<Form onSubmit={handleSubmit(onSubmit)} />
```
```

## trigger

Manually triggers form or input validation. This method is also useful when you have dependent validation (input validation depends on another input's value).

**Props**

| Name | Type | Description | Example |
| --- | --- | --- | --- |
| `name` | `undefined` | Triggers validation on all fields. | `trigger()` |
|  | `string` | Triggers validation on a specific field value by **name**. | `trigger("yourDetails.firstName")` |
|  | `string[]` | Triggers validation on multiple fields by **name**. | `trigger(["yourDetails.lastName"])` |

### Example

```
```
1
2
```



```
import ForgeReconciler, { useForm, Form, Label, Textfield, Button } from "@forge/react"

export default function App() {
  const {
    register,
    trigger,
    formState: { errors },
    getFieldId,
  } = useForm()

  return (
    <Form>
      <Label labelFor={getFieldId("firstName")}>First Name</Label>
      <Textfield {...register("firstName", { required: true })} />

      <Label labelFor={getFieldId("lastName")}>Last Name</Label>
      <Textfield {...register("lastName", { required: true })} />

      <Button
        type="button"
        onClick={async () => {
          const result = await trigger("lastName")
        }}
      >
        Trigger
      </Button>

      <Button
        type="button"
        onClick={async () => {
          const result = await trigger(["firstName", "lastName"])
        }}
      >
        Trigger Multiple
      </Button>

      <Button
        type="button"
        onClick={() => {
          trigger()
        }}
      >
        Trigger All
      </Button>
    </Form>
  )
}
```
```

### Note

* Isolate render optimisation only applicable for targeting a single field name with `string` as payload, when supplied with `array` and `undefined` to trigger will re-render the entire formState.

## clearErrors

This function can manually clear errors in the form.

**Props**

| Type | Description | Example |
| --- | --- | --- |
| `undefined` | Remove all errors. | `clearErrors()` |
| `string` | Remove single error. | `clearErrors("firstName")` |
| `string[]` | Remove multiple errors. | `clearErrors(["firstName", "lastName"])` |

### Note

* This will not affect the validation rules attached to each inputs.
* This method doesn't affect validation rules or isValid formState.

## Known Limitations

* For performance reasons, `useForm` capabilities are limited to input state handling, validation, and submission.
  Capabilities such as dynamically setting values, clearing values, and watching form state are currently not supported. For these cases, apps will either need to handle their own state management or rely on third-party capabilities through Custom UI or the `Frame` component.
