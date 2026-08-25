# eligibility

## Description

check if your app is eligible for certain programs like Runs on Atlassian

## Usage

```
1Usage: forge eligibility [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-e, --environment [environment]  specify the environment (see your default
3                                 environment by running forge settings list)
4--non-interactive                run the command without input prompts
5-v, --major-version [version]    specify a major version
6-h, --help                       display help for command
7
```

## Operation

The `forge eligibility` command allows you to check if your app is eligible or not for the
Runs on Atlassian program. If not eligible, the output of the command displays a list of reasons
as well.

## Further information

See [this documentation](/platform/forge/runs-on-atlassian/) for more information
on the Runs on Atlassian program.
