# register

## Description

register an app you didn't create so you can run commands for it

## Usage

```
1
Usage: forge register [options] [name]
```

## Options

```
1
2
3
--verbose                                      enable verbose mode
-s, --developer-space-id <Developer Space id>  specify the Developer Space id to use
-h, --help                                     display help for command
```

## Operation

Forge contacts an Atlassian service to register the specified app, sets the owner to the Atlassian `accountId` that is running the `register` command, and updates the manifest with a new app ID.

If the app has already been registered with Atlassian due to previously running `forge create` or `forge register`, running `forge register` again updates the manifest with a new app ID for your app and sets your account as the owner of the app with that ID. It does not affect the earlier registration of the app.

If you run `register` multiple times for an existing app, the app will be disconnected from all environments, stored variables, provider client secrets, and storage associated with the previous app IDs and environments. Doing this is only advisable for a very limited set of use cases, such as an app under development that has not been deployed to multiple environments yet.

## Examples

```
```
1
2
```



```
forge register macro-hello-world
```
```

Registers the `macro-hello-world` Forge app with Atlassian.

## Troubleshooting

* If you have created an app without running `forge create`, such as by copying an existing app's source tree, and are receiving errors at deploy or install time, you must initialize the app by running `forge register` instead of `forge create`.
* If you find that you your app has lost access to stored settings, environment variables, and storage because you accidentally ran `register` more than once and want to reset your app to a previous registration, replace the app id field in the `manifest.yml` file with the previous app ID.
* If you see an error message indicating that the "name" argument is either null or has a length greater than 50 when you are registering a new app, run the command again with an app name containing between 1 and 50 characters.
