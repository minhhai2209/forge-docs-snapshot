# variables list

## Description

list the environment variables

## Usage

```
1Usage: forge variables list [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-e, --environment [environment]  specify the environment (see your default
3                                 environment by running forge settings list)
4--json                           output results in JSON format (default:
5                                 false)
6-h, --help                       display help for command
7
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
