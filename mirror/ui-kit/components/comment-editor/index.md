# Comment editor

This component is currently only available in Confluence and Jira modules.

To add the `CommentEditor` component to your app:

```
1
import { CommentEditor } from "@forge/react";
```

## Description

The comment editor provides a contained comment editor UI with a simple toolbar.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `defaultValue` | `JSONDocNode` | No | Sets the default editor content. |
| `features` | `Features` | No | Sets the enabled features in the editor. If not set, all editor features are enabled. See [Features](#features) for a list of features. |
| `isDisabled` | `boolean` | No | Disables the editor. |
| `onChange` | `(value?: JSONDocNode) => void` | No | The handler that is called when the content in the editor changes. |
| `onSave` | `(value?: JSONDocNode) => void` | No | Renders a Save button at the bottom of the editor. Handler is called when this button is clicked. |
| `onCancel` | `() => void` | No | Renders a Cancel button at the bottom of the editor. Handler is called when this button is clicked. |

### Features

You can use the `features` prop to enable or disable specific editor features. In the comment editor,
disabling features removes them from the toolbar, as well as stops them from being able to be used in the editor itself.
The following features are available:

| Property | Type | Description |
| --- | --- | --- |
| `blockType` | `boolean` | Enables different text types, including headings and quote blocks. |
| `textFormatting` | `boolean` | Enables different formatting, such as bold and italic. |
| `list` | `boolean` | Enables lists to be inserted. |
| `textColor` | `boolean` | Enables different colors to be applied to the text. |
| `hyperLink` | `boolean` | Enables hyperlinks when pasting links. |
| `codeBlock` | `boolean` | Enables code blocks to be inserted. |
| `insertBlock` | `boolean` | Displays the link, codeblock, and quoteblock options in the toolbar. |
| `quickInsert` | `boolean` | Allows quick insertions of a block type via the `/` shortcut. |

## Examples

### Default appearance

![Example image of comment editor](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-default.png?_v=1.5800.1785)

```
```
1
2
```



```
export const CommentEditorExample = () => {
  return <CommentEditor />;
};
```
```

### Enabling and disabling features

By default, all editor features are enabled. To enable certain features and disable the
rest, you must pass in the `features` object with the specific features you want to enable.

![Example image of comment editor with custom features](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-custom.png?_v=1.5800.1785)

```
```
1
2
```



```
export const CommentEditorWithToggledFeaturesExample = () => {
  return (
    <CommentEditor
      features={{
        blockType: true,
        textFormatting: true,
        textColor: true,
        list: true,
      }}
    />
  );
};
```
```

### Action buttons

The `onSave` prop will render a Save button for the user to interact with. Upon clicking, the value can be stored in state. `onCancel` will render a Cancel button that fires a callback.

![Example image of comment editor with save and cancel buttons](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-with-action-buttons.png?_v=1.5800.1785)

```
```
1
2
```



```
const CommentEditorWithActionButtons = () => {
  const [savedContent, setSavedContent] = useState();

  return (
    <>
      <CommentEditor
        onSave={(value) => {
          setSavedContent(value);
        }}
        onCancel={() => {
          // handle cancel
        }}
      />
    </>
  );
};
```
```

### onChange

To access the input value of the editor while it's being edited, `onChange` can be used.

![Example image of comment editor using onchange](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-actions-on-change.png?_v=1.5800.1785)

```
```
1
2
```



```
const CommentEditorWithActionButtons = () => {
  const [editorValue, setEditorValue] = useState();

  return (
    <>
      <CommentEditor onChange={(value) => setEditorValue(value)} />
      <Box paddingBlockStart="space.100">
        <Button
          onClick={() => {
            console.log(editorValue);
          }}
        >
          Submit
        </Button>
      </Box>
    </>
  );
};
```
```

### Default value

To set a default value in the editor, pass in the `defaultValue` prop. This will be the initial content within the editor.

![Example image of comment editor with default value](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-default-value.png?_v=1.5800.1785)

```
```
1
2
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

const CommentEditorWithDefaultValue = () => {
  return (
    <>
      <CommentEditor defaultValue={editorValue} />
    </>
  );
};
```
```

### Disabled editor

To disable the editor, pass in the `isDisabled` prop. This will disable all interactions with the editor.

![Example image of comment editor disabled](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-disabled.png?_v=1.5800.1785)

```
```
1
2
```



```
const CommentEditorDisabled = () => {
  return (
    <>
      <CommentEditor isDisabled />
    </>
  );
};
```
```

### Example with ADF Renderer

The `CommentEditor` can be used together with the `AdfRenderer` component to display the content of a submitted value in a read-only format. This is useful for displaying the content of the editor after it has been saved.

![Example image of comment editor with adf renderer](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-full-example-1.png?_v=1.5800.1785)
![Example image of comment editor with adf renderer](https://dac-static.atlassian.com/platform/forge/ui-kit/images/editor/editor-full-example-2.png?_v=1.5800.1785)

```
```
1
2
```



```
import { useState } from "react";
import { CommentEditor, AdfRenderer, Button, Box } from "@forge/react";

const pressableStyles = xcss({
  marginTop: "space.200",
  color: "color.text.subtle",
  fontWeight: "font.weight.bold",
  padding: "space.100",
  borderRadius: "border.radius",
  ":hover": {
    backgroundColor: "color.background.neutral.subtle.hovered",
    color: "color.text",
  },
});

export const PressableExample = () => {
  const [showEditor, setShowEditor] = useState(false);
  const [comment, setComment] = useState(undefined);
  return (
    <>
      {comment && !showEditor ? <AdfRenderer document={comment} /> : null}
      {showEditor ? (
        <CommentEditor
          defaultValue={comment}
          onSave={(content) => {
            setComment(content);
            setShowEditor(false);
          }}
          onCancel={() => setShowEditor(false)}
        />
      ) : (
        <Pressable xcss={pressableStyles} onClick={() => setShowEditor(true)}>
          {comment ? "Edit comment" : "Add comment"}
        </Pressable>
      )}
    </>
  );
};
```
```
