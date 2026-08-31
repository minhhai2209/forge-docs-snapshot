# Line

To add the `LineChart` component to your app:

```
1import { LineChart } from '@forge/react';
2
```

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `colorAccessor` | `number` | `string` | No | Accessor to define the color grouping. |
| `colorPalette` | `string[]` | `{ key: string; value: string }[]` | No | Custom color palette for the chart. Can be an array of color strings (e.g., `['#0052CC', '#FF5630']`) or an array of objects with `key` and `value` properties to map specific data categories to colors (e.g., `[{ key: 'category1', value: '#0052CC' }]`). |
| `data` | `unknown[]` | Yes | Data can be one of two formats:    1. An [array of arrays](#1--array-of-arrays). 2. An [array of objects](#2--array-of-objects). |
| `height` | `number` | No | The static height of the chart in pixels. Defaults to `400`. |
| `hideMenu` | `boolean` | No | When true, hides the menu in the top right corner. Defaults to `false`. |
| `showBorder` | `boolean` | No | Adds a border around the chart. Defaults to `true`. |
| `subtitle` | `string` | No | A string value that represents the subtitle of the chart. This appears below the title. |
| `title` | `string` | No | A string value that represents the title of the chart. |
| `width` | `number` | No | The static width of the chart in pixels. If this is not specified, the width is responsive. |
| `xAccessor` | `number` | `string` | Yes | Accessor to define the x-axis values. This can be a numerical or string index. For more information on all accessors, see [Data](#data). |
| `yAccessor` | `number` | `string` | Yes | Accessor to define the y-axis values. |

## Data

Data can be one of two formats, an array of arrays or an array of objects. Both examples below will produce the same line chart:

![Example image of a rendered series line bar chart](https://dac-static.atlassian.com/platform/forge/ui-kit/images/line-chart/multiple-line-chart-example.png?_v=1.5800.2300)

### 1. Array of arrays

Each entry in the dataset is an array. These arrays require a minimum of two items to denote the x and y coordinates. Optionally, an extra item may be included to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are number indices, identified by the position within each array.

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
```



```
const arrayData = [
  // in this example ['x value', 'y value', 'color value']
  ['January', 10, 'Done'],
  ['January', 1, 'To do'],
  ['January', 25, 'Blocked'],
  ['January', 5, 'In progress'],
  ['February', 5, 'Done'],
  ['February', 5, 'To do'],
  ['February', 15, 'Blocked'],
  ['February', 20, 'In progress'],
  ['March', 15, 'Done'],
  ['March', 10, 'To do'],
  ['March', 25, 'Blocked'],
  ['March', 20, 'In progress'],
  ['April', 30, 'Done'],
  ['April', 20, 'To do'],
  ['April', 5, 'Blocked'],
  ['April', 10, 'In progress'],
];

export const LineChartWithArrayDataExample = () => {
  return <LineChart
    data={arrayData}
    xAccessor={0} // position 0 in item array
    yAccessor={1} // position 1 in item array
    colorAccessor={2} // position 2 in item array
  />;
}
```
```

### 2. Array of objects

Each entry in the dataset is an object. These objects require a minimum of two properties in the form of key-value pairs to denote the x and y coordinates. Optionally, an extra property may be included to indicate color grouping.

For this data format, the `xAccessor`, `yAccessor` and `colorAccessor` are string indices, identified by the key of the key-value pairs.

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
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
```



```
const objectData = [
  {
    xAxis: 'January', // x value
    value: 10, // y value
    status: 'Done', // color value
  },
  {
    xAxis: 'January',
    value: 1,
    status: 'To do',
  },
  {
    xAxis: 'January',
    value: 25,
    status: 'Blocked',
  },
  {
    xAxis: 'January',
    value: 5,
    status: 'In progress',
  },
  {
    xAxis: 'February',
    value: 5,
    status: 'Done',
  },
  {
    xAxis: 'February',
    value: 5,
    status: 'To do',
  },
  {
    xAxis: 'February',
    value: 15,
    status: 'Blocked',
  },
  {
    xAxis: 'February',
    value: 20,
    status: 'In progress',
  },
  {
    xAxis: 'March',
    value: 15,
    status: 'Done',
  },
  {
    xAxis: 'March',
    value: 10,
    status: 'To do',
  },
  {
    xAxis: 'March',
    value: 25,
    status: 'Blocked',
  },
  {
    xAxis: 'March',
    value: 20,
    status: 'In progress',
  },
  {
    xAxis: 'April',
    value: 30,
    status: 'Done',
  },
  {
    xAxis: 'April',
    value: 20,
    status: 'To do',
  },
  {
    xAxis: 'April',
    value: 5,
    status: 'Blocked',
  },
  {
    xAxis: 'April',
    value: 10,
    status: 'In progress',
  },
];

export const LineChartWithObjectDataExample = () => {
  return <LineChart
    data={objectData}
    xAccessor={'xAxis'}
    yAccessor={'value'}
    colorAccessor={'status'}
  />;
}
```
```
