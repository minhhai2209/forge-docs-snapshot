# login

## Description

log in to your Atlassian account

## Usage

```
1
Usage: forge login [options]
```

## Options

```
1
2
3
4
5
--verbose                 enable verbose mode
-u, --email <user email>  specify the email to use
-t, --token <api token>   specify the API token to use
--non-interactive         run the command without input prompts
-h, --help                display help for command
```

## Examples

```
1
forge login --user FORGE_EMAIL
```

Prompts you to enter an API token then logs you in to Forge with the specified credentials.

```
1
forge login --email FORGE_EMAIL --token FORGE_API_TOKEN
```

Logs you in to Forge with the specified credentials.

## Operation

The `forge login` command allows you to authenticate to Atlassian so that you can run Forge commands requiring an authenticated user. When you login, Forge stores your credentials in your computer' local credentials store, sometimes referred to as a keychain.

You can optionally provide your credentials by setting environment variables instead of using `forge login`. This method is often used when automating Forge tasks.

Both methods require that you specify an Atlassian API token as well as an email address that you have registered with Atlassian. If you do not yet have an Atlassian API token, go to [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) to obtain one.

The `--non-interactive` option causes the command to produce an error rather than prompt the user for values, if the `--email` or `--token` options are not provided on the command line.
It is rarely used in practice, as automation scripts generally use environment variables to set credentials.

## Troubleshooting

* If your login does not succeed, verify that you are using the email address associated with your Atlassian account and the correct API token.
* If you are certain that you are using the correct credentials and you are accessing Forge from behind a corporate firewall, you may need to use a proxy.
* If your login cannot access the credential store, verify that your keychain is running and accepts its prompts for access. See [Before you begin](https://developer.atlassian.com/platform/forge/getting-started/#before-you-begin) for more information.
* If your development environment doesn’t have a keychain (for example, Windows Subsystem for Linux or a Docker container), you can log in via [environment variables](https://developer.atlassian.com/platform/forge/getting-started/#using-environment-variables-to-login) instead. However, note that doing so will store your token in plaintext, which might be less secure than using a keychain.
