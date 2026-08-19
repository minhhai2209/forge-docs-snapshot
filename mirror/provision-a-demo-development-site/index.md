# Provision a demo development site

Forge can provision a demo development site when you need an Atlassian site for developing and
testing an app. A demo site is a fully featured Atlassian cloud site with realistic seeded data and enterprise editions of Jira, Confluence, Jira Service Management, and Rovo.

## Before you begin

Install the latest version of the Forge CLI and [log in](/platform/forge/getting-started/#log-in-with-an-atlassian-api-scoped-token).

```
1
2
npm install -g @forge/cli@latest
forge login
```

## Provision a site

To provision a demo site before installing an app, run:

If you already have an active demo site, the CLI returns that site instead of provisioning another
one. Otherwise, the CLI requests a site and displays its provisioning status. When the site is ready,
the CLI displays its name, URL, status, and expiry date.

You can press **Ctrl+C** while waiting without cancelling the provisioning request. Provisioning
continues in the background. Run `forge site provision` again later to display the active site.

## Install an app to your demo site

Deploy your app first. Deploying an app does not provision a site.

Install the deployed app to your demo site:

```
```
1
2
```



```
forge install --demo-site
```
```

You can also use the short form:

The CLI resolves your latest active demo site. If you don't have one, it offers to provision one,
waits until it is ready, and then continues the standard installation flow.

You can't combine `--demo-site` with `--site`. To install to a specific traditional development
site, run `forge install --site <site>` instead.

## Demo site lifecycle

Only one active demo site is assigned to each developer. You can use the same site to develop and
test multiple Forge apps.

Demo sites are active for 90 days by default. The CLI doesn't extend or deactivate sites.

Deactivating a demo site doesn't uninstall an app from other Atlassian sites. Running
`forge uninstall` removes the selected app installation but doesn't deactivate the demo site.

## Troubleshooting

### The site command isn't available

Update to the latest Forge CLI. If the command is still unavailable, you can continue to use a
[traditional Atlassian cloud developer site](http://go.atlassian.com/cloud-dev).

### Provisioning continues after you close the terminal

Provisioning is handled in the background. Run `forge site provision` again to check whether your
site is ready.

### Your demo site has expired or was deactivated

Run `forge site provision` to request a new active site.

### No sites are currently available

The demo-site pool can temporarily reach capacity. Retry `forge site provision` later, or install
your app to a traditional development site with `forge install --site <site>`.
