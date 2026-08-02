# Publish a Developer Space to the Atlassian Marketplace

Publishing your Developer Space to the Atlassian Marketplace makes your space and its published apps publicly discoverable, enabling you to share and sell apps.
This process also creates your Marketplace Partner profile and grants you Marketplace admin permissions.

## Overview

* Only a [Developer Space admin](https://developer.atlassian.com/platform/forge/developer-space/developer-space-roles/#roles-and-what-they-can-do) can publish a developer space to the Marketplace.
* Publishing the space creates the [public marketplace partner profile](https://developer.atlassian.com/platform/marketplace/creating-a-marketplace-listing/#create-your-marketplace-partner-profile) on the Atlassian Marketplace.
* The admin gains Marketplace admin permissions to manage the marketplace partner profile and listings.

## Prerequisites

Before you can publish your Developer Space, ensure the following:

* You are an [admin](https://developer.atlassian.com/platform/forge/developer-space/developer-space-roles/#roles-and-what-they-can-do) of the Developer Space.
* The space has a billing account setup, and you’ve provided billing consent.
* The space profile name is complete and accurate.
* You have reviewed and are ready to accept the [Marketplace Partner Agreement](https://atlassianpartners.atlassian.net/wiki/spaces/resources/overview).

## How to publish your Developer Space

1. In the Developer Console, select your Developer Space and open the **Settings** page.
2. Find the “Make public on Marketplace” section. This section appears after the Billing account, Developer Space ID, and Developer Space profile.
3. **Review the information:**

   * Publishing your developer space makes its details—such as the developer space name and your email contact—publicly visible and discoverable on the Atlassian Marketplace.
   * You will gain [Marketplace admin permissions](/platform/marketplace/managing-permissions-on-your-vendor-account/) and can monitor business metrics in the dashboard.
4. Click **Review & publish**.  
   A modal will open, prompting you to review and accept the Atlassian Marketplace Partner Agreement.
   You must check the agreement box to enable the “Accept & publish” button.
5. Select **Accept & publish**. Once you accept, the automated process will begin immediately.

   * If the space name is not unique, you will be prompted to edit it in the modal and try again.
   * On success, you’ll see a confirmation message.

## What changes after publishing

* Your Developer Space is now public and discoverable on the Atlassian Marketplace. A corresponding [marketplace partner profile](https://developer.atlassian.com/platform/marketplace/become-a-partner/#associate-your-account-with-a-partner-profile) will be automatically created.
* The admin who published the space gains Marketplace admin permissions for the new vendor account.
* The Developer Space profile name is no longer editable from the Settings page. These settings are now managed via the Marketplace.
* The “Make public on Marketplace” section updates to show your space is public, with a link to your vendor profile.
* When you're preparing to [publish a Forge app](https://marketplace.atlassian.com/manage/apps/create) on the Marketplace:

  * **Vendor** dropdown displays all of your published developer spaces (Marketplace vendor profiles).
  * **Choose a Forge app** dropdown displays all Forge apps in the selected published developer space that are deployed to production and have sharing enabled. Learn more about [sharing your app](https://developer.atlassian.com/platform/forge/distribute-your-apps/#distribute-your-apps).

**Important:** When publishing a Forge app, the Vendor you select must be the same Developer Space where your Forge app is assigned. If you select a different vendor, your Forge app won't appear in the "Choose a Forge app" dropdown.

### Troubleshooting: "No Forge apps available"

If you see "No Forge apps available" when trying to publish a Forge app on Marketplace, verify the following:

| Requirement | How to check |
| --- | --- |
| **Forge app is assigned to the correct Developer Space** | In the [Developer Console](https://developer.atlassian.com/console/myapps/), check that your app is assigned to the Developer Space that matches the Vendor you selected. |
| **Developer Space is published to Marketplace** | Your Developer Space must be published before it appears in the Vendor dropdown. Follow the steps in [How to publish your Developer Space](#how-to-publish-your-developer-space). |
| **Forge app is deployed to production** | Run `forge deploy -e production` to deploy your app. See [Promote an app to staging or production](/platform/forge/staging-and-production-apps/). |
| **Sharing is enabled for the Forge app** | In the Developer Console, go to your app's **Distribution** settings and enable sharing. See [Start sharing your app](/platform/forge/distribute-your-apps/#start-sharing-your-app). |
| **You are an admin of the Developer Space** | Only Developer Space admins can see their published spaces in the Vendor dropdown. Check your role in the Developer Console under **Members**. |

## Frequently asked questions

#### Can I unpublish a Developer Space?

Once a Developer Space is published, a corresponding Marketplace vendor profile is automatically created and remains publicly visible on the Atlassian Marketplace. Published Developer Spaces cannot be unpublished, but you can [submit a support request](https://developer.atlassian.com/support) if you want to archive the published Developer Space.

#### What if I already have a Marketplace Partner Profile?

Publishing a Developer Space creates a new vendor profile. If you need to merge or manage multiple profiles, contact [Atlassian support](https://developer.atlassian.com/support).

#### Who can manage the Marketplace profile after publishing?

The Admin who published the space becomes the Marketplace admin. You can add additional Marketplace admins via the Marketplace.
