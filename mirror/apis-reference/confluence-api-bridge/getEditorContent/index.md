# getEditorContent

`getEditorContent` is an asynchronous function that allows your macro to retrieve the current, up-to-date [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) of the editor. It returns a JSON-stringified `data` object containing the ADF of the document. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Example

This example shows how to use `getEditorContent`.

```
1import { getEditorContent } from '@forge/confluence-bridge';
2
3const editorContent = await getEditorContent(); // Use editorContent as desired
4
```

## Response Type

The `getEditorContent` function returns an object with the following structure:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified editor [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example Response

```
1{
2    data: '{"version":1,"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"hello world!"}]},{"type":"extension","attrs":{"extensionKey":"cool-macro","extensionType":"com.atlassian.ecosystem","parameters":{"localId":"0","extensionId":"ari:cloud:ecosystem::extension/cool-macro","extensionTitle":"Cool macro","layout":"extension","forgeEnvironment":"DEVELOPMENT","render":"native"},"text":"Cool macro","layout":"default","localId":"0"}}]}'
3}
4
```

### Example response after `data` goes through JSON.parse

```
1{
2    "version": 1,
3    "type": "doc",
4    "content": [
5        {
6            "type": "paragraph",
7            "content": [
8                {
9                    "type": "text",
10                    "text": "hello world!"
11                }
12            ]
13        },
14        {
15            "type": "extension",
16            "attrs": {
17                "extensionKey": "cool-macro",
18                "extensionType": "com.atlassian.ecosystem",
19                "parameters": {
20                    "localId": "0",
21                    "extensionId": "ari:cloud:ecosystem::extension/cool-macro",
22                    "extensionTitle": "Cool macro",
23                    "layout": "extension",
24                    "forgeEnvironment": "DEVELOPMENT",
25                    "render": "native"
26                },
27                "layout": "default",
28                "localId": "0",
29                "text": "Cool macro"
30            }
31        }
32    ]
33}
34
```
