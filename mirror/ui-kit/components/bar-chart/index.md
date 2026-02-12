# Bar chart

To add the `BarChart` component to your app:

```
1
import { BarChart } from '@forge/react';
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

Data can be one of two formats, an array of arrays or an array of objects. Both examples below will produce the same bar chart:

![Example image of a rendered group bar](https://dac-static.atlassian.com/platform/forge/ui-kit/images/bar-chart/bar-chart-data.png?_v=1.5800.1846)

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
  ['Jan', 5, 'Sophie'],
  ['Jan', 10, 'Taylor'],
  ['Jan', 25, 'Lee'],
  ['Jan', 15, 'Charli'],
  ['Feb', 13, 'Sophie'],
  ['Feb', 5, 'Taylor'],
  ['Feb', 15, 'Lee'],
  ['Feb', 22, 'Charli'],
  ['Mar', 2, 'Sophie'],
  ['Mar', 15, 'Taylor'],
  ['Mar', 4, 'Lee'],
  ['Mar', 18, 'Charli'],
  ['Apr', 10, 'Sophie'],
  ['Apr', 30, 'Taylor'],
  ['Apr', 5, 'Lee'],
  ['Apr', 8, 'Charli'],
];

export const BarChartWithArrayDataExample = () => {
  return <BarChart 
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

For this data format, the `xAccessor` and `yAccessor` are string indices, identified by the key of the key-value pairs.

```
```
1
2
```



```
const objectData = [
  {
    xAxis: 'Jan', // x value
    value: 5, // y value
    teamMember: 'Sophie', // color value
  },
  {
    xAxis: 'Jan',
    value: 1,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'Jan',
    value: 22,
    teamMember: 'Lee',
  },
  {
    xAxis: 'Jan',
    value: 6,
    teamMember: 'Charli',
  },
  {
    xAxis: 'Feb',
    value: 13,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'Feb',
    value: 3,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'Feb',
    value: 10,
    teamMember: 'Lee',
  },
  {
    xAxis: 'Feb',
    value: 3,
    teamMember: 'Charli',
  },
  {
    xAxis: 'Mar',
    value: 1,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'Mar',
    value: 5,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'Mar',
    value: 4,
    teamMember: 'Lee',
  },
  {
    xAxis: 'Mar',
    value: 12,
    teamMember: 'Charli',
  },
  {
    xAxis: 'Apr',
    value: 6,
    teamMember: 'Sophie',
  },
  {
    xAxis: 'Apr',
    value: 13,
    teamMember: 'Taylor',
  },
  {
    xAxis: 'Apr',
    value: 33,
    teamMember: 'Horse',
  },
  {
    xAxis: 'Apr',
    value: 1,
    teamMember: 'Charli',
  },
];
export const BarChartWithObjectDataExample = () => {
  return <BarChart 
    data={objectData} 
    xAccessor={"xAxis"} // key of x value in object item
    yAccessor={"value"} // key of y value in object item
    colorAccessor={"teamMember"} // key of color value in object item
  />;
};
```
```
