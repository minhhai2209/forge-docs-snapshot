# eligibility

## Description

check if your app is eligible for certain programs like Runs on Atlassian

## Usage

```
1
Usage: forge eligibility [options]
```

## Options

```
1
2
3
4
5
6
--verbose                        enable verbose mode
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--non-interactive                run the command without input prompts
-v, --major-version [version]    specify a major version
-h, --help                       display help for command
```

## Operation

The `forge eligibility` command allows you to check if your app is eligible or not for the
Runs on Atlassian program. If not eligible, the output of the command displays a list of reasons
as well.

## Further information

See [this documentation](/platform/forge/runs-on-atlassian/) for more information
on the Runs on Atlassian program.
