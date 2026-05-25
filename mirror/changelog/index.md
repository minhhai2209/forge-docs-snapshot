# Forge changelog

Previously, [we announced an upcoming fix](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-3138 "https://developer.atlassian.com/platform/forge/changelog/#CHANGE-3138") to how Forge SQL returns `DATETIME` column values when the time component is `00:00:00`. We are now rolling out this update on Jun 5, 2026 instead of Oct 6, 2026

As this change relates to a bugfix in an underlying library dependency, deferring the update could expose the platform to security vulnerabilities. However, updating the library as scheduled means rolling out the `DATETIME` fix earlier than expected.

**What's changing:**

Previously, querying the value of a `DATETIME` column where the time component is set to `00:00:00` would result in only the date portion being returned. For example, the value `'1970-01-01 00:00:00'` would be returned as `'1970-01-01'`. After this update, the full value including the time component will be correctly returned (`'1970-01-01 00:00:00'`).  
  
This affects `DATETIME` column values that were set in the following ways:

1. The value was explicitly set with a time component of `00:00:00`, or
2. The value was set with only the date component, in which case the time component defaults to `00:00:00`.

**What you should do:**

If your Forge app reads `DATETIME` values from Forge SQL and parses the returned string, verify that your parsing logic handles the full `YYYY-MM-DD HH:MM:SS` format.

**Why we're accelerating this:**

Remaining on an outdated version of this library dependency has the potential to leave Forge SQL exposed to security vulnerabilities. We cannot responsibly defer a necessary security update to honour the original grace period. We apologise for the shortened notice and appreciate your understanding.
