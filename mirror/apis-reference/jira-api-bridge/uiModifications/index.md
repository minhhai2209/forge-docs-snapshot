# uiModifications

To consume the UI modifications (UIM) API, your app needs to import the `@forge/jira-bridge` package:

```
1
import { uiModificationsApi } from '@forge/jira-bridge';
```

## Initialization

### onInit method signature

```
1
onInit(<initCallback>, <registerFieldsCallback>): void
```

### onInit method description

The `onInit` method takes two callback functions:

* `initCallback`: where your app queries field or screen tab data and requests modifications.
* `registerFieldsCallback`: where your app specifies which fields will be changed by `initCallback`.

The values returned by `registerFieldsCallback` are used to:

* Show a loading indicator next to the relevant fields while `initCallback` runs.
* Enforce which fields can be modified inside `initCallback`.

There is no need to register screen tabs in order to modify them.

The callback functions are invoked whenever one of the following events occurs.

#### For Jira

* A *Global issue create* (GIC), *Issue view*, or *Issue transition* is opened from a supported entry point.
* The `project` or `issueType` in the context changes.
* (GIC only) An issue is created with the *Create another issue* checkbox enabled.

#### For Jira Service Management

* The *Request create portal* is opened.
* The `portal` or `requestType` in the context changes.

The `initCallback` function receives a single object argument with the following attributes:

* `api` – the API used to find and modify fields and/or screen tabs.
* `uiModifications` – an array of UIM entities registered for the given context.

The `registerFieldsCallback` function receives an object containing:

* `uiModifications` – an array of UIM entities registered for the given context.

```
```
1
2
```



```
uiModificationsApi.onInit(({ api, uiModifications }) => {
  // You can find form fields using the FieldsHookApi
  const summary = api.getFieldById('summary');
  // You can manipulate the fields you found
  if (summary) {
    summary.setDescription('New summary description');
  }
  // You can find screen tabs using the ScreenTabsHookApi
  const tabs = api.getScreenTabs();
  // You can manipulate the tabs you found
  if (Array.isArray(tabs) && tabs.length > 0) {
    tabs[0].setVisible(true);
    tabs[0].focus();
  }
}, ({ uiModifications }) => {
  // This function should return an array of the IDs of the fields
  // which are going to be changed in initCallback
  return ['summary'];
})
```
```

All modifications requested synchronously using this API will be batched and applied at once.
That means that consecutive modifications applied by the same `FieldAPI/ScreenTabAPI` method within the `onInit` callback will override the previous ones.

```
```
1
2
```



```
uiModificationsApi.onInit(({ api }) => {
    const { getFieldById } = api;
    const summary = getFieldById('summary');

    summary.setDescription('First description'); // will be overridden by the next `summary.setDescription` call
    summary.setDescription('Second description'); //  this change will be applied
}, ({ uiModifications }) => {
    return ['summary'];
})
```
```

If a `Promise` is returned from the callback, all of the modifications will be postponed until the `Promise` resolves.
This may be useful in a scenario when the app needs to perform an async operation before it requests a change.

UIM blocks any changes requested for fields within `initCallback` for any field IDs not in the array returned from `registerFieldsCallback`.

If the `initCallback` doesn’t return a `Promise` which resolves after all field and tab modification requests are made, then field and tab modifications requested asynchronously will be ignored.

## Reacting to change

### onChange method signature

```
```
1
2
```



```
onChange(<changeCallback>, <registerFieldsCallback>): void
```
```

### onChange method description

The `onChange` method also takes two callback functions:

* `changeCallback`: where your app queries field or screen tab data and requests modifications in response to user input.
* `registerFieldsCallback`: where your app specifies which fields will be changed by `changeCallback`.

The values returned by `registerFieldsCallback` are used to:

* Show a loading indicator next to the relevant fields while `changeCallback` runs.
* Enforce which fields can be modified inside `changeCallback`.

There is no need to register screen tabs in order to modify them.

Both callback functions are called whenever:

* The `blur` field event is triggered by one of the supported text fields (`summary` or `description`).
* The `change` field event is triggered by any other supported field (for example, when a user picks an option in a select-type field, or commits a value in Issue view).

The `changeCallback` function receives a single object argument with the following attributes:

* `api` – the API used to find and modify fields and/or screen tabs.
* `change` – an object with the `current` attribute containing the `FieldAPI` of the field that triggered the change event.
* `uiModifications` – an array of UIM entities registered for the given context.

The `registerFieldsCallback` function receives an object containing:

* `change` – an object with the `current` attribute containing the `FieldAPI` of the field that triggered the change event.
* `uiModifications` – an array of UIM entities registered for the given context.

```
```
1
2
```



```
uiModificationsApi.onChange(({ api, change, uiModifications }) => {
  // You can find form fields using the FieldsHookApi
  // You can also manipulate the fields you found or access the field
  // that triggered the change
  const { current } = change;
  if (current.getId() === 'summary') {
    // hint: You may want to read the content of uiModifications before
    // deciding what changes need to be applied here
    current.setDescription('New summary description');
  }
  // You can find screen tabs using the ScreenTabsHookApi
  const tabs = api.getScreenTabs();
  // You can manipulate the tabs you found
  if (Array.isArray(tabs) && tabs.length > 0) {
    tabs[0].setVisible(true);
    tabs[0].focus();
  }
}, ({ change, uiModifications }) => {
  // This function should return an array of the IDs of the fields
  // which are going to be changed in changeCallback
  return ['summary'];
})
```
```

All modifications requested synchronously using this API will be batched and applied at once.
That means that consecutive modifications applied by the same `FieldAPI/ScreenTabAPI` method within the `onChange` callback will override the previous ones.

```
```
1
2
```



```
uiModificationsApi.onChange(({ api }) => {
    const { getFieldById } = api;
    const summary = getFieldById('summary');

    summary.setDescription('First description'); // will be overridden by the next `summary.setDescription` call
    summary.setDescription('Second description'); //  this change will be applied
}, ({ uiModifications }) => {
    return ['summary'];
})
```
```

If a `Promise` is returned from the `callback`, all of the modifications will be postponed until the `Promise` resolves. This may be useful in a scenario when the app needs to perform an async operation before it requests a change.

UIM blocks any changes requested for fields within `changeCallback` for any field IDs not in the array returned from `registerFieldsCallback`.

If the `changeCallback` doesn’t return a `Promise` which resolves after all field modification requests are made, then field modifications requested asynchronously will be ignored.

## Error handling

### onError method signature

```
```
1
2
```



```
onError(<errorCallback>): void
```
```

### onError method description

An `errorCallback` is where apps can process information about the errors that happened during the execution of UI modifications. The callback function is called when:

* A `validation error` occurs, which means data passed to one of the [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) or [ScreenTabAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-screentabapi) methods was invalid.
* A `conflict error` occurs, which means multiple apps attempted to call the same [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) or [ScreenTabAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-screentabapi) method on the same field or tab.
* An `unregistered field` occurs, which means an app attempted to call the [FieldAPI](/platform/forge/apis-reference/jira-api-bridge/uiModifications/#common-fieldapi) with a field ID that’s not registered in the `registerFieldsCallback`.

The `errorCallback` function will receive one object as an argument.
This object contains the following attributes:

* `errors` - the array of objects with error data

```
```
1
2
```



```
uiModificationsApi.onError(({ errors }) => {
    // you can process errors' data in the errorCallback
    for (const error of errors) {
        if (error.type === 'FIELD_VALIDATION_FAILED') {
            logFieldValidationError(error);
        }

        if (error.type === 'SCREENTABS_VALIDATION_FAILED') {
            logScreenTabsValidationError(error);
        }

        if (error.type === 'MULTIPLE_APPS_CONFLICT') {
            logConflictError(error);
        }

        if (error.type === 'APPLY_CHANGES_FOR_UNREGISTERED_FIELD') {
            logUnregisteredFieldError(error);
        }
    }
})
```
```

#### field validation error shape

```
```
1
2
```



```
{
    type: 'FIELD_VALIDATION_FAILED',
    fieldId: string,
    fieldType: string,
    method: string, // for example: setRequired
    message?: string; // additional information about the error
}
```
```

#### screen tab validation error shape

```
```
1
2
```



```
{
    type: 'SCREENTABS_VALIDATION_FAILED',
    message?: string; // additional information about the error
}
```
```

#### conflict error shape

```
```
1
2
```



```
{
    type: 'MULTIPLE_APPS_CONFLICT',
    cause: 'FIELD',
    fieldId: string;
    fieldType: string;
    lifecycleHook: 'onInit' | 'onChange';
    method: string, // for example: setValue
    message: string; // additional information about the error
}
```
```

#### unregistered field error shape

```
```
1
2
```



```
{
    type: 'APPLY_CHANGES_FOR_UNREGISTERED_FIELD',
    fieldId: string;
    fieldType: string;
    message: string; // additional information about the error
}
```
```

## Querying fields

### getFieldById method signature

```
```
1
2
```



```
getFieldById<fieldType>(<fieldId>): FieldAPI | undefined
```
```

### getFieldById method description

The `getFieldById` method lets your app access a specific field on the current view. It:

* Uses a generic type parameter: `fieldType` (string) – the **type** of the field that the app wants to work on.
* Accepts one argument: `fieldId` (string) – the ID of the field that the app wants to work on.
* Returns a `FieldAPI` object if the field exists on the supported view.
* Returns `undefined` if the field doesn't exist or isn’t supported by UIM.

Example usage with regular field:

```
```
1
2
```



```
uiModificationsApi.onInit(({ api }) => {
  const { getFieldById } = api;
  const description = getFieldById('description')
  // You can perform operations on 'description'
  // field using the FieldAPI here
}, () => ['description'])
```
```

Example usage with custom field:

```
```
1
2
```



```
    uiModificationsApi.onInit(({ api }) => {
    const { getFieldById } = api;
    const select = getFieldById<'com.atlassian.jira.plugin.system.customfieldtypes:select'>('customfield_10035')
    // You can perform operations on 'customfield_10035'
    // single select field using the FieldAPI here
}, () => ['customfield_10035'])
```
```

## Iterating over supported fields

### getFields method signature

```
```
1
2
```



```
getFields(): FieldAPI[]
```
```

### getFields method description

Returns an array of `FieldAPI` objects with all supported fields available on a current view form.

Example usage:

```
```
1
2
```



```
uiModificationsApi.onInit(({ api }) => {
  const { getFields } = api;
  const fields = getFields();
  // You can iterate over fields
  // and perform operations on each
  // field using the FieldAPI here
}, () => [])
```
```

## Supported fields per view

# Support for custom fields

Jira

Jira Service Management

### Global issue create

### Issue view (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

### Issue transition (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

## Common FieldAPI

The changes requested by setters in this API aren't applied immediately.
They're batched and only applied after the execution of the `onInit` or `onChange` callback ends.
This means that reading the values using getters will always provide the initial form field state, which is immutable.

### getId

Returns the field's ID.

### getType

Returns the field's type.

### setName

```
```
1
2
```



```
setName(value: string): FieldAPI
```
```

Changes the field's name.

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/set-name.png?_v=1.5800.1798)

Example:

```
```
1
2
```



```
field.setName('New name for the field');
```
```

### getName

Returns the field's name.

### setDescription

```
```
1
2
```



```
setDescription(value: string): FieldAPI
```
```

Changes the field's description.

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/set-description.png?_v=1.5800.1798)

Example:

```
```
1
2
```



```
field.setDescription('This the description!');
```
```

### getDescription

```
```
1
2
```



```
getDescription(): string
```
```

Returns the field’s description.

### setVisible

```
```
1
2
```



```
setVisible(value: boolean): FieldAPI
```
```

Changes field visibility. The form payload will contain the field’s value, but the field won’t be visible in the UI if this is set to `false`.

Example:

```
```
1
2
```



```
field.setVisible(false);
```
```

### isVisible

Returns `true` if the field is currently visible. Returns `false` otherwise.

### setValue

```
```
1
2
```



```
setValue(value: unknown): FieldAPI
```
```

Set a given field's value. See the specific field value contracts in the [Field details section](/platform/forge/custom-ui-jira-bridge/uiModifications/#field-details) below to make sure the changes requested by this method will be applied.

### getValue

See the field contracts below to learn the shape of the data returned by each field.

### setReadOnly

```
```
1
2
```



```
setReadOnly(value: boolean): FieldAPI
```
```

Set if a given field’s value is read-only. If true, the form payload will contain the field’s value, but the user won’t be able to modify the value in the UI.

Example:

```
```
1
2
```



```
field.setReadOnly(true);
```
```

On the Issue view, fields that don't have a value are automatically hidden when set to read-only. This is the default behavior when the user doesn't have permission to edit.

### isReadOnly

Returns `true` if the field's value currently can't be modified. Returns `false` otherwise.

### setRequired

```
```
1
2
```



```
setRequired(value: boolean): FieldAPI
```
```

Set a given field as required. Fields required by system configuration can't be set to non-required.
Example:

```
```
1
2
```



```
field.setRequired(true);
```
```

### isRequired

Returns `true` if the field is currently required. Returns `false` otherwise.

### setOptionsVisibility

```
```
1
2
```



```
setOptionsVisibility(options: string[], isVisible: boolean): FieldAPI
```
```

Applies a visibility rule based on a list of option `ids` and `isVisible` arguments for a given field's dropdown list of options.

Note that the method only allows you to either make some options visible or make some options hidden, not both.

Example:

```
```
1
2
```



```
// Only display the enumerated options, others will be hidden
field.setOptionsVisibility(['field-option-id-1', 'field-option-id-2'], true);

// Only hide the enumerated options, others will be visible
field.setOptionsVisibility(['field-option-id-1', 'field-option-id-2'], false);

// Special case, hide all options in the dropdown
field.setOptionsVisibility([], true);
```
```

Options hidden in the dropdown can still be selected as a field's default value or by using `field.setValue`.

# Known limitation

In **Issue view** and **Issue transition**, the number of **options** that can be set via the `setOptionsVisibility` method can't be greater than **100** per one update.

This means that each field with `setOptionsVisibility` support has its own 100 **options** limit.

### getOptionsVisibility

```
```
1
2
```



```
getOptionsVisibility(): OptionsVisibility | undefined
```
```

Returns an `object` containing the `isVisible: boolean` and `options: string[]` attributes. The `options` attribute contains IDs of options with modified visibility.

This method, when called within the `onInit` callback, always returns `undefined`, meaning the visibility of options wasn't yet modified by `setOptionsVisibility`.

## Field details

### issue type

type: `issuetype`

#### setValue signature

The execution of the `setValue` method will initiate a UIM context change in **Global issue create** (GIC).
Issue type is a part of the UIM invocation context. Changing the issue type with `setValue` changes that context.

UI modifications won’t be applied to an issue type field that’s out of the [UIM app invocation context](/platform/forge/manifest-reference/modules/jira-ui-modifications/#uim-app-invocation-context).

Note that issue types have different UIM app invocation contexts, so UIM functionality may not be applied the same way, in particular when it comes to [setting visibility of options](/platform/forge/custom-ui-jira-bridge/uiModifications/#setoptionsvisibility).

```
```
1
2
```



```
setValue(id: string): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): IssueTypeField
```
```

#### issue type field shape

```
```
1
2
```



```
{
    id: string,
    name: string,
}
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-issue-type.png?_v=1.5800.1798)

### priority

type: `priority`

#### setValue signature

```
```
1
2
```



```
setValue(id: string): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): PriorityField
```
```

#### Priority field shape

```
```
1
2
```



```
{ 
  id: string,   // '2'
  name: string, // 'High'
  iconUrl?: string,
}
```
```

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-priority.png?_v=1.5800.1798)

### project picker

type: `com.atlassian.jira.plugin.system.customfieldtypes:project`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(id: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ProjectPickerField
```
```

#### Project Picker field shape

```
```
1
2
```



```
{ 
  projectId: string,   // '10002'
} | null
```
```

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-project.png?_v=1.5800.1798)

### Resolution

type: `resolution`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(id: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ResolutionField
```
```

#### Resolution field shape

```
```
1
2
```



```
{ 
  id: string,
  value: string,
} | null
```
```

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-resolution.png?_v=1.5800.1798)

### summary

type: `summary`

#### setValue signature

```
```
1
2
```



```
setValue(id: SummaryField): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): SummaryField
```
```

#### Summary field shape

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-summary.png?_v=1.5800.1798)

### assignee

type: `assignee`

#### setValue signature

```
```
1
2
```



```
setValue(accountId: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): AssigneeField
```
```

#### Assignee field shape

```
```
1
2
```



```
null | {
    accountId: string,
}
```
```

# Known limitation

The number of unique `accountIds` that can be set via the `setValue` method can't be greater than 90 per one batched update.

This means that all calls to `setValue` for user-based fields performed in a single `onInit` or `onChange` callback are counted against this limit.

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-assignee.png?_v=1.5800.1798)

### reporter

type: `reporter`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(accountId: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ReporterField
```
```

#### reporter field shape

```
```
1
2
```



```
null | {  accountId: string }
```
```

# Known limitation

The number of unique `accountIds` that can be set via the `setValue` method can't be greater than 90 per one batched update.

This means that all calls to `setValue` for user-based fields performed in a single `onInit` or `onChange` callback are counted against this limit.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-reporter.png?_v=1.5800.1798)

### labels

type: `labels`

#### setValue signature

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): LabelsField
```
```

#### labels field shape

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-labels.png?_v=1.5800.1798)

### description

type: `description`

The `description` field can be configured using either the rich-text "Wiki style renderer" (current default) or plain-text "Default style renderer". Each renderer requires a different value type, and apps will need to match the type they receive from `getValue` in any calls to `setValue`.
For more information on how to configure field renderers, please refer to <https://support.atlassian.com/jira-cloud-administration/docs/configure-renderers/>

#### setValue signature

```
```
1
2
```



```
setValue(value: DescriptionField): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DescriptionField
```
```

#### description field shape (Global issue create, Issue transition)

```
```
1
2
```



```
string // Plain-text editor
|
type ADF = {
    version: 1,
    type: 'doc',
    content: Node[]
} // Rich-text editor (ADF format)
// https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
```
```

#### description field shape (Issue view)

```
```
1
2
```



```
type ADF = {
    version: 1,
    type: 'doc',
    content: Node[]
} // Rich-text editor (ADF format)
// https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-description.png?_v=1.5800.1798)
![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-description-plain-text.png?_v=1.5800.1798)

### components

type: `components`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ComponentsField
```
```

#### components field shape

```
```
1
2
```



```
[
    {
        id: string,
        name: string,
    },
    {
        id: string,
        name: string,
    },
    ...
  ]
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-components.png?_v=1.5800.1798)

### fix versions

type: `fixVersions`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): FixVersionsField
```
```

#### fix versions field shape

```
```
1
2
```



```
[
    {
        id: string,
        name: string,
    },
    {
        id: string,
        name: string,
    },
    ...
  ]
```
```

# Known limitation

In **Issue view** and **Issue transition**, you can only set up to 100 IDs per update using the `setValue` method.

This means that each supported field has its own limit of 100 IDs.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-fix-versions.png?_v=1.5800.1798)

### affects versions

type: `versions`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): VersionsField
```
```

#### affects versions field shape

```
```
1
2
```



```
[
    {
        id: string,
        name: string,
    },
    {
        id: string,
        name: string,
    },
    ...
  ]
```
```

# Known limitation

You can only set up to 100 IDs per update using the `setValue` method.

This means that each field of this type has its own limit of 100 IDs.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-affects-versions.png?_v=1.5800.1798)

### single select

type: `com.atlassian.jira.plugin.system.customfieldtypes:select`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(id: string): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): SelectField
```
```

#### select field shape

```
```
1
2
```



```
null | {
    id: string,
    value: string,
}
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-select.png?_v=1.5800.1798)

### multi select

type: `com.atlassian.jira.plugin.system.customfieldtypes:multiselect`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): MultiSelectField
```
```

#### multi select field shape

```
```
1
2
```



```
[
    {
        id: string,
        value: string,
    },
    {
        id: string,
        value: string,
    },
    ...
]
```
```

# Known limitation

In **Issue view** and **Issue transition**, you can only set up to 100 IDs per update using the `setValue` method.

This means that each supported field has its own limit of 100 IDs.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-multi-select.png?_v=1.5800.1798)

### Cascading select

type: `com.atlassian.jira.plugin.system.customfieldtypes:cascadingselect`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(value: {
    parentId: string;
    childId: string | null;
} | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): CascadingSelectField
```
```

#### cascading select field shape

```
```
1
2
```



```
null | {
    parent: { id: string; value: string };
    child: { id: string; value: string } | null;
}
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-cascading-select.png?_v=1.5800.1798)

### checkboxes

type: `com.atlassian.jira.plugin.system.customfieldtypes:multicheckboxes`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(ids: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): MultiCheckboxesField
```
```

#### checkboxes field shape

```
```
1
2
```



```
[
    {
        id: string,
        value: string,
    },
    {
        id: string,
        value: string,
    },
    ...
]
```
```

# Known limitation

In **Issue view** and **Issue transition**, you can only set up to 100 IDs per update using the `setValue` method.

This means that each supported field has its own limit of 100 IDs.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-multi-check-boxes.png?_v=1.5800.1798)

### radio buttons

type: `com.atlassian.jira.plugin.system.customfieldtypes:radiobuttons`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(id: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): RadioButtonsField
```
```

#### radio buttons field shape

```
```
1
2
```



```
null | {
    id: string,
    value: string,
}
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/radio-buttons.png?_v=1.5800.1798)

### paragraph

type: `com.atlassian.jira.plugin.system.customfieldtypes:textarea`

#### setValue signature

```
```
1
2
```



```
setValue(value: ParagraphField): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ParagraphField
```
```

#### paragraph field shape

```
```
1
2
```



```
string // Plain-text editor
|
type ADF = {
    version: 1,
    type: 'doc',
    content: Node[]
} // Rich-text editor (ADF format)
// https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-paragraph.png?_v=1.5800.1798)
![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-paragraph-plain-text.png?_v=1.5800.1798)

### text field

type: `com.atlassian.jira.plugin.system.customfieldtypes:textfield`

#### setValue signature

```
```
1
2
```



```
setValue(value: TextField): FieldAPI
```
```

#### getValue signature

#### text field shape

```
```
1
2
```



```
string // Plain-text editor
```
```

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-text.png?_v=1.5800.1798)

### user picker

type: `com.atlassian.jira.plugin.system.customfieldtypes:userpicker`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(accountId: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): UserPickerField
```
```

#### user picker field shape

```
```
1
2
```



```
null | {
    accountId: string,
}
```
```

# Known limitation

The number of unique `accountIds` that can be set via the `setValue` method can't be greater than 90 per one batched update.

This means that all calls to `setValue` for user-based fields performed in a single `onInit` or `onChange` callback are counted against this limit.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-user-picker.png?_v=1.5800.1798)

### multi user picker

type: `com.atlassian.jira.plugin.system.customfieldtypes:multiuserpicker`

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(accountId: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): MultiUserPickerField
```
```

#### multi user picker field shape

```
```
1
2
```



```
[
    {
        accountId: string,
    },
    {
        accountId: string,
    },
    ...
  ]
```
```

# Known limitation

The number of unique `accountIds` that can be set via the `setValue` method can't be greater than 90 per one batched update.

This means that all calls to `setValue` for user-based fields performed in a single `onInit` or `onChange` callback are counted against this limit.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-multi-user-picker.png?_v=1.5800.1798)

### people

type: `com.atlassian.jira.plugin.system.customfieldtypes:people`

This field is available in a [team-managed](https://support.atlassian.com/jira-software-cloud/docs/work-in-jira-software-cloud-team-managed-projects/) project only.

The `people` field can be configured using either the single or multiple value field. In the case of a single value configuration, only the first value from the array provided via the `setValue` will be displayed in the field.

#### setValue signature

Use `[]` to unset the value.

```
```
1
2
```



```
setValue(accountId: string[]): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): PeopleField
```
```

#### people field shape

```
```
1
2
```



```
[
    {
        accountId: string,
    },
    {
        accountId: string,
    },
    ...
  ]
```
```

# Known limitation

The number of unique `accountIds` that can be set via the `setValue` method can't be greater than 90 per one batched update.

This means that all calls to `setValue` for user-based fields performed in a single `onInit` or `onChange` callback are counted against this limit.

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-people-picker.png?_v=1.5800.1798)

### url

type: `com.atlassian.jira.plugin.system.customfieldtypes:url`

#### setValue signature

```
```
1
2
```



```
setValue(url: string): FieldAPI
```
```

#### getValue signature

#### url field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-url.png?_v=1.5800.1798)

### date picker

type: `com.atlassian.jira.plugin.system.customfieldtypes:datepicker`

#### setValue signature

Use `null` to unset the value.

The provided string must be in the `yyyy-MM-dd` date format.

```
```
1
2
```



```
setValue(date: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DatePickerField
```
```

#### date picker field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-date-picker.png?_v=1.5800.1798)

### date time picker

type: `com.atlassian.jira.plugin.system.customfieldtypes:datetime`

#### setValue signature

Use `null` to unset the value.

The provided string must be in the `YYYY-MM-DDThh:mmTZD` date format.

```
```
1
2
```



```
setValue(value: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DatePickerField
```
```

#### date picker field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-date-time.png?_v=1.5800.1798)

### due date

type: `duedate`

#### setValue signature

Use `null` to unset the value.

The provided string must be in the `yyyy-MM-dd` date format.

```
```
1
2
```



```
setValue(date: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DatePickerField
```
```

#### date picker field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-due-date.png?_v=1.5800.1798)

### target start

type: `com.atlassian.jpo:jpo-custom-field-baseline-start`

#### setValue signature

Use `null` to unset the value.

The provided string must be in the `yyyy-MM-dd` date format.

```
```
1
2
```



```
setValue(date: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DatePickerField
```
```

#### date picker field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-target-start.png?_v=1.5800.1798)

### target end

type: `com.atlassian.jpo:jpo-custom-field-baseline-end`

#### setValue signature

Use `null` to unset the value.

The provided string must be in the `yyyy-MM-dd` date format.

```
```
1
2
```



```
setValue(date: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): DatePickerField
```
```

#### date picker field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-target-end.png?_v=1.5800.1798)

### number

type: `com.atlassian.jira.plugin.system.customfieldtypes:float`

#### setValue signature

Use `null` to unset the value.

```
```
1
2
```



```
setValue(value: number | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): NumberField
```
```

#### number custom field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-number.png?_v=1.5800.1798)

### parent

type: `parent`

#### setValue signature

```
```
1
2
```



```
setValue(id: string | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): ParentField
```
```

#### parent field shape

```
```
1
2
```



```
{ 
  id: string,  
  key: string, 
} | null
```
```

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-parent.png?_v=1.5800.1798)

### status

type: `status`

#### setValue signature

The screen will appear if configured for the used transition ID.

The get value method returns the ID and name of the current status. You should pass the transition ID to the set value method.

```
```
1
2
```



```
setValue(transitionId: string): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): StatusField | null
```
```

#### status field shape

```
```
1
2
```



```
{ 
  id: string,  
  name: string, 
}
```
```

#### Reference screenshot

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-status.png?_v=1.5800.1798)

### original estimate

type: `timeoriginalestimate`

#### setValue signature

Use `null` to unset the value.

The input should be an integer greater than 0, representing the estimated time in minutes. See [What are time estimations?](https://support.atlassian.com/jira-software-cloud/docs/what-are-time-estimates-days-hours-minutes/)

```
```
1
2
```



```
setValue(value: number | null): FieldAPI
```
```

#### getValue signature

```
```
1
2
```



```
getValue(): OriginalEstimateField
```
```

#### original estimate field shape

#### Reference screenshots

![](https://dac-static.atlassian.com/platform/forge/images/jira-ui-modifications/field-original-estimate.png?_v=1.5800.1798)

## Querying screen tabs

### getScreenTabById method signature

```
```
1
2
```



```
getScreenTabById(<tabId>): ScreenTabAPI | undefined
```
```

### getScreenTabById method description

The `getScreenTabById` method lets your app access a specific screen tab on the current view. ßIt:

* Accepts one argument: `tabId` (string) – the identifier of the screen tab that the app wants to work on.
* Returns a `ScreenTabAPI` object if the tab exists on Global issue create (GIC) or Issue view.
* Returns `undefined` if the screen tab doesn't exist or isn’t supported by UIM.

Example usage with a regular screen tab:

```
```
1
2
```



```
uiModificationsApi.onInit(({ api }) => {
  const { getScreenTabById } = api;
  const tab = getScreenTabById('<identifier>')
  // You can perform operations on a specific screen tab
  // using the ScreenTabAPI here
}, () => [''])
```
```

## Iterating over screen tabs

### getScreenTabs method signature

```
```
1
2
```



```
getScreenTabs(): ScreenTabAPI[]
```
```

### getScreenTabs method description

Returns an array of `ScreenTabAPI` objects with all screen tabs mounted on the current view.

Example usage:

```
```
1
2
```



```
uiModificationsApi.onInit(({ api }) => {
  const { getScreenTabs } = api;
  const tabs = getScreenTabs();
  // You can iterate over screen tabs
  // (or access them by index)
  // and perform operations on each
  // screen tab using the ScreenTabAPI here.
}, () => [])
```
```

## Common ScreenTabAPI

The changes requested by setters in this API aren't applied immediately.
They’re batched and only applied after the execution of the `onInit` or `onChange` callback ends.
This means that reading the values using getters will always provide the screen tab’s initial state, which is immutable.

### getId

Returns the screen tab identifier.

### setVisible

```
```
1
2
```



```
setVisible(value: boolean): ScreenTabAPI
```
```

Changes tab visibility.

Example:

```
```
1
2
```



```
tab.setVisible(false);
```
```

# Don't hide in-focus tabs

Make sure you don't try to hide the tab that's currently in focus. If you do, your UIM won't be applied and the `onError` callback will receive a `SCREENTABS_VALIDATION_FAILED` error.

### isVisible

Returns `true` if the tab is currently visible. Returns `false` otherwise.

### focus

Switches the focus to a given screen tab. Automatically puts other visible tabs out of focus.

Example:
