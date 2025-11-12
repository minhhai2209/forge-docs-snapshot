# Upgrade to @forge/react major version 10

This guide is only applicable for migrating existing UI Kit apps on @forge/react major version 9 to the latest version of UI Kit.

The [latest version of UI Kit](/platform/forge/changelog/#1590) is now generally available. This version comes with a new major version of `@forge/react` containing 37 updated components.

While updating from `@forge/react` version 9 to version 10 (UI Kit latest) will provide you with more features and capabilities, it may also contain breaking changes for the apps that are using `@forge/react` version 9.
Changes to the components - including which components have breaking changes - are outlined below.

To upgrade your app to the latest version, run `npm install --save @forge/react@latest` in your terminal.

## Component changes in new version

The most significant changes are to the **[Form](#form), [Tabs](#tabs)** and **[Table](#table)** components. The capabilities of these components have been enhanced; however, this does mean there are breaking changes between the two versions.

If your app is heavily reliant on these three components, we recommend you review the updated documentation to understand the differences and the effort required to migrate your app.

## Badge

Breaking changes

* `Badge` has a new `max` prop that defaults to the value of 99. It will render badge content as 99+ for values greater than 99.

## Button

Breaking changes

* The `disabled` prop has been renamed to `isDisabled`.
* `icon` and `iconPosition` have been updated to `iconBefore` and `iconAfter`. `iconBefore` and `iconAfter` take the same values as icon and will position before and after the button children contents accordingly.

## ButtonSet

Breaking changes

* The `ButtonSet` component has been replaced by [ButtonGroup](/platform/forge/ui-kit/components/button-group/). There are no other breaking changes outside of the component name change.

## Checkbox

No breaking changes

## CheckboxGroup

Breaking changes

* The `children`, `description` and `label` props have been removed. The `options` prop, `HelperMessage` component, and `Label` component can be used instead.

```
```
1
2
```



```
<Label labelFor="products">Products</Label>
<CheckboxGroup name="products" options={[
  { label: 'Jira', value: 'jira' },
  { label: 'Confluence', value: 'confluence' },
]} />
<HelperMessage>Pick a product</HelperMessage>
```
```

## Code

Breaking changes

* The functionality of Code has now been separated into two different components:
  * `Code` should now only be used for inline code.
  * [CodeBlock](/platform/forge/ui-kit/components/code-block/) has been added and should be used for code blocks.

## DateLozenge

Breaking changes

* `DateLozenge` has been removed and can be replaced by using [Lozenge](/platform/forge/ui-kit/components/lozenge/).
* The date value must be formatted to the desired display value.

## DatePicker

Breaking changes

* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="start-date">Start date</Label>
<DatePicker id="start-date" />
<HelperMessage>Enter a start date</HelperMessage>
```
```

## Form

Breaking changes

* The `submitButtonText` and `actionButtons` props have been removed. A `Button` component with the `type="submit"` prop must be used within your `Form` component to allow for form submissions.
* The `Form` component should now be used with the [useForm](/platform/forge/ui-kit-2/use-form/) hook for state management. See [example usage](/platform/forge/ui-kit/components/form/#field-level-validation).

## Heading

Breaking changes

* The `size` prop has been removed. The `as` prop is now required instead. Heading [accessibility guidelines](/platform/forge/ui-kit/components/heading/#accessibility-considerations) should be followed.

## Image

No breaking changes

## Inline

Breaking changes

* The `grow` prop is temporarily removed and will be re-added in the future. `hug` and `fill` behaviour can be replaced by setting the desired width on the `xcss` prop on a Box component.

```
```
1
2
```



```
<Inline>
  <Box xcss={{backgroundColor: 'color.background.discovery'}}>hugged</Box>
  <Box xcss={{backgroundColor: 'color.background.information', width:'100%'}}>filled</Box>
</Inline>
```
```

## Link

No breaking changes

## ModalDialog

Breaking changes

* Replaced by [Modal](/platform/forge/ui-kit/components/modal/).
* The `closeButtonText` and `header` props have been removed.
  * A `Button` component will need to be rendered to close `Modal`.
  * The `header` prop has been replaced by `ModalTitle`.

## Radio

Breaking changes

* The `defaultChecked` prop has been removed. Use `isChecked` instead.

## RadioGroup

Breaking changes

* The `children` prop has been replaced by `options`.
* The `description` and `label` props have been removed. The `options` prop, `HelperMessage` component, and `Label` component can be used instead.

```
```
1
2
```



```
<Label labelFor="color">Color</Label>
<RadioGroup id="color" options={[
  { name: 'color', value: 'red', label: 'Red' },
  { name: 'color', value: 'blue', label: 'Blue' },
  { name: 'color', value: 'yellow', label: 'Yellow' },
]} />
<HelperMessage>Pick a color</HelperMessage>
```
```

## Range

Breaking changes

* Now spans the full width of its container.
* The `label` prop has been removed. The `Label` component can be used instead.

```
```
1
2
```



```
<Label labelFor="range">Range</Label>
<Range id="range" />
```
```

## SectionMessage

Breaking changes

* The `appearance` prop now takes different values.
  * `information` replaces `info`.
  * `success` replaces `confirmation`.
  * `discovery` replaces `change`.

## Select

Breaking changes

* The `children` prop has been replaced by `options`.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="fruit">Favourite fruit</Label>
<Select
  inputId="fruit"
  options={[
    { label: 'Apple', value: 'apple' },
    { label: 'Banana', value: 'banana' },
  ]}
/>
<HelperMessage>Pick a fruit</HelperMessage>
```
```

## Stack

No breaking changes

## StatusLozenge

Breaking changes

* The `StatusLozenge` component has been replaced by [Lozenge](/platform/forge/ui-kit/components/lozenge/). There are no other breaking changes outside of the component name change.

## Table

Breaking changes

* The `Table` component has been replaced by [DynamicTable](/platform/forge/ui-kit/components/dynamic-table/).
* Individual `Head`, `Row` and `Cell` components have been removed in favour of data being passed in via arrays and objects.
* Major breaking changes were made here to provide a more powerful table with additional features.

## Tabs

Breaking changes

* The code layout of `Tabs` has been updated. See an [example](/platform/forge/ui-kit/components/tabs/) of the new Tabs component.

## Tag group

No breaking changes

## Tag

Breaking changes

* The color prop values are now camel cased instead of snake case.
  * i.e. `greyLight` replaces `grey-light`.
* `children` is now replaced by the `text` prop.

## Text area

Breaking changes

* Now spans the full width of its container.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="message">Message</Label>
<TextArea id="message" />
<HelperMessage>Enter a message</HelperMessage>
```
```

## Text field

Breaking changes

* Component renamed from `TextField` to `Textfield`.
* Now spans the full width of its container.
* The `description` and `label` props have been removed. Use the `HelperMessage` and `Label` components instead.

```
```
1
2
```



```
<Label labelFor="email">Email</Label>
<Textfield id="email" />
<HelperMessage>Enter an email</HelperMessage>
```
```

## Text

No breaking changes

## Toggle

Breaking changes

* The `label prop` has been removed. Use the `Label` component instead.

```
```
1
2
```



```
<Toggle id="toggle" />
<Label labelFor="toggle">Toggle</Label>
```
```

Breaking changes

* The `text` prop has been replaced by `content`.

## User

No breaking changes

## UserGroup

No breaking changes

## UserPicker

Breaking changes

* Now spans the full width of its container.
