# Runtime egress permissions

Using the capabilities discussed on this page may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program.
To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Having visibility and control over the external systems that your app communicates and shares
data with helps maintain the security of your app and your app users.

Runtime egress permissions apply to all Function as a Service (FaaS) functions, including
Custom UI resolvers.

## API redirects

Atlassian app API redirects are treated as internal traffic, as such they do not require egress declarations in your
app's manifest. Atlassian has already addressed all known instances of redirects, and you can now remove egress
declarations for internal domains like `api.media.atlassian.com`.

If you're using a third-party API that redirects to an external domain, you must declare the external domain in your
app's manifest.

If you encounter any issues with a redirect that you believe should be handled by Atlassian, please reach out to
[Atlassian support](https://ecosystem.atlassian.net/servicedesk/customer/portal/34)

## Define external domains in the manifest file

By default, if your Forge app is relying on a FaaS function that calls a third-party website
(using `axios` or any library that relies on `fetch` middleware), your app
invocation will fail.

To allow the calls to work, you must disclose these external domains by adding them as new entries
in the `permissions.external.fetch.backend` section of the `manifest.yml` file of your app.

For example, to allow calls to the third-party website `ingest.sentry.io`, use the
following configuration:

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - '*.ingest.sentry.io'
```
```

###### Example as an object

You can also define external domains as objects with additional properties:

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: false
```
```

## Update the manifest file

You must define the new entries in the `manifest.yml` file before you deploy the app.
See [Permissions](/platform/forge/manifest-reference/permissions/) to know how to define these new entries
in the `external` section.

Modifying these entries may result in a major version upgrade of your app. Your app users may again
be required to agree to the permissions of your app.

### Automatically update the manifest file

The CLI will automatically detect invalid configuration and the command `forge lint --fix` can be used to
add the missing entries in your manifest.

```
```
1
2
```



```
/Users/agrant/my-apps/hello-world-app/src/index.js
14:30   error    The domain https://www.google-analytics.com is not included in the external permissions of your app manifest  egress-permission-required

X 1 issue (1 error, 0 warnings)
  Run forge lint --fix to automatically fix 1 error and 0 warnings.
```
```

### Manually update the manifest file

1. Navigate to the top-level directory of your app and open the `manifest.yml` file.
2. In the `permissions` section, add and remove `external.fetch.backend` entries as needed.

   For example, add the *<https://www.google-analytics.com>* for the `external` fetch backend configuration.

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     external:
       fetch:
         backend:
           - 'https://www.google-analytics.com'
   ```
   ```
3. In the `index.js` file of your Forge app, you can now leverage the new configuration:

   ```
   ```
   1
   2
   ```



   ```
   import api from '@forge/api';
   // your google analytics config
   const measurement_id = `G-XXXXXXXXXX`;
   const api_secret = `<secret_value>`;
   const sendAnalytics = async () => {
     return await api.fetch(
       `https://www.google-analytics.com` +
       `/mp/collect?measurement_id=${measurement_id}` +
       `&api_secret=${api_secret}`,
       {
         body: JSON.stringify({
           // your analytics payload here
         })
       }
     )
   };

   sendAnalytics().then(() => console.log('success'));
   ```
   ```

   In this example, we're sending analytics events to Google API,
   via [Forge fetch](/platform/forge/runtime-reference/fetch-api/).
4. Run the `forge deploy` command to reflect these changes in your app.

### Validate entries via the forge lint command

You can use the `forge lint` command to help detect any invalid entries in the permissions of your app.
For example, Atlassian supports a limited number of
[external URL formats](/platform/forge/manifest-reference/permissions/#external-permissions).
If an invalid URL format is detected in your app permissions, the linter highlights the invalid URL,
and a recommendation to fix it, as shown in the example below:

```
```
1
2
```



```
/Users/agrant/my-apps/hello-world-app/manifest.yml
38:11   error    Invalid 'external.fetch.backend' permission in   manifest.yml file - 'https://example.com?test=key'. Learn  about   permissions at: http://go.atlassian.com/e-permissions.    valid-permissions-required
```
```

After fixing the URL, run `forge deploy` to deploy the changes. Note, if we detect major changes
in your app, you may need to complete the *Upgrade the app* section below to deploy the changes.

## Upgrade the app

A major version upgrade of your app may be needed for any of the following:

* Changes in `permissions`
* New egress controls
* Updates to the targets of existing permissions

Changes to the app’s permissions won’t take effect until the app is upgraded. If you’ve previously
deployed your app and a major change is detected, you’ll need to redeploy your app.

To upgrade your app:

1. Navigate to your app's top-level directory.
2. Start the upgrade by running:

   ```
   ```
   1
   2
   ```



   ```
   forge install --upgrade
   ```
   ```

   You’ll see output that’s similar to the following example:

   ```
   ```
   1
   2
   ```



   ```
   ┌───────────────┬──────────────────────────────┬────────────────┬─────────────┐
   │ Environment   │ Site                         │ Atlassian app  │ Scopes      │
   ├───────────────┼──────────────────────────────┼────────────────┼─────────────┤
   │ ❯ development │ example-dev.atlassian.net    │ Jira           │ Latest      │
   │   development │ example-dev.atlassian.net    │ Confluence     │ Latest      │
   │   production  │ example.atlassian.net        │ Confluence     │ Out-of-date │
   └───────────────┴──────────────────────────────┴────────────────┴─────────────┘
   ```
   ```
3. Select the `Out-of-date` installation to upgrade by using the arrow keys, and then press the enter key
   to upgrade the version of the app installed.
4. Wait for the *Upgrade successful* message to appear.

Make sure to repeat these steps for each `Out-of-date` installation listed for the site that
you're upgrading. After completing these steps, your app will now run with the implemented updates.

If you've previously shared the app via the developer console, users will need to upgrade the app
[via the installation link](/platform/forge/distribute-your-apps/#share-an-app-update)
or through the
[Universal Plugin Manager (UPM)](https://confluence.atlassian.com/upm/about-the-universal-plugin-manager-305759439.html).

If you've listed your app on the Atlassian Marketplace, you’ll need to publish the new version to
the Marketplace to update the egress controls of your app. After which, you'll need to ask your users
to uninstall and reinstall the app via its Marketplace listing.
