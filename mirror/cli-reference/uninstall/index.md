# uninstall

## Description

uninstall the app from an Atlassian site

## Usage

```
1
Usage: forge uninstall [options]
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
--verbose                        enable verbose mode
-s, --site [site]                site URL (example.atlassian.net)
-p, --product [Atlassian app]    Atlassian app (Jira, Confluence, Compass,
                                 Bitbucket)
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--batch                          select up to 10 installations to uninstall
                                 (default: false)
-h, --help                       display help for command
```

## Operation

This command lets you uninstall your app from a specified site. For example:

```
1
forge uninstall --site example.atlassian.net
```

### Batch uninstallation

You can also use the `--batch` option to uninstall your app from *all non-production* environments. This option is useful for clearing apps from multiple sites to make room for more apps.

For example, the following command will uninstall your app from sites across all non-production environments:

```
```
1
2
```



```
forge uninstall --batch
```
```

The `--batch` option also supports filtering by product and environment. For example, the following command will uninstall your app from all sites in the *staging* environment:

```
```
1
2
```



```
forge uninstall --batch --environment staging
```
```

The `forge uninstall --batch` command can only uninstall your app from up to 10 sites at a time. If you need to uninstall your app from more sites, you'll need to re-run the command again.
