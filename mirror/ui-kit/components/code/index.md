# Code

To add the `Code` component to your app:

```
1import { Code } from '@forge/react';
2
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

![Example image of inline code](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code/code-inline.png?_v=1.5800.2309)

```
1const CodeDefaultExample = () => {
2  return (
3    <Text>
4      To start creating a changeset, run <Code>yarn changeset</Code>. Then
5      you'll be prompted to select packages for release.
6    </Text>
7  );
8};
9
```
