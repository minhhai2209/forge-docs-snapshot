# XCSS

With components support `xcss` prop, `xcss` utility function should be used to
wrap the XCSS style definition before passing it to the component.

```
1
import { xcss } from "@forge/react";
```

## Description

XCSS is a styling API that utilizes [Atlassian Design Tokens](https://atlassian.design/tokens/) to style primitive components safely with tokens.

### Key features

* XCSS restricts nested selectors completely from usage.
* Pseudo class / element selectors are supported currently.
* The majority of style attributes will be restricted to Atlassian Design Token based values to ensure safety and consistency.

### Supported components

XCSS support is currently available on the [Box](/platform/forge/ui-kit/components/box/) and [Pressable](/platform/forge/ui-kit/components/pressable/) components.

### Supported properties

## Props

### Border

#### Border color

Border color related properties accept
[border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border).
Learn about applying the right
[color tokens](https://atlassian.design/foundations/color-new#color-roles) by understanding color roles
and referring to [accessibility guidelines](https://atlassian.design/foundations/accessibility/#colors).

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `borderColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) e.g. `'color.border'` | Set the color of the borders |
| `borderBlockColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of the logical block borders of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderBlockEndColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of the logical block-end border of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderBlockStartColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of the logical block-start border of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderBottomColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of an element's bottom border. |
| `borderInlineColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set color of the logical inline borders of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderInlineEndColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of the logical inline-end border of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderInlineStartColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of the logical inline start border of an element, which maps to a physical border color depending on the element's writing mode, directionality, and text orientation. |
| `borderLeftColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of an element’s left border. |
| `borderRightColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of an element’s right border. |
| `borderTopColor` | string | [Border color tokens](https://atlassian.design/components/tokens/all-tokens#color-border) | Set the color of an element’s top border. |

#### Border radius

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `borderRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set border radius of an element's side e.g. bottom-left corner. |
| `borderBottomLeftRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set border radius of an element's bottom-left corner. |
| `borderBottomRightRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set border radius of an element's bottom-right corner. |
| `borderTopLeftRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set border radius of an element's top-left corner. |
| `borderTopRightRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set border radius of an element's top-right corner. |
| `borderEndEndRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set a logical border radius on an element, which maps to a physical border radius that depends on the element's writing-mode, direction, and text-orientation. |
| `borderEndStartRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set a logical border radius on an element, which maps to a physical border radius depending on the element's writing-mode, direction, and text-orientation. |
| `borderStartEndRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set a logical border radius on an element, which maps to a physical border radius depending on the element's writing-mode, direction, and text-orientation. |
| `borderStartStartRadius` | string | [Border radius tokens](https://atlassian.design/components/tokens/all-tokens#radius) | Set a logical border radius on an element, which maps to a physical border radius that depends on the element's writing-mode, direction, and text-orientation. |

#### Border width

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `borderWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of an element's border. |
| `borderBlockWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical block borders of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderBlockEndWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical block-end border of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderBlockStartWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical block-start border of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderBottomWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the bottom border of an element. |
| `borderInlineWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical inline borders of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderInlineEndWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical inline-end border of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderInlineStartWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the logical inline-start border of an element, which maps to a physical border width depending on the element's writing mode, directionality, and text orientation. |
| `borderLeftWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the left border of an element. |
| `borderRightWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the right border of an element. |
| `borderTopWidth` | string | [Border width tokens](https://atlassian.design/components/tokens/all-tokens#border-width) | Set the width of the top border of an element. |

#### Border style

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `borderTopStyle` | string | `'dotted' | 'dashed' | 'solid' | 'none' | 'hidden'` | Set the line style of an element's top border. |
| `borderBottomStyle` | string | `'dotted' | 'dashed' | 'solid' | 'none' | 'hidden'` | Set the line style of an element's bottom border. |
| `borderRightStyle` | string | `'dotted' | 'dashed' | 'solid' | 'none' | 'hidden'` | Set the line style of an element's right border. |
| `borderLeftStyle` | string | `'dotted' | 'dashed' | 'solid' | 'none' | 'hidden'` | Set the line style of an element's left border. |
| `borderStyle` | string | `'dotted' | 'dashed' | 'solid' | 'none' | 'hidden'` | Set the line style for all four sides of an element's border. |

### Color

The colour related properties are used to style and enhance the text and background colours of the elements.
Learn about applying the right
[color tokens](https://atlassian.design/foundations/color-new#color-roles) by understanding color roles
and referring to [accessibility guidelines](https://atlassian.design/foundations/accessibility/#colors).

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `color` | string | [Text color tokens](https://atlassian.design/components/tokens/all-tokens#color-text) e.g. `'color.text'` | Set color of children text elements inside the element. |
| `backgroundColor` | string | [Background color tokens](https://atlassian.design/components/tokens/all-tokens#color-background) e.g. `'color.background.selected'` | Set the background color of an element. |

### Typography

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `textAlign` | `string` | `'left' | 'center' | 'right' | 'justify'` | Set the horizontal alignment of the text inside an element. |

### Opacity

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `opacity` | string | [Opacity tokens](https://atlassian.design/components/tokens/all-tokens#opacity) e.g. `'opacity.disabled'` | Set the opacity of an element. |

### Shadow

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `boxShadow` | `string` | [Shadow tokens](https://atlassian.design/components/tokens/all-tokens#elevation-shadow) e.g. `'elevation.shadow.overflow'` | Set shadow around an element. |

### Size

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `width` | `string` | `'30px' | '25em' | '10%'` | Set an element's width. |
| `height` | `string` | `'30px' | '25em' | '10%'` | Set an element's height. |
| `minWidth` | `string` | `'30px' | '25em' | '10%'` | Sets the minimum width of an element. |
| `maxWidth` | `string` | `'30px' | '25em' | '10%'` | Set the maximum width of an element |
| `minHeight` | `string` | `'30px' | '25em' | '10%'` | Set the minimum height of an element. |
| `maxHeight` | `string` | `'30px' | '25em' | '10%'` | Set the maximum height of an element. |

### Layout

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `display` | `string` | `'block' | 'inline-block' | 'inline' | 'none'` | Set the display type of an element. |
| `flexGrow` | `string` | `number` | Set how much an element will grow relative to the rest of the flexible items inside the same container. |
| `overflow` | `string` | `'visible' | 'hidden' | 'scroll' | 'auto'` | Sets the desired behavior when content does not fit in a container. |

### Space

| Name | Type | Allowed values | Description |
| --- | --- | --- | --- |
| `margin` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) e.g. `'space.050'` | Set the margin area on all four sides of an element. |
| `marginBlock` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block start and end margins of an element, which maps to physical margins depending on the element's writing mode, directionality, and text orientation. |
| `marginBlockEnd` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block end margin of an element, which maps to a physical margin depending on the element's writing mode, directionality, and text orientation. |
| `marginBlockStart` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block start margin of an element, which maps to a physical margin depending on the element's writing mode, directionality, and text orientation. |
| `marginBottom` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the margin area on the bottom of an element. |
| `marginInline` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set both the logical inline start and end margins of an element, which maps to physical margins depending on the element's writing mode, directionality, and text orientation. |
| `marginInlineEnd` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical inline end margin of an element, which maps to a physical margin depending on the element's writing mode, directionality, and text orientation. |
| `marginInlineStart` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical inline start margin of an element, which maps to a physical margin depending on the element's writing mode, directionality, and text orientation. |
| `marginLeft` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the margin area on the left side of an element. |
| `marginRight` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the margin area on the right side of an element. |
| `marginTop` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the margin area on the top of an element. |
| `padding` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the padding area on all four sides of an element at once. |
| `paddingBlock` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block start and end padding of an element, which maps to physical padding properties depending on the element's writing mode, directionality, and text orientation. |
| `paddingBlockEnd` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block end padding of an element, which maps to a physical padding depending on the element's writing mode, directionality, and text orientation. |
| `paddingBlockStart` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical block start padding of an element, which maps to a physical padding depending on the element's writing mode, directionality, and text orientation. |
| `paddingBottom` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the height of the padding area on the bottom of an element. |
| `paddingInline` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical inline start and end padding of an element, which maps to physical padding properties depending on the element's writing mode, directionality, and text orientation. |
| `paddingInlineEnd` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical inline end padding of an element, which maps to a physical padding depending on the element's writing mode, directionality, and text orientation. |
| `paddingInlineStart` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the logical inline start padding of an element, which maps to a physical padding depending on the element's writing mode, directionality, and text orientation. |
| `paddingLeft` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the width of the padding area to the left of an element. |
| `paddingRight` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the width of the padding area on the right of an element. |
| `paddingTop` | string | [Space tokens](https://atlassian.design/components/tokens/all-tokens#space) | Set the height of the padding area on the top of an element. |

## Examples

### Basic

XCSS can pull together different types of interactions and UI in a safer, more composable way.

![Example of using basic xcss on box component](https://dac-static.atlassian.com/platform/forge/ui-kit/images/xcss/xcss-basic.png?_v=1.5800.1863)

```
```
1
2
```



```
import React from "react";

import { Heading, Box, Stack, xcss } from "@forge/react";

const textStyle = xcss({
  color: "color.text",
});

const cardStyle = xcss({
  backgroundColor: "color.background.accent.purple.subtlest",
  padding: "space.200",
  borderColor: "color.border.discovery",
  borderWidth: "border.width",
  borderStyle: "solid",
  borderRadius: "radius.small",
  width: "240px",
});

export const Basic = () => (
  <Box xcss={cardStyle}>
    <Stack space="space.100">
      <Heading as="h3" level="h600">
        Heading
      </Heading>
      <Box xcss={textStyle}>Description</Box>
    </Stack>
  </Box>
);
```
```

### Interactivity

To enable interactivity, use familiar selectors like `:hover`.

![Example of using xcss with hover on box component](https://dac-static.atlassian.com/platform/forge/ui-kit/images/xcss/xcss-interactivity.png?_v=1.5800.1863)

```
```
1
2
```



```
import React from "react";

import { Heading, Box, Stack, Link, xcss } from "@forge/react";

const textStyle = xcss({
  color: "color.text",
  marginBottom: "space.200",
});

const cardStyle = xcss({
  backgroundColor: "elevation.surface",
  padding: "space.200",
  borderColor: "color.border",
  borderWidth: "border.width",
  borderStyle: "solid",
  borderRadius: "radius.small",
  ":hover": {
    backgroundColor: "elevation.surface.hovered",
  },
});

const GetStartedCard = ({ header, description }) => {
  return (
    <Box xcss={cardStyle}>
      <Stack space="space.100" alignInline="start">
        <Heading as="h3" level="h600">
          {header}
        </Heading>
        <Box xcss={textStyle}>{description}</Box>
        <Link href="/">Get started</Link>
      </Stack>
    </Box>
  );
};

export const InteractivityExample = () => (
  <Inline space="space.200">
    <GetStartedCard
      header="Set up"
      description="Create a project and add tasks"
    />
    <GetStartedCard
      header="Plan project"
      description="Assign tasks and set timelines"
    />
  </Inline>
);
```
```
