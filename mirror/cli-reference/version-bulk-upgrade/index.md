# version bulk-upgrade

## Description

upgrades installations from one major version to another version.

## Usage

```
1
Usage: forge version bulk-upgrade [options] [command]
```

## Options

```
1
2
--verbose         enable verbose mode
-h, --help        display help for command
```

## Commands

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
cancel [options]  cancels a version upgrade that is in progress.
help [command]    display help for command
list [options]    returns a summary of version update requests. Details include:
 - upgrade ID
 - upgrade request status
 - start date
 - completed date
 - from version
 - to version
 - number of updates completed
 - number of updates pending
 - number of updates failed
start [options]   upgrades installations using one major version to another version. The version selection list displays:
 - major version number
 - deployment date
 - number of installations
```

## Operation

The `forge version bulk-upgrade` command lets you upgrade a maximum of 500 installations in 1 request.
This allows you to safely migrate large sets of customers simultaneously, and verify that the app is working correctly for them.

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

Once a batch of 500 installations is upgraded, you can verify that the upgrade has completed successfully and start migrating another batch.

## Limitations

When using this command, it's important to be aware of several limitations that may affect its usage:

* Apps are limited to one concurrent bulk upgrade per environment.
* Developers will be limited to one concurrent bulk upgrade per Atlassian account.
* A global limit will be enforced on global concurrent bulk upgrades.

If you find that you've hit the global limit for concurrent bulk upgrades, wait 30 minutes and retry.

## Further information
