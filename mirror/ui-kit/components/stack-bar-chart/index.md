# Stack Bar chart

To add the `StackBarChart` component to your app:

```
1import { StackBarChart } from '@forge/react';
2
```

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `colorAccessor` | `number` | `string` | Yes | Accessor to define the color grouping. |
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

Data can be one of two formats, an array of arrays or an array of objects. Both examples below will produce the same stack bar chart:

![Example image of a rendered stack bar chart](https://dac-static.atlassian.com/platform/forge/ui-kit/images/stack-bar-chart/stack-bar-chart-data.png?_v=1.5800.2310)

### 1. Array of arrays

Each entry in the dataset is an array. These arrays require three items to denote the x and y coordinates and to indicate color grouping.

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
  ["Jan", 4, "Done"],
  ["Jan", 5, "To do"],
  ["Jan", 10, "Blocked"],
  ["Jan", 6, "In progress"],
  ["Feb", 5, "Done"],
  ["Feb", 10, "To do"],
  ["Feb", 15, "Blocked"],
  ["Feb", 10, "In progress"],
  ["Mar", 1, "Done"],
  ["Mar", 14, "To do"],
  ["Mar", 25, "Blocked"],
  ["Mar", 10, "In progress"],
  ["Apr", 5, "Done"],
  ["Apr", 2, "To do"],
  ["Apr", 5, "Blocked"],
  ["Apr", 8, "In progress"],
]

export const StackBarChartWithArrayDataExample = () => {
  return <StackBarChart 
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
```



```
const objectData = [
  {
    xAxis: 'Jan', // x value
    value: 4, // y value
    status: 'Done', // color value
  },
  {
    xAxis: 'Jan',
    value: 5,
    status: 'To do',
  },
  {
    xAxis: 'Jan',
    value: 10,
    status: 'Blocked',
  },
  {
    xAxis: 'Jan',
    value: 6,
    status: 'In progress',
  },
  {
    xAxis: 'Feb',
    value: 5,
    status: 'Done',
  },
  {
    xAxis: 'Feb',
    value: 10,
    status: 'To do',
  },
  {
    xAxis: 'Feb',
    value: 15,
    status: 'Blocked',
  },
  {
    xAxis: 'Feb',
    value: 10,
    status: 'In progress',
  },
  {
    xAxis: 'Mar',
    value: 1,
    status: 'Done',
  },
  {
    xAxis: 'Mar',
    value: 14,
    status: 'To do',
  },
  {
    xAxis: 'Mar',
    value: 25,
    status: 'Blocked',
  },
  {
    xAxis: 'Mar',
    value: 10,
    status: 'In progress',
  },
  {
    xAxis: 'Apr',
    value: 5,
    status: 'Done',
  },
  {
    xAxis: 'Apr',
    value: 2,
    status: 'To do',
  },
  {
    xAxis: 'Apr',
    value: 5,
    status: 'Blocked',
  },
  {
    xAxis: 'Apr',
    value: 8,
    status: 'In progress',
  },
];
export const StackBarChartWithObjectDataExample = () => {
  return <StackBarChart 
    data={objectData} 
    xAccessor={"xAxis"} // key of x value in object item
    yAccessor={"value"} // key of y value in object item
    colorAccessor={"status"} // key of color value in object item
  />;
};
```
```
