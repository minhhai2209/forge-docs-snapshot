# webtrigger create

## Description

get a web trigger URL

## Usage

```
1Usage: forge webtrigger create [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-f, --functionKey <functionKey>  web trigger key from the manifest.yml file
3--readSecretKey                  read the secret key for an authenticated
4                                 (HMAC) web trigger from stdin
5--noKeyExpiry                    create the web trigger URL with a key that
6                                 does not expire
7-s, --site [site]                site URL (example.atlassian.net)
8-p, --product [Atlassian app]    Atlassian app (Jira, Confluence, Compass,
9                                 Bitbucket)
10-e, --environment [environment]  specify the environment (see your default
11                                 environment by running forge settings list)
12-h, --help                       display help for command
13
```
