# Badge

To add the `Badge` component to your app:

```
1
import { Badge } from '@forge/react';
```

## Description

A badge is a visual indicator for numeric values, such as tallies and scores.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"added" | "default" | "important" | "primary" | "primaryInverted" | "removed"` | No | Affects the visual style of the badge. |
| `children` | `string | number` | Yes | The value displayed within the badge. A badge should only be used in cases where you want to represent a number. Use a lozenge for non-numeric information. |
| `max` | `number | false` | No | The maximum value to display. Defaults to 99. If the value is 100, and max is 50, "50+" will be displayed. This value should be greater than 0. If set to `false` the original value will be displayed regardless of whether it is larger than the default maximum value. |

## Examples

### Appearance

#### Default

The default form of a badge.

![Example image of a rendered default badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-default.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeDefaultExample = () => {
  return <Badge>{25}</Badge>;
};
```
```

#### Primary

Use a `primary` badge to help draw attention to new or updated information.

![Example image of a rendered primary badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-primary.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgePrimaryExample = () => {
  return <Badge appearance="primary">{25}</Badge>;
};
```
```

#### Primary inverted

Use a `primaryInverted` badge when high contrast against a darker background color is needed.

![Example image of a rendered primary inverted badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-primary-inverted.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgePrimaryInvertedExample = () => {
  return <Badge appearance="primaryInverted">{25}</Badge>;
};
```
```

#### Important

Use an `important` badge to call attention to information that needs to stand out. For example, notifications in Confluence.

![Example image of a rendered important badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-important.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeImportantExample = ()=> {
  return <Badge appearance="important">{25}</Badge>;
};
```
```

#### Added

Use an `added` badge to indicate when an item has been added. For example, in a changelog or activity feed.

![Example image of a rendered added badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-added.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeAddedExample = () => {
  return <Badge appearance="added">{25}</Badge>;
};
```
```

#### Removed

Use a `removed` badge to indicate when an item has been removed. For example, in a changelog or activity feed.

![Example image of a rendered removed badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-removed.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeRemovedExample = () => {
  return <Badge appearance="removed">{25}</Badge>;
};
```
```

### Max value

#### Default

Use the max prop to cap the value of a badge. When the value to display is greater than the max prop, a + will be appended. The default max value of a badge is 99.

![Example image of a rendered default max badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-maxvalue-default.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeMaxDefault = () => {
  return (
    <Badge appearance="primary">
      {100}
    </Badge>
  );
};
```
```

#### Max value enabled

![Example image of a rendered capped badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-maxvalue-enabled.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeMaxValueEnabled = () => {
  return (
    <Badge appearance="primary" max={500}>
      {1000}
    </Badge>
  );
};
```
```

#### Max value disabled

![Example image of a rendered capped badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-maxvalue-disabled.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeMaxValueDisabled = () => {
  return (
    <Badge appearance="primary" max={false}>
      {1000}
    </Badge>
  );
};
```
```

### Badge with a Text component

![Example image of a rendered badge with text](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-textcomponent-example.png?_v=1.5800.1877)

```
```
1
2
```



```
const BadgeWithText = () => {
  return (
    <Inline alignBlock="center" space="space.100">
      <Text>New issues</Text>
      <Badge appearance="added" max={25}>30</Badge>
    </Inline>
  );
};
```
```

## Accessibility considerations

When using the `Badge` component, we recommend keeping the following accessibility considerations in mind:

* Use badges in conjunction with a single item or label to avoid ambiguity around which item is being quantified.
* Don't rely on color alone to signify whether a value is positive or negative.
* Number values are grouped and separated differently in many countries and regions. Use your Atlassian app's internationalization library, or the browser's internationalization with the user's locale set correctly so that number values show in a familiar format.
