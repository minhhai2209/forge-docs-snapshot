# Code

To add the `Code` component to your app:

```
1
import { Code } from '@forge/react';
```

## Description

Code highlights short strings of code snippets inline with body text.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `string` | No | Content to be rendered in the inline code block. |

## Examples

### Inline code

Formatted code can appear in a variety of contexts, increasing the legibility and contrasting it against default paragraph text.

Use inline code when you wish to highlight a short code snippet from the surrounding default text, such as when referencing variable names.

![Example image of inline code](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code/code-inline.png?_v=1.5800.1798)

```
1
2
3
4
5
6
7
8
const CodeDefaultExample = () => {
  return (
    <Text>
      To start creating a changeset, run <Code>yarn changeset</Code>. Then
      you'll be prompted to select packages for release.
    </Text>
  );
};
```
