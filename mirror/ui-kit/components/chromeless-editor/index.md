# Chromeless editor

This component is currently only available in Confluence and Jira modules.

To add the `ChromelessEditor` component to your app:

```
1import { ChromelessEditor } from "@forge/react";
2
```

## Description

The chromeless editor is a simple text editor that does not have a toolbar. It's ideal for when you want complete control and responsibility over the editor UI, and for when you want users to interact with the input via markdown shortcuts.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `defaultValue` | `JSONDocNode` | No | Sets the default editor content. |
| `features` | `Features` | No | Sets the enabled features in the editor. If not set, all editor features are enabled. Note, for the `ChromelessEditor`, these features do not appear in a toolbar. See [Features](#features) for a list of features. |
| `isDisabled` | `boolean` | No | Disables the editor. |
| `onChange` | `(value?: JSONDocNode) => void` | No | The handler that is called when the content in the editor changes. |

### Features

You can use the `features` prop to enable or disable specific editor features. By default, all of the the following features below are enabled:

| Property | Type | Description |
| --- | --- | --- |
| `blockType` | `boolean` | Enables different heading levels and the quote block to be inserted. |
| `textFormatting` | `boolean` | Enables different formatting decorations to be applied to text, such as bold and italic. |
| `list` | `boolean` | Enables lists to be inserted. |
| `textColor` | `boolean` | Enables different colors to be applied to text. |
| `hyperLink` | `boolean` | Enables hyperlinks when pasting links. |
| `codeBlock` | `boolean` | Enables code blocks to be inserted. |
| `insertBlock` | `boolean` | Displays the link, codeblock, and quoteblock options in the toolbar. |
| `quickInsert` | `boolean` | Allows quick insertions of a block type via the `/` shortcut. |

## Examples

### Default

The default appearance of the `ChromelessEditor` component is a blank editor with no toolbar or features. It accepts a subset of the `CommentEditor` props and has the same capabilities, but does not include any of the default UI features like, the toolbar or action buttons.

![Example image of a blank editor](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/chromeless-editor.png?_v=1.5800.2303)

```
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
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
```



```
const editorValue = {
  version: 1,
  type: "doc",
  content: [
    {
      type: "heading",
      attrs: {
        level: 1,
      },
      content: [
        {
          type: "text",
          text: "Heading",
        },
      ],
    },
    {
      type: "blockquote",
      content: [
        {
          type: "paragraph",
          content: [
            {
              type: "text",
              text: "Quote block",
            },
          ],
        },
      ],
    },
    {
      type: "codeBlock",
      attrs: {
        language: "javascript",
      },
      content: [
        {
          type: "text",
          text: "const foo = 'bar'",
        },
      ],
    },
  ],
};

export const ChromelessEditorExample = () => {
  return <ChromelessEditor defaultValue={editorValue} />;
};
```
```
