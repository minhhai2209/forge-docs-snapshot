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
