# assistant

## Description

[⚠️ experimental feature] manage AI assistant settings (Rovo/Gemini)

## Usage

```
1
Usage: forge assistant [options] [command]
```

## Options

```
1
2
--verbose            enable verbose mode
-h, --help           display help for command
```

## Commands

```
1
2
3
4
5
6
on [options] <name>  [⚠️ experimental feature] enable AI assistant for error
                     analysis (specify name: rovo or gemini)
                     When errors occur during Forge command execution, error
                     details will be sent to your AI agent to help you
                     understand and resolve issues.
off [options]        disable AI assistant for error analysis
```
