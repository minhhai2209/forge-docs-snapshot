# Forge changelog

The `forge deploy` command now includes pre-deployment approval checks. Some changes, such as those triggering a major version upgrade, now require explicit developer acknowledgment before the deployment can proceed.

**What's changing**  
When you run `forge deploy`, the CLI linter (`forge lint`) now checks for conditions that require manual approval. A common example is a **major version upgrade**, which occurs when you modify app scopes. Because major upgrades require site administrators to manually approve the update, the CLI now asks you to acknowledge this impact.

If an approval is required, the deployment will pause and display the specific rule to approve (for example, `MAJOR_VERSION_RULE`).

To proceed with the deployment, you must run:

`forge deploy --approve <ruleName>`

**What you need to do**

For more information on why these approvals are required, see the documentation on [major version upgrades](https://developer.atlassian.com/platform/forge/versions/#major-version-upgrades "https://developer.atlassian.com/platform/forge/versions/#major-version-upgrades").
