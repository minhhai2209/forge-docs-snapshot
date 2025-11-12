# Add content security and egress controls

Using the capabilities discussed on this page may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program.
To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Having visibility and control over the external systems that your app communicates and shares data
with helps maintain the security of your app and your app users.

To do this, we require you to do the following:

1. Define the external domains your app will be communicating with.
2. Use custom Content Security Policies (CSP).

## Define the external domains in the manifest file

When using the Forge platform, you need to disclose the domains outside of Atlassian cloud
that your app will be sending data to and receiving data from. This includes actions being performed
on the frontend of your Custom UI app, for example, sending analytics payloads, or loading images from
a third-party website.

To disclose the domains, you need to include new entries in the `permissions.external` section
of the `manifest.yml` file of your app.

The following table outlines the different types of external resources your app can access:

| Resource Type | Description | Example declaration |
| --- | --- | --- |
| Fetch (Backend) | External domains Forge functions can communicate with. | ``` permissions:   external:     fetch:       backend:         - '*.example-dev.com'         - remote: remote-backend ``` |
| Fetch (Client) | External sources allowed for an app's connect-src policy. | ``` permissions:   external:     fetch:       client:         - '*.example-dev.com' ``` |
| Fonts | External sources allowed for an app's font-src policy. | ``` permissions:   external:     fonts:       - 'https://www.example-dev.com/fonts.css' ``` |
| Styles | External styles allowed for an app's style-src policy. | ``` permissions:   external:     styles:       - 'https://www.example-dev.com/stylesheet.css' ``` |
| Frames | External sources allowed for an app's frame-src policy. | ``` permissions:   external:     frames:       - 'https://www.example-dev.com/embed/page' ``` |
| Images | External sources allowed for an app's img-src policy. | ``` permissions:   external:     images:       - 'https://www.example-dev.com/image.png' ``` |
| Media | External sources allowed for an app's media-src policy. | ``` permissions:   external:     media:       - 'https://www.example-dev.com/video.mp4' ``` |
| Scripts | External sources allowed for an app's script-src policy. | ``` permissions:   external:     scripts:       - 'https://www.example-dev.com/script.js' ``` |

For additional details about external permissions, refer to the [external permissions](/platform/forge/manifest-reference/permissions/#external-permissions) documentation.

## Use custom content security policies

By default, Atlassian blocks any policies that are considered unsafe for your Custom UI app.
To include capabilities, such as `inline CSS`, you will need to declare these policies in the `manifest.yml` file
of your app. You can do this by including new entries in the `permissions.content` section
of the `manifest.yml` file.

For example, to allow inline CSS in your app, use the following configuration:

```
```
1
2
```



```
permissions:
  content:
    styles:
      - 'unsafe-inline'
```
```

## Update the manifest file

You must define the new entries in the `manifest.yml` file before you deploy the app.
See [Permissions](/platform/forge/manifest-reference/permissions/) to learn how to define these new entries
in both the `external` and `content` sections.

Modifying these entries may result in a major version upgrade of your app. Your app users may again
be required to agree to the permissions of your app. See the
[Upgrade the app](#upgrade-the-app)
section below for more details.

### Manually update the manifest file

1. Navigate to the top-level directory of your app and open the `manifest.yml` file.
2. In the `permissions` section, add and remove `content` and `external` entries as needed.

   For example, add the *unsafe-inline* `content` style CSP, and \**.giphy.com* for the `external` images.

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     content:
       styles:
         - 'unsafe-inline'
     external:
       images:
         - '*.giphy.com'
   ```
   ```
3. In the `index.html` file of your Custom UI app, you can now leverage the new configuration:

   ```
   ```
   1
   2
   ```



   ```
   <html>
       <body>
           <p style="color: blue; font-size: 46px;">Hello world!</p>
           <img src="https://media1.giphy.com/media/d2jioMTLON9bDogE/giphy.gif" />
       </body>
   </html>
   ```
   ```

   In the above example, we're using `inline CSS` to modify our style, as well as include an
   `image` from a third-party website.
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
38:11   error    Invalid 'external.fetch.client' permission in the manifest.yml file - 'https://example.com?test=key'. Learn more about permissions at: http://go.atlassian.com/forge-permissions.  valid-permissions-required
```
```

After fixing the URL, run `forge deploy` to deploy the changes.

If we detect major changes
in your app, you may need to complete the *Upgrade the app* section below to deploy the changes.

## Upgrade the app

A major version upgrade of your app may be needed for any of the following:

* Changes in `permissions`
* New egress controls
* Updates to the targets of existing permissions
* Addition of any CSPs in the `unsafe-*` category

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
you're upgrading. After completing these steps, your app is now running with the new updates.

If you've previously shared the app via the developer console, users will need to
[upgrade the app via the installation link](/platform/forge/distribute-your-apps/#share-an-app-update).

If you've listed your app on the Atlassian Marketplace, you’ll need to publish the new version to
the Marketplace to update the egress controls of your app. After which, you'll need to ask your users
to uninstall and reinstall the app via its Marketplace listing.
