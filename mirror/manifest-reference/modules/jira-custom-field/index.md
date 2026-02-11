# Jira custom field

The `jira:customField` module creates a new custom field in Jira,
which makes it easier for users to add information to issues, specific to their teams' needs.

This module can be used in Jira and Jira Service Management.

## Manifest example

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
51
52
53
54
55
56
57
58
59
60
61
62
63
modules:
  jira:customField:
    - key: story-points-field
      name: Story Points
      description: Track story points for agile development
      type: number
      view:
        resource: story-points-view
      edit:
        resource: story-points-edit
    - key: contact-info-field
      name: Contact Information
      description: Structured contact information with name, email, and phone
      type: object
      schema:
        type: object
        properties:
          fullName:
            type: string
            maxLength: 100
          email:
            type: string
            format: email
          phone:
            type: string
            pattern: "^[+]?[0-9\\s\\-\\(\\)]{10,20}$"
          department:
            type: string
            enum: ["Engineering", "Sales", "Marketing", "Support", "HR"]
        required: ["fullName", "email"]
        additionalProperties: false
      view:
        resource: contact-info-view
        render: native
        formatter:
          expression: "value != null ? `${value.fullName} (${value.email})` + (value.phone ? ` - ${value.phone}` : '') : 'No contact information'"
          export: true
        experience:
          - "issue-view"
          - "portal-view"
      edit:
        resource: contact-info-edit
        render: native
        experience:
          - "issue-view"
          - "issue-create"
          - "issue-transition"
          - "portal-request"
        validation:
          expression: "value == null || (value.fullName?.length > 0 && value.email?.length > 0)"
          errorMessage: "Full name and email are required"
      searchSuggestions:
        expression: '["Engineering", "Sales", "Marketing", "Support", "HR"]'

resources:
  - key: story-points-view
    path: src/frontend/storyPointsView.jsx
  - key: story-points-edit
    path: src/frontend/storyPointsEdit.jsx
  - key: contact-info-view
    path: src/frontend/contactInfoView.jsx
  - key: contact-info-edit
    path: src/frontend/contactInfoEdit.jsx
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.   This key becomes a part of the custom field key as described in the [Field lifecycle section](#field-lifecycle).  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the field.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | The description of the field.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `type` | `string` | Yes | The type of the value stored by the field. Available types are:  * `string` * `number` * `user` * `group` * `datetime` * `date` * `object`    **Important:** When using `object` type, you **must** include `view.formatter.expression` to enable JQL search and proper field display. Without this formatter, the field will not be searchable in JQL queries. |
| `collection` | `none|list` (default: `none`) |  | The kind of collection that the field values should be stored in. See [collection types](#collection-types) for more details. |
| `readOnly` | `boolean` |  | Whether or not the field is read-only. Read-only fields can't be edited by users. Defaults to `false`. |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `function` | `string` | Required if using [triggers](/platform/forge/manifest-reference/modules/trigger/). | A reference to the function module that defines the module. |
| `view.render` | `'native'` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `view.resource` | `string` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | A reference to the static `resources` entry that your view entry point wants to display. See [Resources](/platform/forge/manifest-reference/resources) for more details. Available only for [UI Kit](/platform/forge/ui-kit/components/). |
| `view.experience` | `string[]` | yes | Indicates on which view experiences this rendering should be used. Currently supported view experiences:  * `'issue-view'` * `'portal-view'` |
| `view.formatter.expression` | `string` | Required for the `object` type; otherwise, optional | A Jira expression that renders the value as a string. See [formatter](#formatter) for more details. |
| `view.formatter.export` | `boolean` |  | Whether to use the formatter for values exported to CSV. See [Using formatters in CSV export](#using-formatters-in-csv-export) for more details. |
| `view.value.function` | `string` |  | A function that computes the value of the field. See [value function](#value-function) for more details. |
| `edit.function` | `string` |  | A reference to the `function` module that provides the field editing experience. |
| `edit.resource` | `string` |  | A reference to the static `resources` entry that your edit entry point will display. See [Resources](/platform/forge/manifest-reference/resources) for more details. To submit the view, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit). |
| `edit.render` | `'native'` |  | Indicates if your edit entry point should display as UI Kit. |
| `edit.experience` | `string[]` | yes | Indicates on which view experiences this rendering should be used. Currently supported edit experiences:  * `'issue-view'` * `'issue-create'` * `'issue-transition'` * `'portal-request'` |
| `edit.isInline` | `boolean` |  | Indicates if your edit entry point should display inline on the issue view. |
| `edit.validation.expression` | `string` |  | A Jira expression that validates the field value. See [validation](#validation) for more details. |
| `edit.validation.errorMessage` | `string` or `i18n object` |  | The error message to show when the validation expression returns `false`.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `edit.parser.expression` | `string` |  | A Jira expression that parses strings into valid values of this field. See [parser](#parser) for more details. |
| `schema` | `object` | Allowed only for the `object` type | A [JSON schema](https://json-schema.org/) that desribes values stored in the field. |
| `displayConditions` | `object` |  | The object that defines whether or not the field is displayed on the issue view or global issue create (GIC) (other views or REST APIs are not affected). See [display conditions](#display-conditions). |
| `searchSuggestions.expression` | `string` | Requires either `function` or `expression`. Only one of the two properties must be present. | A [Jira expression](/cloud/jira/platform/jira-expressions/) that provides value suggestions in advanced search. See [search suggestions](#search-suggestions) for more details. |
| `searchSuggestions.function` | `string` | Requires either `function` or `expression`. Only one of the two properties must be present. | A reference to the `function` module that provides value suggestions in advanced search. See [search suggestions](#search-suggestions) for more details. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed`, `customer`, and `anonymous`. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |

## Rendering

### View mode

Forge apps can provide rendering of the field with [UI Kit](/platform/forge/ui-kit/).

##### UI Kit

```
```
1
2
```



```
modules:
    jira:customField:
      view:
        resource: key
        render: native
```
```

You can obtain the current value of the field from the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook, like this:

```
```
1
2
```



```
const context = useProductContext();
const fieldValue = context?.extension.fieldValue;
```
```

### Edit mode

Forge apps can optionally provide their own editing experience of the field
with [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/) by specifying the `edit` property.

##### UI Kit

With UI Kit, use the [CustomFieldEdit](/platform/forge/ui-kit/jira-components/custom-field-edit) component to render the edit view.

```
```
1
2
```



```
modules:
    jira:customField:
      edit:
        resource: key
        render: native
```
```

You can obtain the current value of the field from the [getContext API](/platform/forge/custom-ui-bridge/view/#getcontext), like this:

```
```
1
2
```



```
const { fieldValue } = await view.getContext();
```
```

To update the field value, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit), like this:

```
```
1
2
```



```
await view.submit(fieldValue);
```
```

Default editing, appropriate to the field's data type, is used if the edit resource is not provided.

##### Custom UI

```
```
1
2
```



```
modules:
    jira:customField:
      edit:
        resource: key
```
```

You can obtain the current value of the field from the [getContext API](/platform/forge/custom-ui-bridge/view/#getcontext), like this:

```
```
1
2
```



```
const { fieldValue } = await view.getContext();
```
```

To update the field value, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit), like this:

```
```
1
2
```



```
await view.submit(fieldValue);
```
```

Default editing, appropriate to the field's data type, is used if the edit resource is not provided.

### Experience

The `experience` property determines where a specific extension should be rendered within Jira views. Jira will default to rendering the built-in field if a view or edit entry point lacks a defined experience.
This means that extensions must now opt-in for new views. This change ensures that fields which are irrelevant to the context or may not function correctly are not rendered.

```
```
1
2
```



```
jira:customFieldType:
  - key: cf-with-experience
    name: Example custom field
    description: This field will render on every view
    type: number
    edit:
      resource: key
      render: native
      isInline: true
      experience:
        - "issue-view"
        - "issue-create"
        - "issue-transition"
        - "portal-request"
    view:
      resource: key
      render: native
      isInline: true
      experience:
        - "issue-view"
        - "portal-view"
```
```

### Issue view

By default, when you define an editing function for a Jira custom field created by a Forge app, switching to the field’s edit mode opens a modal. However, when using [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/), you can enable inline editing by including the `isInline` property in the app’s manifest.

```
```
1
2
```



```
modules:
  jira:customField:
    edit:
      resource: key
      render: native
      isInline: true
```
```

The `isInline` property is added temporarily for a [deprecation period of modal experience](https://developer.atlassian.com/changelog/#CHANGE-2536) and will be removed on **August 1, 2025**.
After this date all fields on issue view will be rendered inline by default. If you still want to use modal experience in your fields,
use the [Modal](/platform/forge/ui-kit/components/modal/) component for UI Kit fields and the [Modal bridge API](/platform/forge/apis-reference/ui-api-bridge/modal/) for Custom UI fields.

For UI Kit, use the [CustomFieldEdit](/platform/forge/ui-kit/jira-components/custom-field-edit) component to render the edit view.
In issue view, the `onSubmit` function in the CustomFieldEdit component will be called on blur events, "Enter" key press, or on clicking confirmation action button, so you can place
the submit logic there. Otherwise, you can create your own logic to use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit) outside the `onSubmit` function.

#### Inline edit migration guide

Here are two guides for migrating apps to use `isInline` property:

How to edit custom fields inline (suggested approach for minimalistic UI)

##### Original manifest and edit files

The `manifest.yml` file with no `isInline` property:

```
```
1
2
```



```
modules:
  jira:customField:
    - key: my-cf
      ...
      edit:
        resource: edit
        render: native
        experience:
          - "issue-create"
          - "issue-transition"
          - "issue-view"
          - "portal-request"
      ...
```
```

The `edit.jsx` file with the deprecated way of app rendering:

```
```
1
2
```



```
import React, { useState, useEffect } from "react";
import ForgeReconciler, {
  Form,
  Label,
  Textfield,
  useForm,
  FormSection,
  FormFooter,
  ButtonGroup,
  LoadingButton,
  Button,
} from "@forge/react";
import { view } from "@forge/bridge";

const Edit = () => {
  const [renderContext, setRenderContext] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { handleSubmit, register, getFieldId, getValues } = useForm();

  useEffect(() => {
    view
      .getContext()
      .then((context) => setRenderContext(context.extension.renderContext));
  }, []);

  const onSubmit = async () => {
    try {
      setIsLoading(true);
      const { fieldName } = getValues();
      await view.submit(fieldName || "world");
    } catch (e) {
      setIsLoading(false);
      console.error(e);
    }
  };

  return renderContext === "issue-view" ? (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormSection>
        <Label labelFor={getFieldId("fieldName")}>Custom field value</Label>
        <Textfield {...register("fieldName")} />
      </FormSection>
      <FormFooter>
        <ButtonGroup>
          <Button appearance="subtle" onClick={view.close}>
            Close
          </Button>
          <LoadingButton
            appearance="primary"
            type="submit"
            isLoading={isLoading}
          >
            Submit
          </LoadingButton>
        </ButtonGroup>
      </FormFooter>
    </Form>
  ) : (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Label labelFor={getFieldId("fieldName")}>Custom field value</Label>
      <Textfield {...register("fieldName")} />
    </Form>
  );
};
```
```

Outcome:
![Original experience](https://dac-static.atlassian.com/platform/forge/images/migration-guide-old-modal.png?_v=1.5800.1840)

##### Updated files

To update the app, add the `isInline` property to app's manifest file and replace the [Form](/platform/forge/ui-kit/components/form) component with the [CustomFieldEdit](/platform/forge/ui-kit/jira-components/custom-field-edit) component to handle the correct inline rendering and the field's value submission.

The `manifest.yml` file with `isInline` property:

```
```
1
2
```



```
modules:
  jira:customField:
    - key: my-cf
      ...
      edit:
        resource: edit
        render: native
        isInline: true
        experience:
          - "issue-create"
          - "issue-transition"
          - "issue-view"
          - "portal-request"
      ...
```
```

The `edit.jsx` file - version with inline edit experience:

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import ForgeReconciler, { Label, Textfield } from "@forge/react";
import { CustomFieldEdit } from "@forge/react/jira";
import { view } from "@forge/bridge";

const Edit = () => {
  const [value, setValue] = useState("");

  const onSubmit = useCallback(async () => {
    try {
      await view.submit(value);
    } catch (e) {
      console.error(e);
    }
  }, [view, value]);

  const handleOnChange = useCallback((e) => {
    setValue(e.target.value);
  }, []);

  return (
    <CustomFieldEdit onSubmit={onSubmit}>
      <Label labelFor="textfield">Field label</Label>
      <Textfield onChange={handleOnChange} id="textfield" />
    </CustomFieldEdit>
  );
};
```
```

Outcome:
![Updated experience to inline edit](https://dac-static.atlassian.com/platform/forge/images/migration-guide-inline.png?_v=1.5800.1840)


How to edit custom fields in the modal (for more complex UI)

##### Original manifest and edit files

The `manifest.yml` file with no `isInline` property:

```
```
1
2
```



```
modules:
  jira:customField:
    - key: my-cf
      ...
      edit:
        resource: edit
        render: native
        experience:
          - "issue-create"
          - "issue-transition"
          - "issue-view"
          - "portal-request"
      ...
```
```

The `edit.jsx` file with the deprecated way of app rendering:

```
```
1
2
```



```
import React, { useState, useEffect } from "react";
import ForgeReconciler, {
  Form,
  Label,
  Textfield,
  useForm,
  FormSection,
  FormFooter,
  ButtonGroup,
  LoadingButton,
  Button,
} from "@forge/react";
import { view } from "@forge/bridge";

const Edit = () => {
  const [renderContext, setRenderContext] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const { handleSubmit, register, getFieldId, getValues } = useForm();

  useEffect(() => {
    view
      .getContext()
      .then((context) => setRenderContext(context.extension.renderContext));
  }, []);

  const onSubmit = async () => {
    try {
      setIsLoading(true);
      const { fieldName } = getValues();
      await view.submit(fieldName || "world");
    } catch (e) {
      setIsLoading(false);
      console.error(e);
    }
  };

  return renderContext === "issue-view" ? (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormSection>
        <Label labelFor={getFieldId("fieldName")}>Custom field value</Label>
        <Textfield {...register("fieldName")} />
      </FormSection>
      <FormFooter>
        <ButtonGroup>
          <Button appearance="subtle" onClick={view.close}>
            Close
          </Button>
          <LoadingButton
            appearance="primary"
            type="submit"
            isLoading={isLoading}
          >
            Submit
          </LoadingButton>
        </ButtonGroup>
      </FormFooter>
    </Form>
  ) : (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <Label labelFor={getFieldId("fieldName")}>Custom field value</Label>
      <Textfield {...register("fieldName")} />
    </Form>
  );
};
```
```

Outcome:
![Original experience](https://dac-static.atlassian.com/platform/forge/images/migration-guide-old-modal.png?_v=1.5800.1840)

##### Updated files

To update the app, add the `isInline` property to app's manifest file and replace the [Form](/platform/forge/ui-kit/components/form) component with [Modal](/platform/forge/ui-kit/components/modal) and [Button](/platform/forge/ui-kit/components/button) components to handle the correct modal rendering and the field's value submission.

The `manifest.yml` file with `isInline` property:

```
```
1
2
```



```
modules:
  jira:customField:
    - key: my-cf
      ...
      edit:
        resource: edit
        render: native
        isInline: true
        experience:
          - "issue-create"
          - "issue-transition"
          - "issue-view"
          - "portal-request"
      ...
```
```

The `edit.jsx` - version with modal edit experience:

```
```
1
2
```



```
import React, { useState, useCallback } from "react";
import ForgeReconciler, {
  Label,
  Textfield,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalTitle,
  ModalTransition,
  Button,
} from "@forge/react";
import { view } from "@forge/bridge";

const Edit = () => {
  const [value, setValue] = useState("");
  const [isOpen, setIsOpen] = useState(true);

  const closeModal = () => view.close();
  const onSubmit = useCallback(async () => {
    try {
      await view.submit(value);
    } catch (e) {
      console.error(e);
    }
  }, [view, value]);

  const handleOnChange = useCallback((e) => {
    setValue(e.target.value);
  }, []);

  return (
    <ModalTransition>
      {isOpen && (
        <Modal>
          <ModalHeader>
            <ModalTitle>Modal title</ModalTitle>
          </ModalHeader>
          <ModalBody>
            <Label labelFor="textfield">Field label</Label>
            <Textfield onChange={handleOnChange} id="textfield" />
          </ModalBody>
          <ModalFooter>
            <Button appearance="primary" onClick={onSubmit}>
              Submit
            </Button>
            <Button appearance="subtle" onClick={closeModal}>
              Close
            </Button>
          </ModalFooter>
        </Modal>
      )}
    </ModalTransition>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <Edit />
  </React.StrictMode>
);
```
```

Outcome:
![Updated experience to modal edit](https://dac-static.atlassian.com/platform/forge/images/migration-guide-new-modal.png?_v=1.5800.1840)

### Issue creation and issue transition dialog

Jira custom fields created by Forge apps that have editing functions defined can be added to
the new `Create issue dialog` and `Issue transition dialog` by users with the appropriate permission. Validation of these fields
is performed when the Create issue form is submitted.

In the `Create issue dialog` and `Issue transition dialog`, users can update field values inline.
This means that the edit entry point is rendered directly in the dialog. Default edit rendering is used unless you specify otherwise.
In apps using UI Kit, the entered value is submitted when the user clicks outside the field or elsewhere on the dialog.
An issue is created only after the value has been submitted.

Your app can find out which view a field is rendered on using the renderContext property
from the Atlassian app context:

```
```
1
2
```



```
const {
  extensionContext: { renderContext },
} = useProductContext();
```
```

To update a field's value before issue creation in apps using Custom UI or UI Kit, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit):

```
```
1
2
```



```
await view.submit(fieldValue);
```
```

For UI Kit, use the [CustomFieldEdit](/platform/forge/ui-kit/jira-components/custom-field-edit) component to render the edit view. The `onSubmit` function in the `CustomFieldEdit` component will be called on blur events, so you can place the submit logic there. Otherwise, you can create your own logic to use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit) outside the `onSubmit` function.

After issue creation is confirmed, non-required custom fields need to resolve a promise to
update their value within 10 seconds. If they don't, the issue will be created with the default
values.

### Portal request

All custom fields on Jira Service Management portal request are rendered inline. To use Custom UI or UI Kit for app rendering, specify the `portal-request` experience in the `edit` entry point.

To update a field's value before portal request creation in apps using Custom UI or UI Kit, use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit):

```
```
1
2
```



```
await view.submit(fieldValue);
```
```

For UI Kit, use the [CustomFieldEdit](/platform/forge/ui-kit/jira-components/custom-field-edit) component to render the edit view. The `onSubmit` function in the `CustomFieldEdit` component will be called on blur events, so you can place the submit logic there. Otherwise, you can create your own logic to use the [submit API](/platform/forge/apis-reference/ui-api-bridge/view/#submit) outside the `onSubmit` function.

After portal request creation is confirmed, non-required custom fields need to resolve a promise to
update their value within 10 seconds. If they don't, the issue will be created with the default
values.

### Formatter

The formatter is used to render the field on views where rendering with functions is not supported,
for example in email notifications or on the global issue navigator page.

Formatters are declared with [Jira expressions](/cloud/jira/platform/jira-expressions/),
making them fast enough to be invoked synchronously whenever a rendered human-readable field value is required.

If a formatter expression is applied to a set of issues, the number of [expensive operations](/cloud/jira/platform/jira-expressions/#expensive-operations)
executed by it must be constant. In other words, the expression must not contain any operations labeled with
[N](/cloud/jira/platform/jira-expressions-type-reference).

The following [context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables)
are available in the formatter expression:

* `user` ([User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user)):
  The user that wants to modify the field value.
* `issue` ([Issue](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#issue)):
  The edited issue.
* `project` ([Project](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#project)):
  The project the issue belongs to.
* `fieldId` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The ID of the field. For example, `customfield_10020`.
* `value`: The value that's being set on the field. The type of this variable depends on the data type of the field and can be one of the following:

  * [String](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#string), if the data type is `string` or `group`.
  * [Number](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#number), if the data type is `number`.
  * [User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user), if the data type is `user`.
  * [Map](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#map), if the data type is `object`.
  * [Date](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#date), if the data type is `datetime`.
  * [CalendarDate](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#calendardate), if the data type is `date`.

  If the field stores a [collection](#collection-types), the value type will be a
  [List](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#list) with items of one of the types specified above.

The formatter expression must return a `string` value that represents how the field should be displayed in the UI.

#### Using formatters in CSV export

By default, formatters aren't used for issue export to CSV.
Thanks to this, exported values can be seamlessly imported back to Jira.

To change that behavior, set the `export` property to `true`:

```
```
1
2
```



```
view:
  formatter:
    expression: "formatter expression"
    export: true
```
```

We recommend using this option in combination with specifying a [parser](#parser),
to make importing such an export possible.

#### Formatter example 1

In the simplest possible case, your formatter will just transform the current value without requiring any additional information.
For example, you can render a text-based progress bar for a field that stores progress as a number between 0 and 100:

```
```
1
2
```



```
view:
  formatter:
    expression: "`${'▰'.repeat(value / 10).padEnd(10, '▱')} (${value}%)`"
```
```

#### Formatter example 2

Imagine you have a string field whose values are IDs of some external components. A Forge function that renders this field
makes a call to your service to resolve those IDs into human-readable names.
While such external calls are not possible in Jira expressions, you can store the mapping between IDs and names in an
[entity property](/cloud/jira/platform/jira-entity-properties/), and read it in the formatter:

```
```
1
2
```



```
view:
  formatter:
    expression: |-
      let mapping = project.properties.get('idToNameMapping');
      mapping.get(value)
```
```

Since your app stores the data required to format the field on the Jira side, the user experience remains fast and reliable.

See the [documentation for Jira expressions](/cloud/jira/platform/jira-expressions/) to find out what else is possible.

## Data types

Each field type has to be based on a predefined data type.

The data type controls what kind of values the REST API accepts and returns for the field,
the field's behavior in JQL, and the default rendering behavior.

The available data types are:

* `string` - values represent plain strings. JQL offers autocomplete and exact comparison.
* `number` - values represent numbers (double-precision 64-bit IEEE 754 floating points).
* `user` - values represent users identified by Atlassian account IDs.
  The field behaves like any other user field in Jira when you interact with it in the UI or the REST API.
* `group` - values represent groups identified by names.
  The field behaves like any other group field in Jira when you interact with it in the UI or the REST API.
* `object` - values are arbitrary JSON objects. See below for more details.
* `datetime` - values are strings that represent dates with time and timezone.
  The field behaves like any other datetime field in Jira when you interact with it in the UI or the REST API.
  However, if milliseconds are provided, they are ignored.
* `date` - values are strings that represent dates.
  The field behaves like any other date field in Jira when you interact with it in the UI or the REST API.

### Object type

The `object` type makes use of additional properties compared to other types.

The required `formatter` property contains a
[Jira expression](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/) that returns a string.
This string is used to represent the value if the rendering function is not provided, or where the rendering function is not supported.
For example, the column view in the Global Issue Navigator.

The optional `schema` property contains the [JSON schema](https://json-schema.org/) that is used
to validate values stored in the field.

###### Object type JQL search

By default, you can search for a text string anywhere in the content of an object-type field.
To enable more fine-grained searching, create *Field properties* with the `searchAlias` schema property .

This means that, for a field named `X`:

* using the default behavior you can search the entire value stored in this field using `X ~ "text to search for"`
* by defining a field property, such as `Y`, in the schema with `searchAlias`,
  you can search that field property using `X.Y = value`.

The JQL type of each property created with `searchAlias` is derived from the schema type, using these rules:

* `string` schema type becomes a `string` in JQL.
* `number` schema type becomes a `number` in JQL.
* `integer` schema type becomes a `number` in JQL.
* `boolean` schema type becomes a `string` in JQL.
* `array` schema type becomes an array of items of a type following these rules. For example, an
  array containing items with the schema type `integer` becomes an array of items with the type
  `number` in JQL.
* search aliases for any other schema type are ignored.

It's possible to override the schema type with `searchType`.
This enables you to use the complex types supported in JQL but not available in the JSON schema.
The following search types are available:

* `text`, tokenized before indexing and enables searching for particular words.
* `user`, indexed as a user and enables user-based searching.
  The expected value is an *account ID* string (a universal Atlassian user identifier).
* `group`, indexed as a group and enables group-based searching.
  The expected value is a group ID.
* `date`, indexed as a date and enables date range searching and ordering.
  The expected date format is [YYYY]-[MM]-[DD].
  The expected date time format is [YYYY]-[MM]-[DD]T[hh]:[mm] with optional offset from UTC: +/-[hh]:[mm] or `Z` for no offset.
  For reference, see the [ISO\_8601](http://www.w3.org/TR/NOTE-datetime) standard.

Pairs of conflicting field properties, those with the same name and path but different types, are ignored.

###### Object type JQL search example

This is an example of a field that stores money. It showcases the use of:

* the `formatter` and `schema` properties.
* JQL search aliases.

```
```
1
2
```



```
  jira:customField:
    - key: cf-type-money
      name: Development cost
      description: Tracks the development cost of features, in different currencies
      type: object
      view:
        formatter: 
          expression: "`${value.amount} ${value.currency}`"
      schema:
        properties:
          amount:
            type: number
            searchAlias: Amount
          currency:
            type: string
            enum: [ "USD", "EURO", "AUD" ]
            searchAlias: Currency
          spender:
            type: string
            searchType: user
            searchAlias: Spender
        required: [ "amount", "currency" ]
```
```

The schema ensures that values of this field look like this:

```
```
1
2
```



```
{
  "amount": 100,
  "currency": "USD",
  "spender": "<account-id>"
}
```
```

With the formatter in place, displayed on the issue search, the value will be a string `100 USD`.

In addition to the default text search of the entire field value, more fine-grained search using these field properties is available:

* **Amount** (JQL type: `number`),
* **Currency** (JQL type: `string`),
* **Spender** (JQL type: `user`).

### Collection types

A Forge custom field can store a collection of up to 100 values.
This is done by declaring the `collection` property, which specifies the collection type.
For example, to create a field that stores a list of strings, declare it as:

```
```
1
2
```



```
type: string
collection: list
```
```

These data types can be part of a collection:

Using any other data type in combination with `collection:list` prevents the field from appearing in Jira.

## Field lifecycle

A [locked](https://confluence.atlassian.com/x/1Y4fOw) instance of each custom field defined in the manifest
is created upon deployment. For the field to be visible on issues, a Jira admin must first
[add it to screens](https://support.atlassian.com/jira-cloud-administration/docs/add-a-custom-field-to-a-screen/).

Unlike [`jira:customFieldType`](/platform/forge/manifest-reference/modules/jira-custom-field-type/) which creates field types that administrators can instantiate multiple times, `jira:customField` creates a single, app-controlled field instance.

The field disappears when the app is uninstalled or if the field is removed from the manifest.
If the app is reinstalled within 30 days, or the field is restored, the field will reappear with all the previous data intact.
All changes made to the field in the manifest (e.g. changing the name) are reflected in Jira after the app is deployed.
(**Warning**: changing the [data type](#data-types) after the field has been used with the old type
is not supported, and will result in undefined behavior, potentially making the field unusable.)

The type of the field (accessible through the `schema.custom` property in the
response of the [Get fields REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-fields/#api-rest-api-2-field-get))
is equal to the exact ID of the module, that is: `ari:cloud:ecosystem::extension/{app-id}/{environment-id}/static/{module-key}`, where:

* `{app-id}` is your app ID defined in the manifest.
* `{environment-id}` is the ID associated with the installation environment.
* `{module-key}` is the key of the custom field module defined in the manifest.

If you need to fetch this ID in your app (for example, to identify the field in the response of the
[Get fields REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-fields/#api-rest-api-2-field-get)),
use the `localId` property from the Atlassian app context. It has the following format:

```
```
1
2
```



```
ari:cloud:ecosystem::extension/<app-id>/<environment-id>/static/<invoked-module-key>
```
```

You can use it to create the ID of your custom field type.
There are two ways to get the Atlassian app context, depending on your app's rendering method:

## Read-only fields

Read-only fields are those that have `readOnly` set to `true` in their definition in the manifest.
They aren't editable by users, neither through the UI nor the
[Edit issue REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/#api-rest-api-2-issue-issueIdOrKey-put).

They are great for showing values derived from the issue state. While you can show anything using
[issue panels](/platform/forge/manifest-reference/modules/jira-issue-panel/) or [issue context panels](/platform/forge/manifest-reference/modules/jira-issue-context/),
custom fields may be a better choice if you need all their benefits, such as
JQL search, configuration on screens, or being part of the issue import and export.

The value of such fields has to be calculated beforehand and set with the dedicated
[REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-custom-field-values--apps-/#api-rest-api-2-app-field-fieldIdOrKey-value-put).
One pattern to achieve this is to listen to Atlassian app triggers for events that may affect
the values and update the values as necessary.

Additionally, updating the value on every issue view can be achieved with the [value function](#value-function).

Note that read-only fields won't be rendered on Jira Cloud issue create or transition screens, or Jira Service Management portal requests.

## Validation

A field value can be validated with [Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/).

Validation takes place whenever an issue is edited or created, but not when the app updates the value directly
with [the private field update REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-custom-field-values--apps-/#api-rest-api-2-app-field-fieldIdOrKey-value-put).

The following [context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables)
are available in the validation expression:

* `user` ([User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user)):
  The user that wants to modify the field value.
* `issue` ([Issue](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#issue)):
  The edited issue.
* `project` ([Project](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#project)):
  The project the issue belongs to.
* `fieldId` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The ID of the field. For example, `customfield_10020`.
* `value`: The value that's being set on the field. The type of this variable depends on the data type of the field and can be one of the following:

  * [String](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#string), if the data type is `string` or `group`.
  * [Number](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#number), if the data type is `number`.
  * [User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user), if the data type is `user`.
  * [Map](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#map), if the data type is `object`.
  * [Date](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#date), if the data type is `datetime`.
  * [CalendarDate](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#calendardate), if the data type is `date`.

  If the field stores a [collection](#collection-types), the value type will be a
  [List](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#list) with items of one of the types specified above.

The expression can return three types of values:

* `true` means that the validation was successful, and the operation is allowed.
* `false` means that the value is invalid. The error message defined in the manifest's `validation.errorMessage` property will be shown to the user.
* `String` means that the value is invalid. The returned string will be shown as the error message to the user.

#### Validation example 1

Allow only numbers between 0 and 100, plus empty (`null`) values:

```
```
1
2
```



```
edit:
  validation:
    expression: value == null || value >= 0 && value <= 100
    errorMessage: Only values between 0 and 100 are allowed.
```
```

#### Validation example 2

Allow only users from group `field-editors` to edit the value of the field,
unless it's a new issue being created, and the field value is empty.

```
```
1
2
```



```
edit:
  validation:
    expression: |-
      let isIssueCreate = issue == null || issue.id == null;
      let isEmpty = value == null; 
      let hasPermission = user.groups().includes('field-editors');
      isIssueCreate && isEmpty || hasPermission
    errorMessage: You don't have permission to edit this field.
```
```

See the [documentation for Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/) to find out what else is possible.

### Value Function

Forge apps can provide a value function that computes the value of the field.

This function is invoked on every issue view, so that the freshly computed value is shown to the user
whenever they open the issue page. Jira also saves this value into the database against the issue.
Thanks to this, the value is not only available for that one particular user interaction,
but also becomes immediately refreshed for the REST API, all other views, JQL search, etc.

This is useful mostly for [read-only](#read-only-fields) fields that show some derived data.
Because the value function is invoked only on the issue view, you will most likely still need to listen to events and update values asynchronously.
However, you can at least guarantee that users will always see a fresh value on the issue view.

Manifest example:

```
```
1
2
```



```
jira:customField:
  - key: field-key
    name: Name
    type: string
    view:
      value:
        function: computeValue
```
```

The function receives a list of issue IDs and returns a list of values for those issues.

Here is a payload example:

```
```
1
2
```



```
{
  "field": {
    "id": "customfield_10000",
    "key": "4886f49a-482d-41ba-bd73-6aeb5ee40e0f__DEVELOPMENT__my-custom-field-key",
    "type": "ari:cloud:ecosystem::extension/4886f49a-482d-41ba-bd73-6aec5ee40e0f/4e9fe62d-2575-4b2d-b0d7-5a37f43a80a9/static/my-custom-field-key",
    "name": "My custom field"
  },
  "issues": [
    {
      "id": 10001,
      "value": "value1"
    },
    {
      "id": 10002,
      "value": "value2"
    }
  ]
}
```
```

Here is an example of how to define the value function:

```
```
1
2
```



```
function valueFunctionName(arg) {
  return arg.issues.map((issue) => computeCurrentValue(arg.field, issue.id));
}

function computeCurrentValue(field, issueId) {
  // return the value of the field for the given issue ID
}
```
```

The values returned must be compatible with the format expected by the
[Edit Issue](/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-put)
REST API operation.

In the value function, make all calls to an Atlassian API as the app developer
by using the [`api.asApp()` method](/platform/forge/runtime-reference/product-fetch-api/#contextual-methods). `asUser` isn't supported.
Remember that the newly computed value will be visible to all users,
not only the user who triggered the update, so you shouldn't ever need to rely on user-specific behavior anyway.

For example, for the `user` type field the value must be an object that contains `accountId`.
So the function would have to return a list of values like this:

```
```
1
2
```



```
[{
  "accountId": "<user-1>"
}, {
  "accountId": "<user-2>"
}, {
  "accountId": "<user-1>"
}]
```
```

The order of values returned must be the same as the order of issues received in the argument.

Note that the issue view is the only view where the value function is invoked.
However, the function is still expected to work with multiple issues at once (accepting and returning lists).
Other views may become supported, including ones that display more than one issue at a time.
Therefore, make sure your function has constant performance regardless of the number of issues in the argument.

### Rendering hierarchy

The rendering hierarchy goes from functions (highest priority), to formatter expressions, to default rendering (lowest priority).

On views that support rendering with functions, the function is used if defined.
Otherwise, the formatter expression is used.
If neither is defined, the default rendering for the field's data type is used.

On the issue view, if the [value function](#value-function) is defined, it is invoked first,
then its result is passed on to the rendering function, formatter expression, or the default rendering component.

On views that don't support rendering with functions,
the formatter expression is used if defined in the manifest and supported on the view,
otherwise the raw field value is shown.

Some views don’t support custom edit rendering, including: boards, issue navigator, bulk edit view, transition screen, and more.
In these cases the default editing experience appropriate for the field’s data type is used.

### Display conditions

[Display conditions](../../display-conditions) for custom fields work only on the issue view, and the global issue create (GIC) form.
They allow you to change the visibility of custom fields for the current user.
Note that there are no guardrails: you can use display conditions to hide
a required field, making it impossible to create issues.

## Parser

The parser takes a string produced by the formatter and converts it into the shape expected by the field.

Use it when, on editing an issue, the user may provide a value that doesn’t conform to the underlying data type implementation of a field.
In such cases, the parser will convert the input into storable values.

Formatted string values may appear when:

* importing issues from CSV, especially when the formatter is used for export
* interacting with Jira views that don’t support editing with Custom UI or UI Kit, such as bulk update
* performing a JQL search
* using the [edit issue](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-put) REST API

#### Example

As an example, let’s use an [object type](#object-type) field that stores amounts of money in a given currency.

The actual values stored by the field would be JSON objects that look like this:

```
```
1
2
```



```
{
  "amount": 100,
  "currency": "USD"
}
```
```

To make the values human-readable, your app would declare a formatter that makes the values look like `100 USD`.

Now, to make the field able to consume strings like `100 USD`,
the app should declare a parser that can take such a string and transform it into a JSON object:

```
```
1
2
```



```
edit:
  parser:
    expression: |-
      let parts = value.split(' ');
      { 
        amount: Number(parts[0]), 
        currency: parts[1] 
      }
```
```

#### Specification

Parsers are declared with [Jira expressions](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/).

##### Parser input

The following [context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables)
are available in the parser expression:

* `user` ([User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user)):
  The current user.
* `issue` ([Issue](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#issue)):
  The issue being edited.
* `project` ([Project](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#project)):
  The project to which the issue belongs.
* `fieldId` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The ID of the field. For example, `customfield_10020`.
* `value`: A string provided by the user.

##### Output

The parser is expected to return a value compatible with the underlying data type of the field, as specified in the table below.

If the field stores a [collection](#collection-types), the returned value should be a
[List](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#list) with items of one of the types specified above.

## Search suggestions

When writing JQL queries in [advanced search](https://support.atlassian.com/jira-software-cloud/docs/what-is-advanced-searching-in-jira-cloud/),
users expect to receive automatic suggestions for valid values.
By default, we try to provide these suggestions automatically for Forge custom fields, differently for each data type.
For example, for fields of type `user`, we compile the list of suggestions from the pool of all Jira users.

Apps can override this default behavior and provide their own custom suggestions.
This is achieved by adding the `searchSuggestions` section into the field definition in the manifest.
The suggestion provider can be either a [Jira expression](/cloud/jira/platform/jira-expressions/),
or a Forge [function](/platform/forge/manifest-reference/modules/function/).

In the search suggestions function, calls to an Atlassian API must be done as the app developer by using [api.asApp()](https://developer.atlassian.com/platform/forge/runtime-reference/product-fetch-api/).
Making requests on behalf of a user with `api.asUser()` won’t work.

#### Input

The Jira expression has access to the following [context variables](/cloud/jira/platform/jira-expressions/#context-variables):

* `fieldId` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The ID of the field. For example, `customfield_10020`.
* `fieldType` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The type of the field. For example, `ari:cloud:ecosystem::extension/4211172c-5e6b-4170-9fce-f3314107517e/3b0cdefc-4f24-4696-a7dd-1092d95637f9/static/module-key`.
* `fieldName` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The name of the field. For example, `Issue progress`.
* `user` ([User](/cloud/jira/platform/jira-expressions-type-reference#user)): The user who is receiving the suggestions.
* `query` ([String](/cloud/jira/platform/jira-expressions-type-reference#string)): The string that the user already typed into the editor as the value of the field.
  Use it to narrow down the list of suggestions.

Similarly, the function receives an argument object with the same set of information:

```
```
1
2
```



```
{
  "fieldId": "<The ID of the field>",
  "fieldType": "<The type of the field>",
  "fieldName": "<The name of the field>",
  "query": "<the value entered by the user>",
  "user": {
    "accountId": "<the ID of the user that is requesting the suggestions>"
  },
  "context": {
    "cloudId": "<the ID of the instance the app is running on>"
  }
}
```
```

The following example shows a signature that can serve as a starting point for your function's implementation:

```
```
1
2
```



```
export function generateSearchSuggestions({ fieldId, fieldType, query, user: { accountId }, context: { cloudId }}) {
    // your implementation goes here
}
```
```

#### Output

The function or expression must return a list of suggestions.
Each suggestion can be either a plain string,
or an object that contains the value that’s used in JQL when the user selects the suggestion, and a label that the user sees on the list:

```
```
1
2
```



```
[
  {
    "value": "340f8126-50f7-4fe7-8765-1a151678b917",
    "label": "Value 1"
  },
  {
    "value": "771617fc-7417-4a4a-8b47-9230bbac47a0",
    "label": "Value2 2"
  }
]
```
```

If your values are already human-readable, you can just return plain strings:

```
```
1
2
```



```
["Value 1", "Value 2", "Value 3"]
```
```

## Known limitations

While we're working hard to make Forge custom fields indistinguishable from regular custom fields,
reaching full parity takes time.
This section summarizes the features missing from Forge custom fields.

### UI Kit and Custom UI rendering

Rich rendering with UI Kit and Custom UI is fully supported on the Jira Cloud issue view and issue creation screens, as well as on the Jira Service Management portal request screen.

Other places use the formatter to display field values, and simple built-in components are offered for editing.
For more details, see [rendering hierarchy](#rendering-hierarchy).

Eventually, we're planning to introduce fully custom rendering to as many places as possible.

### Support in other Atlassian apps

Forge custom fields may not be fully supported in Atlassian apps other than Jira Cloud and Jira Service Management,
such as Jira Mobile, or Confluence. Additionally, support in tools within Jira Cloud
(for example, [Jira automation](https://www.atlassian.com/software/jira/features/automation)) may be lacking.

We're constantly working on bringing the power of Forge fields to as many Atlassian apps and tools as we can.

### We are waiting for your feedback

If there is an issue that you would particularly like to be solved, let us know by
creating a ticket in the [Forge Jira project](https://ecosystem.atlassian.net/jira/dashboards/37320).

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Extension data

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type/value | Description |
| --- | --- | --- |
| `type` | `'jira:customField'` | The type of the module. |
| `entryPoint` | `'edit'` `'view'` | The entry point of the module. |
| `fieldId` | `string` | The ID of the field. For example, `customfield_10020`. |
| `fieldType` | `string` | The type of the field. For example, `ari:cloud:ecosystem::extension/4211172c-5e6b-4170-9fce-f3314107517e/3b0cdefc-4f24-4696-a7dd-1092d95637f9/static/module-key`. |
| `fieldValue` | `string` `string[]` `number` `object` | The value of the field. It has a type corresponding to the [data type](#data-types) of the field. |
| `issue.id` | `string` | The ID of the issue on which the module is rendered. |
| `issue.key` | `string` | The key of the issue on which the module is rendered. |
| `issue.type` | `string` | The name of the type of the issue on which the module is rendered. |
| `issue.typeId` | `string` | The ID of the type of the issue on which the module is rendered. |
| `project.id` | `string` | The ID of the project where the module is rendered. |
| `project.key` | `string` | The key of the project where the module is rendered. |
| `project.type` | `'business'`  `'software'`  `'product_discovery'`  `'service_desk'`  `'ops'` | The type of the project where the module is rendered. |
| `renderContext` | `'issue-view'` `'issue-create'` `'issue-transition'` `'portal-view'` `'portal-request'` | The context in which the extension is rendered. |
| `experience` | `'issue-view'` `'issue-create'` `'issue-transition'` `'portal-view'` `'portal-request'` | The type of experience in which the extension is rendered. While the render context is tied to a specific view, the experience property defines the type of view. |
| `issueTransition.id` | `string` | The ID of the transition on which the module is rendered. Only available for `issue-transition` experience. |
| `portal.id` | `number` | The ID of the service desk, depending on the page where it is rendered. Only available for `portal-view` and `portal-request` experiences. |
| `request.typeId` | `number` | The ID of the request type, depending on the page where it is rendered. Only available for `portal-view` and `portal-request` experiences. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Example

The following example declares a number-type field that represents issue progress:

```
```
1
2
```



```
jira:customField:
  - key: issue-progress
    name: Issue progress
    description: The progress of the issue, on a scale from 0 to 100.
    type: number
    readOnly: false
    view:
      resource: renderIssueProgress
      render: native
      experience:
        - "issue-view"
        - "portal-view"
      formatter:
        expression: "`${'▰'.repeat(value / 10).padEnd(10, '▱')} (${value}%)`"
        export: true
    edit:
      resource: editIssueProgress
      render: native
      experience:
        - "issue-view"
        - "issue-create"
        - "issue-transition"
        - "portal-request"
      validation:
        expression: value == null || (value >= 0 && value <= 100)
        errorMessage: The value must be a number between 0 and 100.
      parser:
        expression: "Number(value.replace('[^\\d]', ''))"
    searchSuggestions:
      expression: '["0", "25", "50", "75", 100"]'
resources:
  - key: renderIssueProgress
    path: src/frontend/index.jsx
  - key: editIssueProgress
    path: src/frontend/editIssueProgress.jsx
```
```

## Frequently asked questions

### Setup and configuration

#### How do I create a custom field?

The minimum required properties for a `jira:customField` are `key`, `name`, `description`, and `type`. Here's the basic manifest structure:

```
```
1
2
```



```
modules:
  jira:customField:
    - key: my-basic-field
      name: My Basic Field
      description: A simple custom field for storing text
      type: string

resources:
  - key: view-component
    path: src/view.jsx
  - key: edit-component
    path: src/edit.jsx
```
```

For UI Kit fields, you'll also need `view.render: native` and either `view.function` or `view.resource`. For object types, `view.formatter.expression` is mandatory.

#### Can I create custom fields without custom field types?

Yes, `jira:customField` and `jira:customFieldType` are completely independent modules. You can create `jira:customField` instances without defining any `jira:customFieldType`. They serve different purposes:

* `jira:customField`: Creates specific field instances controlled by your app
* `jira:customFieldType`: Creates field type templates for administrators to use

Most apps use one or the other, not both together.

#### How do I make object fields searchable in JQL?

For `jira:customField` with `type: object`, you must include the `view.formatter.expression` property to enable JQL search functionality and proper field display. Without the formatter expression, the app cannnot be deployed and the object field will not be searchable via JQL.

#### What data types can I use?

Supported types are: `string`, `number`, `user`, `group`, `datetime`, `date`, and `object`. You can also use collections with `collection: list` for array values.

### Administration and permissions

#### Can administrators modify my custom fields?

No, fields created with `jira:customField` are locked and fully controlled by your app. Jira administrators can only add these fields to screens but cannot modify their configuration, name, or behavior. If you need administrator-configurable fields, use [`jira:customFieldType`](/platform/forge/manifest-reference/modules/jira-custom-field-type/) instead.

#### How do I make my custom field visible to users?

After deploying your app, a Jira administrator must [add the field to screens](https://support.atlassian.com/jira-cloud-administration/docs/add-a-custom-field-to-a-screen/). The field exists but is hidden until added to appropriate screens (create, edit, view screens).

#### Who can update field values?

While administrators can't change the `jira:customField` configuration, users and automation can update field values:

* **Users**: Can edit field values through Jira's UI (unless field is marked `readOnly: true`)
* **Automation rules**: Can update field values using Jira's automation system
* **REST API**: Values can be updated via [Edit Issue REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/#api-rest-api-2-issue-issueIdOrKey-put)
* **App code**: Your app can update values using the [private field update REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-custom-field-values--apps-/#api-rest-api-2-app-field-fieldIdOrKey-value-put)

Validation rules you define in the manifest apply to user and automation updates, but not to direct app updates.

### Field behavior

#### What happens during the field lifecycle?

The field lifecycle for `jira:customField` follows these stages:

1. **Creation**: Field is automatically created as a locked instance when app is deployed
2. **Visibility**: Jira admin must add field to screens to make it visible to users
3. **Usage**: Users can interact with the field based on your view/edit configuration
4. **Updates**: Changes to field definition in manifest are reflected after app redeployment
5. **Removal**: Field disappears when app is uninstalled or field is removed from manifest
6. **Recovery**: If app is reinstalled within 30 days, field reappears with data intact
7. **Permanent deletion**: After 30 days, field data is permanently lost

#### What happens to field data when I uninstall my app?

When your app is uninstalled, the custom field disappears from Jira. However, if the app is reinstalled within 30 days, the field will reappear with all previous data intact. After 30 days, the field data is permanently lost.

#### How do view and edit modes differ?

* **View mode**: How the field appears when users are viewing an issue (read-only display)
* **Edit mode**: How the field appears when users are editing an issue (input controls)

You define these separately in your manifest using `view` and `edit` properties.

#### How do I make fields read-only?

Set `readOnly: true` in your manifest. Read-only fields can only be updated by your app via REST API, not by users or automation:

```
```
1
2
```



```
jira:customField:
  - key: computed-field
    name: Computed Field
    type: number
    readOnly: true
```
```

### Validation and requirements

#### How do I validate user input?

Use the `edit.validation.expression` property with Jira expressions:

```
```
1
2
```



```
edit:
  validation:
    expression: "value == null || (value >= 0 && value <= 100)"
    errorMessage: "Value must be between 0 and 100"
```
```

#### How do I make a field required?

Custom fields cannot be made required through the manifest. Jira administrators can configure field requirements through screen schemes and field configurations after the field is added to screens.

#### What are the limitations?

[Refer here](#known-limitations)

### API access

#### How do I access field values via API?

Field values are accessible through standard Jira REST APIs:
