# containers get-login

## Description

get login password for the image repository

## Usage

```
1
Usage: forge containers get-login [options]
```

## Options

```
1
2
3
--verbose        enable verbose mode
--password-only  display only the password
-h, --help       display help for command
```

## Operation

This command is used with Forge Containers, which is currently available under
[Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap).
EAPs are offered to selected users for testing and feedback purposes.

APIs and features under EAP are:

* Unsupported and subject to change without notice
* Not recommended for use in production environments

Use `forge containers get-login` to retrieve a temporary API token, which can be used for authenticating with the Forge Containers registry
(namely, `forge-ecr.services.atlassian.com`).

Use this token with your image management tools. For example, use the token with `podman login` to `https://docs.podman.io/en/v5.1.0/markdown/podman-login.1.html` first with the Forge Containers registry; afterwards, you can use `podman push` to `https://docs.podman.io/en/v2.1.1/markdown/podman-push.1.html`.

The `forge containers get-login` command must be run in the app's *root folder* (that is, where the manifest file is located).

For a complete list of `forge containers` subcommands, refer to the command's [reference](/platform/forge/cli-reference/containers/#operation).

## Login session

The API token provided by `forge containers get-login` authenticates a login session that:

* Is app-specific
* Expires after 12 hours
* Becomes invalid once the app is updated

## Example

With `podman login`:

```
```
1
2
```



```
forge containers get-login --password-only | podman login --username AWS --password-stdin forge-ecr.services.atlassian.com
```
```

## Further information
