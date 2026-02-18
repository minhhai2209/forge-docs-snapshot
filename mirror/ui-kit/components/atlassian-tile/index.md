# Atlassian tile (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

To add the `AtlassianTile` component to your app:

```
1
import { AtlassianTile } from "@forge/react";
```

## Description

The `AtlassianTile` component displays tiles for Atlassian object types, such as stories, tasks, epics, and blogs.

Compared to the standard [Tile](/platform/forge/ui-kit/components/tile) component, `AtlassianTile` has fixed color, size, and styling options. This keeps Atlassian object types consistent across the platform and aligned with Atlassian Design System (ADS) specifications. Because `AtlassianTile` stays in sync with ADS, any changes to tile styling in the design system are reflected in your app automatically.

Use `AtlassianTile` for Atlassian object types such as Confluence pages or Jira work items. For your own custom tiles, use the [Tile](/platform/forge/ui-kit/components/tile) and [Icon](/platform/forge/ui-kit/components/icon) components instead.

### Atlassian tile types

The following image shows some of the available Atlassian tile types. For the full list of Atlassian tile types and usage guidelines, see the [Atlassian Design System](https://atlassian.design/components/object/object-tile) object tile component.

![Grid of available Atlassian tile types with labels](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-tile/atlassian-tile-examples.png?_v=1.5800.1858)

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `glyph` | `AtlassianTileType` | Yes | The Atlassian tile type to display. Color is applied automatically based on the type. |
| `label` | `string` | No | The label for the Atlassian tile. If the icon is decorative, use an empty string. Defaults to a human-readable version of the icon type (for example, "Story" for a story icon). |
| `size` | `'xsmall' | 'small' | 'medium' | 'large' | 'xlarge'` | No | The size of the tile. Defaults to `medium`.   * `xsmall`: 20px * `small`: 24px * `medium`: 32px * `large`: 40px * `xlarge`: 48px |
| `isBold` | `boolean` | No | Whether the Atlassian tile should be bold in appearance. Defaults to `false`. |

## Examples

### Default

The default appearance of an Atlassian tile with the default size (medium).

![Example image of default AtlassianTile](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-tile/atlassian-tile-default.png?_v=1.5800.1858)

```
```
1
2
```



```
const AtlassianTileDefault = () => {
  return <AtlassianTile glyph="whiteboard" label="whiteboard Atlassian tile" />;
};
```
```

### Size

Atlassian tiles can be displayed in five sizes: xsmall (20px), small (24px), medium (32px), large (40px), and xlarge (48px). The medium size is the default.

![Example image of Atlassian tile sizes](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-tile/atlassian-tile-size.png?_v=1.5800.1858)

```
```
1
2
```



```
const AtlassianTileSize = () => {
  return (
    <>
      <AtlassianTile glyph="story" size="xsmall" label="Extra small story tile (20px)" />
      <AtlassianTile glyph="story" size="small" label="Small story tile (24px)" />
      <AtlassianTile glyph="story" size="medium" label="Medium story tile (32px)" />
      <AtlassianTile glyph="story" size="large" label="Large story tile (40px)" />
      <AtlassianTile glyph="story" size="xlarge" label="Extra large story tile (48px)" />
    </>
  );
};
```
```

### Bold appearance

Atlassian tiles can be displayed with a bold appearance using the `isBold` prop. When `isBold` is `true`, the tile uses a darker icon color and a bright background color.

![Example image of Atlassian tiles with bold appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-tile/atlassian-tile-bold.png?_v=1.5800.1858)

```
```
1
2
```



```
const AtlassianTileBold = () => {
  return (
    <>
      <AtlassianTile glyph="story" label="story tile" isBold={true} />
      <AtlassianTile glyph="blog" label="blog tile" isBold={true} />
      <AtlassianTile glyph="bug" label="bug tile" isBold={true} />
      <AtlassianTile glyph="page-live-doc" label="page live doc tile" isBold={true} />
      <AtlassianTile glyph="changes" label="changes tile" isBold={true} />
    </>
  );
};
```
```

### Atlassian icons in tiles

Use `AtlassianTile` when you need Atlassian icons in tiles. The [Atlassian icon](/platform/forge/ui-kit/components/atlassian-icon) component is not supported with the [Tile](/platform/forge/ui-kit/components/tile) component. This keeps icon and tile styling consistent with the Atlassian Design System.

For tiles with custom or non-Atlassian icons, use the [Tile](/platform/forge/ui-kit/components/tile) component with the standard [Icon](/platform/forge/ui-kit/components/icon) component.

See the [Atlassian icon](/platform/forge/ui-kit/components/atlassian-icon) component for Atlassian icons without tiles.

## Accessibility considerations

When using the `AtlassianTile` component, we recommend keeping the following accessibility considerations in mind:

### Provide meaningful labels

Always provide a meaningful `label` prop that describes the content type the Atlassian tile represents. This ensures screen readers can properly announce the tile to users. If the tile is purely decorative and doesn't convey meaningful information, use an empty string for the `label`.
