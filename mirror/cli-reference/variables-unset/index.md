# variables unset

## Description

remove an environment variable

## Usage

```
1Usage: forge variables unset [options] <key>
2
```

## Options

```
1--verbose                        enable verbose mode
2-e, --environment [environment]  specify the environment (see your default
3                                 environment by running forge settings list)
4-h, --help                       display help for command
5
```

## Operation

The `forge variables unset` command allows the developer to remove (unset) an app-specific environment variable from a specific environment (for example, `development` or `staging`).
When you run `forge variables unset` command without an environment option (`--environment` or `-e`), the command unsets the variables in your *default environment*. Your default environment is set the first time you run an environment-specific command.

## Examples

```
```
1
2
```



```
forge variables unset EXT_SERVICE_PORT
```
```

This command removes the Forge environment variable `EXT_SERVICE_PORT` and its value from your app's default environment.

```
```
1
2
```



```
forge variables unset -e production EXT_SERVICE_PORT
```
```

This command removes the Forge environment variable `EXT_SERVICE_PORT` and its value from your app's `production` environment.

## Troubleshooting

If you don't see environment variables that you're certain you've set, check the variables for other environments. Forge uses your default environment if you don't specify one, so variables meant for another environment might have been unintentionally applied there.
