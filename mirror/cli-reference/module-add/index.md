# module add

## Description

[Preview] add a module to your Forge App. ⚠️ This will modify your app files
(manifest.yml, source files, and package.json).

## Usage

```
1Usage: forge module add [options]
2
```

## Options

```
1--verbose                         enable verbose mode
2-t, --module-type <type>          module type to add (e.g. jira:issuePanel,
3                                  jiraServiceManagement:portalFooter,
4                                  confluence:macro, etc.)
5-u, --ui-type <ui-kit|custom-ui>  UI framework (ui-kit, custom-ui)
6-p, --product <product>           target product (Jira, Jira Service
7                                  Management, Confluence, etc.)
8--dry-run                         show what would be generated
9--force                           overwrite existing files and upgrade
10                                  conflicting dependencies to template
11                                  versions
12--variables <json>                template variables as a JSON object, e.g.
13                                  '{"moduleKey":"my-panel","title":"My
14                                  Panel"}'. Implies --non-interactive
15                                  (requires -t/--module-type)
16--no-install                      skip installing dependencies
17--non-interactive                 run the command without input prompts
18-h, --help                        display help for command
19
```
