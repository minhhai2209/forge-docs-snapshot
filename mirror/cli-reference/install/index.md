# install

## Description

manage app installations

## Usage

```
1
Usage: forge install [options] [command]
```

## Options

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
17
18
19
20
21
22
--verbose                          enable verbose mode
-e, --environment [environment]    specify the environment (see your default
                                   environment by running forge settings list)
-s, --site [site]                  site URL (example.atlassian.net)
-p, --product [Atlassian app]      Atlassian app (Jira, Confluence, Compass,
                                   Bitbucket)
--upgrade [target]                 upgrade an existing installation (allowed
                                   values: all (default), code)
--confirm-scopes                   skip confirmation of scopes for the app
                                   before installing or upgrading the app
                                   (default: false)
-l, --license [license]            specify the license value for the app
                                   (allowed values: active, standard,
                                   advanced, inactive, and trial)
--license-modes [licenseModes...]  specify the list of license mode value for
                                   the app (allowed values: user-access)
--users-with-access [user...]      specify the list of Atlassian Account
                                   IDs(aaid) for users who have access to the
                                   app
--major-version <majorVersion>     specify the major version to install
--non-interactive                  run the command without input prompts
-h, --help                         display help for command
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
