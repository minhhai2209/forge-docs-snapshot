# updateMacroContent

`updateMacroContent` is an asynchronous function that allows your macro to update itself. It takes in a macro ADF parameter and returns `true` if the update succeeded and `false` if it failed. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Function Parameter

The `updateMacroContent` function accepts the following parameter:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified macro [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example

```
1
2
3
const params = {
    data: "<stringified_macro_adf_object>"
};
```

## Example

This example shows how to use `updateMacroContent`.

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
import { updateMacroContent } from '@forge/confluence-bridge';

const newMacroADF = {
  type: "extension",
  attrs: {
    extensionKey: "cool-macro",
    extensionType: "com.atlassian.ecosystem",
    localId: "0",
    parameters: {
        "localId": "0",
        "extensionId": "cool-macro",
        "extensionTitle": "Cool macro",
        "layout": "extension",
        "forgeEnvironment": "DEVELOPMENT",
        "render": "native"
    },
    text: "Cool macro",
  },
};

const updatedMacroADF = {
  data: JSON.stringify(newMacroADF),
}

const updateMacroContentResult = await updateMacroContent(updatedMacroADF); // Returns true or false
```

## Response Type

The `updateMacroContent` function returns `true` if the update was successful and `false` otherwise.
