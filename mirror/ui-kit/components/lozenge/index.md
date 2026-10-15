# Lozenge

To add the `Lozenge` component to your app:

```
1import { Lozenge } from '@forge/react';
2
```

## Description

A lozenge is a visual indicator used to highlight an item's status for quick recognition.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"warning"` | `"success"` | `"discovery"` | `"danger"` | `"neutral"` | `"information"` | `AccentColor` | No | The appearance of the lozenge. Legacy semantic appearances are also supported (`"default"` | `"removed"` | `"inprogress"` | `"moved"` | `"new"`). |
| `children` | `string` | No | Elements to be rendered inside the lozenge. This should ideally be just a word or two. |
| `isBold` | `boolean` | No | **Deprecated.** Will be removed in a future major release. Lozenge will be bold by default. For labels and categorization, use Tag instead. |
| `maxWidth` | `string | number` | No | Max-width of lozenge container. Default to 200px. |

## Examples

### Neutral

Use `neutral` lozenges for general status without specific semantic meaning. For example: "default", "standard", "inactive", or "draft".

![Example image of a neutral lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-neutral.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeNeutralExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="neutral">Draft</Lozenge>
    <Lozenge appearance="neutral">Inactive</Lozenge>
  </Inline>
);
```
```

### Success

Use `success` lozenges to represent a constructive or positive status. For example: "available", "completed", "approved", "resolved", or "added".

![Example image of a success lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-success.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeSuccessExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="success">Completed</Lozenge>
    <Lozenge appearance="success">On track</Lozenge>
    <Lozenge appearance="success">Approved</Lozenge>
  </Inline>
);
```
```

### Warning

Use `warning` lozenges to represent a cautionary status that requires attention. For example: "pending", "needs review", "at risk", or "approaching deadline".

![Example image of a warning lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-warning.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeWarningExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="warning">At risk</Lozenge>
    <Lozenge appearance="warning">Needs review</Lozenge>
  </Inline>
);
```
```

### Danger

Use `danger` lozenges to represent a critical or problematic status. For example: "error", "declined", "failed", "blocked", or "urgent".

![Example image of a danger lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-danger.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeDangerExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="danger">Blocked</Lozenge>
    <Lozenge appearance="danger">Failed</Lozenge>
    <Lozenge appearance="danger">Overdue</Lozenge>
  </Inline>
);
```
```

### Information

Use `information` lozenges to represent informational or in-progress status. For example: "in progress", "modified", "reviewing", or "open".

![Example image of an information lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-information.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeInformationExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="information">In progress</Lozenge>
    <Lozenge appearance="information">Modified</Lozenge>
    <Lozenge appearance="information">Reviewing</Lozenge>
  </Inline>
);
```
```

### Discovery

Use `discovery` lozenges to represent new features, updates, or promotional labels. For example: "new", "beta", "premium", or "preview".

![Example image of a discovery lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-discovery.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeDiscoveryExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="discovery">New</Lozenge>
    <Lozenge appearance="discovery">Beta</Lozenge>
    <Lozenge appearance="discovery">Premium</Lozenge>
  </Inline>
);
```
```

### Accent colors

In addition to semantic colors, lozenges support accent colors. In most cases, accent colors are used for user-generated content, where customers can choose a color and the text label.

![Example image of a accent color lozenges](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-accent-colors.png?_v=1.5800.2384)

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
```



```
import { Inline, Lozenge } from '@forge/react';

const LozengeAccentColorsExample = () => (
  <Inline space="space.100">
    <Lozenge appearance="accent-red">Red</Lozenge>
    <Lozenge appearance="accent-orange">Orange</Lozenge>
    <Lozenge appearance="accent-yellow">Yellow</Lozenge>
    <Lozenge appearance="accent-lime">Lime</Lozenge>
    <Lozenge appearance="accent-green">Green</Lozenge>
    <Lozenge appearance="accent-teal">Teal</Lozenge>
    <Lozenge appearance="accent-blue">Blue</Lozenge>
    <Lozenge appearance="accent-purple">Purple</Lozenge>
    <Lozenge appearance="accent-magenta">Magenta</Lozenge>
    <Lozenge appearance="accent-gray">Gray</Lozenge>
  </Inline>
);
```
```

### Max width

When the text in the lozenge exceeds the maximum width, it will be truncated with an ellipsis. By default, the maximum width of a lozenge is 200px. You can use the `maxWidth` prop to customize the width of the lozenge.

Avoid truncation wherever possible by using shorter text in lozenges. The truncated text is not focusable or accessible.

![Example image of a default lozenge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/lozenge/lozenge-max-width.png?_v=1.5800.2384)

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
```



```
import { Lozenge, Stack } from '@forge/react';

const LozengeMaxWidthExample = () => (
  <Stack space='space.050' alignInline='start'>
    <Lozenge>
      Default max width with long text which truncates
    </Lozenge>
    <Lozenge maxWidth={100}>
      Custom max width with long text which truncates
    </Lozenge>
  </Stack>
);
```
```

## Accessibility considerations

When using the `Lozenge` component, we recommend keeping the following accessibility considerations in mind:

* Don't use color alone to signify an important state. Instead, use an accurate label. For example: for a critical status, use words like "Error" or "Warning".
* Don't use lozenges for long text. Lozenges are not focusable, so any text that gets truncated after 200 pixels (or the custom `maxWidth` value) will not be accessible.
