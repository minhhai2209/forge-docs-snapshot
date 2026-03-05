# useTheme

The `useTheme` hook retrieves the current theme from the Atlassian app (Jira, Confluence, etc.) and reactively updates your Forge app when the theme changes. This is the preferred way to access theme information in UI Kit apps, rather than accessing `theme.colorMode` via [useProductContext](/platform/forge/ui-kit/hooks/use-product-context).

### Usage

To add the `useTheme` hook to your app:

```
1
import { useTheme } from "@forge/react";
```

Here is an example of using the `useTheme` hook to access theme information:

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
import React from "react";
import ForgeReconciler, { useTheme, Heading, Text } from "@forge/react";

const App = () => {
  const theme = useTheme();

  if (!theme) {
    return <Text>Loading theme...</Text>;
  }

  return (
    <>
      <Heading as="h1">Current Theme</Heading>
      <Text>Color mode: {theme.colorMode}</Text>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### Function signature

```
```
1
2
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
