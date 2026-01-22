# Use the Forge CLI on a corporate network

Building and deploying Forge apps requires your local development environment to communicate with
Atlassian services and upload your app artifacts to our hosted environment.
Because of this, your local development environment will need Internet connectivity.

Corporate network environments
often have additional restrictions on local administrative permissions, downloading artifacts from public
package repositories, and connecting to external sites via an HTTP proxy or through a firewall's allowlist.
For developers who are building apps from within these environments, some additional configuration steps may
be required in order for the CLI to run successfully.

Depending on your network environment, you may need to
perform some or all of these additional configuration steps.

**Support limitations**

Configuring the Forge CLI to work in a specific network environment depends on your network's unique configuration.
Consequently, Atlassian may not be able to provide comprehensive support for troubleshooting issues you encounter.

The list of outbound connections on this page is updated periodically and may not always reflect the exact behavior
of the latest version of the Forge CLI.

Using the `global-agent` module to enable the Forge CLI to work with a network proxy is an unsupported modification
to the Forge CLI.

Check out this video for troubleshooting tips when using the Forge CLI on a corporate network:

## Configuring NPM to use a local repository

Some corporate networks prevent access to public package repositories. Instead, a local package mirror is
used to host approved packages and manage the bill of materials for software dependencies.

Because the Forge CLI
is built on Node.js, installing the Forge CLI requires access to the [central NPM repository](https://registry.npmjs.org) to download and install the Forge CLI dependencies.

If you need to use a local NPM repository, run the following command in your terminal:

```
```
1
2
```



```
npm config set registry ${yourRegistry}
```
```

Where `${yourRegistry}` is the HTTP URL to your local NPM package repository.

Avoid using NPM v11.3.0 due to a known [bug](https://github.com/npm/cli/issues/8216).
If you encounter errors during installation, use v11.4.0 (or later) instead.

## Installing `node-gyp`

The Forge CLI has a dependency on a third-party package called [node-gyp](https://github.com/nodejs/node-gyp). Installing `node-gyp` is slightly more complex than installing regular Node.js packages because
it has non-JavaScript dependencies including some components that may need to be provided by your operating system.
In some situations, the Forge CLI installation process may attempt to dynamically retrieve `node-gyp`’s native platform
dependencies from external repositories, which will fail if you are required to use a local NPM package mirror. Or,
the `node-gyp` installation may fail because it tries to build itself from the source, but the right build tools are
not installed in your local development environment.

In this scenario, you should instead install the build `node-gyp` dependencies for your operating system as
described in the [node-gyp instructions](https://github.com/nodejs/node-gyp?tab=readme-ov-file#installation).

After you’ve completed this pre-installation, you should try to [install the Forge CLI](/platform/forge/getting-started/#install-the-forge-cli) again.

## Configuring the development environment to work with an HTTP proxy

If your network requires outbound connections using an HTTP proxy, you will need to provide the Forge CLI with
details on your proxy server configuration.

If you are unsure, you *may* be working from a network with an HTTP
proxy if you are seeing connectivity errors when trying to run commands with the Forge CLI. These could be SSL
certificate errors, connection timeout errors, or connection reset errors. For example:

```
```
1
2
```



```
request to https://api.atlassian.com/graphql failed, reason: read ECONNRESET`
```
```

You will need to know the connection details of your proxy server. Contact your network administrator or IT team
for this information if you are unsure.

### Configuring NPM to use the proxy

NPM is the package manager for Node.js, which is used to download dependencies. By default, NPM downloads packages from the
[central NPM repository](https://registry.npmjs.org). Therefore, to install the Forge CLI,
and the additional packages required for the CLI to work with a proxy, you also need to configure NPM to use your
proxy configuration.

This can be done by running the following command in your terminal:

```
```
1
2
```



```
npm config set proxy ${yourProxyServer}
```
```

Replace `${yourProxyServer}` with the HTTP URL of your proxy server. For example:

```
```
1
2
```



```
npm config set proxy http://proxy.example.com:8888
```
```

### Configuring Forge CLI to use the proxy

The Forge CLI can be configured to work with a proxy server by modifying it to use the `global-agent` NPM package.
This can be done by performing the following steps:

1. Install the package by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install -g global-agent
   ```
   ```
2. Set the HTTP URL for connecting to your proxy as an environment variable by running:

   ```
   ```
   1
   2
   ```



   ```
   export GLOBAL_AGENT_HTTP_PROXY=${yourProxyServer}
   ```
   ```
3. Insert the following line of JavaScript to the third line of Forge’s `cli.js`:

   ```
   ```
   1
   2
   ```



   ```
   require('global-agent/bootstrap');
   ```
   ```

**Finding cli.js**

`cli.js` will be located in the ‘lib’ folder of your Node.js installation.

For example:
`%YOUR_NODE_INSTALLATION%/lib/node_modules/@forge/cli/out/bin/cli.js`

* **Changes will be overwritten on upgrade**  
  These configuration steps include modifying a file that is distributed with the Forge CLI. If you upgrade your
  installation of the Forge CLI to a newer version, your changes will be overwritten and will need to be re-applied.
* **Making HTTPS connections through your proxy**  
  Depending on your proxy configuration, HTTPS connections may not work as expected. In this circumstance, you can
  try setting `export NODE_TLS_REJECT_UNAUTHORIZED=0` to temporarily disable server certificate validation as a way
  to troubleshoot or workaround this issue. Setting this value is not recommended as a permanent solution as it is
  inherently insecure and can make your Node.js development environment susceptible to man-in-the-middle attacks.

### Configuring forge tunnel to work with self-signed certificates

The forge [tunnel](https://developer.atlassian.com/platform/forge/tunneling/) command allows you to run your app code locally on your machine via the Forge CLI and Cloudflare.

If your forge app makes egress requests and your corporate proxy replaces certficates with self-signed ones, you will need to make change to your TLS settings.

Either:

* Export `TUNNEL_NO_TLS_VERIFY=true` before running the tunnel command.
* Disable TLS inspection between the developer laptop and `forge-outbound-proxy.services.atlassian.com` which is the host that egress requests from your forge app are routed through.

## Allowing the Forge CLI to make outbound connections

If you are developing Forge apps from behind a corporate firewall, you may need to contact your network administrator to allow the CLI to connect to the external hosts it depends on. Below is a table showing which external hosts may need to be allowlisted by your network administrator in order for the Forge CLI to function correctly.

| Destination domain | Purpose | Required or optional |
| --- | --- | --- |
| [api.atlassian.com](http://api.atlassian.com) | [api.atlassian.com](http://api.atlassian.com) is a GraphQL endpoint that the Forge CLI uses to manage the details of your Forge apps. | **Required.** The Forge CLI will not work correctly if this connection is blocked. |
| [forge-templates.us-west-2.prod.public.atl-paas.net](http://forge-templates.us-west-2.prod.public.atl-paas.net) | This is a CNAME for [d95wqm0r9zz5j.cloudfront.net](http://d95wqm0r9zz5j.cloudfront.net) This is a CDN where Forge app templates are stored. The Forge CLI retrieves these templates for use when the `forge create` command is run. | **Required.** You will not be able to create new Forge apps if this connection is blocked. |
| [forge-node-runtime.prod-east.frontend.public.atl-paas.net](http://forge-node-runtime.prod-east.frontend.public.atl-paas.net) | This is a CNAME for [d1i66qtumh4yze.cloudfront.net](http://d1i66qtumh4yze.cloudfront.net) This is the CDN from which the Forge CLI downloads the latest Forge runtime packages. | **Required.** You will not be able to deploy Forge apps if this connection is blocked. |
| [forge-cdn-tmp-prod.s3.us-west-2.amazonaws.com](http://forge-cdn-tmp-prod.s3.us-west-2.amazonaws.com) | This is an S3 bucket where the Forge CLI uploads your front-end resources (if using Custom UI or UI Kit). | **Required.** You will not be able to deploy Forge apps with front-end components if this connection is blocked. |
| [deployment-artifacts-914424261525-us-west-2.s3.us-west-2.amazonaws.com](http://deployment-artifacts-914424261525-us-west-2.s3.us-west-2.amazonaws.com) | The production Forge environment is sharded into multiple AWS accounts. This is an S3 bucket where the Forge CLI may upload your bundled app artifact, depending on which shard your app is assigned to. | **Required.** You will not be able to deploy Forge apps if this connection is blocked. |
| [deployment-artifacts-372253104996-us-west-2.s3.us-west-2.amazonaws.com](http://deployment-artifacts-372253104996-us-west-2.s3.us-west-2.amazonaws.com) | The production Forge environment is sharded into multiple AWS accounts. This is an S3 bucket where the Forge CLI may upload your bundled app artifact, depending on which shard your app is assigned to. | **Required.** You will not be able to deploy Forge apps if this connection is blocked. |
| [deployment-artifacts-149731130117-us-west-2.s3.us-west-2.amazonaws.com](http://deployment-artifacts-149731130117-us-west-2.s3.us-west-2.amazonaws.com) | The production Forge environment is sharded into multiple AWS accounts. This is an S3 bucket where the Forge CLI may upload your bundled app artifact, depending on which shard your app is assigned to. | **Required.** You will not be able to deploy Forge apps if this connection is blocked. |
| [registry.npmjs.org](http://registry.npmjs.org) | The Forge CLI downloads packages from the central NPM repository when you add npm dependencies to your app project. | **Required.** You will not be able to create or develop Forge apps if you cannot manage the NPM dependencies of your app. You can configure your local environment to use a local NPM package mirror as an alternative to using the central NPM repository (See **Configuring NPM to use a local repository**). |
| [github.com](http://github.com) | The Forge CLI retrieves and downloads some dependencies from Github during installation. | **Required.** You will not be able to install the Forge CLI if this connection is blocked. |
| [objects.githubusercontent.com](http://objects.githubusercontent.com) | The Forge CLI retrieves and downloads some dependencies from Github during installation. | **Required.** You will not be able to install the Forge CLI if this connection is blocked. |
| <as.atlassian.com> | The Forge CLI periodically sends anonymised usage information to Atlassian so that we can improve the CLI over time. | Optional. The Forge CLI will continue to function, even if this connection is blocked. You can disable the CLI from attempting to make this connection by running `forge settings set usage-tracking false`. |
| [developer.atlassian.com](http://developer.atlassian.com) | The `forge lint` command may periodically download OpenAPI spec files from [developer.atlassian.com](http://developer.atlassian.com) in order to identify missing API scopes from your app manifest. | Optional. The `forge lint` command may not work correctly if this connection is blocked. Running `forge deploy --no-verify` may be necessary to skip linting during deployment if this connection is blocked. |
| [app.launchdarkly.com](http://app.launchdarkly.com) | This is a CNAME for [c3.shared.global.fastly.net](http://c3.shared.global.fastly.net).  The Forge CLI uses LaunchDarkly as a feature-flagging service, allowing us to incrementally roll out changes to different cohorts of users.  NOTE: LaunchDarkly is a third party service not owned by Atlassian. Changes to their network infrastructure (such as their API host name) are outside of Atlassian's control. | Optional. The Forge CLI will continue to function, even if this connection is blocked. You may have difficulty enrolling in Early Access Programs for Forge, as these programs may include feature flags for the Forge CLI. |
| [o55978.ingest.sentry.io](http://o55978.ingest.sentry.io) | The Forge CLI uses [sentry.io](http://sentry.io) to track errors and usage so that we can improve the CLI over time. | Optional. The Forge CLI will continue to function, even if this connection is blocked. You can disable the CLI from attempting to make this connection by running `forge settings set usage-tracking false`. |
| Cloudflare tunnel connections: see [Cloudflare docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/deploy-tunnels/tunnel-with-firewall/) | Forge CLI versions `10.1.0` and beyond use Cloudflare to power the `forge tunnel` command. Only the ports listed in [Cloudflare docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/deploy-tunnels/tunnel-with-firewall/) under 'Required for tunnel operation' are needed. 'Optional' ports are not required. | Optional. You will not be able to use the `forge tunnel` command if this connection is blocked. It is still possible to build and deploy Forge apps without the local debugging benefit of the tunnel. |
