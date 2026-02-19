# Horizontal Stack Bar chart

To add the `HorizontalStackBarChart` component to your app:

```
1
import { HorizontalStackBarChart } from '@forge/react';
```

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `colorAccessor` | `number` | `string` | Yes | Accessor to define the color grouping. |
| `colorPalette` | `string[]` | `{ key: string; value: string }[]` | No | Custom color palette for the chart. Can be an array of color strings (e.g., `['#0052CC', '#FF5630']`) or an array of objects with `key` and `value` properties to map specific data categories to colors (e.g., `[{ key: 'category1', value: '#0052CC' }]`). |
| `data` | `unknown[]` | Yes | Data can be one of two formats:    1. An [array of arrays](#1--array-of-arrays). 2. An [array of objects](#2--array-of-objects). |
| `height` | `number` | No | The static height of the chart in pixels. Defaults to `400`. |
| `subtitle` | `string` | No | A string value that represents the subtitle of the chart. This appears below the title. |
| `title` | `string` | No | A string value that represents the title of the chart. |
| `width` | `number` | No | The static width of the chart in pixels. If this is not specified, the width is responsive. |
| `xAccessor` | `number` | `string` | Yes | Accessor to define the x-axis values. This can be a numerical or string index. For more information on all accessors, see [Data](#data). |
| `yAccessor` | `number` | `string` | Yes | Accessor to define the y-axis values. |

## Data

Data can be one of two formats, an array of arrays or an array of objects. Both examples below will produce the same horizontal stack bar chart:

![Example image of a rendered horizontal stack bar chart](https://dac-static.atlassian.com/platform/forge/ui-kit/images/horizontal-stack-bar-chart/horizontal-stack-bar-chart-data.png?_v=1.5800.1863)

### 1. Array of arrays

Each entry in the dataset is an array. These arrays require three items to denote the x and y coordinates and to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are number indices, identified by the position within each array.

```
```
1
2
```



```
const arrayData = [
  // in this example ['x value', 'y value', 'color value']
  ["April", 9, "Done"],
  ["April", 3, "To do"],
  ["April", 2, "In progress"],
  ["April", 3, "Blocked"],
  ["March", 3, "Done"],
  ["March", 4, "To do"],
  ["March", 2, "In progress"],
  ["March", 4, "Blocked"],
  ["February", 4, "Done"],
  ["February", 6, "To do"],
  ["February", 7, "In progress"],
  ["February", 3, "Blocked"],
  ["January", 6, "Done"],
  ["January", 3, "To do"],
  ["January", 2, "In progress"],
  ["January", 4, "Blocked"],
];

export const HorizontalStackBarChartWithArrayDataExample = () => {
  return <HorizontalStackBarChart
    data={arrayData}
    xAccessor={0} // position 0 in item array
    yAccessor={1} // position 1 in item array
    colorAccessor={2} // position 2 in item array
  />;
};
```
```

### 2. Array of objects

Each entry in the dataset is an object. These objects require three properties in the form of key-value pairs to denote the x and y coordinates and to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are string indices, identified by the key of the key-value pairs.

```
```
1
2
```



```
const objectData = [
  {
    xAxis: "April", // x value
    value: 9, // y value
    status: "Done", // color value
  },
  {
    xAxis: "April",
    value: 3,
    status: "To do",
  },
  {
    xAxis: "April",
    value: 2,
    status: "In progress",
  },
  {
    xAxis: "April",
    value: 3,
    status: "Blocked",
  },
  {
    xAxis: "March",
    value: 3,
    status: "Done",
  },
  {
    xAxis: "March",
    value: 4,
    status: "To do",
  },
  {
    xAxis: "March",
    value: 2,
    status: "In progress",
  },
  {
    xAxis: "March",
    value: 4,
    status: "Blocked",
  },
  {
    xAxis: "Ferbruary",
    value: 4,
    status: "Done",
  },
  {
    xAxis: "Ferbruary",
    value: 6,
    status: "To do",
  },
  {
    xAxis: "Ferbruary",
    value: 7,
    status: "In progress",
  },
  {
    xAxis: "Ferbruary",
    value: 3,
    status: "Blocked",
  },
  {
    xAxis: "January",
    value: 6,
    status: "Done",
  },
  {
    xAxis: "January",
    value: 3,
    status: "To do",
  },
  {
    xAxis: "January",
    value: 2,
    status: "In progress",
  },
  {
    xAxis: "January",
    value: 4,
    status: "Blocked",
  },
];
export const HorizontalStackBarChartWithObjectDataExample = () => {
  return <HorizontalStackBarChart
    data={objectData}
    xAccessor={"xAxis"} // key of x value in object item
    yAccessor={"value"} // key of y value in object item
    colorAccessor={"status"} // key of color value in object item
  />;
};
```
```
