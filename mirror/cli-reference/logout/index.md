# logout

## Description

log out of your Atlassian account

## Usage

```
1
Usage: forge logout [options]
```

## Options

```
1
2
--verbose   enable verbose mode
-h, --help  display help for command
```

## Operation

This command removes the Atlassian account credentials that were added to your local credentials store by your most recent `forge login`. After you run `forge logout`, you will not be able to use Forge commands that
require authentication until you have run `forge login` again or set your credentials in environment variables.

* If you are using Forge on a shared computer like a server, it is best practice to log out of Forge when you've finished the task you were doing.
* If you work on multiple Forge apps and use different Atlassian accounts for each one, remember to log out of your account after working on an app.

* [login](https://developer.atlassian.com/platform/forge/cli-reference/login) - Forge login command reference page
