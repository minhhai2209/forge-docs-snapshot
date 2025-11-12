# variables set

## Description

set an environment variable

## Usage

```
1
Usage: forge variables set [options] [key] [value]
```

## Options

```
1
2
3
4
5
--verbose                        enable verbose mode
--encrypt                        encrypt variable (default: false)
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
-h, --help                       display help for command
```

## Operation

The `forge variables set` command allows you to set app-specific environment variables for each environment in which the app is run. Forge provides a `development`, `staging`, and `production` environment for each app, but you can create more environments through `forge environments create`.

When you run `forge variables set` without an environment option (`--environment` or `-e`), the command sets the variables in your *default environment*. Your default environment is set the first time you run an environment-specific command.

Encrypted Forge environment variables allow you to securely store secrets.

Forge environment variables are useful when your app requires different configurations depending on the environment in which it is running. You can either set the individual configuration parameters in variables for each environment, or configure them in code grouped by the environment name and use a Forge environment variable to select the set of configuration values to use.

Forge environment variables are associated with a single app and environment context. Deploying the app to another environment won’t copy the environment variables across to the new environment context.

## Examples

```
```
1
2
```



```
forge variables set EXT_SERVICE_PORT 3000
```
```

This command stores the value `3000` for the key `EXT_SERVICE_PORT` (in cleartext) in your app's Forge environment variables. Since no environment (`--environment`) is specified, the environment variable will be stored in your default environment.

```
```
1
2
```



```
forge variables set --encrypt --environment production EXT_SERVICE_KEY "jIexOA3wwT8gRJlP"
```
```

This command encrypts then stores the value `jIexOA3wwT8gRJlP` for the key `EXT_SERVICE_KEY` in the app's Forge environment variables for the `production` environment. The value is received by Atlassian in cleartext and encrypted on Atlassian's servers before storage.

After setting or updating an environment variable with forge variables set, you must run `forge deploy` for the changes to take effect in your deployed app. Environment variable updates are not applied until the next deployment. Redeploying your app will ensure your app uses the latest values in its runtime environment.

## Troubleshooting

### Environment variable changes aren’t reflected in my app

After you set or update an environment variable with `forge variables set`, you need to redeploy your app with `forge deploy` for the changes to take effect. The new or updated variable values are only available after deployment.
If your app is still using the old value, make sure you’ve redeployed to the correct environment.

### I can’t find the environment variable I set

If you don’t see an environment variable you’re sure you set, check the variables for other environments. By default, Forge uses your default environment unless you specify one with the `-e` flag. The variable might have been set in a different environment than you expected.
