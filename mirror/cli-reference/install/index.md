# install

## Description

manage app installations

## Usage

```
1Usage: forge install [options] [command]
2
```

## Options

```
1--verbose                          enable verbose mode
2--app-id-override <appId>          App ID to use (skips reading from manifest)
3-e, --environment [environment]    specify the environment (see your default
4                                   environment by running forge settings list)
5-s, --site [site]                  site URL (example.atlassian.net)
6-p, --product [Atlassian app]      Atlassian app (Jira, Confluence, Compass,
7                                   Bitbucket)
8-d, --demo-site                    install onto your demo site instead of a
9                                   site passed with --site
10--upgrade [target]                 upgrade an existing installation (allowed
11                                   values: all (default), code)
12--confirm-scopes                   skip confirmation of scopes for the app
13                                   before installing or upgrading the app
14                                   (default: false)
15-l, --license [license]            specify the license value for the app
16                                   (allowed values: active, standard,
17                                   advanced, inactive, and trial)
18--license-modes [licenseModes...]  specify the list of license mode value for
19                                   the app (allowed values: user-access)
20--users-with-access [user...]      specify the list of Atlassian Account
21                                   IDs(aaid) for users who have access to the
22                                   app
23--major-version <majorVersion>     specify the major version to install
24--non-interactive                  run the command without input prompts
25-h, --help                         display help for command
26
```

## Commands

```
```
1
2
```



```
list [options]                     list app installations
```
```
