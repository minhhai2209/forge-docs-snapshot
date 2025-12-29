# Exceeding limits and suspended apps

Learn how usage overages are billed, how to monitor your consumption, and the conditions that may lead to app suspension.

## Apps exceeding limits

If your app exceeds any limits, you can often fix the issue yourself:

* Most app limits are enforced through Forge CLI validation, where
  you'll immediately receive an error. Most errors have trivial fixes, such as shortening
  your app's name.
* For resource-bound limit errors (such as the total number of apps), you need to
  remove the relevant resources. You can uninstall an app with the `forge uninstall` command.
  Once you remove all installations of an app, delete it from the
  [developer console](https://developer.atlassian.com/apps/).

We understand that some limits can be hard to monitor; as such, we are working on
better monitoring tools for future releases.
Meanwhile, if we detect that your app consistently exceeds our limits, we'll
first contact you to understand why. If your app needs higher storage capacity or a higher cyclic invocation limit, you can contact
us through [Developer and Marketplace support](https://developer.atlassian.com/support).
If your app needs an increase in other quotas or limits, please let us know through the
[Forge Jira Project](https://ecosystem.atlassian.net/jira/software/c/projects/FRGE/issues/).

We aim to unblock reasonable use cases, and we will work with you to achieve this.
However, repeated or prolonged failure to address requests to comply with limits may result in
further action being taken (such as app suspension).

## Suspended apps

An app may be temporarily suspended if it negatively impacts the Forge
platform, regardless of whether it’s in breach of any quotas or limits.

Suspended apps cannot be:

* **Invoked**: Suspended apps cannot be invoked by any existing installations. Invoking
  a suspended app will return an `App is currently unavailable, please try again later` error.
* **Installed**: Attempting to install a suspended app will return an
  `App installation is not available while the app is suspended` error.
* **Deployed**: Running `forge deploy` command on a suspended app will return an
  `App management is unavailable while the app is suspended` error.

If your app is suspended, we'll submit a ticket through
[Developer and Marketplace support](https://developer.atlassian.com/support)
and mention you, so that you can help us fix the issue as soon as possible.

If you're not a Jira user, we’ll email you a link to the issue.

If have an issue with quotas or limits but haven't been contacted by our team, you
can seek assistance from the
[Forge developer community](https://community.developer.atlassian.com/c/forge).

See the [Forge Terms](/platform/forge/developer-terms/) for more information.
