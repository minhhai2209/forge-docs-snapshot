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
