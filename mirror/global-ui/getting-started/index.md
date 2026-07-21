# Getting started with global:ui (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This tutorial walks you through creating your first app using the `global:ui` module. By the end,
you'll have a working global app that appears in the Atlassian app switcher with its own side
navigation and content area.

## Before you begin

Complete [Getting started](/platform/forge/getting-started/) before working through
this tutorial.

Forge apps can't be viewed by anonymous users. When testing a Forge app, you should be logged in to your
Atlassian cloud developer site.

### Set up a cloud developer site

An Atlassian cloud developer site lets you install and test your app on
Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:

1. Go to <http://go.atlassian.com/cloud-dev> and
   create a site using the email address associated with your Atlassian account.
2. Once your site is ready, log in and complete the setup wizard.

You can install your app to multiple Atlassian sites. However, app
data won't be shared between separate Atlassian apps, sites,
or Forge environments.

The limits on the numbers of users you can create are as follows:

* Confluence: 5 users
* Jira Service Management: 1 agent
* Jira Software and Jira Work Management: 5 users

## Install the experimental CLI

The `global:ui` module requires an experimental version of the Forge CLI during the EAP. Install it
by running:

```
```
1
2
```



```
npm install -g @forge/cli@latest
```
```

This experimental CLI version includes `global:ui` templates. Once the EAP concludes, these
templates will be available in the standard Forge CLI.

## Create your app

1. Navigate to the directory where you want to create the app. A new subdirectory with
   the app’s name will be created there.
2. Create your app by running:
3. Enter a name for your app (up to 50 characters). For example, *my-global-app*.
4. Select **Global (EAP)** as the category.
5. Select your template.
6. Change to the app subdirectory to see the app files:

## Template structure

Your app has the following structure:

```
```
1
2
```



```
my-global-app/
├── manifest.yml        # App configuration
├── package.json
└── src/
    └── frontend/
        └── index.jsx   # UI Kit frontend code
```
```

### manifest.yml

The manifest declares the `global:ui` module and the required Atlassian app link:

```
```
1
2
```



```
modules:
  global:ui:
    - key: my-app
      resource: main
      render: native
      title:
        default: My App
      resolver:
        function: resolver
app:
  id: ari:cloud:ecosystem::app/<your-app-id>
  runtime:
    name: nodejs22.x
  compatibility:
    confluence:
      required: true
resources:
  - key: main
    path: src/frontend
    tunnel:
      port: 3000
```
```

Key parts of the manifest:

* **`global:ui` module** — Defines your app's entry point with a title and resource.
* **`compatibility` section** — Declares Confluence as the required Atlassian app. Users must have
  Confluence for the app to be installed.
* **`resources`** — Points to your frontend code.

For full details, see the [global:ui module reference](/platform/forge/global-ui/global-ui-module/).

### Frontend code

The frontend uses the `Global`, `Sidebar`, and `Main` components to build the app layout:

```
```
1
2
```



```
import React from "react";
import ForgeReconciler, {
  Global,
  Sidebar,
  LinkMenuItem,
  Main,
} from "@forge/react/global";
import { Text } from "@forge/react";

const App = () => {
  return (
    <Global>
      <Sidebar>
        <LinkMenuItem label="Dashboard" href="/dashboard" icon="chart-bar" />
        <LinkMenuItem label="Settings" href="/settings" icon="settings" />
      </Sidebar>
      <Main>
        <Text>Welcome to your global app!</Text>
      </Main>
    </Global>
  );
};

ForgeReconciler.render(<App />);
```
```

For icon guidelines and a list of icons to avoid in global navigation, see [Using icons](/platform/forge/global-ui/ui-kit-components/#using-icons).

For all available `global:ui` components, see [global:ui UI Kit components](/platform/forge/global-ui/ui-kit-components/).

## Deploy your app

1. Build and deploy your app by running:
2. Install your app by running:
3. When prompted, select your Atlassian site.

## View your app

Once installed, your app appears in the Atlassian app switcher. You can also access it directly
using the following URL format:

```
```
1
2
```



```
{site-hostname}/apps/a/{app-id}/e/{env-id}
```
```

To find your environment ID, run:

```
```
1
2
```



```
forge environments list
```
```

## Next steps
