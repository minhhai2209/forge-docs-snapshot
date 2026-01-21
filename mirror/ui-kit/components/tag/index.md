# Tag

To add the `Tag` component to your app:

```
1
import { Tag } from "@forge/react";
```

## Description

A tag labels UI objects for quick recognition and navigation.

## Props

| `Name` | `Type` | Required | Description |
| --- | --- | --- | --- |
| `text` | `string` | Yes | Text to be displayed in the tag. |
| `href` | `string` | No | URI or path. If provided, the tag will be a link. |
| `appearance` | `"default" | "rounded"` | No | Set whether tags should be rounded. |
| `color` | `"standard" | "green" | "lime" | "blue" | "red" | "purple" | "magenta" | "grey" | "teal" |"orange" | "yellow" | "limeLight" | "orangeLight" | "magentaLight" | "greenLight" | "blueLight" | "redLight" | "purpleLight" | "greyLight" | "tealLight" | "yellowLight"` | No | The color theme to apply, setting both background and text color. Default is `standard`. |
| `elemBefore` | `Component` | No | Component to be rendered before the tag. |

## Examples

### Default

The default form of a tag, where text is required. Tags with static text can be used as a flag or as a reference to an object or attribute.

![Example image of a tag](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/tag-default.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagDefaultExample = () => {
  return (
    <Tag text="Tag" />
  );
};
```
```

### Tag link

A tag with an `href` can link to more information on the tagged item.

![Example image of a tag link](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/tag-link.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagLinkExample = () => {
  return (
    <Tag
      href="https://www.atlassian.com"
      text="Tag link"
    />
  );
};
```
```

### Removable

Once a tag has been removed, it cannot be re-rendered. Removable tags are visible in "edit" mode or in multi-select controls.

![Example image of a removable tag](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/removable-tag.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagRemovableExample = () => {
  return (
    <Tag 
      text="Removable tag" 
      removeButtonLabel="Remove" 
    />;
  );
};
```
```

### Removable link

A removable tag with an `href` can link to more information.

![Example image of a removable link tag](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/removable-link.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagRemovableLinkExample = () => {
  return (
    <Tag 
      text="Removable tag link" 
      removeButtonLabel="Remove" 
      href="/components/tag" 
    />
  );
};
```
```

### Color

The color theme for background and text.

![Example image of colored tags](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/tag-color.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagColorExample = () => {
  return (
    <TagGroup>
      <Tag text="standard Tag" color="standard" />
      <Tag text="blue Tag" color="blue" />
      <Tag text="green Tag" color="green" />
      <Tag text="teal Tag" color="teal" />
      <Tag text="purple Tag" color="purple" />
      <Tag text="red Tag" color="red" />
      <Tag text="yellow Tag" color="yellow" />
      <Tag text="orange Tag" color="orange" />
      <Tag text="magenta Tag" color="magenta" />
      <Tag text="lime Tag" color="lime" />
      <Tag text="grey Tag" color="grey" />
    </TagGroup>
  );
};
```
```

### Text max length

The maximum width for a tag is 200px. If the text within the tag exceeds this width, it will be truncated and an ellipsis (...) will be added to indicate there is more text.

![Example image of a tag](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag/tag-max-length.png?_v=1.5800.1790)

```
```
1
2
```



```
const TagTextMaxLengthExample = () => {
  return (
    <Tag
      appearance="default"
      text="Croissant tiramisu gummies"
    />
  );
};
```
```
