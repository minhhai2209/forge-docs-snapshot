# Migrate a macro module from Connect to Forge

This page describes how to migrate Confluence content macros from Connect to Forge.

It also describes the differences between Connect and Forge custom macro data.

After migrating your Connect app's [staticContentMacro](/cloud/confluence/modules/static-content-macro/) and
[dynamicContentMacro](/cloud/confluence/modules/dynamic-content-macro/) modules to Forge [macro modules](/platform/forge/manifest-reference/modules/macro/),
the existing Connect macros saved within Confluence pages will invoke the corresponding Forge macro module, along with a migrated version of the Connect app's
stored configuration data.

## Declare the Forge macro in your manifest

The first step is to declare the Forge macro module in your Forge app's manifest.

To render existing Connect macros with your new Forge macro module, make sure the Forge macro key matches your existing Connect macro key.

# Module keys must be unique

If you have an existing Connect macro in your manifest's `connectModules` section with the same key, you must remove it before adding the corresponding Forge macro module.

A Connect macro and Forge macro cannot exist side-by-side in your manifest with the same key.

For example, if your Connect app had a macro with key `static-macro-key`, your manifest should include it in `modules.macro[].key`, like this:

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
modules:
  macro:
    - key: static-macro-key # Forge macro key - matches Connect macro key
      resource: main
      # ...
remotes:
  - key: connect
    baseUrl: https://hello-world-app.example.com
app:
  id: ari:cloud:ecosystem::app/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
  connect:
    key: my-connect-app # Target connect app key
    remote: connect
```

## Macro lifecycle

Macros created with the Connect version of your app are stored in Confluence in the Connect storage format, represented here as Atlassian Document Format.
Note that the Connect format uses an `extensionType` of `com.atlassian.confluence.macro.core`:

```
```
1
2
```



```
{
  "type": "extension",
  "attrs": {
    "extensionType": "com.atlassian.confluence.macro.core",
    "extensionKey": "static-macro-key",
    "parameters": {
      "macroParams": {
        "myConnectField": {
          "value": "some text"
        }
      }
    }
  }
}
```
```

When a user installs the Forge version of your app, the existing Connect macros are still stored in the Connect format; they are not automatically migrated.

When a user views a page with an existing Connect macro, Confluence looks for the corresponding macro with a matching key in your Forge app, and renders it.
Even though the macro hasn't been migrated to the Forge format yet, existing config parameters are provided to your Forge macro.

Only when a user edits the configuration of the macro and publishes the page does the storage format get migrated to the Forge format.
Note that the Forge format uses an `extensionType` of `com.atlassian.ecosystem`, and the `extensionKey` is now prefixed with your app ID:

```
```
1
2
```



```
{
  "type": "extension",
  "attrs": {
    "extensionType": "com.atlassian.ecosystem",
    "extensionKey": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee/static/static-macro-key",
    "parameters": {
      "guestParams": {
        "myForgeField": "some text"
      },
      "macroParams": {
        "myConnectField": {
          "value": "some text"
        }
      }
    }
  }
}
```
```

Note that the `type` of the macro (`extension` for default block layout, `bodiedExtension` for bodied, `inlineExtension` for inline), is preserved during migration,
*even if the Forge macro declares a different type* in the `layout` [parameter](/platform/forge/manifest-reference/modules/macro/#:~:text=layout).

You can revert the macro to the Connect format by restoring an older version of the Confluence page from the page history view. This can be useful during development
and testing migrating Connect macro data, covered in the next section.

## Accessing and migrating Connect macro data

The method to access data from your existing Connect macros is the same as
[accessing configuration data for a Forge app](/platform/forge/add-configuration-to-a-macro/#use-the-configuration).

The first time a user edits an existing Connect macro using Forge, all existing Connect parameters are available through the provided config object.

Then, when the user saves the macro, only the parameters explicitly declared by your Forge app are stored.
Only these parameters are available in the config object on subsequent macro edits. Any other Connect parameters will no longer be available to the Forge app.
You can think of this as a one-time migration of Connect parameters to Forge parameters.

# Explicitly save all Connect parameters you wish to keep

If your Forge macro does not save some of the Connect parameters on a user's first macro edit, they will no longer be accessible through the config object on subsequent edits.

You can revert the page to a previous version during development to access the Connect parameters again.

You can choose to use the same parameter keys in your Forge app as in your Connect app, or you can rename them.
Renaming is recommended if you have to transform the values to be compatible with your Forge app.

Classic configuration

Custom configuration

For example, if you had a parameter from your Connect app called `myConnectField`, and you create a `Textfield` component with `name="myConnectField"`, the value will be automatically populated:

```
```
1
2
```



```
import React from "react";
import { view } from "@forge/bridge";
import ForgeReconciler, { Textfield } from "@forge/react";

const Config = () => {
  const [context, setContext] = useState(undefined);

  useEffect(() => {
    view.getContext().then(setContext);
  }, []);
  const config = context?.extension.config;

  return (
    <>
      {/* Keep an existing Connect field as is.
       * This will automatically be populated with the parameter from your Connect macro, if it exists */}
      <Textfield name="myConnectField" label="My Connect Field" />
      {/* Add a new Forge field, with a transformed value from Connect, if it exists */}
      <Textfield
        name="myForgeField"
        label="My Forge Field"
        defaultValue={config?.myOldConnectField?.replace("old", "new")}
      />
    </>
  );
};
ForgeReconciler.addConfig(<Config />);
```
```

## Connect macro parameters

Connect macro parameters maintain their existing format when passed to a Forge macro module, and do not undergo any automatic conversion.

Here's some notable differences to be aware of:

* A Connect parameter represents an array as a comma-separated string, such as `VALUE1,VALUE2`.
  * If the values your Connect app stored in the array contained a literal comma (`,`) this is not automatically escaped, so special handling is needed.
  * Forge supports arrays natively, and can store this data with no special handling required.
* If the Connect macro stores the value representing the "Current Space" for the `spacekey` [parameter type](/cloud/confluence/modules/macro-input-parameter/),
  the Forge app receives the string `"currentSpace()"`, instead of the literal space key.

### Connect parameter type mapping

The below table shows how various [Connect parameter types](/cloud/confluence/modules/macro-input-parameter/) are passed to Forge macro modules.
Note that values are always passed as strings, regardless of the original type.

| Connect parameter type | Examples |
| --- | --- |
| `attachment` | * Single: `"file_name.txt"` * Multiple: `"file_name.txt,file_name.json"` |
| `boolean` |  |
| `confluence-content` | * Single: `"Page Title 1"` * Multiple: `"Page Title 1,Page Title 2"` |
| `enum` | * Single: `"OPTION_1"` * Multiple: `"OPTION_1,OPTION_2"` |
| `int` |  |
| `spacekey` | * Single: `"currentSpace()"` * Multiple: `"currentSpace(),SPACEKEY2"` |
| `url` | * `"https://example.com/test"` |
| `username` | * Single: `"5e68dltko888jugaukrgg55e"` * Multiple: `"5e68dltko888jugaukrgg55e,5d33vdjq0ilg19qyy25ik45v"` |
| `string` |  |

The below table lists some special cases, and how they can be accessed from Forge macro modules:

| Connect macro parameter | Example | Forge equivalent |
| --- | --- | --- |
| Matched [Autoconvert](/cloud/confluence/modules/autoconvert/) URL | `"https://www.example.com/converted"` | `extension.config[urlParameter]` |
| `plain-text` macro body | `"Plain text body\n\nThis is a new line"` | `extension.config.__bodyContent` |
| `rich-text` macro body | `"<h1>Rich Text Body</h1>"` | `extension.macro.body` |

## Product context parameters

Many of the [Connect context parameters](/cloud/confluence/modules/static-content-macro/#:~:text=supported%20variables) available to macros are still
accessible via [Forge product context](/platform/forge/ui-kit/hooks/use-product-context/).

The following table lists the mappings between these parameters in Connect and Forge:

| Connect context | Forge product context | Description |
| --- | --- | --- |
| `macro.id` | `extension.connectMetadata.macroId` | The unique ID of the Connect macro. Only exists for migrated Connect macros. |
| `macro.body` | Not supported | The macro body, truncated to 128 characters |
| `macro.truncated` | Not supported | True if the macro body was truncated, false if not |
| `page.id` | `extension.content.id` | The ID of the content this component appears in |
| `page.title` | Not supported. Page information can be fetched using the [Confluence API](/cloud/confluence/rest/api-group-content/#api-wiki-rest-api-content-id-get) using the content ID. | The page title |
| `page.type` | The page type |
| `page.version` | The page version |
| `space.id` | `extension.space.id` | The space ID |
| `space.key` | `extension.space.key` | The space key |
| `output.type` | `extension.isEditing` | Whether the page is in view or edit mode (formerly `display` or `preview`) |

## Limitations and differences

In this section, we cover some limitations and differences between Connect and Forge macros.

### General

* `macroId` is not available for newly created Forge macros. You can use the more generic `localId` instead.
* Forge macros are not supported in the [legacy Confluence editor](https://support.atlassian.com/confluence-cloud/docs/convert-pages-to-the-new-editor/).
  * Existing macros cannot be rendered in the legacy editor once migrated to Forge, however if they define an [`adfExport` function](/platform/forge/change-the-confluence-frontend-with-the-ui-kit/#specify-the-export-view), that static content will be shown.
  * Existing macros cannot be edited in the legacy editor once migrated to Forge. [Convert the page to the new editor](https://support.atlassian.com/confluence-cloud/docs/convert-pages-to-the-new-editor/) to be able to edit Forge macros.
  * New Forge macros cannot be created in the legacy editor.

### Macro layout

* Forge macros do not support adding plain text or [multi-bodied macros](/cloud/confluence/working-with-a-multi-bodied-macro/).
  * Reading existing `plain-text` bodies from Connect macros is supported through the `__bodyContent` key in the config object.
  * If you want to provide a similar experience to plain text macros in your Forge app, you can use a [TextArea](/platform/forge/ui-kit/components/text-area) component in your macro configuration.
* You cannot change the body type of an existing macro as part of the migration, even if the Forge macro declares a different type in the `layout` parameter.
* Forge macros can be *children* of Connect or Forge rich bodied macros, with some limitations:

### Configuration data

* If a user has not changed parameter values from the default values specified in Connect, the parameter values are not saved with the macro and will not appear in the
  migrated configuration data.
  * If you want the default parameter values set in your Forge app, set the `defaultValue` properties of your Forge fields to match the default values in your Connect app.

You can read more about the [limitations and differences when adopting Forge from Connect](/platform/adopting-forge-from-connect/limitations-and-differences/) generally.
