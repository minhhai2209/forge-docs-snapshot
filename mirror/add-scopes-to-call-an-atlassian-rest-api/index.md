# Add scopes to call an Atlassian REST API

Your app needs to have the relevant `scopes` when:

When making Atlassian app API requests from a remote back end, your app also requires at least one of the `read:app-user-token` and `read:app-system-token` scopes
that allow the remote back end to call those calls under the identity of the current user or the identity of the
app's "bot" user. For information on these scopes, see [Permissions](/platform/forge/manifest-reference/permissions/).

## Update the manifest file

App scopes must be defined in the manifest file prior to deploying the app. See
[Permissions](/platform/forge/manifest-reference/permissions/) for detailed information
about each scope.

### Use the forge lint command

You can use the `forge lint` command to assist you with adding missing scopes in your app.

1. Navigate to the top-level directory of your app and run the following command:

   If your app has missing permissions, these will be highlighted individually in the output.

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
   The linter checks the app code for known errors. Warnings are problems you should
   fix, but that won't stop the app code from building.
   Press Ctrl+C to cancel.

   /src/index.jsx
     10:57   warning  Confluence endpoint: GET /api/content requires
     "read:confluence-content.summary" scope  permission-scope-required

   14:56   warning  Confluence endpoint: GET /api/content requires
     "read:confluence-content.summary" scope  permission-scope-required

   19:51   warning  Jira endpoint: GET /rest/api/3/user requires
     "read:jira-user" scope  permission-scope-required

   ⚠ 3 problems (0 errors, 3 warnings)
     Run forge lint --fix to automatically fix 0 errors and 3 warnings.
   ```
2. Rerun `forge lint` with the `--fix` argument to automatically add missing scopes to the
   `manifest.yml` file.

   The example below shows all three detected issues were fixed. You can rerun step 1
   to continue investigating outstanding errors.

   ```
   ```
   1
   2
   ```



   ```
   ✔ Fixed 0 errors and 3 warnings

   Run forge lint to review outstanding errors and warnings
   ```
   ```
3. Run `forge deploy` to deploy the above changes.
4. You'll need to complete the *Upgrade the app* section below to apply the changes.

### Manually update the manifest file

1. Navigate to the top-level directory of your app and open the `manifest.yml` file.
2. In the permissions section, add or remove `scopes` as needed. For example, add
   the *write:confluence-content* scope.

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     scopes:
       - write:confluence-content
   ```
   ```
3. Run `forge deploy` to deploy the above changes.
4. You'll need to complete the *Upgrade the app* section below to apply the changes.

## Upgrade the app

Changes to the app's scopes won't take effect until the app is upgraded.
If you've previously deployed your app, and you change the `scopes` in your manifest file,
you also need to redeploy your app before installing it.

1. Navigate to your app's top-level directory.
2. If you've changed the `scopes` in your manifest file since you last deployed your app, deploy
   your app again by running:
3. Start the upgrade by running:

   ```
   ```
   1
   2
   ```



   ```
   forge install --upgrade
   ```
   ```

   You’ll see output similar to the following example.

   ```
   ```
   1
   2
   ```



   ```
   ┌───────────────┬──────────────────────────────┬──────────────────┬─────────────┐
   │ Environment   │ Site                         │ Atlassian app    │ Scopes      │
   ├───────────────┼──────────────────────────────┼──────────────────┼─────────────┤
   │ ❯ development │ example-dev.atlassian.net    │ Jira             │ Latest      │
   │   development │ example-dev.atlassian.net    │ Confluence       │ Latest      │
   │   production  │ example.atlassian.net        │ Confluence       │ Out-of-date │
   └───────────────┴──────────────────────────────┴──────────────────┴─────────────┘
   ```
   ```
4. Select the `Out-of-date` installation to upgrade by using the arrow keys, and then press the enter key
   to upgrade the version of the app installed.
5. Wait for the *upgrade successful* message to appear.

Make sure that you repeat these steps for each `Out-of-date` installation listed for the site that you are upgrading. After completing these steps, your app runs with the updated scopes.
