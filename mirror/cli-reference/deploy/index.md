# deploy

## Description

deploy your app to an environment

## Usage

```
1
Usage: forge deploy [options] [command]
```

## Options

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
--verbose                        enable verbose mode
-f, --no-verify                  disable pre-deployment checks
-v, --major-version [version]    specify a major version to update (Preview)
-t, --tag <tag>                  specify a build tag to deploy (from
                                 forge build)
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--non-interactive                run the command without input prompts
-h, --help                       display help for command
```

## Commands

```
1
list [options]                   list app deployments
```

## Example

```
```
1
2
```



```
forge deploy -e staging --no-verify
```
```

This command will deploy your app to the `staging` environment without running
`forge lint` or any other pre-deployment check.

```
```
1
2
```



```
forge deploy --tag 3f6f3d
```
```

This command will deploy your app to the default environment using the app bundle uploaded via `forge build --tag 3f6f3d`.

```
```
1
2
```



```
forge deploy --tag 3f6f3d -e production
```
```

This command will deploy your app to the `production` environment using the app bundle uploaded via `forge build --tag 3f6f3d`.

## Operations

The `forge deploy` command bundles and deploys your app's code to the Forge platform.
Apps must be deployed first before they can be installed on any site.

By default, this command:

1. Runs pre-deployment checks (like `forge lint`) and reports any compilation errors.
2. Deploys app changes to your [default environment](/platform/forge/environments-and-versions/#default-environments).

## Backporting

Minor version upgrades are applied by default to the latest major version in the environment
you’re deploying to. You can, however, use the `--major-version` option to backport minor version
upgrades to an older major version. See [Backporting](/platform/forge/versions/#backporting) for more details.

## Further information

* See [Environments and versions](/platform/forge/environments-and-versions/#environments-and-versions)
  for additional information about the `development`, `staging`, and `production` environments.
* See [App Versions](/platform/forge/versions/) for details about how deploying changes creates minor or major
  versions of your app.
* Once you've deployed your app, you can install it. See [forge install](/platform/forge/cli-reference/install/) for details about installing your app through the Forge CLI.
* [Set up continuous delivery for Forge apps](/platform/forge/set-up-cicd/) - this tutorial demonstrates how
  to deploy your code to [staging](/platform/forge/set-up-cicd/#deploy-to-staging) and [production](/platform/forge/set-up-cicd/#deploy-to-production) via Bitbucket pipeline.
* The following tutorials feature the use of `forge deploy` in the course of creating a Hello World app:
