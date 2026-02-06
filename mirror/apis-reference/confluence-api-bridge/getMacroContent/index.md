# getMacroContent

`getMacroContent` is an asynchronous function that allows your macro to retrieve the current, up-to-date [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) of the macro as seen in the editor. It returns a JSON-stringified `data` object containing the ADF of the macro. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Example

This example shows how to use `getMacroContent`.

```
1
2
3
import { getMacroContent } from '@forge/confluence-bridge';

const macroContent = await getMacroContent(); // Use macroContent as desired
```

## Response Type

The `getMacroContent` function returns an object with the following structure:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified macro [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example Response

```
1
2
3
{
    data: '{"type":"bodiedExtension","attrs":{"extensionKey":"cool-bodied-macro","extensionType":"com.atlassian.ecosystem","layout":"default","localId":"0","parameters":{"localId":"0","extensionId":"ari:cloud:ecosystem::extension/cool-bodied-macro","extensionTitle":"Cool bodied macro","forgeEnvironment":"DEVELOPMENT","render":"native"}},"content":[{"content":[{"text":"hello","type":"text"}],"type":"paragraph"}]}'
}
```

### Example response after `data` goes through JSON.parse

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
{
    "type": "bodiedExtension",
    "attrs": {
        "extensionKey": "cool-bodied-macro",
        "extensionType": "com.atlassian.ecosystem",
        "layout": "default",
        "localId": "0",
        "parameters": {
            "localId": "0",
            "extensionId": "ari:cloud:ecosystem::extension/cool-bodied-macro",
            "extensionTitle": "Cool bodied macro",
            "forgeEnvironment": "DEVELOPMENT",
            "render": "native"
        }
    },
    "content": [
        {
            "content": [
                {
                    "text": "hello",
                    "type": "text"
                }
            ],
            "type": "paragraph"
        }
    ]
}
```
