# updateMacroContent

`updateMacro` is an asynchronous function that allows your macro to update itself. It takes in a macro ADF parameter and returns `true` if the update succeeded and `false` if it failed. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Function Parameter

The `updateMacro` function accepts the following parameter:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified macro [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example

```
1const params = {
2  data: "<stringified_macro_adf_object>",
3};
4
```

## Example

This example shows how to use `updateMacro`.

```
1import { updateMacro } from "@forge/confluence-bridge";
2
3const newMacroADF = {
4  type: "extension",
5  attrs: {
6    extensionKey: "cool-macro",
7    extensionType: "com.atlassian.ecosystem",
8    localId: "0",
9    parameters: {
10      localId: "0",
11      extensionId: "cool-macro",
12      extensionTitle: "Cool macro",
13      layout: "extension",
14      forgeEnvironment: "DEVELOPMENT",
15      render: "native",
16    },
17    text: "Cool macro",
18  },
19};
20
21const updatedMacroADF = {
22  data: JSON.stringify(newMacroADF),
23};
24
25const updateMacroContentResult = await updateMacro(updatedMacroADF); // Returns true or false
26
```

## Response Type

The `updateMacro` function returns `true` if the update was successful and `false` otherwise.
