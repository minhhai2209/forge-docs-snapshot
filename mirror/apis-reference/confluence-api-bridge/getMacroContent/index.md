# getMacroContent

`getMacroContent` is an asynchronous function that allows your macro to retrieve the current, up-to-date [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) of the macro as seen in the editor. It returns a JSON-stringified `data` object containing the ADF of the macro. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Example

This example shows how to use `getMacroContent`.

```
1import { getMacroContent } from '@forge/confluence-bridge';
2
3const macroContent = await getMacroContent(); // Use macroContent as desired
4
```

## Response Type

The `getMacroContent` function returns an object with the following structure:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified macro [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example Response

```
1{
2    data: '{"type":"bodiedExtension","attrs":{"extensionKey":"cool-bodied-macro","extensionType":"com.atlassian.ecosystem","layout":"default","localId":"0","parameters":{"localId":"0","extensionId":"ari:cloud:ecosystem::extension/cool-bodied-macro","extensionTitle":"Cool bodied macro","forgeEnvironment":"DEVELOPMENT","render":"native"}},"content":[{"content":[{"text":"hello","type":"text"}],"type":"paragraph"}]}'
3}
4
```

### Example response after `data` goes through JSON.parse

```
1{
2    "type": "bodiedExtension",
3    "attrs": {
4        "extensionKey": "cool-bodied-macro",
5        "extensionType": "com.atlassian.ecosystem",
6        "layout": "default",
7        "localId": "0",
8        "parameters": {
9            "localId": "0",
10            "extensionId": "ari:cloud:ecosystem::extension/cool-bodied-macro",
11            "extensionTitle": "Cool bodied macro",
12            "forgeEnvironment": "DEVELOPMENT",
13            "render": "native"
14        }
15    },
16    "content": [
17        {
18            "content": [
19                {
20                    "text": "hello",
21                    "type": "text"
22                }
23            ],
24            "type": "paragraph"
25        }
26    ]
27}
28
```
