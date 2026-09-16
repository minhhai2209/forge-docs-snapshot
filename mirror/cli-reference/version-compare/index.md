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
1Usage: forge version compare [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-e, --environment [environment]  specify the environment (see your default
3                                 environment by running forge settings list)
4--non-interactive                run the command without input prompts
5--version1 <version>             1st version to compare
6--version2 <version>             2nd version to compare
7--environment1 <environment>     1st environment to compare
8--environment2 <environment>     2nd environment to compare
9-f, --out-file <outFile>         specify a file to output the results
10-h, --help                       display help for command
11
```
