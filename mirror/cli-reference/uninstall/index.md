# uninstall

## Description

uninstall the app from an Atlassian site

## Usage

```
1Usage: forge uninstall [options]
2
```

## Options

```
1--verbose                               enable verbose mode
2-s, --site [site]                       site URL (example.atlassian.net)
3-p, --product [Atlassian app]           Atlassian app (Jira, Confluence, Compass, Bitbucket)
4-e, --environment [environment]         specify the environment (see your default environment by running forge settings list)
5--batch                                 select up to 10 installations to uninstall (default: false)
6-i, --installation-id <installationId>  specify the installation ID
7--app-id-override <appId>               App ID to use (skips reading from manifest)
8-h, --help                              display help for command
9
```

## Operation

This command lets you uninstall your app from a specified site. For example:

```
1forge uninstall --site example.atlassian.net
2
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
