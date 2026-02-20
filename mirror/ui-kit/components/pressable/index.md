# Pressable

To add the `Pressable` component to your app:

```
1
import { Pressable } from "@forge/react";
```

## Description

A pressable is a primitive for building custom buttons.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `backgroundColor` | [Background color tokens](https://atlassian.design/components/tokens/all-tokens#color-background) | No | Token representing the background color with a built-in fallback value. |
| `children` | `string | ForgeElement` | No | Elements to be rendered inside the pressable component. |
| `isDisabled` | `boolean` | No | Disables the button. |
| `onClick` | `() => void` | No | Handler called on click. |
| `padding` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS shorthand for `paddingBlock` and `paddingInline` together. |
| `paddingBlock` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS shorthand `paddingBlock`. |
| `paddingBlockEnd` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS `paddingBlockEnd`. |
| `paddingBlockStart` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS `paddingBlockStart`. |
| `paddingInline` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS shorthand `paddingInline`. |
| `paddingInlineEnd` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS `paddingInlineEnd`. |
| `paddingInlineStart` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | Tokens representing CSS `paddingInlineStart`. |
| `xcss` | `XCSSProp` | No | Applies a subset of permitted styles using Atlassian Design System tokens. For a list of supported style properties on this component, see [XCSS](/platform/forge/ui-kit/components/xcss). |

## Examples

### Default

Pressable is unstyled by default, aside from basic focus styles.

![Example image of an unstyled pressable](https://dac-static.atlassian.com/platform/forge/ui-kit/images/pressable/pressable-default.png?_v=1.5800.1869)

```
```
1
2
```



```
import { Pressable } from "@forge/react";

export const PressableExample = () => {
  const handleClick = () => {
    console.log("Clicked");
  };

  return <Pressable onClick={handleClick}>Pressable</Pressable>;
};
```
```

### Basic styling with XCSS

Pressable can be styled using [XCSS](/platform/forge/ui-kit/components/xcss).

Ensure that the styling indicates the interaction state using `:hover` and `:active` pseudo-classes.

![Example image of a styled pressable](https://dac-static.atlassian.com/platform/forge/ui-kit/images/pressable/pressable-basic-styling.png?_v=1.5800.1869)

```
```
1
2
```



```
import { Pressable, xcss } from "@forge/react";

const pressableStyles = xcss({
  color: "color.text.subtle",
  fontWeight: "font.weight.bold",
  borderRadius: "border.radius",

  ":hover": {
    backgroundColor: "color.background.neutral.subtle.hovered",
    color: "color.text",
  },
});

export const PressableExample = () => {
  const handleClick = () => {
    console.log("Clicked");
  };

  return (
    <Pressable
      onClick={handleClick}
      padding="space.100"
      backgroundColor="color.background.neutral.subtle"
      xcss={pressableStyles}
    >
      Edit comment
    </Pressable>
  );
};
```
```

### Advanced styling

Use a combination of XCSS and other primitives for more complex designs.

![Example image of a styled pressable](https://dac-static.atlassian.com/platform/forge/ui-kit/images/pressable/pressable-advanced-styling.png?_v=1.5800.1869)

```
```
1
2
```



```
const pressableStyles = xcss({
  minWidth: "150px",
  backgroundColor: "elevation.surface.raised",
  padding: "space.200",
  borderRadius: "border.radius",
  borderColor: "color.border",
  borderStyle: "solid",
  borderWidth: "border.width",
  ":hover": {
    backgroundColor: "color.background.neutral.subtle.hovered",
  },
  ":active": {
    backgroundColor: "color.background.neutral.subtle.pressed",
  },
});

export const PressableExample = () => {
  const handleClick = () => {
    console.log("click");
  };

  return (
    <Pressable xcss={pressableStyles} onClick={handleClick}>
      <Stack space="space.0" alignInline="start">
        <Inline space="space.100" alignBlock="center">
          <Text color="color.text.success" weight="bold" size="large">
            2
          </Text>
          <Lozenge appearance="success">on track</Lozenge>
        </Inline>
        <Text as="span" size="small" color="color.text.subtlest">
          -1 from last week
        </Text>
      </Stack>
    </Pressable>
  );
};
```
```

## Accessibility considerations

* Avoid using `isDisabled`. Disabled buttons are not reachable in the tab order and don’t receive hover, focus, or click events, making them entirely inaccessible to some people.
  Wherever possible, avoid using `isDisabled` and instead use validation or other techniques to show users how to proceed.
* Use clear labels for assistive technology. Pressable elements should always announce what action will happen once pressed, especially for elements with no visible label such as icon buttons.
