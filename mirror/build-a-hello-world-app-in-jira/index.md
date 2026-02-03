# Part 1: Build a Jira hello world app

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-build-a-hello-world-app-in-jira)

This tutorial will walk you through creating a sample Forge app for Jira.
There are three parts to the tutorial:

1. This page: describes creating, changing, and installing a simple hello world app. The
   focus is on learning the CLI commands needed to work with apps.
2. [Call a Jira API:](/platform/forge/call-a-jira-api) describes how to make API calls to the Jira REST API.
3. [Change the frontend with UI Kit:](/platform/forge/change-the-jira-frontend-with-the-ui-kit/)
   describes how to use UI Kit components.

We recommend you work through all three parts to get a good understanding of how to develop apps with
Forge.

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

## Create your app

Create an app based on the Jira issue panel template.

1. Navigate to the directory where you want to create the app. A new subdirectory with
   the app’s name will be created there.
2. Create your app by running:
3. Enter a name for your app (up to 50 characters). For example, *hello-world-app*.
4. Select *Jira* as the Atlassian app.
5. Select the *UI Kit* category.
6. Select the *jira-issue-panel* template.
7. Change to the app subdirectory to see the app files:

### jira-issue-panel template

The app we'll create will display an issue panel on all Jira issues,
and will have a function that provides the contents of the panel.

The `jira-issue-panel` template uses Node.js and has the following structure:

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
* `src/resolvers/index.js`: Where you write backend functions (resolver functions) for your app. To learn more about resolvers, see the [Custom UI Resolver](/platform/forge/runtime-reference/custom-ui-resolver/) documentation.

## Change the panel title

This app displays content in a Jira issue panel using the `jira:issuePanel` module. Jira
shows the title of the `jira:issuePanel` as the panel's heading. Let's change the
title to include your name.

1. In the app’s top-level directory, open the `manifest.yml` file.
2. Find the `title` entry under the `jira:issuePanel` module.
3. Change the value of `title` from `hello-world-app` to `Forge app for <your name>`. For example,
   *Forge app for Mia*.

Your `manifest.yml` file should look like the following, with your values for the
title and app ID:

```
```
1
2
```



```
modules:
  jira:issuePanel:
    - key: hello-world-app-hello-world-issue-panel
      resource: main
      resolver:
        function: resolver
      render: native
      title: hello-world-app
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
  id: '<your app id>'
```
```

## Install your app

To use your app, it must be installed onto an Atlassian site. The
`forge deploy` command builds, compiles, and deploys your code; it'll also report any compilation errors.
The `forge install` command then installs the deployed app onto an Atlassian site with the
required API access.

You must run the `forge deploy` command before `forge install` because an installation
links your deployed app to an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

## View your app

With your app installed, it’s time to see the app on an issue.

1. Create a new Jira issue.
   [Learn more about Jira issues](https://support.atlassian.com/jira-core-cloud/docs/create-and-work-with-issues/).
2. In the issue view, click **View app actions** and select your app. Your app should display like the example below.

![A Jira issue displaying the hello world forge app](https://dac-static.atlassian.com/platform/forge/images/forge-getting-started-jira-initial-state.png?_v=1.5800.1813)

3. To view new changes in your app, run `forge deploy` again, or run `forge tunnel`.
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

In the next tutorial, you'll learn how to make API calls to Jira using Forge. This tutorial
uses the `forge tunnel`, so make sure you are familiar with using this command.

[![A button to go to the next tutorial](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1813)](/platform/forge/call-a-jira-api/)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
