# Contributors

Multiple people can work together on a Forge app at the same time. They are
known as contributors, and they include the app owner.

When a contributor is added to an app, the contributor can access
the app via the CLI and developer console, and perform some of the
same actions as the app owner. This page explains how
[roles and permissions](/platform/forge/contributors/#roles-and-permissions),
[environments](/platform/forge/contributors/#custom-environments),
[tunneling](/platform/forge/contributors/#tunneling),
and [deployments](/platform/forge/contributors/#deployments) work with multiple contributors.

## Roles and permissions

You can assign one of the following roles to app contributors:

* **Admin** - Edit app details, manage contributors, and manage the app in production environments.
* **Deployer** - Manage the app in development, staging, and production environments.
* **Developer** - Manage the app in development and staging environments.
* **Viewer** - View limited app information in the developer console, including app environments
  and monitoring tools.

An app owner takes on the role of an **admin** by default, but with additional permissions to
*transfer app ownership* and *delete the app*.

App contributors can perform the following actions, no matter their role:

1. Install apps onto sites where they're site admins of
2. Receive alert notifications
3. View alert activities
4. View all app metrics
5. View all app installations
6. View all app contributors
7. View staging and development logs
8. View deployment history

## Specific roles and permissions

Depending on the assigned role, a contributor has specific permissions associated with the following
*activities* performed in the developer console:

### App development activities

The following table outlines the roles and permissions associated with app development activities.

| Permissions |
| --- |
| Admin | Deployer | Developer | Viewer |
| Deploy changes to staging, development, and custom development environments |  |  |  |  |
| Set environment variables on staging, development, and custom development environments |  |  |  |  |
| Create and delete custom development environments |  |  |  |  |
| Deploy changes to production |  |  |  |  |
| Set environment variables on production |  |  |  |  |

### App monitoring activities

The following table outlines the roles and permissions associated with app monitoring activities.

| Permissions |
| --- |
| Admin | Deployer | Developer | Viewer |
| View contributor history |  |  |  |  |
| View and download production logs |  |  |  |  |

![](https://dac-static.atlassian.com/platform/forge/images/dev-console-role-permissions/_EditorPanelIcon_.svg?_v=1.5800.1742)

Granted as an advanced permission to contributors of

*deployer*

,

*developer*

,
and

*viewer*

roles. Gives contributors access to production logs for sites that have activated

[log sharing](https://developer.atlassian.com/platform/forge/access-app-logs/)

.

### App and contributor management activities

The following table outlines the permissions associated with app and contributor management activities.

| Permissions |
| --- |
| Admin | Deployer | Developer | Viewer |
| Delete an app |  |  |  |  |
| Transfer app ownership |  |  |  |  |
| Manage settings (edit app name, icon, and description) |  |  |  |  |
| Manage contributors (add, edit, and remove contributors, and set or update contributor roles) |  |  |  |  |
| Create alert rules |  |  |  |  |
| Manage alert rules (disable and enable alert rules, edit alert rules, delete alert rules, and view alert rule activity) |  |  |  |  |
| View open and closed alerts, view alert rules, and be added as an alert responder. |  |  |  |  |
| Manage distribution (edit details and generate or regenerate distribution links) |  |  |  |  |
| Share distribution links |  |  |  |  |
| Manage a bulk upgrade (Production) |  |  |  |  |
| Manage a bulk upgrade (Non-production) |  |  |  |  |
|

## Default environments

When you run the `forge deploy` command for the first time without specifying an environment, you are prompted
to set your default development environment. Setting a default environment lets you work on an app without
impacting the work of other contributors.

When setting the name of your default development environment, make sure not to use any
sensitive information. You can change your default environment and its name at any time
using `forge settings`.

By default, the CLI will run commands for your default *development* environment unless you specify
another with the `--environment` flag.

## Custom environments

When you run the `forge deploy` command for the first time without specifying an environment, you are prompted
to set your default development environment. Setting a default environment lets you work on an app without
impacting the work of other contributors.

When setting the name of your default development environment, make sure not to use any
sensitive information. You can change your default environment and its name at any time
using `forge settings`.

By default, the CLI will run commands for your default *development* environment unless you specify
another with the `--environment` flag.

## Tunneling

There can only be one tunnel in an environment at a time. When running a tunnel, only your usage will
be displayed, and if another contributor has an active tunnel in progress in the same environment, you'll terminate their tunnel. To avoid impact on other contributors when tunneling, use your own development environment.

By default, the CLI will run commands for your default *development* environment.

To tunnel to a specific environment, provide the `-e` argument to the Forge CLI commands:

```
```
1
2
```



```
forge tunnel -e my-dev-environment
```
```

## Deployments

There can only be one deployment occurring in an environment at the same time. If you attempt to deploy while another deployment is in progress in the same environment, your deployment will be blocked. You can re-attempt deployment once the previous deployment is complete.

By default, the CLI will run commands for your default *development* environment.

To deploy to a specific environment, provide the `-e` argument to the Forge CLI commands:

```
```
1
2
```



```
forge deploy -e my-dev-environment
```
```

## Known limitations

* You can't remove the app owner.
* If an alert is muted, notifications are muted for all contributors.
