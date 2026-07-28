# module add

## Description

[Preview] add a module to your Forge App. ⚠️ This will modify your app files
(manifest.yml, source files, and package.json).

## Usage

```
1
Usage: forge module add [options]
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
10
11
12
13
14
15
16
17
18
--verbose                         enable verbose mode
-t, --module-type <type>          module type to add (e.g. jira:issuePanel,
                                  jiraServiceManagement:portalFooter,
                                  confluence:macro, etc.)
-u, --ui-type <ui-kit|custom-ui>  UI framework (ui-kit, custom-ui)
-p, --product <product>           target product (Jira, Jira Service
                                  Management, Confluence, etc.)
--dry-run                         show what would be generated
--force                           overwrite existing files and upgrade
                                  conflicting dependencies to template
                                  versions
--variables <json>                template variables as a JSON object, e.g.
                                  '{"moduleKey":"my-panel","title":"My
                                  Panel"}'. Implies --non-interactive
                                  (requires -t/--module-type)
--no-install                      skip installing dependencies
--non-interactive                 run the command without input prompts
-h, --help                        display help for command
```
