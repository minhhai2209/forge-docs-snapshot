# Forge changelog

You can now use the Forge CLI to provision a demo development site and install your app directly to it. A demo development site is a One Atlassian environment containing realistic seeded data and enterprise editions of Jira, Confluence, Jira Service Management, and Rovo.

## What’s changing

You can provision or retrieve your active demo development site by running:

`forge site provision`

If you already have an active demo site, the CLI returns it instead of provisioning another one. Otherwise, the CLI requests a new site and displays its provisioning status.

You can also deploy and install your app directly to your demo site:

`forge deploy
forge install --demo-site`

The short form of `--demo-site` is `-d`:

`forge install -d`

If you don’t have an active demo site when running `forge install --demo-site`, the CLI offers to provision one before continuing with the standard installation flow.

Key details include:

**Site allocation:** Each developer can have one active demo development site. You can use the same site to develop and test multiple Forge apps.

**Site lifecycle:** Demo sites are active for 90 days by default.

**Background provisioning:** You can press **Ctrl+C** while waiting without cancelling the provisioning request. Run `forge site provision` again later to check its status.

**Installation options:** You can’t combine `--demo-site` with `--site`. Existing `forge install` and `forge install --site <site>` workflows continue to support traditional Atlassian development sites.

## What you need to do

Update to the latest version of the Forge CLI:

`npm install -g @forge/cli@latest`

No action is required if you want to continue using an existing Atlassian development site.

To use a Forge demo development site, either provision one first with `forge site provision` or run `forge install --demo-site` after deploying your app.

For more information, see:
