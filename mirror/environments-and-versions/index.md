# Environments

When you call `forge create`, we automatically create three environments for you:

* development
* staging
* production

Environments are where you deploy your app. Once an app is running in an environment,
you can install it from that environment on to an Atlassian site with `forge install`.
This process is documented in our
[app tutorials](/platform/forge/build-a-hello-world-app-in-confluence/#install-your-app).

We recommend using the *development* environment for testing your changes, *staging* for
a stable version of your app, and *production* as the version of your app that’s ready
for use.

By default, the CLI will run commands for the *development* environment unless you specify
another with the `--environment` flag.

While your app is deployed to development, your app title will have the suffix `(DEVELOPMENT)`.
Similarly, while your app is deployed to staging, it will have the suffix `(STAGING)`.
Once you deploy your app to production, your app title will no longer have any suffix.

## Environment restrictions

When using the *staging* environment, you can't use the `forge tunnel` command. You'll need
to redeploy your app using `forge deploy` each time you make a code change.

When using the *staging* and *development* environments, you won't be able to view the scopes defined
for the APIs included in your Forge app. You'll need to deploy your app to the *production* environment
for scopes to display. See
[View Forge app permissions](/platform/forge/manage-your-apps/#view-forge-app-permissions/) for
more details.

When using the *production* environment, you can't use the `forge tunnel` or `forge logs` commands.
To debug issues, you’ll need to redeploy your affected
code to the *staging* or *development* environments where you have access to
[debugging](https://developer.atlassian.com/platform/forge/debugging/) tools.
For apps installed on sites you don’t have access to, you’ll need to ask the app
user to
[download the logs for your app and send them to you](https://developer.atlassian.com/platform/forge/access-app-logs/).

## Environment variables

Environment variables are key-value pairs you can manage via the
[Forge CLI variables commands](https://developer.atlassian.com/platform/forge/cli-reference/variables/). Each
of your variables has separate values corresponding to the different environments your app is deployed
to (development, staging, production). As with other Forge CLI commands, the
[Forge CLI variables commands](https://developer.atlassian.com/platform/forge/cli-reference/variables/) act on the
development environment unless another environment is specified explicitly.

Environment variables can not be accessed by the frontend directly.
If you need access to them in your frontend code you can create a [resolver function](https://developer.atlassian.com/platform/forge/runtime-reference/forge-resolver/) to return them. Keep in mind that if they are returned to the frontend they will be visible to the user in the network traffic.

* List your environment variables by running:
* Set a variable with key *MY\_KEY* and value *my-value* by running:

  ```
  ```
  1
  2
  ```



  ```
  forge variables set MY_KEY my-value
  ```
  ```
* Set an encrypted variable by providing the `--encrypt` option by running:

  ```
  ```
  1
  2
  ```



  ```
  forge variables set --encrypt MY_KEY my-value
  ```
  ```

  Encrypted values are protected from `forge variables list` output. However, they are
  passed to your app's environment as clear text.
* Unset a variable with key *MY\_KEY* by running:

  ```
  ```
  1
  2
  ```



  ```
  forge variables unset MY_KEY
  ```
  ```
* Read a variable with key *MY\_KEY* in your code as below:
* The same variable can be set in the production environment through the `--environment` option.

  ```
  ```
  1
  2
  ```



  ```
  forge variables set --environment production --encrypt MY_KEY my-value
  ```
  ```

When you add or update an environment variable, the change won’t take effect in your app until you redeploy to that environment. Each environment (development, staging, production, or custom) uses the variable values from its most recent deployment. Remember to redeploy after making changes to environment variables to ensure your app uses the latest values.

## Forge tunnel

When you're using the `forge tunnel` command, you must prefix environment variables with
`FORGE_USER_VAR_`.

Set the value of `MY_KEY` by prefixing `FORGE_USER_VAR_` to the variable name, then
running the following command in your terminal:

```
```
1
2
```



```
export FORGE_USER_VAR_MY_KEY=test
```
```

You do not need to change variable assignment when using environment variables with `forge tunnel`,
the variable is still accessed with `MY_KEY`.

```
```
1
2
```



```
const myVar = process.env.MY_KEY // MY_KEY will be "test"
```
```

## Default environments

When you run the `forge deploy` command for the first time without specifying an environment, you are prompted
to set your default development environment. Setting a default environment lets you work on an app without
impacting the work of other contributors.

When setting the name of your default development environment, make sure not to use any
sensitive information. You can change your default environment and its name at any time
using `forge settings`.

By default, the CLI will run commands for your default *development* environment unless you specify
another with the `--environment` flag.

## Custom environments

You can create and manage additional development [environments](/platform/forge/environments-and-versions/) with `forge environments`. Additional development environments allow multiple contributors to tunnel and deploy to their own development environment simultaneously.

To create a new development environment:

1. Run the following command in your CLI:

   ```
   ```
   1
   2
   ```



   ```
   forge environments create
   ```
   ```
2. Enter a name for your environment.

   ```
   ```
   1
   2
   ```



   ```
   Create a new development environment.

   ? Enter a name for your environment: my-dev-environment

   Creating environment...

   Created DEV my-dev-environment

   You can now tunnel or deploy to this new development environment.
   ```
   ```

## Versions

When you run forge deploy, a new version is created in the Forge environment you specified
(or in your [default environment](#default-environments)). See
[App versions](/platform/forge/versions/) for more information.
