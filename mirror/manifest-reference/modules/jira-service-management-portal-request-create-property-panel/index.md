# Jira Service Management portal request create property panel

The `jiraServiceManagement:portalRequestCreatePropertyPanel` module is displayed on the request creation screen in the
customer portal and enables apps to save arbitrary data during request creation as Jira issue properties. For more
information on Jira entity properties, see [Jira entity properties](/platform/forge/manifest-reference/modules/jira-entity-property).

This module can be used in Jira Service Management.

![Example of a Portal request create property panel](https://dac-static.atlassian.com/platform/forge/images/portal-request-create-property-panel-demo.png?_v=1.5800.1801)

## Portal Request Create Property Panel Lifecycle

The `jiraServiceManagement:portalRequestCreatePropertyPanel` uses [Jira entity properties](/platform/forge/manifest-reference/modules/jira-entity-property).
The form data from the Forge portal request create property panel can be saved to the original request create form state using
`view.submit` method of`@forge/bridge` library.

### Form data schema

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `fields` | List of `field` object | Yes | This is a list of all the field objects present in the Forge portal request create property panel form. |
| `isValid` | `boolean` | yes | The value will be `true` if all the fields in the Forge portal request create property panel form are valid and `false` otherwise. |
| `unlicensedAccess` | List<string> |  | A list of unlicensed user types that can access this module. Valid values are: `unlicensed`, `customer`, and `anonymous`. For more information, see [Access to Forge apps for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users). |

### Field Object schema

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | This is a unique identifier for the fields present in the Forge portal request create property panel form. |
| `value` | `object` | yes | The data stored corresponding to each field in the Forge portal request create property panel form. |

The `view.submit` method can be invoked every time the fields in the Forge portal request create property panel form is
updated. The field data would be stored in the
[Jira issue property](/cloud/jira/platform/rest/v3/api-group-issue-properties/#api-rest-api-3-issue-issueidorkey-properties-propertykey-get) when the request form is submitted.

Once the portal request creation form is saved, the data stored using the
`jiraServiceManagement:portalRequestCreatePropertyPanel` module can be retrieved from the extension context of
`jiraServiceManagement:portalRequestDetail`.

See the [example](#example) for more details.

Issue properties persisted using `view.submit` are stored as an object containing your fields, under a property key matching the UUID component of the `app.id` property in your app manifest. For example, if your `app.id` is `ari:cloud:ecosystem::app/d3adb33f-2ed0-4502-82f5-54ae21ea2f72`, your issue property will have the key `d3adb33f-2ed0-4502-82f5-54ae21ea2f72`.

You can retrieve this data via REST using the [Jira issue property API](/cloud/jira/platform/rest/v3/api-group-issue-properties/#api-rest-api-3-issue-issueidorkey-properties-propertykey-get) by passing the UUID component of your `app.id` as the property key, e.g. `/rest/api/3/issue/{issueIdOrKey}/properties/d3adb33f-2ed0-4502-82f5-54ae21ea2f72`.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | If using [Custom UI](/platform/forge/custom-ui/) or modern versions of [UI Kit](/platform/forge/ui-kit/) | The key of a static `resources` entry that your module will display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | If using modern versions of [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` |  | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |
| `viewportSize` | `'small'`, `'medium'`, `'large'` or `'xlarge'` |  | The [display size](/platform/forge/manifest-reference/resources) of `resource`. Can only be set if the module is using the `resource` property. Remove this property to enable automatic resizing of the module. |

## Extension context

### UI Kit and Custom UI

Use the [useProductContext](/platform/forge/ui-kit/hooks/use-product-context/) hook to access the extension context in UI Kit or [getContext](/platform/forge/apis-reference/ui-api-bridge/view/#submit) bridge method in Custom UI.

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `portal.id` | `number` | The id of the service desk, where the module is rendered. |
| `request.typeId` | `number` | The id of the request type, where the module is rendered. |
| `location` | `string` | The full URL of the host page where this module is displayed. |

## Example

In the portal request create property panel app:

```
```
1
2
```



```
const App = () => {

  const handleEntityChange = async (data) => {
    const property = {
      key: "some-key",
      value:  data.target.value,
    };
    await view.submit({ fields: [property], isValid: true });
  };

  return (
    <>
      <Label labelFor="textfield">Project name</Label>
      <Textfield
        id="textfield"
        appearance="standard"
        onChange={handleEntityChange}
      />
    </>
  );
};
```
```

In the portal request detail app:

```
```
1
2
```



```
const App = () => {
  const context = useProductContext();
  const requestProperty = context?.extension?.request?.property;
  return ...
};
```
```
