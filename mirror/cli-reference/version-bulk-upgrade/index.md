# version bulk-upgrade

## Description

upgrades installations from one major version to another version.

## Usage

```
1Usage: forge version bulk-upgrade [options] [command]
2
```

## Options

```
1--verbose         enable verbose mode
2-h, --help        display help for command
3
```

## Commands

```
1start [options]   upgrades installations using one major version to another version. The version selection list displays:
2 - major version number
3 - deployment date
4 - number of installations
5list [options]    returns a summary of version update requests. Details include:
6 - upgrade ID
7 - upgrade request status
8 - start date
9 - completed date
10 - from version
11 - to version
12 - number of updates completed
13 - number of updates pending
14 - number of updates failed
15cancel [options]  cancels a version upgrade that is in progress.
16
```

## Operation

The `forge version bulk-upgrade` command lets you upgrade a maximum of 1800 installations in 1 request.
This allows you to safely migrate large sets of customers simultaneously, and verify that the app is working correctly for them.

The `forge version bulk-upgrade` command is separate from [Rolling releases](/platform/forge/rolling-releases/). For rolling release code rollouts, use Developer Console. See [View app rollouts](/platform/forge/view-app-rollouts/) for details.

For example, to initiate a bulk migration on all apps in `production`:

1. Run the following command.

   ```
   ```
   1
   2
   ```



   ```
   forge version bulk-upgrade start --environment production
   ```
   ```

   This command will display a list of installations for each version in an interactive table.
2. On the interactive table, select the version that needs to be upgraded. Doing so will let you see the target versions which installations can be upgraded to.
3. Once the target version is selected, this will return the `requestId`.

You can then use the `requestId` to track the status of your request through the `list` subcommand:

```
```
1
2
```



```
forge version bulk-upgrade list --environment production
```
```

This will return details for the currently running request, including the number of updates completed, pending, and failed.

Once a batch of 1800 installations is upgraded, you can verify that the upgrade has completed successfully and start migrating another batch.

## Setting upgrade limits

To control how many installations are upgraded in a single bulk-upgrade request:

```
```
1
2
```



```
forge version bulk-upgrade start --environment production --limit 500
```
```

If you do not specify a limit parameter, you will be prompted as part of the CLI's interactive flow.

If you specify a limit higher than the maximum allowed per bulk-upgrade request, it will be automatically reduced to the maximum allowed value. You'll receive a warning showing the adjusted limit.

## Limitations

When using this command, it's important to be aware of several limitations that may affect its usage:

* Apps are limited to one concurrent bulk upgrade per environment.
* Developers will be limited to one concurrent bulk upgrade per Atlassian account.
* A global limit will be enforced on global concurrent bulk upgrades.
* For apps that use [Forge Container services](/platform/forge/containers-reference/), some installations may not upgrade successfully. If this happens, retry to complete the upgrade.

If you find that you've hit the global limit for concurrent bulk upgrades, wait 30 minutes and retry.

## Further information
