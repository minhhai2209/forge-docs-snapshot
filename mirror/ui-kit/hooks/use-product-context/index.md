# useProductContext

This hook reads the context in which the component is currently running. Note that the context data is loaded asynchronously, so its output will be `undefined` while it is still loading.

### Usage

To add the `useProductContext` hook to your app:

```
1import { useProductContext } from "@forge/react";
2
```

Here is an example of an app that displays all its context information with `useProductContext`.

![The app display on a Confluence page](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/hooks-examples/useproductcontext.png?_v=1.5800.2317)

```
1import React from "react";
2import ForgeReconciler, {
3  Code,
4  Heading,
5  Text,
6  useProductContext,
7} from "@forge/react";
8
9const App = () => {
10  const context = useProductContext();
11
12  return (
13    <>
14      <Heading as="h3">Product context</Heading>
15      <Text>
16        Module key from context:
17        <Code>{context?.moduleKey}</Code>
18      </Text>
19    </>
20  );
21};
22
23ForgeReconciler.render(
24  <React.StrictMode>
25    <App />
26  </React.StrictMode>
27);
28
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
```



```
function useProductContext(): ProductContext | undefined;

interface ProductContext {
  accountId?: string;
  cloudId?: string;
  workspaceId?: string;
  extension: ExtensionData;
  license?: LicenseDetails;
  localId: string;
  locale: string;
  moduleKey: string;
  siteUrl: string;
  timezone: string;
  theme?: {
    colorMode: string;
    light: string;
    dark: string;
    spacing: string;
    [key: string]: string;
  };
}

interface ExtensionData {
  [k: string]: any;
}

interface LicenseDetails {
  active: boolean;
  billingPeriod: string;
  ccpEntitlementId: string;
  ccpEntitlementSlug: string;
  isEvaluation: boolean;
  subscriptionEndDate: string | null;
  supportEntitlementNumber: string | null;
  trialEndDate: string | null;
  type: string;
}
```
```

### Arguments

None.

### Returns

* **ProductContext:** An object containing contextual information about the current environment in which the app is running. The data available depends on the module in which your app is used.
  * **accountId:** The Atlassian ID of the user that interacted with the app.
  * **cloudId:** The ID identifying the cloud context of this app installation, such as the ID of a Jira or Confluence instance.
  * **workspaceId:** The ID identifying the workspace context of this app installation. This is specific to Bitbucket apps.
  * **extension**: Contextual information about the current environment that depends on the extension being used. The format of this information varies across different Atlassian apps that the component may be installed on.
  * **license**: Contains information about the license of the app. Note: this field is only present for paid apps in the production environment. license is `undefined` for free apps, apps not listed on the Atlassian Marketplace, and apps in development and staging environments. See the `LicenseDetails` type for what information is available.
  * **localId**: The unique ID for this instance of this component in the content.
  * **locale**: The locale of the user that interacted with the app.
  * **moduleKey**: The key for the module as defined in the `manifest.yml` file.
  * **siteUrl**: The URL of the site that the app is running on (e.g. <https://example.atlassian.net>).
  * **timezone**: The timezone of the user that interacted with the app.
  * **theme.colorMode** Current color mode. Can be `light` or `dark`. For accessing theme information, prefer using the [useTheme](/platform/forge/ui-kit/hooks/use-theme) hook instead, as it is reactive to theme changes in the Atlassian app.
