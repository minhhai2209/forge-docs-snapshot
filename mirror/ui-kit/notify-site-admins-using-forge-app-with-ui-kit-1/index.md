# Notify site admins using Forge app with UI Kit 1

With the upcoming deprecation of UI Kit 1 it is important to contact any site admins that are using a UI Kit 1 version of your Forge app.

Even if you have upgraded your Forge app to the latest version of UI Kit, please be aware that sites using your Forge app might not be using this version. This could be the case if you released it as a major version change, site admins will have to manually update their site to use this.

Alternatively, if you released this as a minor update on the latest major version, sites which have an older major version installed won't automatically receive your minor update.

See the [Forge version](/platform/forge/versions/) docs for more information on how versioning works in Forge.

## How do I find sites with an old version of my Forge app installed?

You can see what versions of your app sites have installed via the developer console. See [view app installations](/platform/forge/view-app-installations/) for details. You can use the "version" filter and select the "out-of-date" option to find any sites that are not on the latest version.

You can also run `forge install list` [see cli reference](/platform/forge/cli-reference/install-list/) to show the current installations of your Forge app. This command also includes the Installation ID.

## Can I update a previous major version of my Forge app from UI Kit 1 to 2?

Yes, you can use [Forge version backporting](/platform/forge/versions/#backporting) if your changes do not constitute a breaking change.

Currently only apps that are paid can contact site admins see [how do I contact a customer](/platform/marketplace/sales-and-evaluations-reports/#how-do-i-contact-a-customer-) and the [licenses report](https://developer.atlassian.com/platform/marketplace/licenses/) for details on how to this.
