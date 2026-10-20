# useTheme

The `useTheme` hook retrieves the current theme from the Atlassian app (Jira, Confluence, etc.) and reactively updates your Forge app when the theme changes. This is the preferred way to access theme information in UI Kit apps, rather than accessing `theme.colorMode` via [useProductContext](/platform/forge/ui-kit/hooks/use-product-context).

### Usage

To add the `useTheme` hook to your app:

```
1import { useTheme } from "@forge/react";
2
```

Here is an example of using the `useTheme` hook to access theme information:

```
1import React from "react";
2import ForgeReconciler, { useTheme, Heading, Text } from "@forge/react";
3
4const App = () => {
5  const theme = useTheme();
6
7  if (!theme) {
8    return <Text>Loading theme...</Text>;
9  }
10
11  return (
12    <>
13      <Heading as="h1">Current Theme</Heading>
14      <Text>Color mode: {theme.colorMode}</Text>
15    </>
16  );
17};
18
19ForgeReconciler.render(
20  <React.StrictMode>
21    <App />
22  </React.StrictMode>
23);
24
```

### Function signature

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
```



```
type Theme = {
  colorMode: string;
  light: string;
  dark: string;
  spacing: string;
  [key: string]: string;
};

function useTheme(): Theme | null;
```
```

### Arguments

None.

### Returns

* **Theme**: Returns a theme object containing the current theme configuration from the Atlassian app. The object includes:
  * **light**: Theme identifier for light mode.
  * **dark**: Theme identifier for dark mode.
  * **spacing**: Spacing token identifier.
  * Additional theme properties may be available as key-value pairs.
