# containers docker-login

## Description

authenticate to container registry

## Usage

```
1
Usage: forge containers docker-login [options]
```

## Options

```
1
2
--verbose   enable verbose mode
-h, --help  display help for command
```

## Operation

This command is used with Forge Containers, which is currently available under
[Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap).
EAPs are offered to selected users for testing and feedback purposes.

APIs and features under EAP are:

* Unsupported and subject to change without notice
* Not recommended for use in production environments

Use `forge containers docker-login` to retrieve a temporary API token, which can be used for authenticating with the Forge Containers registry
(namely, `forge-ecr.services.atlassian.com`).

You can use this token specifically for authenticating a *locally installed docker CLI*; if you use a different image management tool, [use `forge containers get-login` instead](/platform/forge/cli-reference/containers-get-login/).

The `forge containers docker-login` command must be run in the app's *root folder* (that is, where the manifest file is located).

For a complete list of `forge containers` subcommands, refer to the command's [reference](/platform/forge/cli-reference/containers/#operation).

## Login session

The API token provided by `forge containers docker-login` authenticates a login session that:

* Is app-specific
* Expires after 12 hours
* Becomes invalid once the app is updated

## Further information
