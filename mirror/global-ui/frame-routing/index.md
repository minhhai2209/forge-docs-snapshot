# Add custom content to a global:ui app using Frame (EAP)

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge global:ui module and Global component is governed by the Atlassian Developer Terms. The Forge `global:ui` module and Global component are considered Early Access Materials and currently support only UI Kit (`render: native`), as set forth in Section 12 of the Atlassian Developer Terms and are subject to applicable terms, conditions, and disclaimers. The Forge `global:ui` module, Global component, and any related documentation are provided solely for testing purposes and are considered Atlassian Confidential Information.
As conditions on your right to use the Forge global:ui module and Global component during this EAP, you agree not to (and not to authorize any third party to) deploy any Marketplace App using the Forge global:ui module or Global component in a Production environment.

To join the EAP for `global:ui`, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/19016?xpis=eyJicmlkZ2UiOiJzbWFydExpbmtzIiwiaWQiOiIxNzgyMzUxNTgzNDkwIiwic291cmNlIjoiY29uZmx1ZW5jZSJ9).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This tutorial shows you how to embed a Custom UI resource in the main content area of a
`global:ui` app using the [`Frame`](/platform/forge/ui-kit/components/frame/) component.
You'll also wire up sidebar navigation so clicking a menu item updates the content
inside the Frame without reloading it.

By the end, you'll have a working app where:

* The sidebar uses `global:ui` UI Kit components to navigate between routes.
* The main content area renders a React app inside a `Frame`.
* A history listener inside the Frame responds to URL changes from the sidebar, displaying
  the correct page without remounting the Frame.

## Before you begin

Complete [Getting started with global:ui (EAP)](/platform/forge/global-ui/getting-started/)
before working through this tutorial. This tutorial extends the app you create there.

You should also be familiar with [Add routing to a Custom UI full page app](/platform/forge/add-routing-to-a-full-page-app/),
which explains the `view.createHistory()` pattern that this tutorial builds on.

## How it works

The `global:ui` module only supports UI Kit for its navigation chrome. To render fully
custom content, you place a `Frame` component inside `<Main>`. The Frame loads a separate
static resource — a standalone React app — in an isolated container.

The challenge is that sidebar navigation updates the URL, but the Frame can't hear that
change by default. Remounting the Frame on every navigation causes a slow reload. Instead,
the Frame uses `view.createHistory()` from `@forge/bridge` to subscribe to URL changes
and update its internal React Router without remounting.

Only one `Frame` component is supported per `global:ui` module.

## App structure

After completing this tutorial, your app has the following structure:

```
```
1
2
```



```
my-global-app/
├── manifest.yml
├── src/
│   └── frontend/
│       └── index.jsx         # UI Kit shell: sidebar + Frame
└── static/
    └── main-content/            # Custom UI resource loaded by Frame
        ├── package.json
        ├── vite.config.js
        ├── index.html
        └── src/
            ├── main.jsx
            └── App.jsx       # Routing with view.createHistory()
```
```

## Step 1: Create the Custom UI resource

The Frame component loads a separate static resource. You'll build it with
[Vite](https://vitejs.dev/) and [React Router](https://reactrouter.com/).

1. In the top-level directory of your app, create the `static/main-content/` directory:

   ```
   ```
   1
   2
   ```



   ```
   mkdir -p static/main-content/src
   ```
   ```
2. Create `static/main-content/package.json`:

   ```
   ```
   1
   2
   ```



   ```
   {
     "name": "main-content",
     "private": true,
     "scripts": {
       "dev": "vite --port 3001",
       "build": "vite build"
     },
     "dependencies": {
       "@forge/bridge": "6.1.0-next.8",
       "react": "^18.2.0",
       "react-dom": "^18.2.0",
       "react-router": "^7.0.0"
     },
     "devDependencies": {
       "@vitejs/plugin-react": "^4.0.0",
       "vite": "^5.0.0"
     }
   }
   ```
   ```
3. Create `static/main-content/vite.config.js`:

   ```
   ```
   1
   2
   ```



   ```
   import { defineConfig } from "vite";
   import react from "@vitejs/plugin-react";

   export default defineConfig({
     plugins: [react()],
     base: "./",
     build: { outDir: "build" },
   });
   ```
   ```
4. Create `static/main-content/index.html`:

   ```
   ```
   1
   2
   ```



   ```
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Frame App</title>
     </head>
     <body>
       <div id="root"></div>
       <script type="module" src="/src/main.jsx"></script>
     </body>
   </html>
   ```
   ```
5. Create `static/main-content/src/main.jsx`:

   ```
   ```
   1
   2
   ```



   ```
   import React from "react";
   import ReactDOM from "react-dom/client";
   import App from "./App";

   ReactDOM.createRoot(document.getElementById("root")).render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   );
   ```
   ```

## Step 2: Add routing inside the Frame

The Frame resource needs to listen for URL changes from the sidebar and render the
correct page. You use `view.createHistory()` from `@forge/bridge` to subscribe to
these changes and pass the current location to React Router.

Create `static/main-content/src/App.jsx`:

```
```
1
2
```



```
import { useEffect, useState } from "react";
import { view } from "@forge/bridge";
import { Router, Routes, Route } from "react-router";

function ForYouPage() {
  return <h1>For you</h1>;
}

function DashboardPage() {
  return <h1>Dashboard</h1>;
}

function SettingsPage() {
  return <h1>Settings</h1>;
}

export default function App() {
  const [historyState, setHistoryState] = useState(null);
  const [navigator, setNavigator] = useState(null);

  useEffect(() => {
    (async () => {
      const history = await view.createHistory();
      setNavigator(history);
      setHistoryState({ action: history.action, location: history.location });
      history.listen((location, action) => setHistoryState({ action, location }));
    })();
  }, []);

  if (!navigator || !historyState) {
    return <div>Loading...</div>;
  }

  return (
    <Router
      navigator={navigator}
      navigationType={historyState.action}
      location={historyState.location}
    >
      <Routes>
        <Route path="/" element={<ForYouPage />} />
        <Route path="/for-you" element={<ForYouPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Router>
  );
}
```
```

**What this code does:**

* `view.createHistory()` creates a history object connected to the Atlassian platform's URL system.
* `history.listen()` subscribes to URL changes. When the sidebar navigates to `/dashboard`,
  this callback fires and updates `historyState`.
* React Router receives the updated `location` and renders the matching `<Route>` — no
  Frame remount required.

The routes `/` and `/for-you` both render `ForYouPage` because the platform's mandatory
**For you** sidebar item navigates to the root route.

## Step 3: Update the UI Kit shell

Update `src/frontend/index.jsx` to use the `global:ui` layout with a `Frame` in the main
content area:

```
```
1
2
```



```
import React from "react";
import ForgeReconciler from "@forge/react";
import { Frame } from "@forge/react";
import { Global, Sidebar, LinkMenuItem, Main } from "@forge/react/global";

const App = () => (
  <Global>
    <Sidebar>
      <LinkMenuItem label="Dashboard" href="/dashboard" icon="chart-bar" />
      <LinkMenuItem label="Settings" href="/settings" icon="settings" />
    </Sidebar>
    <Main>
      <Frame resource="main-content" />
    </Main>
  </Global>
);

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

For icon guidelines and a list of icons to avoid in global navigation, see [Using icons](/platform/forge/global-ui/ui-kit-components/#using-icons).

The `resource` prop on `Frame` must match a key in the `resources` section of your
`manifest.yml` — you'll add that in the next step.

## Step 4: Update the manifest

Add the `main-content` resource and tunnel ports to your `manifest.yml`:

```
```
1
2
```



```
modules:
  global:ui:
    - key: my-global-app-global-ui
      resource: main
      render: native
      resolver:
        function: resolver
      title: My Global App
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
    tunnel:
      port: 3000
  - key: main-content
    path: static/main-content/build
    tunnel:
      port: 3001
app:
  runtime:
    name: nodejs24.x
  compatibility:
    confluence:
      required: true
  id: ari:cloud:ecosystem::app/<your-app-id>
```
```

The `path` for `main-content` points to the Vite build output. The `tunnel.port` values
allow both resources to run concurrently during local development.

## Step 5: Build the Custom UI resource

Before deploying, build the Frame resource:

1. Navigate to the `static/main-content` directory and install dependencies:

   ```
   ```
   1
   2
   ```



   ```
   cd static/main-content
   npm install
   ```
   ```
2. Build the assets:

   Vite outputs the built files to `static/main-content/build/`, which is the path
   referenced in your manifest.
3. Navigate back to the app's top-level directory:

## Step 6: Deploy and install your app

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

## View your app

Once installed, open your app from the Atlassian app switcher. You should see:

* The **Dashboard** and **Settings** items in the sidebar, below the platform-provided
  **For you** item.
* Clicking a sidebar item updates the main content area instantly, without reloading the
  Frame.

After making changes to the Frame resource, rebuild it with `npm run build` in the
`static/main-content` directory, then run `forge deploy` again to upload the updated assets.

## Next steps
