# autocomplete

## Description

configures autocomplete for the Forge CLI

## Usage

```
1Usage: forge autocomplete [options] [install|uninstall]
2
```

## Options

```
1--verbose   enable verbose mode
2-h, --help  display help for command
3
```

## Operation

The `autocomplete` command is available for zsh and bash shells. Installation adds a line to your shell initialization file that enables autocomplete in new shell sessions. Running `autocomplete uninstall` removes the line.

When the `autocomplete` command is installed, press **Tab** to complete commands and options as you enter them. Autocompletion isn’t supported for subcommands (for example, `forge variables list`).

## Examples

```
```
1
2
```



```
forge autocomplete install
```
```

Installs Forge CLI `autocomplete`, updating the shell initialization file to enable it when you next start a shell.

The command interactively advises you that it will modify the shell config file. You must reply `Y` for the installation to continue.

```
```
1
2
```



```
forge autocomplete uninstall
```
```

Uninstalls Forge CLI `autocomplete`.
