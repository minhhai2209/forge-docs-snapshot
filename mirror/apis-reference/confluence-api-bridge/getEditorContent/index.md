# getEditorContent

`getEditorContent` is an asynchronous function that allows your macro to retrieve the current, up-to-date [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) of the editor. It returns a JSON-stringified `data` object containing the ADF of the document. This function works only in edit modes (e.g. a Live Doc or edit mode of a Page). You can get this info from the `isEditing` property in the [extension context](/platform/forge/manifest-reference/modules/macro/#extension-context).

## Example

This example shows how to use `getEditorContent`.

```
1
2
3
import { getEditorContent } from '@forge/confluence-bridge';

const editorContent = await getEditorContent(); // Use editorContent as desired
```

## Response Type

The `getEditorContent` function returns an object with the following structure:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `string` | A stringified editor [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |

### Example Response

```
1
2
3
{
    data: '{"version":1,"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"hello world!"}]},{"type":"extension","attrs":{"extensionKey":"cool-macro","extensionType":"com.atlassian.ecosystem","parameters":{"localId":"0","extensionId":"ari:cloud:ecosystem::extension/cool-macro","extensionTitle":"Cool macro","layout":"extension","forgeEnvironment":"DEVELOPMENT","render":"native"},"text":"Cool macro","layout":"default","localId":"0"}}]}'
}
```

### Example response after `data` goes through JSON.parse

```
```
1
2
```



```
{
    "version": 1,
    "type": "doc",
    "content": [
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": "hello world!"
                }
            ]
        },
        {
            "type": "extension",
            "attrs": {
                "extensionKey": "cool-macro",
                "extensionType": "com.atlassian.ecosystem",
                "parameters": {
                    "localId": "0",
                    "extensionId": "ari:cloud:ecosystem::extension/cool-macro",
                    "extensionTitle": "Cool macro",
                    "layout": "extension",
                    "forgeEnvironment": "DEVELOPMENT",
                    "render": "native"
                },
                "layout": "default",
                "localId": "0",
                "text": "Cool macro"
            }
        }
    ]
}
```
```
