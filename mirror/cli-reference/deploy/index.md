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
10
11
--verbose                        enable verbose mode
-f, --no-verify                  disable pre-deployment checks
-v, --major-version [version]    specify a major version to update (Preview)
-t, --tag <tag>                  specify a build tag to deploy (from forge
                                 build)
--skip-rollout                   Skip rolling release rollout after deployment
--approve <rule...>              list of validation rules to approve
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

## Pre-approval

The `forge deploy` command relies on pre-deployment checks (via `forge lint`). Some of those checks may require a developer approval before being able to continue the deployment flow.

Such an example is related to the detection of a major app version bump, which may require admins to manually approve the upgrade of your app (see [major versions](/platform/forge/versions/#major-version-upgrades) for more details).

If this happens, the CLI linter blocks the deployment and asks for your approval, for example:

```
```
1
2
```



```
forge deploy -e production
Deploying your app to the production environment.
Press Ctrl+C to cancel.

Running forge lint...

./manifest.yml
0:0     approval  This deployment triggers a major version upgrade in the production environment because: Change due to scope modification.
For more information, see: https://go.atlassian.com/forge-major-app-version-upgrades  MAJOR_VERSION_RULE

⚠ 1 issue (0 error, 0 warnings, 1 approval)
  Issue found is not automatically fixable with forge lint.
  
The deployment failed due to 1 approval requested. Run forge deploy --approve MAJOR_VERSION_RULE to acknowledge and proceed.
```
```

To continue the deployment, run `forge deploy --approve [ruleName]` to approve the rule.

Note that bypassing the linter at deployment time (via `forge deploy --no-verify`) also bypasses the pre-deployment approval checks.

This CLI feature is only available from version `13.3` onwards.

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
