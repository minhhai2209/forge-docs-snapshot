# variables list

## Description

list the environment variables

## Usage

```
1
Usage: forge variables list [options]
```

## Options

```
1
2
3
4
5
6
--verbose                        enable verbose mode
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--json                           output results in JSON format (default:
                                 false)
-h, --help                       display help for command
```

## Operation

The `forge variables list` command displays all environment variables set for your app through the `forge variables set` command. When you run `forge variables list` without an environment option (`--environment` or `-e`), the command returns the variables from your *default environment*. Your default environment is set the first time you run an environment-specific command.

The values of encrypted Forge environment variables will not be displayed.

Forge environment variables are associated with a single app and environment context.
Deploying the app to another environment won’t copy the environment variables across to the new environment context.

## Examples

This displays the values of Forge environment variables set in your default environment.

```
```
1
2
```



```
forge variables list -e production
```
```

This command displays the values of Forge environment variables set in the `production` environment.

## Troubleshooting

If you don't see environment variables that you're certain you've set, check the variables for other environments. Forge uses your default environment if you don't specify one, so variables meant for another environment might have been unintentionally applied there.
