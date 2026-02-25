# Inline

To add the `Inline` component to your app:

```
1
import { Inline } from '@forge/react';
```

## Description

An inline manages the horizontal layout of direct children using flexbox.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `alignBlock` | `"start" | "center" | "end" | "baseline" | "stretch"` | No | Used to align children along the main axis. |
| `alignInline` | `"start" | "center" | "end" | "stretch"` | No | Used to align children along the cross axis. |
| `grow` | `"hug" | "fill"` | No | Used to set whether the container should grow to fill the available space. |
| `spread` | `"space-between"` | No | Used to distribute the children along the main axis. |
| `space` | `"space.0" | "space.025" | "space.050" | "space.075" | "space.100" | "space.150" | "space.200" | "space.300" | "space.400" | "space.500" | "space.600" | "space.800" | "space.1000"` | No | Represents the space between each child. |
| `shouldWrap` | `boolean` | No | Used to set whether children are forced onto one line or will wrap onto multiple lines. |
| `separator` | `string` | No | Renders a separator string between each child. |
| `rowSpace` | `"space.0" | "space.025" | "space.050" | "space.075" | "space.100" | "space.150" | "space.200" | "space.300" | "space.400" | "space.500" | "space.600" | "space.800" | "space.1000"` | No | Represents the space between rows when content wraps. Used to override the space value in between rows. |

## Examples

The following example uses this `ExampleBox` component in their code blocks.

```
```
1
2
```



```
const ExampleBox = () => {
  return (
    <Box
      xcss={{
        backgroundColor: 'color.background.discovery',
        borderRadius: 'border.radius',
        borderStyle: 'solid',
        borderWidth: 'border.width',
        borderColor: 'color.border.discovery',
        padding: 'space.200'
      }}
    />
  )
}
```
```

### Basic

Use an inline component to configure the layout of a group of elements horizontally. Use the given props to configure display behavior using design tokens, as shown in the more complex examples below.

![Example image of a rendered basic inline](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-basic.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineExample = () => {
  return (
    <Inline>
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Space

Control the spacing between items with the `space` prop.

![Example image of a rendered inline space](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-space.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineSpaceExample = () => {
  return (
    <Inline space="space.200">
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Row space

When content is set to wrap, the `space` prop applies equal spacing between rows. For a different space value between rows use the `rowSpace` prop.

![Example image of a rendered inline row space](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-row-space.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineRowSpaceExample = () => {
  return (
    <Box xcss={{ width: "200px" }}>
      <Inline space="space.100" rowSpace="space.300" shouldWrap>
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
      </Inline>
    </Box>
  )
}
```
```

### Block alignment

To control the alignment of items you can use the `alignBlock` props which control alignment in the vertical axis respectively.

![Example image of a rendered block alignment](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-align-block.png?_v=1.5800.1877)

```
```
1
2
```



```
const LongBox=  () => {
  return (    
    <Box
      xcss={{
        backgroundColor: 'color.background.discovery',
        borderRadius: 'border.radius',
        borderStyle: 'solid',
        borderWidth: 'border.width',
        borderColor: 'color.border.discovery',
        padding: 'space.200',
        height: '80px'
      }}
    />
)}

const InlineStartBlock = () => {
  return (
    <Inline space="space.050" alignBlock="start">
      <ExampleBox />
      <ExampleBox />
      <LongBox/>
    </Inline>
  );
}

const InlineCenterBlock = () => {
  return (
    <Inline space="space.050" alignBlock="center">
      <LongBox/>
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}

const InlineEndBlock = () => {
  return (
    <Inline space="space.050" alignBlock="end">
      <LongBox/>
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}

const InlineBaselineBlock = () => {
  return (
    <Box xcss={{height: '100px'}}>
      <Inline space="space.050" alignBlock="baseline">
        <LongBox/>
        <ExampleBox />
        <ExampleBox />
      </Inline>
    </Box>
  );
}

const InlineStretchBlock = () => {
  return (
    <Inline space="space.050" alignBlock="stretch">
      <LongBox/>
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Inline alignment

To control the alignment of items you can use the `alignInline` props which control alignment in the horizontal axis.

![Example image of a rendered inline inline alignment](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-align-inline.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineStartInline = () => {
  return (
    <Inline space="space.050" alignInline="start">
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}

const InlineCenterInline = () => {
  return (
    <Inline space="space.050" alignInline="center">
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}

const InlineEndInline = () => {
  return (
    <Inline space="space.050" alignInline="end">
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Spread

Elements can be set to stay together, spaced at the given value (default behavior) or spread equally in the space available.

![Example image of a rendered inline spread](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-spread.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineSpreadExample = () => {
  return (
    <Inline spread='space-between'>
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Wrap

When the number of items goes beyond the available space, use `shouldWrap` to create new rows of content.

![Example image of a rendered inline wrap](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-wrap.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineWrapExample = () => {
  return (
    <Box xcss={{ width: "200px" }}>
      <Inline space="space.100" shouldWrap>
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
        <ExampleBox />
      </Inline>
    </Box>
  );
}
```
```

### Separator

For logically related elements it's possible to specify a `separator` character value.

![Example image of a rendered inline separator](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-separator.png?_v=1.5800.1877)

```
```
1
2
```



```
const InlineSeparatorExample = () => {
  return (
    <Inline space="space.100" separator="•">
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
      <ExampleBox />
    </Inline>
  );
}
```
```

### Width control

By default an `Inline` will have its width influenced by the context where it appears. To control the width, use the grow prop with the values:

* `hug` (default) to use space only as required by its children, or
* `fill` to take all space provided by the parent element.

![Example image of inline with grow property](https://dac-static.atlassian.com/platform/forge/ui-kit/images/inline/inline-grow.png?_v=1.5800.1877)

```
```
1
2
```



```
const ExampleBox = () => {
  return (
    <Box
      xcss={{
        backgroundColor: 'color.background.discovery',
        borderRadius: 'border.radius',
        borderStyle: 'solid',
        borderWidth: 'border.width',
        borderColor: 'color.border.discovery',
        padding: 'space.200'
        // display and flexGrow style needs to be added for the 
        // `grow` prop to control the width correctly
        display: 'block',
        flexGrow: 1 
      }}
    />
  )
}


const InlineGrowExample = () => {
  return (
    <Stack alignInline="start" space="space.100">
      <Inline grow="hug">
        <ExampleBox>
          Wrapping <Code>Inline</Code> is set to <Code>grow="hug"</Code>
        </ExampleBox>
      </Inline>
      <Inline grow="fill">
        <ExampleBox>
          Wrapping <Code>Inline</Code> is set to <Code>grow="fill"</Code>
        </ExampleBox>
      </Inline>
    </Stack>
  );
}
```
```
