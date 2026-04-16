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
