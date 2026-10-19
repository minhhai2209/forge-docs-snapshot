# Badge

To add the `Badge` component to your app:

```
1import { Badge } from '@forge/react';
2
```

## Description

A badge is a visual indicator for numeric values, such as tallies and scores.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `appearance` | `"warning"` | `"success"` | `"inverse"` | `"discovery"` | `"danger"` | `"neutral"` | `"information"` | `"informationBold"` | `"successBold"` | `"dangerBold"` | `"warningBold"` | `"discoveryBold"` | No | Affects the visual style of the badge. Legacy semantic appearances are also supported for backward compatibility (`"added"` | `"removed"` | `"important"` | `"default"` | `"primary"` | `"primaryInverted"`). |
| `children` | `string | number` | Yes | The value displayed within the badge. A badge should only be used in cases where you want to represent a number. Use a lozenge for non-numeric information. |
| `max` | `number | false` | No | The maximum value to display. Defaults to 99. If the value is 100, and max is 50, "50+" will be displayed. This value should be greater than 0. If set to `false` the original value will be displayed regardless of whether it is larger than the default maximum value. |

## Examples

### Appearance

Badge supports the semantic appearance names listed in the props table. Legacy appearance names are still supported for backward compatibility, but shouldn’t be used in new code. The examples below show legacy values only to help you migrate existing usage.

#### Default

Use `neutral` for general-purpose numeric information that doesn't require semantic meaning. This is the default appearance.

**New:** `appearance="neutral"` **Legacy:** `appearance="default"` (or omit the prop)

![Example image of a rendered neutral badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-neutral.png?_v=1.5800.2390)

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
18
19
20
21
```



```
import { Badge, Stack, Text } from '@forge/react';

const BadgeNeutralExample = () => {
  return (
    <Stack space="space.100">
      <Stack space="space.050" alignInline="center">
        <Badge appearance="neutral">{8}</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="neutral"
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="default">{8}</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="default"
        </Text>
      </Stack>
    </Stack>
  );
};
```
```

#### Information

Use `information` to draw attention to new or updated information, or to highlight informative numeric data.

**New:** `appearance="information"` **Legacy:** `appearance="primary"`

![Example image of a rendered information badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-information.png?_v=1.5800.2390)

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
18
19
20
21
```



```
import { Badge, Stack, Text } from '@forge/react';

const BadgeInformationExample = () => {
  return (
    <Stack space="space.100">
      <Stack space="space.050" alignInline="center">
        <Badge appearance="information">{12}</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="information"
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="primary">{12}</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="primary"
        </Text>
      </Stack>
    </Stack>
  );
};
```
```

#### Inverse

Use `inverse` when high contrast against a darker background color is needed.

**New:** `appearance="inverse"` **Legacy:** `appearance="primaryInverted"`

![Example image of a rendered inverse badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-inverse.png?_v=1.5800.2390)

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
18
19
20
21
22
23
```



```
import { Badge, Box, Stack, Text } from '@forge/react';

const BadgeInverseExample = () => {
  return (
    <Box backgroundColor="color.background.brand.bold" padding="space.200">
      <Stack space="space.100">
        <Stack space="space.050" alignInline="center">
          <Badge appearance="inverse">{12}</Badge>
          <Text size="small" color="color.text.inverse">
            appearance="inverse"
          </Text>
        </Stack>
        <Stack space="space.050" alignInline="center">
          <Badge appearance="primaryInverted">{12}</Badge>
          <Text size="small" color="color.text.inverse">
            appearance="primaryInverted"
          </Text>
        </Stack>
      </Stack>
    </Box>
  );
};
```
```

#### Success

Use `success` to show positive values or additions. For example, when characters are added to a line of code in Bitbucket, or when displaying growth metrics.

**New:** `appearance="success"` **Legacy:** `appearance="added"`

![Example image of a rendered success badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-success.png?_v=1.5800.2390)

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
18
19
20
21
```



```
import { Badge, Stack, Text } from '@forge/react';

const BadgeSuccessExample = () => {
  return (
    <Stack space="space.100">
      <Stack space="space.050" alignInline="center">
        <Badge appearance="success">+100</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="success"
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="added">+100</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="added"
        </Text>
      </Stack>
    </Stack>
  );
};
```
```

#### Danger

Use `danger` to show negative values, removals, or critical information. For example, when characters are removed from a line of code in Bitbucket, or when displaying critical counts.

**New:** `appearance="danger"` **Legacy:** `appearance="removed"`

![Example image of a rendered danger badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-danger.png?_v=1.5800.2390)

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
18
19
20
21
```



```
import { Badge, Stack, Text } from '@forge/react';

const BadgeDangerExample = () => {
  return (
    <Stack space="space.100">
      <Stack space="space.050" alignInline="center">
        <Badge appearance="danger">-50</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="danger"
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="removed">-50</Badge>
        <Text size="small" color="color.text.subtlest">
          appearance="removed"
        </Text>
      </Stack>
    </Stack>
  );
};
```
```

#### Warning

Use `warning` to call attention to information that requires caution or awareness, such as pending actions or items requiring attention.

**New:** `appearance="warning"` (no direct legacy equivalent)

![Example image of a rendered warning badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-warning.png?_v=1.5800.2390)

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
import { Badge, Stack, Text } from '@forge/react';

const BadgeWarningExample = () => {
  return (
    <Stack space="space.050" alignInline="center">
      <Badge appearance="warning">{5}</Badge>
      <Text size="small" color="color.text.subtlest">
        appearance="warning"
      </Text>
    </Stack>
  );
};
```
```

#### Discovery

Use `discovery` to highlight new features, discoveries, or exploratory information.

**New:** `appearance="discovery"` (no direct legacy equivalent)

![Example image of a rendered discovery badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-discovery.png?_v=1.5800.2390)

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
import { Badge, Stack, Text } from '@forge/react';

const BadgeDiscoveryExample = () => {
  return (
    <Stack space="space.050" alignInline="center">
      <Badge appearance="discovery">{3}</Badge>
      <Text size="small" color="color.text.subtlest">
        appearance="discovery"
      </Text>
    </Stack>
  );
};
```
```

#### Bold appearances

Bold semantic appearances provide higher visual prominence and should be reserved for badges of high importance, such as notification counts. Five bold appearances are available: `informationBold`, `successBold`, `dangerBold`, `warningBold`, and `discoveryBold`.

![Example image of a rendered bold badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-bold.png?_v=1.5800.2390)

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
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
```



```
import { Badge, Inline, Stack, Text } from '@forge/react';

const BadgeBoldExample = () => {
  return (
    <Inline space="space.200" alignBlock="start">
      <Stack space="space.050" alignInline="center">
        <Badge appearance="informationBold">8</Badge>
        <Text size="small" color="color.text.subtlest">
          informationBold
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="successBold">8</Badge>
        <Text size="small" color="color.text.subtlest">
          successBold
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="dangerBold">8</Badge>
        <Text size="small" color="color.text.subtlest">
          dangerBold
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="warningBold">8</Badge>
        <Text size="small" color="color.text.subtlest">
          warningBold
        </Text>
      </Stack>
      <Stack space="space.050" alignInline="center">
        <Badge appearance="discoveryBold">8</Badge>
        <Text size="small" color="color.text.subtlest">
          discoveryBold
        </Text>
      </Stack>
    </Inline>
  );
};
```
```

### Max value

#### Capped number values

Use the `max` prop to cap the value of a badge. When the value to display is greater than the `max` prop, a `+` will be appended. The default `max` value of a badge is `99`.

![Example image of a rendered max value badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-maxvalue.png?_v=1.5800.2390)

```
```
1
2
3
4
5
6
```



```
import { Badge } from '@forge/react';

const BadgeMaxValue = () => {
  return <Badge max={99}>{500}</Badge>;
};
```
```

#### Unlimited values

Set the `max` prop to false to display the value as provided, without a plus symbol (`+`) appended.

![Example image of a rendered max value disabled badge](https://dac-static.atlassian.com/platform/forge/ui-kit/images/badge/badge-maxvalue-disabled.png?_v=1.5800.2390)

```
```
1
2
3
4
5
6
```



```
import { Badge } from '@forge/react';

const BadgeMaxValueDisabled = () => {
  return <Badge max={false}>{5000}</Badge>;
};
```
```

## Accessibility considerations

When using the `Badge` component, we recommend keeping the following accessibility considerations in mind:

* Use badges in conjunction with a single item or label to avoid ambiguity around which item is being quantified.
* Don't rely on color alone to signify whether a value is positive or negative.
* Number values are grouped and separated differently in many countries and regions. Use your Atlassian app's internationalization library, or the browser's internationalization with the user's locale set correctly so that number values show in a familiar format.
