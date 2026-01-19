# Distribute your apps

When you’re ready to share your Forge app with users, you’ll need to enable sharing for your app
in the [developer console](/console/myapps/). This generates a link that you
can share with users to install your app on their Atlassian site.

In order to install it,
they must be the admin of an Atlassian app on that site.

Use this method to share your apps for internal use, or to test your apps
before [listing them on the Atlassian Marketplace](/platform/marketplace/listing-forge-apps/).

Apps that already have a
[license in the app manifest](/platform/marketplace/listing-forge-apps/#enabling-licensing-for-your-app)
or have been submitted for listing on Marketplace can't be shared via installation link;
in order to share and test these apps, you'll need to copy the app's code,
create a new, unlicensed version of the app, and share this version via installation link.

You can [stop sharing your app](/platform/forge/distribute-your-apps/#stop-sharing-your-app) at any time.

## Start sharing your app

1. Using the Forge CLI, [deploy your app to the production environment](/platform/forge/staging-and-production-apps/).
2. In the [developer console](/console/myapps/), choose the app you want to share.
3. Select **Distribution** in the left menu, and under 'Distribution controls', select **Edit**.
4. Select the **Sharing** option, fill in the app details, and select **Save changes**.
5. Select which Atlassian apps you want your user to install your app onto.

   * This affects where users can install your app. For example, if you select
     both Jira and Confluence, your user can only install it on sites running both Jira and
     Confluence.
   * You must tell your user to install it on both Atlassian apps; otherwise, it won't work as expected.
6. Copy the installation link and send it to your user.

When your user visits the link, an installation screen appears, similar to the one below.
It displays information about your app, including the permissions your app is requesting.
From here, your user can choose a site and an Atlassian app to install your app onto.

![User installation screen](https://dac-static.atlassian.com/platform/forge/images/user-installation-screen.png?_v=1.5800.1777)

## Restrict installation links

If you want to restrict or change who can install your app, you can
generate a new installation link. This disables the previous installation link.

Users with the previous link will no longer be able to install your app.
However, if they've already installed your app, they can continue to use it, and update it when you
release new versions.

This action can't be undone.

1. In the [developer console](/console/myapps/), choose the app you want to generate a new link for.
2. Select **Distribution** in the left menu.
3. Next to the installation link, select **Generate new link**.
4. A modal appears. If you’re happy to continue, select **Generate new link**.

## Stop sharing your app

If you want to stop sharing your app with users, you must disable sharing
in the developer console.

1. In the [developer console](/console/myapps/), choose the app you want to stop sharing.
2. Select **Distribution** in the left menu, and under 'Distribution controls', select **Edit**.
3. Select the **Not sharing** option, then select **Save changes**.

Your app is no longer being shared. This has the following effects:

* Users with the installation link will no longer be able to install your app.
* Users who have already installed your app can continue to use it.

You can start sharing your app again any time.

## Share an app update

You might want to deploy a new version of your app that includes updated scopes. Once you've
[deployed the new version to the production environment](/platform/forge/staging-and-production-apps/)
using the Forge CLI, users can:

* Update their forge apps through the
  [Connected apps page](https://support.atlassian.com/security-and-access-policies/docs/manage-your-users-third-party-apps/).
* Bitbucket forge apps can also be uninstalled or upgraded directly from the Bitbucket workspace settings.

If needed, you can copy the installation link from the developer console and send it to them again.

## Distributing an app update to existing installations

After deploying a new major version of your app, you might want to upgrade all installations of the app on an eligible older major version to the newer one.

You can use the [Forge CLI](/platform/forge/cli-reference/version/) to start, cancel and list these bulk major version updates, without site admin approval, with `forge version bulk-upgrade`.

Records from the Forge CLI are time-limited and may not be available indefinitely. It is advisable to document or monitor these records promptly if they are needed for future reference.

### Requirements for eligibility

Currently, [major version updates](/platform/forge/versions/#major-version-upgrades) may require users and admins to re-consent or review the changes before upgrading. For an update to be eligible for bulk distribution, it should adhere to the following criteria:

* The app must remain within the same environment.
* The target version must be greater than the source version.
* The new major version must not introduce new scopes or egress permissions that represent an escalation of privilege. The following changes are eligible for bulk upgrades:
* The new major version’s licensing information must remain unchanged.

### Limitations of the bulk upgrade feature

When considering the bulk upgrade feature, it's important to be aware of several limitations that may affect its usage:

* Apps are limited to one concurrent bulk upgrade per environment.
* Developers will be limited to one concurrent bulk upgrade per Atlassian account.
* A global limit will be enforced on global concurrent bulk upgrades.

If you find that you've hit the global limit for concurrent bulk upgrades, wait around 30 minutes and retry.

## List your app on the Atlassian Marketplace

If you've finished testing your app, and want to provide or sell it to a large customer base,
see [Listing Forge apps on the Atlassian Marketplace](/platform/marketplace/listing-forge-apps/).

Once your app has been submitted for listing on Marketplace, or has a license in the app manifest, it can't be shared
via installation link. In order to share and test this app, you'll need to copy the app's code, create a new, unlicensed
version of the app, and share this version via installation link.

### Forge apps that are compatible with multiple Atlassian apps

The Forge platform lets developers build apps that are compatible with multiple Atlassian apps.
While previously these apps could not be distributed via the Atlassian Marketplace, soon you will be
able to list and distribute apps that are compatible with multiple Atlassian apps.

For more information on building Forge apps that are compatible with multiple Atlassian apps, see
[app compatibility](/platform/forge/app-compatibility/#multiple-app-compatibility--eap-).

When publishing your app on Marketplace, it will detect which Atlassian apps it is compatible with
based on the app's manifest. When admins install the app, it will be installed in the required
Atlassian app. Admins can also choose to connect it to any additional supported Atlassian apps during
installation.

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
