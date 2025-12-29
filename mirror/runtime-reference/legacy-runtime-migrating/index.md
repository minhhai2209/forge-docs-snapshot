# Upgrading from the sandbox runtime

The legacy Javascript sandbox runtime is now [deprecated](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-789). This means that Forge can only create new apps on the
[latest runtime version](/platform/forge/runtime-reference/). In addition:

* From October 29, 2024: Forge apps that haven't been updated since January 1, 2023 will no longer function.
* From February 28, 2025: *All* Forge apps still running on the legacy runtime version will no longer function.

If your app is running on the Javascript sandbox runtime, we strongly advise that you
[upgrade to the latest runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

This page provides information on how to upgrade your app to the
[latest version of the Forge runtime](/platform/forge/runtime-reference/).
The latest runtime version offers the following advantages over the legacy runtime version:

* Better long-term compatibility with the Node ecosystem
* 512MB available memory per invocation (compared to 128MB in the legacy runtime)
* Improved security and performance

## Required packages

We strongly recommend that you use the latest version of each `@forge/` package. Package versions
released before April 29, 2024, may be incompatible with the native Node.js runtime.

The [native Node.js runtime's GA](/platform/forge/changelog/#CHANGE-1634) coincides
with the release of `@forge/cli@9.0.0`.

## Breaking changes

To minimize the effort of adopting the latest runtime version, we worked on ensuring backward compatibility
with the legacy runtime. However, you may need to refactor your app to address some breaking changes between
runtime versions.

### Node.js LTS version

The legacy runtime runs on an environment that mimics
[Node.js 14](https://nodejs.org/en/blog/release/v14.19.0). The latest runtime uses
[Node.js 18](https://nodejs.org/en/blog/release/v18.12.0), and we intend to support newer versions that
achieve "long-term support" (LTS) status. If your app is affected by any breaking changes between both
versions, you’ll need to address these.

### API redirects

App requests that return redirects to external domains are considered egress. As such, those domains must be declared in
the application manifest.

Atlassian app API redirects are considered internal traffic and don't require egress declarations in the app manifest.
See [Runtime egress permissions](/platform/forge/runtime-egress-permissions/#runtime-egress-permissions) for
detailed instructions.

### New invocation semantics

The legacy runtime used a
[v8 JavaScript isolate](https://v8docs.nodesource.com/node-0.8/d5/dda/classv8_1_1_isolate.html) sandbox. This
sandbox is bootstrapped for every invocation, providing a clean context for each invocation of your app.

The latest Forge runtime handles isolation (and, by extension, security) at the VM layer, making the sandbox
unnecessary. As such, we removed this sandbox; this, incidentally, moderately improves Forge’s invocation
performance.

### Expanded developer responsibilities

Without the v8 JavaScript isolate sandbox, the current runtime no longer guarantees that the local state in your
Forge functions is cleared for each invocation. This introduces new responsibilities for you as a developer to
ensure that customer data does not persist across app invocations. These responsibilities are laid out in our
[shared responsibility model](/platform/forge/shared-responsibility-model/#tenant-safety).

To comply with these new developer responsibilities, review your app code to ensure that:

* Your app must not persist customer data or sensitive content in a global state, in memory or on disk, between subsequent invocations.
* Your app must not copy customer data or sensitive content from one installation to another, unless it has been explicitly permitted by the customer.

### Snapshot removal

The [snapshotting](/platform/forge/runtime-reference/legacy-runtime-reference/#snapshots) feature is no longer
supported in the new native Node.js runtime, as it is no longer required. This feature was enabled by default
in the legacy runtime. If your app uses the `snapshots` flag in your `manifest.yml` file, you'll need to
remove it.

When snapshotting is enabled, the current runtime invokes any globally scoped JavaScript code at deployment rather than invocation time.

With the new native Node.js runtime, your app may be re-initialized if it hasn't been used for a long time or if
it needs to execute multiple times simultaneously. If your app requires globally scoped code to be executed
exactly once per deployment, this change in invocation semantics may require changes to your app.

### Delayed code execution

The latest Forge runtime might keep executing the code after the function returns. For example:

```
```
1
2
```



```
resolver.define("example", () => {
  setTimeout(() => {
    fetch("...");
  }, 5000);
});
```
```

In this example, timers and other asynchronous code may continue executing even after the Forge function returns a response.

When making API calls through `requestJira`, `requestConfluence`, and `requestBitbucket`, outbound HTTP
requests will assume a `Content-type: application/json` if a content type isn’t specified. However, this
default will not be applied to requests to external domains using the `fetch` function or other HTTP clients.

### HTTPS only

All external connections must be done through [HTTPS](https://nodejs.org/api/https.html); plain HTTP or TCP
connections are not allowed. In addition, these connections will be implemented over a custom proxy which will
only allow the following `https.request` options (or equivalents from third-party packages):

* `auth`
* `headers`
* `host`
* `method`
* `port`
  * Only 80, 8080, 443, 8443, 8444, 7990, 8089, 8090, 8085 and 8060.
* `path`

Sending a request with a `body` still works, as long as you specify the correct `Content-Type:` header (for example, `Content-Type: application/json` for a JSON `body`).

## Set runtime version

You can use the `app.runtime.name` setting of the manifest file to set which version of the Forge runtime your app should be deployed.

To keep your app on the Forge runtime legacy version while addressing any breaking changes, set `app.runtime.name` to `sandbox` then re-deploy your app:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"
  runtime:
    name: sandbox
```
```

Once you’re ready to migrate your app to the [latest runtime version](/platform/forge/runtime-reference/),
set `name` to `nodejs24.x` then re-deploy your app:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"
  runtime:
    name: nodejs24.x
```
```

### Upgrading older major versions

In some cases, a site admin can’t or won’t upgrade from an older major version of your app.
You can still update the runtime version used by their app through the `--major-version` option of
the `forge deploy` command. See [Backporting](/platform/forge/versions/#backporting) for
more information.

Older versions of your app that require [new domain declarations](#api-redirect) in the manifest to work cannot be upgraded to the latest runtime. Updating domain declarations in your app manifest creates a major version change, and such changes can't be backported.
