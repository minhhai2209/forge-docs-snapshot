# Tunneling

Tunneling runs your app code locally on your machine via the Forge CLI and
Cloudflare.

Watch our video for an introduction on Forge tunneling.

If you are using a firewall, you might see new connections to Cloudflare tunnel infrastructure. Please allow these for tunneling to work.

More information about this change
can be found [here](https://developer.atlassian.com/platform/forge/changelog/#CHANGE-1785).

## Starting

You can start a tunnel for any app that has been deployed and installed on to a site. To start
a tunnel for your app, run the following command in your CLI:

You'll see output similar to this:

```
```
1
2
```



```
Tunnel redirects requests you make to your local machine. This occurs for any Atlassian site where
your app is installed in the specific development environment. You will not see requests from other
users.

Press Ctrl+C to cancel.

=== Running forge lint...
No issues found.

=== Bundling code...
✔ Functions bundled.

Listening for requests...
```
```

Messages logged to the console will look similar to this:

```
```
1
2
```



```
INFO 17:34:04.955 Count of objects in test array: 0
```
```

Tunneling also helps you debug your app in two ways:

* **Real-time logging for your local app**: By inserting `console.log()` statements in your code,
  you can see the output in the Forge CLI as the code executes.
* **Fast turnaround for changes**: The tunnel watches for code changes and rebuilds your app.
  You don’t need to deploy your app after every change, which lets you test fixes faster.

## Matching your local environment to Forge runtime

Variations in your local environment can cause functions to succeed there but fail in Forge. To prevent this:

1. Ensure that your local environment uses the same version of Node.js used by deployed Forge apps (currently
   [Node.js 20](https://nodejs.org/en/blog/release/v20.0.0)).
2. Don’t include any additional dependencies or libraries in your local environment that are not provided out-of-the-box by Node.js (or bundled directly by your app).

We are evaluating support for an optional Docker image for tunnelling, based on feedback and interest from
Forge app developers.

Tunneling with UI Kit/Custom UI apps are only supported on Chrome and Firefox browsers.

## Tunneling with UI Kit

When running `forge tunnel` with a [UI Kit](/platform/forge/ui-kit/) app, any changes to your source
code triggers a rebundle from the Forge CLI. Once the rebundling is completed successfully, you can
see your changes by refreshing the page that your app is on.

## Tunneling with Custom UI

When running `forge tunnel` with a [Custom UI](/platform/forge/custom-ui/) app, the Forge CLI serves
the content from the `path` directories specified in each `resource` that's defined in your manifest.
This means that if your static assets require rebundling, you need to bundle them before refreshing
the page that your app is on. See [here](/platform/forge/custom-ui/) for more details on `resource`
declarations for Custom UI apps.

### Connecting the tunnel to your own dev server

While `forge tunnel` lets you avoid redeploying your Custom UI app to test changes, you have to
manually bundle it for each change you make. To solve having to do this, popular tools, such as
[create-react-app](https://create-react-app.dev/) can automatically reload your app each time
you change the code. These tools usually host their own server on a specific **port**.

For example, running `npm start` with `create-react-app` starts a server at `http://localhost:3000`
by default. The Forge CLI allows you to proxy tunnel requests to these servers, enabling features,
such as hot-reloading while developing your Custom UI apps.

To connect a server to `forge tunnel`, first identify the port that the server is hosted on.
In the above example, the port would be `3000`. Then, add the following to your `manifest.yml` file,
under the `resource` your server is hosting:

```
```
1
2
```



```
tunnel:
  port: <YOUR_PORT_HERE>
```
```

For example, a `resources` definition might look like this:

```
```
1
2
```



```
resources:
  - key: main
    path: static/hello-world/build
    tunnel:
      port: 3000
```
```

Once a port has been added to a resource definition, running `forge tunnel` causes the Forge CLI
to bypass the `path` directory, and instead proxy the request to `http://localhost:<port>`.

You can then run `forge tunnel`, and start your server by running `npm start`. You can then see
the assets served by your local server by refreshing the page that your app is on. If your server
supports hot-reloading, you no longer need to refresh the page to see updates when you make
changes to the code.

## Tunneling with non-UI functions

When running `forge tunnel` with non-UI functions, such as
[Custom UI resolvers](/platform/forge/runtime-reference/custom-ui-resolver/) and
[web triggers](/platform/forge/manifest-reference/modules/web-trigger), any changes to your source
code triggers a rebundle from the Forge CLI. Once that rebundling is completed successfully,
you can see your changes reflected in the next invocation of the function.

## Tunneling with Forge Containers (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

After [defining a containerised service](/platform/forge/containers-reference/managing-service), you can test it locally before you push its image to your container’s repository. You can then use `forge tunnel` to redirect app invocations from your development site to your local instance of the service.

See [Testing a containerised service locally](/platform/forge/containers-reference/test-service-locally/) for detailed information on how
to set this up.

## Known limitations

* Tunneling with Custom UI apps is only supported on Chrome and Firefox browsers.
* Any logging that happens while you're tunneling won’t show in `forge logs`. This is because your
  app code runs locally while tunneling. `forge logs` only shows information for your deployed app,
  not locally running code.
* If you make changes to the `manifest.yml` file, you must deploy the app with the latest manifest.
  This is needed for the tunnel to pick up the changes.
* Environment variables must be set locally, as the tunnel can't access the values set in other
  environments.
* Tunneling only displays output from your usage of the app, that is, your requests.
* Tunnelled app [resolvers](/platform/forge/runtime-reference/custom-ui-resolver) won't time out, unlike deployed apps.
  Instead, they will continue to run until completed. This is because developer environments have network
  and processing speeds that differ from Forge's runtime environment, preventing us from accurately
  replicating app timeouts during tunnelling.
  [Learn more about deployed app invocation limits.](/platform/forge/platform-quotas-and-limits/#invocation-limits)
* Forge invocations have a [time limit](/platform/forge/platform-quotas-and-limits/#invocation-limits). This may cause issues in two instances:
  * If your local machine has less compute power than the remote Lambda function server,
    you could see local timeouts that wouldn't happen once deployed.
  * Conversely, if your local machine has more power than the remote,
    you could see remote timeouts that didn't happen locally.
* The Forge app UI is only accessible from the same machine running `forge tunnel`.

## Troubleshooting

This section covers common issues that can prevent `forge tunnel` from working correctly.

If you edit `manifest.yml`, run `forge deploy` so the tunnel uses the latest manifest. The tunnel does not replace a deploy. If your change affects installation metadata (for example, permissions or modules), you may also need `forge install --upgrade` on the target site. Otherwise the tunnel can still run while the app misbehaves or fails.

### Tunnel fails to start or connect

Use this section if `forge tunnel` exits immediately, never reaches `Listening for requests...`, or you suspect traffic is not reaching your machine. A firewall, VPN, or corporate proxy can block Cloudflare tunnel traffic even after the CLI has printed `Listening for requests...` — still follow **Check your network and firewall settings** below.

**Check your network and firewall settings**

`forge tunnel` uses [Cloudflare](https://www.cloudflare.com/) to route requests from your Atlassian site to your local machine. If a firewall, VPN, or corporate proxy is blocking outbound connections to Cloudflare, the tunnel cannot establish a connection.

To resolve this:

* Allow outbound connections to Cloudflare tunnel infrastructure. See the [changelog entry](/platform/forge/changelog/#CHANGE-1785) for details on the specific endpoints.
* If you're behind a corporate proxy, configure your system proxy settings so that Node.js can reach external services.
* Try disabling your VPN temporarily to determine whether it is the cause.

**Check that the app is deployed**

You must deploy your app at least once before running `forge tunnel`. The tunnel redirects invocations to your local machine but depends on a deployed version to handle the handshake.

Run the following command to ensure your app is deployed:

Then retry `forge tunnel`.

**Restart the tunnel process**

If the tunnel becomes unresponsive or hangs, press `Ctrl+C` to stop it and run `forge tunnel` again. Stale tunnel processes can prevent new connections from being established.

### Tunnel starts but requests are not received

If the tunnel is running but you don't see any output when you trigger your app:

* Confirm you are using the same Atlassian site and environment where your app is installed. The tunnel only intercepts requests on the environment (for example, `development`) where your app is installed.
* Confirm you are triggering the app from the same browser session on the same machine running `forge tunnel`. The tunnel only displays your own requests — not those from other users.
* Check that your app is installed and enabled on the target site by running:

* **Check Chrome's Local Network Access setting.** Chrome has a flag that controls whether sites can make requests to resources on your local network. If this flag is set to **Enabled (Blocking)**, the tunnel silently fails — the CLI shows `Listening for requests...` but no requests are received.

  To fix this, go to `chrome://flags/#local-network-access-check` in Chrome and set the flag to **Default** or **Disabled**.

### Tunnel exits with an authentication error

If you see an authentication error when running `forge tunnel`, your CLI session may have expired. Re-authenticate by running:

### "Listening for requests..." shown but app isn't working

If the tunnel starts successfully but your app behaves unexpectedly or shows errors:

* **Check for Node.js version mismatches.** Your app uses the Node.js version set in `manifest.yml` under `app.runtime.name` (for example, `nodejs20.x`, `nodejs22.x`, or `nodejs24.x`). If your local Node.js major version does not match that runtime, behaviour may differ from Forge. See [Native Node.js runtime](/platform/forge/function-reference/nodejs-runtime/), install the matching [Node.js release](https://nodejs.org/en/download/), and use a version manager such as `nvm`:

Replace `22` with `20` or `24` if your manifest uses `nodejs20.x` or `nodejs24.x`.

* **Check for local-only dependencies.** If your code relies on packages or environment-specific globals that aren't bundled with your app, functions may work locally but fail once deployed. Ensure all dependencies are declared in `package.json`.
* **Check environment variables.** Environment variables must be set locally when tunneling. Variables set in other Forge environments (for example, production) are not accessible to the tunnel. When tunneling, environment variables must be prefixed with `FORGE_USER_VAR_` — for example, `export FORGE_USER_VAR_MY_KEY=test`. In your code, you still access the value as `process.env.MY_KEY`. See [Environments and versions](/platform/forge/environments-and-versions/#forge-tunnel) for details.
* **Review your console output.** Any errors thrown by your function will appear in the `forge tunnel` output. Look for stack traces or unhandled promise rejections that may indicate the root cause.

### Tunnel is stuck at "Bundling code..."

If `forge tunnel` hangs at the bundling step and never proceeds:

* Check for syntax errors in your source files. Run `forge lint` to identify issues:

* If you are on macOS with Apple Silicon (M1/M2/M3) and using an older Docker-based version of the Forge CLI, see the [Docker bundling issue workaround](#bundling-issues) below.
* Delete the `node_modules` directory and reinstall dependencies, then retry:

```
```
1
2
```



```
rm -rf node_modules && npm install
forge tunnel
```
```

### Troubleshooting Docker issues

Older versions of the Forge tunnel use Docker, which may cause issues.

#### Symlinks limitations

Docker doesn't follow symlinks when creating a container to avoid potential inconsistencies.
Therefore, you can't use symlinks in your app repository.

To work around this, install [Yalc](https://github.com/wclr/yalc) locally and add dependencies
via `yalc add <dependency>` before running `forge tunnel` or `forge deploy`.

#### Bundling issues

The `forge tunnel` command will get stuck in the `Bundling Code` step if you:

* are using a Mac computer with an Apple Silicon chip (for example, M1)
* have updated your Docker Desktop app recently (version 4.25+)

To work around this, disable the "Rosetta"
[setting](https://docs.docker.com/desktop/settings/mac/) on your Docker Desktop and restart
your Docker daemon.

## Related pages

* [Debug functions using IntelliJ](/platform/forge/debug-functions-using-intellij): This tutorial demonstrates debugging back-end Forge functions in Node.js with IntelliJ's debugger.
* [Debug functions using VSCode](/platform/forge/debug-functions-using-vscode): This tutorial demonstrates debugging back-end Forge functions in Node.js with VS Code's debugger.
* [Tunnel](/platform/forge/cli-reference/tunnel/): This reference page outlines the description, usage, and options for the `forge tunnel` CLI command.

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
