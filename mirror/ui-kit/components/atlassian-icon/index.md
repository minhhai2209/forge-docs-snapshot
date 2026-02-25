# Atlassian icon (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

To add the `AtlassianIcon` component to your app:

```
1
import { AtlassianIcon } from "@forge/react";
```

## Description

An Atlassian icon is a visual representation of Atlassian object types, such as blogs, epics, and work items.

Compared to the standard [Icon](/platform/forge/ui-kit/components/icon) component, `AtlassianIcon` has fixed color, size, and styling options. This keeps Atlassian object types consistent across the platform and aligned with Atlassian Design System (ADS) specifications. Because `AtlassianIcon` stays in sync with ADS, any changes to icon styling in the design system are reflected in your app automatically.

Use `AtlassianIcon` for Atlassian object types such as Confluence pages or Jira work items. For your own custom icons, use the [Icon](/platform/forge/ui-kit/components/icon/) component instead.

### Atlassian icon types

The following image shows some of the icon types available with the `AtlassianIcon` UI Kit component.
For the full list of object types and usage guidelines, see the [Atlassian Design System](https://atlassian.design/components/object) object component.

![Grid of available Atlassian icon types with labels](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-icon/atlassian-icon-examples.png?_v=1.5800.1877)

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `glyph` | `AtlassianIconType` | Yes | The Atlassian icon type to display. Color is applied automatically based on the type. |
| `label` | `string` | No | The label for the Atlassian icon. If the icon is decorative, use an empty string. Defaults to a human-readable version of the icon type (for example, "Task" for a task icon). |
| `size` | `'small' | 'medium'` | No | The size of the Atlassian icon: `small` (12px) or `medium` (16px). Defaults to `medium`. |

## Examples

### Default

The default appearance of an Atlassian icon with medium size.

![Example image of default AtlassianIcon](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-icon/atlassian-icon-default.png?_v=1.5800.1877)

```
```
1
2
```



```
const AtlassianIconDefault = () => {
  return <AtlassianIcon glyph="story" label="story icon" />;
};
```
```

### Size

Atlassian icons can be displayed in two sizes: small (12px) and medium (16px). The medium size is the default.

![Example image of AtlassianIcon sizes](https://dac-static.atlassian.com/platform/forge/ui-kit/images/atlassian-icon/atlassian-icon-size.png?_v=1.5800.1877)

```
```
1
2
```



```
const AtlassianIconSize = () => {
  return (
    <>
      <AtlassianIcon glyph="task" label="small task icon" size="small" />
      <AtlassianIcon glyph="task" label="default medium task icon" />
    </>
  );
};
```
```

### Atlassian icons in tiles

You cannot use an `AtlassianIcon` component with the standard [Tile](/platform/forge/ui-kit/components/tile) component. To display Atlassian icons in tiles, you must use the [Atlassian tile](/platform/forge/ui-kit/components/atlassian-tile) component instead. This keeps Atlassian icon and tile styling consistent with the Atlassian Design System.

For tiles with custom or non-Atlassian icons, use the [Tile](/platform/forge/ui-kit/components/tile) component with the standard [Icon](/platform/forge/ui-kit/components/icon/) component.

## Accessibility considerations

When using the `AtlassianIcon` component, we recommend keeping the following accessibility considerations in mind:

### Provide meaningful labels

Always provide a meaningful `label` prop that describes the content type the Atlassian icon represents. This ensures screen readers can properly announce the icon to users. If the icon is purely decorative and doesn't convey meaningful information, set the `label` to an empty string.
