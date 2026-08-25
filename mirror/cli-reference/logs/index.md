# logs

## Description

view app logs

## Usage

```
1Usage: forge logs [options]
2
```

## Options

```
1--verbose                          enable verbose mode
2-e, --environment [environment]    specify the environment (see your default
3                                   environment by running forge settings list)
4-i, --invocation <invocation>      view logs for a given invocation ID
5-n, --limit <limit>                number of log lines to return
6-s, --since <since>                view logs since the specified time. valid
7                                   formats: YYYY-MM-DD, ISO 8061 timestamp or
8                                   a relative time (e.g: 5m, 10h, 2d)
9-g, --grouped                      group logs by invocation ID (default:
10                                   false)
11-c, --containerKey <containerKey>  view logs for a given container
12--instance <instance>              view logs for a given container instance
13--serviceKey <serviceKey>          view logs for a given service
14-f, --functionKey <functionKey>    view logs for a given function
15-h, --help                         display help for command
16
```
