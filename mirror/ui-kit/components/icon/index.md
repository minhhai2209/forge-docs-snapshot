# Icon

# Atlassian has migrated to new icons

In alignment with Atlassian's visual refresh, some icons from UI Kit have been deprecated and new icons have
been added. The `primaryColor` and `secondaryColor` properties have been deprecated. The `large` size in the `size` property has also been deprecated. [Deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) icons and properties will be removed on December 22, 2025.

See [Atlassian Design System legacy icons](https://atlassian.design/components/icon/icon-legacy/icon-explorer)
for a list of deprecated icons, and which icons to migrate to.

To add the `Icon` component to your app:

```
1
import { Icon } from "@forge/react";
```

## Description

An icon is a visual representation of a command, device, directory, or common action.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `glyph` | `"attachment" | "image" | "office-building" | "stopwatch" | ...` | Yes | Name of the icon to be rendered. |
| `label` | `string` | Yes | Text used to describe what the icon is in context. A label is needed when there is no pairing visible text next to the icon. An empty string marks the icon as presentation only. |
| `color` | `string` | No | Color of the icon. Inherits the current font color by default. |
| `primaryColor` | `string` | No | The `primaryColor` prop has been [deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) and will be removed on December 22, 2025. Please use the `color` prop instead. |
| `secondaryColor` | `string` | No | The `secondaryColor` prop has been [deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) and will be removed on December 22, 2025. Please use the [Box](/platform/forge/ui-kit/components/box) component with `backgroundColor` instead. |
| `size` | `"small" | "medium"` | No | The `"large"` size has been [deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) and will be removed on December 22, 2025.  There are two icon sizes – `small` (16px) and `medium` (24px). This pixel size refers to the canvas the icon sits on, not the size of the icon shape itself. |

## Examples

### Default

Valid icons can be found in the [Atlassian Design System Icon Library](https://atlassian.design/components/icon/icon-explorer).

Extract the `core` segment of the icon's import to get the valid icon name to pass into `glyph`. For example, the icon name for `icon/core/thumbs-up` is `thumbs-up`.

![Example image of default icon](https://dac-static.atlassian.com/platform/forge/ui-kit/images/icon/icon-default.png?_v=1.5800.1790)

```
```
1
2
```



```
const IconDefault = () => {
  return (
    <Inline space="space.100">
      <Icon glyph="image" />
      <Icon glyph="attachment" />
      <Icon glyph="office-building" />
      <Icon glyph="stopwatch" />
    </Inline>
  );
};
```
```

### Label

If an icon doesn’t have an existing text label or accessible text, provide a clear label with the label prop.

If an icon is associated with a button or element that has a text label, you don't need to provide alternative text. The `label` of the button or element clarifies the icon's meaning.

![Example image of icon with label](https://dac-static.atlassian.com/platform/forge/ui-kit/images/icon/icon-label.png?_v=1.5800.1790)

```
```
1
2
```



```
const IconUtility = () => {
  return (
    <Inline space="space.1000">

      <Stack space="space.200" alignBlock="center">

        <Heading as="h5">Icons with labels:</Heading>
        
        <Inline space="space.100" alignBlock="center">
          <Icon glyph="epic" color="color.icon.accent.purple" label="Issue type: Epic" />
          <Strong>Beta release</Strong>
        </Inline>

        <Inline space="space.100" alignBlock="center">
          <Icon glyph="warning" color="color.icon.warning" label="warning" />
          <Strong color="color.text.warning">Saving was interrupted</Strong>
        </Inline>

      </Stack>

      <Stack space="space.200" alignBlock="center">

        <Heading as="h5">Icons without labels:</Heading>

        <Inline space="space.100" alignBlock="center">
          <Icon glyph="edit" color="color.text" />
          <Text color="color.text">Last edited: yesterday</Text>
        </Inline>

        <Inline space="space.100" alignBlock="center">
          <Icon glyph="merge-success" color="color.text.success" />
          <Text color="color.text.success">Merged</Text>
        </Inline>
        
      </Stack>

    </Inline>
  );
};
```
```

### Color

The `primaryColor` and `secondaryColor` props are now [deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) and will be removed on December 22, 2025. Please use the `color` prop instead.

The color of the icon can be declared using the `color` property. The icon's color inherits the current font color by default.

Allowed `color` values include any design token with the prefix `color.` found under [Atlassian Design System design tokens](https://atlassian.design/components/tokens/all-tokens).

![Example image of color icon](https://dac-static.atlassian.com/platform/forge/ui-kit/images/icon/icon-color.png?_v=1.5800.1790)

```
```
1
2
```



```
const IconColor = () => {
  return (
    <Inline space="space.100">
      <Icon glyph="whiteboard" color="color.icon.accent.teal" />
      <Icon glyph="error" color="color.icon.danger" />
      <Icon glyph="link" color="color.link" />
    </Inline>
  );
};
```
```

### Size

The `large` size is now [deprecated](https://developer.atlassian.com/changelog/#CHANGE-2647) and will be removed on December 22, 2025.

#### Small

![Example image of small icon](https://dac-static.atlassian.com/platform/forge/ui-kit/images/icon/icon-sizing-small.png?_v=1.5800.1790)

```
```
1
2
```



```
const IconSmall = () => {
  return (
    <Icon glyph="like" label="Like" size="small" />
  );
};
```
```

#### Medium (default)

![Example image of medium icon](https://dac-static.atlassian.com/platform/forge/ui-kit/images/icon/icon-sizing-medium.png?_v=1.5800.1790)

```
```
1
2
```



```
const IconMedium = () => {
  return (
    <Icon glyph="like" label="Like" size="medium" />
  );
};
```
```
