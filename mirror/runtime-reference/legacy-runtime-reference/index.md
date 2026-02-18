# Legacy runtime (deprecated)

The legacy Javascript sandbox runtime is now [deprecated](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-789). This means that Forge can only create new apps on the
[latest runtime version](/platform/forge/runtime-reference/). In addition:

* From October 29, 2024: Forge apps that haven't been updated since January 1, 2023 will no longer function.
* From February 28, 2025: *All* Forge apps still running on the legacy runtime version will no longer function.

If your app is running on the Javascript sandbox runtime, we strongly advise that you
[upgrade to the latest runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

This page describes the environment, features, and security of the *legacy* Javascript sandbox runtime version. This information
is provided as a reference for developers who may still need it while upgrading to the latest runtime version.
The latest runtime version offers the following advantages over the legacy runtime version:

* Better long-term compatibility with the Node ecosystem
* 512MB available memory per invocation (compared to 128MB in the legacy runtime)
* Improved security and performance

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

The `runtime` section of the `manifest.yml` file features a `name` property that lets you specify what runtime to use. To specify the native sandbox runtime, set `name` to `sandbox`:

```
```
1
2
```



```
app:
  runtime:
    name: sandbox
```
```

Adding the `runtime.name` property to the manifest file will not trigger a major upgrade. As such, deploying this change alone to production will automatically install it on all sites.

## Javascript environment

When a Forge app is invoked, the legacy runtime executes its code within an app sandbox, which differs from a traditional Node.js environment.

You'll need to write your functions in a subset of Node.js. Some globals are not exposed, for example:

* `process` (except for `process.env`)
* `queueMicrotask`

This means that some NPM packages that depend on these may not function correctly. The following Node.js built-in modules are not supported:

* `async_hooks`
* `child_process`
* `cluster`
* `constants`
* `dgram`
* `dns`
* `domain`
* `http2`
* `module`
* `net`
* `perf_hooks`
* `readline`
* `repl`
* `sys`
* `tls`
* `trace_events`
* `tty`
* `v8`
* `vm`
* `worker_threads`

## Snapshots and snapshot context

Snapshot is the mechanism of evaluating your function's global scope at each deployment of the app, rather
than at every invocation. Forge apps use snapshots by default, as this improves the response time for your
app. You can [disable snapshots](/platform/forge/manifest-reference/#runtime), but this means your app needs
to be fully evaluated on each invocation. For this reason, you should consider leaving snapshots enabled.

The following image highlights a sample snapshot context. Note that the invocation method is not run at this
point in time.

![A code editor showing the constants declared in the snapshot context](https://dac-static.atlassian.com/platform/forge/images/snapshot-context.png?_v=1.5800.1858)

The `snapshots` flag is available under the `runtime` object with a default value of `true`.

```
```
1
2
```



```
app:
  runtime:
    snapshots: true # Boolean
```
```

## Limitations

### Environment variables

Environment variables are not available in the snapshot context.

#### Example

```
```
1
2
```



```
const myVariable = process.env.MY_VARIABLE;

export const run = () => {
  console.log(myVariable) // Value is undefined
};
```
```

### Randomness

Random values created at snapshot time are not random on each function invocation.

#### Example

```
```
1
2
```



```
const snapshotContextRandom = Math.random();

export const run = () => {
  console.log(snapshotContextRandom); // Same value per invocation
};
```
```

#### Buffers

We discourage using `Buffers` in the snapshot context. If this is detected, warnings will be presented at deploy time.

```
```
1
2
```



```
const snapshotContextBuffer = new Buffer(); // May result in unpredictable behavior

export const run = () => {
  // ...
};
```
```

### Standard globals

#### Process

The global process object is a partial implementation of the [Node JS process](https://nodejs.org/api/process.html).

#### Object signature

#### Fields

| Key | Value |
| --- | --- |
| `platform` | `forge` |
| `env` | See [Environments](/platform/forge/environments-and-versions/). |
| `version` | The underlying Node JS version.   Example:  `process.version // 12.14.1` |
| `versions` | Versions of runtime dependencies.   Example:  `{ forge: 'forge:47', node: '12.14.1' }` |
| `nextTick` | A polyfill of [Node JS nextTick](https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/). |
