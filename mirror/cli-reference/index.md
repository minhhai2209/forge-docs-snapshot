# CLI overview

The Forge CLI is the command line interface for building and deploying Forge apps.

For detailed instructions on setting up your Forge development environment,
refer to our [getting started guide](/platform/forge/getting-started/#before-you-begin).

To install the CLI, run:

```
1npm i -g @forge/cli@latest
2
```

To log in, run:

## Local .forge directory

The Forge CLI and local runtime can create a `.forge` directory in your app's root directory during development. This is expected: it holds generated files and local working data for tasks such as tunneling and inspecting packaged code. Its contents depend on the commands you run and the features your app uses, and can change between CLI versions.

**Do not commit `.forge` to source control.** Add the following entry to your app's `.gitignore` file:

If files in this directory are already tracked by Git, adding an ignore rule does not untrack them. Run the following command from your app's root directory to stop tracking them while keeping your local files:

```
1git rm -r --cached .forge/
2
```

Commit the staged removals together with your `.gitignore` change. This does not remove files from Git history; if you have committed credentials, revoke or rotate them.

The directory can contain:

* Generated function code and runtime files used by the local tunnel.
* A copy of your packaged runtime code when you use `forge build --inspect` or `forge deploy --inspect`.
* Local application cache data.
* Generated configuration and authentication material used for container tunneling.

Treat these as CLI-managed files, not app source files to edit or share. They can contain sensitive information, including resolved app configuration and authentication tokens.

Stop any active tunnels before removing `.forge`. Generated files are recreated when needed, but removing the directory also discards local cache data and saved inspection output. Some files can remain after a command finishes.

## Upgrading

To upgrade the Forge CLI, completely remove the Forge CLI and install it again.

```
```
1
2
3
```



```
npm uninstall -g @forge/cli
npm i -g @forge/cli@latest
```
```

## Supported versions

Each CLI version will only be supported 6 months after release. After this period, the CLI version will be [no longer be supported](/platform/forge/deprecation-policy/#cli-version-support). We recommend regularly updating to the latest CLI version to benefit from new features and improvements.
