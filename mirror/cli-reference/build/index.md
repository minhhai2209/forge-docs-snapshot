# build

## Description

build and upload your app

## Usage

```
1Usage: forge build [options] [command]
2
```

## Options

```
1--verbose          enable verbose mode
2-f, --no-verify    disable pre-build checks
3-t, --tag <tag>    specify a custom build tag for build
4--inspect          save application bundle for inspection
5--non-interactive  run the command without input prompts
6-h, --help         display help for command
7
```

## Commands

```
1list [options]     list builds for your app
2
```

## Operations

The `forge build` command packages your app's code and uploads it to the Forge platform. Each build is assigned a unique, immutable, and case-insensitive tag, either generated automatically or provided by the user. Builds are environment-agnostic, allowing deployment to any environment.

Manifests containing environment variables are not presently supported by this command.

By default, this command:

1. Runs pre-build checks (such as `forge lint`) and reports any compilation errors.

Builds that are not actively deployed to any environment are retained for a minimum of 30 days from either the date they were last deployed or, if never deployed, the date they were created. After this period, they may be subject to cleanup. However, builds that are actively deployed will not be cleaned up as long as they remain deployed.

## Example

This command bundles your app's code, uploads it to the Forge platform, and generates a unique 36-character UUID tag to reference the build.

```
```
1
2
```



```
forge build --tag 3f6f3d
```
```

This command bundles your app's code, uploads it to the Forge platform, and assigns the build tag `3f6f3d`.

### Build Tag Constraints

* Must be unique to this app.
* Can be up to 64 characters long.
* Is case-insensitive
* Must start with an alphanumeric character.
* Can only contain alphanumeric characters, hyphens, underscores, and periods.
