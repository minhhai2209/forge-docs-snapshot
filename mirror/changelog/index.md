# Forge changelog

We’re announcing the **deprecation and upcoming decommission** of the AUI CDN.  
AUI CDN will be shut down after Oct 30, 2026.

**What is AUI CDN?**  
[aui-cdn.atlassian.com](https://aui-cdn.atlassian.com/ "https://aui-cdn.atlassian.com/") hosts **legacy JavaScript and CSS assets** for AUI ([Atlassian User Interface](https://aui.atlassian.com/ "https://aui.atlassian.com/")) versions 5.2.0 – 6.0.9.

**Who is affected?**  
The AUI CDN is primarily used by **Connect apps**, so this mostly affects apps not yet migrated from Connect to Forge. Connect has announced its own [End of Support late 2026](https://www.atlassian.com/blog/developer/announcing-connect-end-of-support-timeline-and-next-steps "https://www.atlassian.com/blog/developer/announcing-connect-end-of-support-timeline-and-next-steps"). In some rare cases, AUI CDN is also used by Forge apps.

**How to check if you're affected**  
Search your app's source code for any URLs containing `aui-cdn.atlassian.com`. If you find any references, your app is loading assets from AUI CDN and **you need to take action before the shutdown**.

**What to do if you're affected**  
Remove all references to `aui-cdn.atlassian.com` from your codebase and migrate to a supported alternative:

* **Recommended:** Migrate AUI to Atlassian Design System or Forge UI Kit. Any Atlassian Connect apps should also [migrate to Forge](https://developer.atlassian.com/platform/forge "https://developer.atlassian.com/platform/forge"), as [Connect End of Support](https://www.atlassian.com/blog/developer/announcing-connect-end-of-support-timeline-and-next-steps "https://www.atlassian.com/blog/developer/announcing-connect-end-of-support-timeline-and-next-steps") has been announced.
* If migrating is not suitable for you (e.g. non-React apps), you have these options:

  * **Bundle AUI directly:** via npm. See the [AUI documentation](https://aui.atlassian.com/aui/latest/docs/ "https://aui.atlassian.com/aui/latest/docs/").
  * **Third-party CDN:** use a CDN that serves npm packages, e.g. [jsDelivr](https://www.jsdelivr.com/package/npm/aui "https://www.jsdelivr.com/package/npm/aui") (`https://cdn.jsdelivr.net/npm/aui@latest/`) or [unpkg](https://unpkg.com/aui/ "https://unpkg.com/aui/") (`https://unpkg.com/aui@latest/`)
  * **Self-host:** download any required AUI assets and serve the static assets yourself

**Timeline**  
AUI CDN will be shut down after Oct 30, 2026. After this date, any requests to `aui-cdn.atlassian.com` will fail, which will break apps that haven't migrated. Please migrate as soon as possible.
