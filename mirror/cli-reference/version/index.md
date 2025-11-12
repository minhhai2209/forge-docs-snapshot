# version

## Description

app version information

## Usage

```
1
Usage: forge version [options] [command]
```

## Options

```
1
2
--verbose               enable verbose mode
-h, --help              display help for command
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
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
bulk-upgrade [options]  upgrades installations from one major version to
                        another version.
compare [options]       returns the details of two versions of the app for comparison. Details include:
 - deployment date
 - egress
 - analytics
 - policies
 - scopes
 - connect keys
 - functions
 - remotes
 - modules
 - license
details [options]       returns the details of a specific version of the app. Details include:
 - egress
 - analytics
 - policies
 - scopes
 - connect keys
 - functions
 - remotes
 - modules
 - license
help [command]          display help for command
list [options]          returns a summary of all major versions of the app. Summary includes:
 - version number
 - deployment date
 - egress
 - analytics
 - policies
 - scopes
 - connect keys
 - functions
 - remotes
 - modules
 - license
```
