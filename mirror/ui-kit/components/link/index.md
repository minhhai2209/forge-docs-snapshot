# Link

To add the `Link` component to your app:

```
1
import { Link } from '@forge/react';
```

## Description

A component that displays a link. Use this component for inline links.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `href` | `string` | Yes | The prop `href` behaves like a HTML `href`. You should include `http(s)://` for full URLs. Relative paths, such as `/wiki`, are also supported. |
| `children` | `string` | Yes | The text to display for the link. |
| `openNewTab` | `boolean` | No | Whether or not the link should open in a new tab. Defaults to `false`. |

## Examples

A link component that will open the `https://atlassian.com` website in a new tab when clicked.

![Example image of rendered link](https://dac-static.atlassian.com/platform/forge/ui-kit/images/link/link-default.png?_v=1.5800.1798)

```
1
2
3
4
5
6
7
const LinkExample = () => {
  return (
    <Text>
      <Link href="https://atlassian.com">Log in</Link> to view this content
    </Text>
  );
}
```
