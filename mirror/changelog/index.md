# Forge changelog

We’re upgrading Jira dashboards to a more modern and flexible experience. As part of this transition, we’re deprecating the legacy Forge modules for dashboards in favor of these new dashboard modules.

**What’s changing**  
The following Forge modules are now deprecated and will be removed on **May 17, 2027**:

These modules are replaced by the new `dashboards:widget` and `dashboards:backgroundScript` modules, which are now General Availability (GA). The new modules are designed for the upgraded Jira dashboard surface (also referred to as AVP dashboards).

**What you need to do**  
To ensure your dashboard extensions continue to work on the new Jira dashboard experience, you must migrate your existing modules:

1. Update your app manifest to use the new [dashboards:widget](https://developer.atlassian.com/platform/forge/manifest-reference/modules/dashboard-widget/ "https://developer.atlassian.com/platform/forge/manifest-reference/modules/dashboard-widget/") and `dashboards:backgroundScript` modules.
2. Complete your migration before the deprecation date of **May 17, 2027** to avoid service disruption for your users.
