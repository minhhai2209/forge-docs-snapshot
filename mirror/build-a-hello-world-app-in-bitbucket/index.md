# Part 1: Build a Bitbucket hello world app

This tutorial will walk you through creating a sample Forge app for Bitbucket.
There are three parts to the tutorial:

1. This page: describes creating, changing, and installing a simple hello world app. The
   focus is on learning the CLI commands needed to work with apps.
2. [Call a Bitbucket API:](/platform/forge/call-a-bitbucket-api) describes how to make API calls to the Bitbucket REST API.
3. [Change the frontend with UI Kit:](/platform/forge/change-the-bitbucket-frontend-with-the-ui-kit/)
   describes how to use UI Kit components.

We recommend you work through all three parts to get a good understanding of how to develop apps with
Forge.

## Before you begin

To complete this tutorial, you need to do complete [Getting started](/platform/forge/getting-started/) before working through
this page.

### Set up a shared team workspace

For Bitbucket apps you need to join or create a [shared Bitbucket team workspace](https://confluence.atlassian.com/bbkb/difference-between-shared-and-personal-workspaces-1141477191.html) (as Forge apps are not supported on personal workspaces).
If you don't have a Bitbucket workspace, see the references below for related instructions:

1. [Creating a Bitbucket Cloud account](https://confluence.atlassian.com/bbkb/creating-a-bitbucket-cloud-account-1206558490.html).
2. [Join or create a workspace](https://support.atlassian.com/bitbucket-cloud/docs/create-your-workspace/).

A free Bitbucket team space can have up to 5 users.

Forge apps can't be viewed by anonymous users. When testing a Forge app, you should be logged in to [Bitbucket](https://bitbucket.org/product).

## Create your app

Create an app based on the Bitbucket repository code overview card template.
You can view the completed app code in the [Bitbucket Forge Hello World repository](https://bitbucket.org/atlassian/bitbucket-forge-hello-world/src/main/).

1. Navigate to the directory where you want to create the app. A new subdirectory with
   the app’s name will be created there.
2. Create your app by running:
3. Enter a name for your app (up to 50 characters). For example, *hello-world-app*.
4. Select *Bitbucket* as the context.
5. Select the *UI Kit* category.
6. Select the *bitbucket-repository-code-overview-card* template.
7. Change to the app subdirectory to see the app files:

### bitbucket-repository-code-overview-card template

The app we'll create will display a card panel on all Bitbucket repository source pages and will have
a function that provides the contents of the panel.

The `bitbucket-repository-code-overview-card` template uses Node.js and has the following structure:

```
```
1
2
```



```
hello-world-app
├── README.md
├── manifest.yml
├── package-lock.json
├── package.json
└── src
    ├── frontend
    │   └── index.jsx
    ├── index.js
    └── resolvers
        └── index.js
```
```

Let’s have a look at what these files are:

* `manifest.yml`: Describes your app. This file contains the name and ID of the app,
  the app permissions, and the modules the app uses. To learn more about the `manifest.yml` file,
  see [Forge manifest](/platform/forge/manifest) documentation.
* `package.json`: The app’s Node.js metadata. See the [Node](https://docs.npmjs.com/cli/v9/configuring-npm/package-json) documentation for more information.
* `package-lock.json`: Records the version of the app’s dependencies.
* `README.md`: Information about the app. We recommend updating this as you change the behavior of the app.
* `src/frontend/index.jsx`: Where you write the application with which the user interacts directly.
* `src/resolvers/index.js`: Where you write the resolver function definitions. To learn more about resolvers, see the [Custom UI Resolver](/platform/forge/runtime-reference/custom-ui-resolver/) documentation.

## Change the panel title

This app displays content in a Bitbucket repository card panel using the `bitbucket:repoCodeOverviewCard`
module. Bitbucket shows the title of the `bitbucket:repoCodeOverviewCard` as the panel's heading.
Let's change the title to include your name.

1. In the app’s top-level directory, open the `manifest.yml` file.
2. Find the `title` entry under the `bitbucket:repoCodeOverviewCard` module.
3. Change the value of `title` to `Forge app for <your name>`. For example, *Forge app for Mia*.

Your `manifest.yml` file should look like the following, with your values for the title and app ID:

```
```
1
2
```



```
modules:
  bitbucket:repoCodeOverviewCard:
    - key: hello-world-app-hello-world-repository-code-overview-card
      resource: main
      resolver:
        function: resolver
      render: native
      title: Forge app for Mia
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: '<your app id>'
```
```

## Install your app

To use your app, it must be installed onto a Bitbucket workspace. The
`forge deploy` command builds, compiles, and deploys your code; it'll also report any compilation errors.
The `forge install` command then installs the deployed app onto a Bitbucket workspace with the required API access.

You must run the `forge deploy` command before `forge install` because an installation
links your deployed app to a Bitbucket workspace.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select *Bitbucket* using the arrow keys and press the enter key.
4. Enter the URL for your workspace. For example, *<https://bitbucket.org/example-workspace/>*.

Forge apps are not supported on personal workspaces. If you install an app to a personal workspace,
you will get an insufficient permissions error. See [set up a shared team workspace](/platform/forge/build-a-hello-world-app-in-bitbucket/#set-up-a-shared-team-workspace).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified workspace.

You can verify the app installation in the specified workspace by navigating to **Installed apps**
in workspace settings. Your installed Forge app will be visible under the *Forge apps* section.
If the app is [distributed](https://developer.atlassian.com/platform/forge/distribute-your-apps/),
you can access the direct distribution link for the app via the *Manage* link next to it,
which allows you to check the app details and manage the app installation, including deleting the app.
Otherwise, you can always delete your app from the workspace by running the `forge uninstall` command from your Forge CLI.

Running the `forge install` command only installs your app into the selected Atlassian app.
To install into multiple Atlassian apps, repeat these steps again, selecting another Atlassian app each time.

You must run `forge deploy` before running `forge install` in any of the Forge environments.

## View your app

With your app installed, it’s time to see the app on a repository.

1. Create a new Bitbucket repository if you haven't already. See [Creating a repository](https://support.atlassian.com/bitbucket-cloud/docs/create-a-repository/) for more information.
2. Navigate to the source page in the repository. Your app should appear in the bottom of the
   **Repository details** pane on the right:

![The app displayed in a Bitbucket repository](https://dac-static.atlassian.com/platform/forge/images/forge-view-bitbucket-app.png?_v=1.5800.1783)

1. To view new changes in your app, run `forge deploy` again, or run `forge tunnel`.
   This is explained fully in the next section.

While your app is deployed to either a development or staging environment, `(development)` or
`(staging)` will appear in your app title. This suffix is removed once you've
[deployed your app to production](/platform/forge/staging-and-production-apps/#environments).

## Deploy app changes

Once your app is installed, it will automatically pick up all minor app deployments
so you don't need to run the `forge install` command again. Minor deployments are changes
that don't modify app permissions in the `manifest.yml` file. You can deploy the changes onto your
developer site or Bitbucket workspace by using one of two methods:

* Manually, by running the `forge deploy` command.
* Automatically, by running the `forge tunnel` command.

Once your app is installed, changes in the manifest are picked up automatically after running `forge deploy`.
However, due to the eventually-consistent nature of our system, you may need to wait up to 5 minutes
for changes in the manifest to be reflected in the Atlassian app.

Tunneling runs your app code locally on your machine via the Forge CLI and Cloudflare. It allows you to speed up development by avoiding the need
to redeploy each code change, and by seeing each invocation as it executes. The Forge tunnel
works similarly to hot reloading,
so any changes you make to your app code can be viewed on your Atlassian site or Bitbucket workspace without losing
the current app state. You don’t
need to run any other commands; you only need to refresh the page.

Once you've completed testing your app changes using `forge tunnel` command, please remember to redeploy your app using the `forge deploy` command.

1. You can start tunneling by running:

You should see output similar to:

```
```
1
2
```



```
Tunnel redirects requests you make to your local machine. This occurs for any Atlassian site where your app is installed in the specific development environment. You will not see requests from other users.
Press Ctrl+C to cancel.


=== Running forge lint...
No issues found.

=== Bundling code...
✔ Functions bundled.
✔ Resources bundled.

Listening for requests...
```
```

You can now automatically deploy changes to your codebase and install packages, while tunneling.
These changes appear on the Atlassian site or Bitbucket workspace where your app is installed.

2. When you are ready to close the tunnel, press **Control** + **C**.

The `forge tunnel` command only forwards traffic when the user (in Jira, Confluence, Jira
Service Management, or Bitbucket) matches the Forge CLI user. For security reasons, you can’t see the traffic
of other users.

For important caveats on how `forge tunnel` works, see
[Tunneling](/platform/forge/tunneling/#known-limitations).

## Next step

In the next tutorial, you'll learn how to make API calls to Bitbucket using Forge. This tutorial
uses the `forge tunnel`, so make sure you are familiar with using this command.

[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1783)](/platform/forge/call-a-bitbucket-api)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
