# logs

## Description

view app logs

## Usage

```
1
Usage: forge logs [options]
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
--verbose                        enable verbose mode
-c, --containers                 view container logs (default: false)
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
-i, --invocation <invocation>    view logs for a given invocation ID
-n, --limit <limit>              number of log lines to return
-s, --since <since>              view logs since the specified time. valid
                                 formats: YYYY-MM-DD, ISO 8061 timestamp or a
                                 relative time (e.g: 5m, 10h, 2d)
-g, --grouped                    group logs by invocation ID (default: false)
-h, --help                       display help for command
```
