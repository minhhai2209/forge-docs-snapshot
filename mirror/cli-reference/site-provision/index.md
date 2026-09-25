# site provision

## Description

provision a demo site for development and testing

## Usage

```
1Usage: forge site provision [options]
2
```

## Options

```
1--verbose   enable verbose mode
2-h, --help  display help for command
3
```

## Operation

Run `forge site provision` to request a demo development site. If you already have an active demo
site, the CLI displays that site instead of provisioning another one.

The command displays provisioning status while it waits. You can press **Ctrl+C** without cancelling
the provisioning request. Run the command again later to display the site when it is ready.

Demo sites are active for 90 days by default.

For the complete workflow, see
[Provision a demo development site](/platform/forge/provision-a-demo-development-site/).
