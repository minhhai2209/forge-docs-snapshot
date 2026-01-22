# Part 1: Build an app compatible with Confluence and Jira

The ability to build Forge apps that are compatible with multiple Atlassian apps is available as a Forge Preview feature.

Preview features are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This tutorial will walk you through creating an app that is compatible with Confluence and Jira.
This app uses the [Confluence macro](/platform/forge/manifest-reference/modules/macro/) and
[Jira issue panel](/platform/forge/manifest-reference/modules/jira-issue-panel/) modules,
and calls both Confluence and Jira APIs.

For more information on building Forge apps that are compatible with multiple Atlassian apps, see
[App compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility--eap-).

There are four parts to the tutorial:

1. **Part 1 – This page:** describes creating, deploying, and installing a hello world app that defines Confluence
   as the required Atlassian app.
2. **Part 2 – [Call a Confluence API](/platform/forge/call-a-confluence-api-in-a-confluence-jira-app):** describes
   how to make API calls to the Confluence REST API.
3. **Part 3 – [Add support for Jira as an optional Atlassian app](/platform/forge/add-support-for-jira-as-an-optional-atlassian-app):**
   describes how to add Jira as an optional Atlassian app, including adding a Jira module and making API calls to the Jira REST API.
4. **Part 4 – [Change the frontend with UI Kit](/platform/forge/change-the-frontend-with-ui-kit-for-a-confluence-jira-app):**
   describes how to use UI Kit components.

This is part 1 of 4 in this tutorial series. We recommend you work through all four parts, in order, to get a good understanding of how to develop Forge apps that are compatible with multiple Atlassian apps.

## Before you begin

If you're completely new to Forge, the [Getting started with Forge](/platform/forge/getting-started/) tutorial walks you through setting up your development environment and using the Forge CLI from your terminal (for example, macOS Terminal, Windows Command Prompt, or PowerShell).

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

### Install the latest CLI version

You will need to ensure you are using the latest `@forge/cli` version.

To install the Forge CLI globally, open your terminal (for example, macOS Terminal, Windows Command Prompt, or a Linux shell) on your local machine and run:

```
```
1
2
```



```
npm install -g @forge/cli@latest
```
```

## Create your app

Create an app based on the Confluence macro template.

1. Navigate to the directory where you want to create the app. A new subdirectory with
   the app’s name will be created there.
2. Create your app by running:
3. Enter a name for your app (up to 50 characters). For example, *hello-world-app*.
4. Select *Multiple* as the Atlassian app or platform tool.
5. Select the *UI Kit* category.
6. Select the *confluence-macro* template.
7. Change to the app subdirectory to see the app files:

### confluence-macro template

The app we'll create will display a macro on a Confluence page,
with a function that provides the contents of the macro.

The `confluence-macro` template uses Node.js and has the following structure:

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
  the app permissions, and the modules the app uses. The app's compatibility is defined here.
  To learn more about the `manifest.yml` file, see [Forge manifest](/platform/forge/manifest) documentation.
* `package.json`: The app’s Node.js metadata. See the [Node](https://docs.npmjs.com/cli/v9/configuring-npm/package-json) documentation for more information.
* `package-lock.json`: Records the version of the app’s dependencies.
* `README.md`: Information about the app. We recommend updating this as you change the behavior of the app.
* `src/frontend/index.jsx`: Where you write the application with which the user interacts directly.
* `src/resolvers/index.js`: Where you write backend functions (resolver functions) for your app. To learn more about resolvers, see the [Custom UI Resolver](/platform/forge/runtime-reference/custom-ui-resolver/) documentation.

### App compatibility in the manifest

The `manifest.yml` file is where the app's `compatibility` is defined. When using `forge create`,
the required Atlassian app is automatically added to the manifest based on the module template you selected.
In this case, it is Confluence:

```
```
1
2
```



```
modules:
  macro:
    - key: hello-world-app-hello-world
      resource: main
      render: native
      resolver:
        function: resolver
      title: hello world app
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: '<your app id>'
  compatibility:
    confluence:
      required: true
```
```

## Change the macro title

This app displays content within a Confluence page using a `macro`. Confluence shows the title of the
macro in the quick insert menu when you add the app to a page. Let's change the title to include your name.

1. In the app’s top-level directory, open the `manifest.yml` file.
2. Find the `title` entry under the `macro` module.
3. Change the value of `title` to `Forge app for <your name>`. For example, *Forge app for Mia*.

Your `manifest.yml` file should look like the following, with your values for the title and app ID:

```
```
1
2
```



```
modules:
  macro:
    - key: hello-world-app-hello-world
      resource: main
      render: native
      resolver:
        function: resolver
      title: Forge app for Mia
      description: Inserts hello world!
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: '<your app id>'
  compatibility:
    confluence:
      required: true
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

   This will automatically install your app into the required Atlassian app, which in this case is Confluence.
3. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

You must install your app into the required Atlassian app before you can install it into other Atlassian apps. This
applies for every Forge environment.

You must also run `forge deploy` before running `forge install` in any of the Forge environments.

## View your app

With your app installed, it’s time to see the app on a page.

1. Edit a Confluence page in your development site.
2. Type `/`
3. Find the macro app by name in the menu that appears and select it.
4. Publish the page.

Your hello world app is now installed into your development site. The app should display on the page like the image below.

![The app displayed in a Confluence page](https://dac-static.atlassian.com/platform/forge/images/forge-getting-started-initial-state.png?_v=1.5800.1794)

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

Next, continue to **Part 2 – [Call a Confluence API](/platform/forge/call-a-confluence-api-in-a-confluence-jira-app)**, where you'll learn how to make API calls to Confluence using Forge. This tutorial uses the `forge tunnel`, so make sure you are familiar with using this command.

If you want to skip to adding Jira as a compatible context, you can go to **Part 3 – [Add support for Jira as an optional Atlassian app](/platform/forge/add-support-for-jira-as-an-optional-atlassian-app)**.

[![Button: Next – Part 2, Call a Confluence API](https://dac-static.atlassian.com/platform/forge/images/button-next-tutorial.svg?_v=1.5800.1794)](/platform/forge/call-a-confluence-api-in-a-confluence-jira-app)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
