# Node.js

The Forge app runtime includes a set of APIs that provide additional functionality to the Forge platform. You
can use these APIs to interact with REST endpoints and to store data.

This runtime supports `Node.js 20` and `Node.js 22`. See [Node.js](https://nodejs.org/en/about/previous-releases) for details on these and earlier versions.
we also intend to support newer versions as they become available. As such, you can import any built-in, local, or third-party
Node modules into your app. This provides compatibility with all Node libraries and NPM packages, allowing you
to leverage the entire JavaScript developer ecosystem.

For details about migrating from the legacy sandbox runtime, see
[Upgrading from legacy runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

## Basic usage

### Update to latest dependencies

The new native Node.js runtime requires the latest version of all Forge packages. Install updates for the packages your app uses, from the command line. For example:

```
1
2
npm install -g @forge/cli@latest
npm install @forge/api@latest
```

Repeat the `npm install` command for any other Forge packages your app uses.

### Declare runtime version

The `runtime` section of the `manifest.yml` file features a `name` property that lets you specify what runtime to use. To specify the native Node.js runtime, set `name` to `nodejs24.x`:

```
1
2
3
app:
  runtime:
    name: nodejs24.x
```

Adding the `runtime.name` property to the manifest file will not trigger a major upgrade. As such, deploying this change alone to production will automatically install it on all sites.

## Concepts

### Invocation

The Forge runtime allows your app to run directly on a secure VM environment. Your app will be provided with
512MB of memory per invocation. For a complete list of resource limits provided per app invocation, refer to
[Platform quotas and limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

### Invocation context

At invocation time, Forge calls a context function. Each module receives different [request parameters](/platform/forge/function-reference/arguments/) based on
the module type.

![A code editor showing the invocation context](https://dac-static.atlassian.com/platform/forge/images/invocation-context.png?_v=1.5800.1805)

You can also explicitly request a Forge function’s context details (for example, the
[environments and versions](/platform/forge/environments-and-versions/) an app is executing in). See
[getAppContext](/platform/forge/runtime-reference/app-context-api/) for more information.

### Developer responsibilities

Within the Forge runtime, it is your responsibility to ensure customer data does not persist across app
invocations. Our [shared responsibility model](/platform/forge/shared-responsibility-model/#tenant-safety) lays out these responsibilities.

To comply with these responsibilities, review your app code to ensure that:

* Your app must not persist customer data or sensitive content in global state, in memory or on disk, between
  subsequent invocations.
* Your app must not copy customer data or sensitive content from one installation to another, unless it has
  been explicitly permitted by the customer.
* Your app must not persist tenant-related data in global variables. This includes registering callbacks to be executed
  later if they are stored in a global queue.
* In your app code, ensure callbacks only uses variables from the current invocation,
  and doesn't refer to global variables that might be modified by the next invocation

### Runtime context

When calling Atlassian APIs like `storage`(legacy),`kvs`, `requestJira`, `requestConfluence`, the Forge runtime
automatically provides the context of the current request. This ensures that operations are executed
against the correct tenant.

#### Trouble shooting "Forge runtime not found" error

If you encounter an error with message `Forge runtime metadata not found. Visit https://go.atlassian.com/nodejs-runtime for more information`,
that's because the runtime context is lost in a rare situation. You can resolve the issue by following the below steps:

1. Confirm that tenant isolation has not been compromised.
   See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities).
2. Navigate to the place where throws the error, use `bindInvocationContext` API to wrap the call.

Code example:

```
```
1
2
```



```
import { bindInvocationContext } from '@forge/api'
import { kvs } from '@forge/kvs'
import { SomeClient } from 'some-library';

const handler = async () => {
  const client = new SomeClient();

  // If calling within a particular event listener produces "Error: Forge runtime not found...." errors, for example:
  // client.on('data', async () => {
  //   await kvs.set('foo', 'bar');
  // });

  // Verify tenant isolation is preserved and wrap the callback in bindInvocationContext
  client.on('data', bindInvocationContext(async () => {
    await kvs.set('foo', 'bar');
  }));
}
```
```

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

When making API calls through `requestJira`, `requestConfluence` and `requestBitbucket`, outbound HTTP
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

### Console and https customizations

While the current runtime uses a full Node.js environment, some `https` and `console` methods are replaced with
custom implementations. These customizations ensure external connections and logs connect to the Forge
platform.

### IP address range changes for outgoing connections

Outgoing connections for Forge apps currently originate from a VPC configured in the Atlassian cloud environment where the Forge functions are executed. For apps deployed in the Forge runtime, outgoing connections will originate from Atlassian’s cloud infrastructure (specifically, the IP addresses
[listed here](https://support.atlassian.com/organization-administration/docs/ip-addresses-and-domains-for-atlassian-cloud-products/#Outgoing-Connections)).

### Redirects to external domains

All requests to Atlassian app APIs that return redirects to external domains are considered egress. If
your app uses such redirects, you’ll need to declare those domains and add permissions for them in your
manifest file:

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - 'https://www.example.com'
```
```

See [Runtime egress permissions](/platform/forge/runtime-egress-permissions/#runtime-egress-permissions) for
detailed instructions.
