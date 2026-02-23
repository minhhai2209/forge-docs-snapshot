# Box

To add the `Box` component to your app:

```
1
import { Box } from '@forge/react';
```

## Description

A box is a generic container that provides managed access to design tokens.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `backgroundColor` | [Background color tokens](https://atlassian.design/components/tokens/all-tokens#color-background) | No | A token alias for background color. See: [Design tokens](https://atlassian.design/components/tokens/all-tokens) for a list of available colors. When the background color is set to a surface token, the current surface CSS variable will also be set to this value in the `Box` styles. |
| `padding` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | A shorthand for `paddingBlock` and `paddingInline` together. |
| `paddingBlock` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical block start and end padding of an element. |
| `paddingBlockEnd` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical block end padding of an element. |
| `paddingBlockStart` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical block start padding of an element. |
| `paddingInline` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical inline start and end padding of an element. |
| `paddingInlineEnd` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical inline end padding of an element. |
| `paddingInlineStart` | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | No | The logical inline start padding of an element. |
| `role` | `string` | No | Accessible role. |
| `xcss` | `XCSSProp` | No | Apply a subset of permitted styles, powered by Atlassian Design System tokens. For a list of supported style properties on this component, see [here](/platform/forge/ui-kit/components/xcss). |

## Examples

### Basic

Box is a general-purpose container that allows for controlled use of design tokens. Use the given props to configure display behavior and styling that aligns with the Atlassian Design System. Use [XCSS](/platform/forge/ui-kit/components/xcss) to style primitive components safely with tokens (and CSS for selected properties).

![Example image of a rendered basic box](https://dac-static.atlassian.com/platform/forge/ui-kit/images/box/box-basic.png?_v=1.5800.1875)

```
```
1
2
```



```
import { Box, xcss } from '@forge/react';

export default () => {
  return (
    <Box
      padding='space.400'
      backgroundColor='color.background.discovery'
    />
  );
};
```
```

### Background color

Box accepts a wide variety of background colors, referenced as semantic design tokens. For the full list of color tokens, visit the [token list](https://atlassian.design/components/tokens/all-tokens).

![Example image of rendered boxes with varying colors](https://dac-static.atlassian.com/platform/forge/ui-kit/images/box/box-color.png?_v=1.5800.1875)

```
```
1
2
```



```
export default () => {
  return (
    <>
      <Box
        padding='space.200'
        backgroundColor='color.background.discovery'
      >
        color.background.discovery
      </Box>
      <Box
        padding='space.200'
        backgroundColor='color.background.success'
      >
        color.background.success
      </Box>
      <Box
        padding='space.200'
        backgroundColor='color.background.warning'
      >
        color.background.warning
      </Box>
    </>
  );
};
```
```

### Padding

Use `padding` props to access spacing design tokens and control internal layout. The following example demonstrates how each prop works with space tokens.

![Example image of rendered boxes with varying paddings](https://dac-static.atlassian.com/platform/forge/ui-kit/images/box/box-padding.png?_v=1.5800.1875)

```
```
1
2
```



```
import { Stack, Inline, Box } from '@forge/react';

export default () => {
  <Inline space="space.300">
    <Stack space="space.100" alignInline="start">
      <Box backgroundColor="color.background.discovery">default</Box>
      <Box backgroundColor="color.background.discovery" padding="space.300">
        padding
      </Box>
    </Stack>
    <Stack space="space.100" alignInline="start">
      <Box
        backgroundColor="color.background.discovery"
        paddingInline="space.300"
      >
        paddingInline
      </Box>
      <Box
        backgroundColor="color.background.discovery"
        paddingInlineStart="space.300"
      >
        paddingInlineStart
      </Box>
      <Box
        backgroundColor="color.background.discovery"
        paddingInlineEnd="space.300"
      >
        paddingInlineEnd
      </Box>
    </Stack>
    <Stack space="space.100" alignInline="start">
      <Box
        backgroundColor="color.background.discovery"
        paddingBlock="space.300"
      >
        paddingBlock
      </Box>
      <Box
        backgroundColor="color.background.discovery"
        paddingBlockStart="space.300"
      >
        paddingBlockStart
      </Box>
      <Box
        backgroundColor="color.background.discovery"
        paddingBlockEnd="space.300"
      >
        paddingBlockEnd
      </Box>
    </Stack>
  </Inline>
};
```
```

The nomenclature used by these props follows [logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties).

### xcss

Box exposes an `xcss` prop. This prop accepts xcss function calls that contain a subset of permitted styles. Box is designed to be used in conjunction with the inline and stack components to create layouts. This example demonstrates how these can be used to create familiar components and patterns. See the dedicated [xcss](/platform/forge/ui-kit/components/xcss) documentation for the range of properties available.

![Example image of rendered boxes with varying colors](https://dac-static.atlassian.com/platform/forge/ui-kit/images/box/box-xcss.png?_v=1.5800.1875)

```
```
1
2
```



```
import { Box, Inline, Stack, Text, Heading, Lozenge, Icon, xcss } from '@forge/react';

const containerStyles = xcss({
  backgroundColor: 'elevation.surface.raised',
  boxShadow: 'elevation.shadow.raised',
  padding: 'space.200',
  borderRadius: 'border.radius',
});

export default () => {
  return (
    <Box xcss={containerStyles} >
      <Stack space="space.100">
        <Text>
          Apply Atlassian design tokens and styling through xCSS
        </Text>
        <Box>
          <Lozenge appearance="inprogress">In progress</Lozenge>
        </Box>
        <Inline alignBlock="center" space="space.050">
          <Icon glyph="emoji-atlassian" label="Atlassian logo" />
          <Strong>FRGE-224</Strong>
        </Inline>
      </Stack>
    </Box>
  );
};
```
```
