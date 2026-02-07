# Prepare to build your first Forge app

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-getting-started)

Welcome to developing with the Forge platform for Atlassian cloud apps. Work through
the steps below to set up your development environment. To get started using Forge,
you’ll install the CLI, log in with an Atlassian API token, and create an Atlassian
developer site that has Confluence and all of the Jira applications installed.

After setting up, you'll go through a three-part tutorial to create a simple hello world app
for Bitbucket, Confluence, Jira, or Jira Service Management.

For more of an introduction to creating and managing an app with the Forge CLI, check out our [Atlassian Developer YouTube channel](https://www.youtube.com/@AtlassianDeveloper).

## Before you begin

Forge apps are written in JavaScript so you'll need to be familiar with JavaScript. It's also helpful to be familiar with React.

### Set up Node.js

The Forge CLI requires a fully supported LTS release of
Node.js installed; namely, versions 20.x, 22.x or 24.x.
Follow the Node.js setup instructions specific to your operating system below:

In this video, we'll walk you through installing the Atlassian Forge CLI on your Mac. Also, you'll find step-by-step written instructions on this page if you prefer to follow along at your own pace

Forge developers on macOS should use Node Version Manager (nvm) to configure
the environment.

1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating).
2. Select the latest Node.js LTS release by running the following in the terminal:

   ```
   1
   2
   nvm install --lts
   nvm use --lts
   ```

If `nvm` command doesn't work, try restarting the terminal.

1. Check your Node.js version, run the following in the terminal:

Which outputs your node version.

### (Optional) Node.js installer

Skip this step if you have successfully completed [Set up Node.js](/platform/forge/installing-forge-on-macos/#set-up-node-js) section.

You can install Node.js using the macOS installer, however this results in
permission errors when working with the Forge CLI. If you must use the installer,
you'll need to enable unsafe permissions to use the Forge global package when
installing Node.js using this method.

1. Download the LTS installer from [Node.js](https://nodejs.org/en/download/).
2. Install the package.
3. Configure npm, permitting unsafe permissions:

   ```
   ```
   1
   2
   ```



   ```
   npm config set unsafe-perm true
   ```
   ```

## Hello world CLI overview

After installing the Forge CLI, follow the prompts in the terminal to build a hello world app. For a complete explanation
of each step, continue reading along with the documentation.

![Hello world CLI overview](https://dac-static.atlassian.com/platform/forge/images/forge-cli-overview-without-description.png?_v=1.5800.1827)

## Install the Forge CLI

Install the Forge CLI using npm. You’ll install the CLI globally so that the commands
can be run across your system.

Do not install `forge` with `root` privileges. In case that has been done, you might need to uninstall forge.
This can be done using the command in mac (or similar in other OS)

```
```
1
2
```



```
sudo rm -rf ~/Library/Preferences/@forge
```
```

1. Install the Forge CLI globally by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install -g @forge/cli
   ```
   ```
2. Verify that the CLI is installed correctly by running:

You should see a version number reported in the terminal. If a version number is not shown, then the installation failed. Repeat step 1 and
look for errors reported in the terminal.

With the CLI installed, view the complete list of Forge commands by running `forge --help`.

## Log in with an Atlassian API token

Create or use an existing Atlassian API token to log in to the CLI. The CLI uses your
token when running commands.

1. Go to <https://id.atlassian.com/manage/api-tokens>.
2. Click **Create API token**.
3. Enter a label to describe your API token. For example, *forge-api-token*.
4. Click **Create**.
5. Click **Copy to clipboard** and close the dialog.

Log in to the Forge CLI to start using Forge commands.

Do not use `sudo` or root user when running `forge`. Doing so may cause issues with file permissions and ownership,
potentially leading Forge CLI not functioning properly when run by a non-privileged user.

1. Start the process by running:
2. You'll be asked whether to allow Forge to collect usage analytics data:

   ```
   ```
   1
   2
   ```



   ```
   Allow Forge to collect CLI usage and error reporting information?
   ```
   ```

   Answering `Yes` will allow Forge to collect data about your app's deployments and installations
   (including error data). This, in turn, helps us monitor Forge's overall performance and reliability.
   The collected data also helps us make better decisions on improving Forge's feature set and performance.

   For information about how Atlassian collects and handles your data, read our
   [Privacy Policy](https://www.atlassian.com/legal/privacy-policy).
3. Enter the email address associated with your Atlassian account.
4. Enter your Atlassian API token. You copied this to the clipboard in step 5.

You will see a message similar to this confirming you are logged in:

```
```
1
2
```



```
✔ Logged in as Mia Krystof
```
```

If you get some permission error, this might be due to installation of `forge` with root permissions.
Try removing forge installation and try to install without root permissions.

The Forge CLI uses your operating system's keychain to securely store your login details.
Any command after `forge login` that requires authentication will read your credentials
from the keychain. When this occurs, your keychain may prompt you for access; approve it to allow the
CLI to run the command.

On Linux, you'll need `libsecret` installed to perform this step.

### Using environment variables to login

If a keychain isn't available, you can store your login email and token through the environment variables `FORGE_EMAIL` and `FORGE_API_TOKEN`, respectively. In continuous integration environments, you can store these environment variables as secrets for your builds. For more information, read our tutorial on [setting up continuous delivery for Forge apps](/platform/forge/set-up-cicd/).

Otherwise, you can also set environment variables manually:

```
```
1
2
```



```
read FORGE_EMAIL
# Enter email
read -s FORGE_API_TOKEN
# Enter API token (will not be displayed)
export FORGE_EMAIL FORGE_API_TOKEN
```
```

This applies to all commands that require `forge login` to be run first.

* If you are using environment variables instead of the keychain, do not use the `forge login` command and proceed directly to utilizing other Forge commands.
* If you use environment variables to store your credentials, the Forge CLI will use them regardless of whether
  there are credentials stored in a local keychain.

## Next steps

You're all set up to build a Forge app in Bitbucket, Confluence, Jira, or Jira Service Management.
