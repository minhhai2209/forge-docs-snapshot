# Horizontal Bar Chart

To add the `HorizontalBarChart` component to your app:

```
1
import { HorizontalBarChart } from '@forge/react';
```

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `colorAccessor` | `number` | `string` | No | Accessor to define the color grouping. |
| `colorPalette` | `string[]` | `{ key: string; value: string }[]` | No | Custom color palette for the chart. Can be an array of color strings (e.g., `['#0052CC', '#FF5630']`) or an array of objects with `key` and `value` properties to map specific data categories to colors (e.g., `[{ key: 'category1', value: '#0052CC' }]`). |
| `data` | `unknown[]` | Yes | Data can be one of two formats:    1. An [array of arrays](#1--array-of-arrays). 2. An [array of objects](#2--array-of-objects). |
| `height` | `number` | No | The static height of the chart in pixels. Defaults to `400`. |
| `subtitle` | `string` | No | A string value that represents the subtitle of the chart. This appears below the title. |
| `title` | `string` | No | A string value that represents the title of the chart. |
| `width` | `number` | No | The static width of the chart in pixels. If this is not specified, the width is responsive. |
| `xAccessor` | `number` | `string` | Yes | Accessor to define the x-axis values. This can be a numerical or string index. For more information on all accessors, see [Data](#data). |
| `yAccessor` | `number` | `string` | Yes | Accessor to define the y-axis values. |

## Data

Data can be one of two formats, an array of arrays or an array of objects. Both examples below will produce the same horizontal bar chart:

![Example image of a rendered grouped horizontal bar chart](https://dac-static.atlassian.com/platform/forge/ui-kit/images/horizontal-bar-chart/grouped-data-horizontal-bar-chart-example.png?_v=1.5800.1869)

### 1. Array of arrays

Each entry in the dataset is an array. These arrays require a minimum of two items to denote the x and y coordinates. Optionally, an extra item may be included to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are number indices, identified by the position within each array.

```
```
1
2
```



```
const arrayData = [
  // in this example ['x value', 'y value', 'color value']
  ['April', 5, 'Sophie'],
  ['April', 3, 'Taylor'],
  ['April', 10, 'Lee'],
  ['April', 8, 'Charli'],
  ['March', 5, 'Sophie'],
  ['March', 2, 'Taylor'],
  ['March', 7, 'Lee'],
  ['March', 1, 'Charli'],
  ['February', 17, 'Sophie'],
  ['February', 5, 'Taylor'],
  ['February', 4, 'Lee'],
  ['February', 11, 'Charli'],
  ['January', 2, 'Sophie'],
  ['January', 10, 'Taylor'],
  ['January', 1, 'Lee'],
  ['January', 8, 'Charli'],
];

export const HorizontalBarChartWithArrayDataExample = () => {
  return <HorizontalBarChart
    data={arrayData}
    xAccessor={0} // position 0 in item array
    yAccessor={1} // position 1 in item array
    colorAccessor={2} // position 2 in item array
  />;
};
```
```

### 2. Array of objects

Each entry in the dataset is an object. These objects require a minimum of two properties in the form of key-value pairs to denote the x and y coordinates. Optionally, an extra property may be included to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are string indices, identified by the key of the key-value pairs.

```
```
1
2
```



```
const objectData = [
  {
    xAxis: 'April', // x value
    value: 5, // y value
    teamMember: 'Sophie', // color value
  },
  {
    xAxis: 'April',
    value: 3,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'April',
    value: 10,
    teamMember: 'Lee',
  },
  {
    xAxis: 'April',
    value: 8,
    teamMember: 'Charli',
  },
  {
    xAxis: 'March',
    value: 5,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'March',
    value: 2,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'March',
    value: 7,
    teamMember: 'Lee',
  },
  {
    xAxis: 'March',
    value: 1,
    teamMember: 'Charli',
  },
  {
    xAxis: 'February',
    value: 17,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'February',
    value: 5,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'February',
    value: 4,
    teamMember: 'Lee',
  },
  {
    xAxis: 'February',
    value: 11,
    teamMember: 'Charli',
  },
  {
    xAxis: 'January',
    value: 2,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'January',
    value: 10,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'January',
    value: 1,
    teamMember: 'Lee',
  },
  {
    xAxis: 'January',
    value: 8,
    teamMember: 'Charli',
  },
];

export const HorizontalBarChartWithObjectDataExample = () => {
  return <HorizontalBarChart
    data={objectData}
    xAccessor={'xAxis'} // key of x value in object item
    yAccessor={'value'} // key of y value in object item
    colorAccessor={'teamMember'} // key of color value in object item
  />;
};
```
```
