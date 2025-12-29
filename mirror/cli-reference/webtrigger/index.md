# webtrigger

## Description

manage webtriggers

## Usage

```
1
Usage: forge webtrigger [options] [command]
```

## Options

```
1
2
--verbose         enable verbose mode
-h, --help        display help for command
```

## Commands

```
1
2
3
4
create [options]  get a web trigger URL
delete [options]  delete a webtrigger URL
help [command]    display help for command
list [options]    list webtrigger URLs
```

## Operation

The `forge webtrigger create` command provides you with a web trigger URL for a Forge function. To do this, you must first configure the function to be invoked by a web trigger in your app's `manifest.yml` file. See [Web trigger API](https://developer.atlassian.com/platform/forge/runtime-reference/web-trigger-api/) for instructions on how to do that.

After successfully deploying and configuring the Forge function, you can now run `forge webtrigger create`. This command requires:

* The `key` of the Forge function (from the manifest), that will be invoked with a web trigger.
* The installation context of the installation in which the Forge function will run. This includes the site, Atlassian app and Forge environment contexts in which your app is installed, visible by running `forge install list` in your app's top-level directory.

The command uses this information to generate and display a URL that can be used to invoke that function in that particular installation. Running `forge webtrigger create` multiple times for the same installation context and function will display the same URL.

### Authentication

By default, Forge does not authenticate web trigger URLs. You’ll need to implement your own authentication inside the trigger itself. For example, you can add a check for an `Authorization` header in the request and validate any provided token.

## Examples

```
```
1
2
```



```
forge webtrigger create
```
```

This will prompt you for the installation context (where your function will run) and the webtrigger function to invoke. The command will then generate and display a URL you can use to invoke that function.

```
```
1
2
```



```
forge webtrigger create --functionKey <function-key-from-manifest>
```
```

This lets you directly enter the key of the Forge function to invoke, then prompts you for the installation context. The command will then generate and display a URL you can use to invoke that function.

## Troubleshooting

When using a significant number of granular scopes, the authorization flow for OAuth 2.0 apps and the `webTrigger.getUrl` Forge requests may fail with a 414 Request-URI Too Large response, a 500 status code, a java exception for `request header is too large` or the error `Failed to get web trigger URL: Request Entity Too Large`.

To address this, use a smaller number of granular scopes or use non-granular scopes.

## Further information

* [forge install list](https://developer.atlassian.com/platform/forge/cli-reference/install-list/) - Reference for the `forge install list` command, which you use to view the installation contexts your app is installed in.
