# Resource limits

Review the size and quantity restrictions for static resource bundles used in Custom UI and UI Kit apps. There are limits on the number and size of static [resources](/platform/forge/manifest-reference/resources/) that can be bundled with your app if you use Custom UI or UI Kit. The following limits apply:

| Category | Resource | Limit | Description |
| --- | --- | --- | --- |
| Custom UI and UI Kit | Bundle files | 5000 | Maximum number of files declared in a single resource bundle. |
| Bundle size | 100 | Maximum bundle size in megabytes (MB) for a resource. |
| Bundle count | 50 | Maximum number of resources per app. |

## Cumulative limits across all resources

Your app can have up to 50 resources, with each resource bundle containing up to 5,000 files and 100 MB. However, cumulative limits apply across all resources in your app:

| Resource | Limit | Description |
| --- | --- | --- |
| Total files | 25000 | Maximum cumulative number of files across all resources in your app. |
| Total bundle size | 1 GB | Maximum cumulative size across all resources in your app. |

**Example:** If you have 50 resources in your app, each resource could theoretically contain 5,000 files and be 100 MB (totaling 250,000 files and 5 GB). However, the cumulative limits mean the actual total across all your resources cannot exceed 25,000 files and 1 GB, regardless of how many resources you use.

For a more typical app with 3 resources, you might have 800 files total (250 + 300 + 250) and 180 MB total (60 MB + 70 MB + 50 MB), which is well within the cumulative limits.

**Consider using multiple entry points instead of multiple resources.**

If your app has multiple views or modules, you can define up to 50 named entry points within a single resource using the [entry property](/platform/forge/manifest-reference/resources/#multiple-entry-points), rather than declaring a separate resource for each view. This approach has several benefits:

* **Lower bundle count usage** — multiple views within one resource count as a single resource against the 50-resource limit.
* **Smaller deploy size and faster load times** — shared dependencies across entry points can be extracted into common chunks, reducing total deploy size and allowing shared code to be cached once and reused across all entry points. For UI Kit, the Forge CLI handles this automatically. For Custom UI, you can achieve the same benefit by configuring code splitting in your own build pipeline (see [webpack code splitting](https://webpack.js.org/guides/code-splitting/) or [Vite multi-page app](https://vite.dev/guide/build#multi-page-app)).

Note that each resource with an `entry` map still counts as a single resource against the 50-resource limit, regardless of how many entries it contains.
