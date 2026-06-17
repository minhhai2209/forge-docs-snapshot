# version compare

## Description

returns the details of two versions of the app for comparison. Details include:

* deployment date
* egress
* analytics
* policies
* scopes
* connect keys
* functions
* remotes
* modules
* license

## Usage

```
1
Usage: forge version compare [options]
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
--verbose                        enable verbose mode
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--non-interactive                run the command without input prompts
--version1 <version>             1st version to compare
--version2 <version>             2nd version to compare
--environment1 <environment>     1st environment to compare
--environment2 <environment>     2nd environment to compare
-f, --out-file <outFile>         specify a file to output the results
-h, --help                       display help for command
```
