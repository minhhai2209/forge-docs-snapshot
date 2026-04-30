# Forge changelog

Going forward, the blanket classification of all updates as major version updates is being replaced with a per-app policy based on each app's migration status.

**Apps that have completed the Connect-to-Forge transition:** Any app whose latest deployed version contains only Forge modules and scopes -with no remaining Atlassian Connect modules - will be re-enrolled into minor version updates once that version has been released. The proportion of the install base that has upgraded to the latest version is not a factor; what matters is that a bulk-upgrade path existed from the last version that included Connect modules to the current Forge-only version.

54 apps that already meet this criteria have been moved back to minor version updates, and we will be refreshing that list on a weekly cadence.

**Apps that have not yet completed the transition:** Apps that still include Connect modules in their latest deployed version will not be able to use minor version updates indefinitely. This measure protects platform stability by ensuring that API traffic from these very large apps continues to be managed through controlled rollouts rather than automatic minor-version upgrades.

**Backporting changes to older major versions (temporarily restricted)**  
For now, you can’t publish updates to earlier major versions. This temporary restriction is in place for the same reason large apps were moved to controlled rollouts: to prevent large, high-impact changes from being automatically applied to a significant number of customers and to protect platform stability.

If you need to backport a fix to an older major version, we may be able to make an exception on a case-by-case basis. Please reach out to Atlassian with the app details, the version you need to backport to, and the rationale for the change.

As always, this policy has no effect on how apps qualify for the Forge revenue share rate. Your latest deployed app version determines revenue share eligibility.

For detailed information on how to use `forge version bulk-upgrade`, see <https://developer.atlassian.com/platform/forge/cli-reference/version-bulk-upgrade/>.
