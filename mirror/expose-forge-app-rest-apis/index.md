# Expose Forge app REST APIs (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

[Forge app REST APIs](/platform/forge/app-rest-apis/) let external systems call your app’s logic
through REST-style HTTP endpoints that run on Atlassian infrastructure. This page shows how to expose
those endpoints from your app using the [`apiRoute` module](/platform/forge/manifest-reference/modules/api-route/).

Currently, this functionality is only available for Jira and Confluence apps.
This feature is currently not available for apps on Isolated Cloud.

## Before you begin

Ensure you are on the latest version of the Forge CLI. To update, run:

```
1
npm install -g @forge/cli@latest
```

## Step 1: Define scopes

To expose secure REST APIs, your Forge app must first declare its own scopes in a separate
`custom-scopes.yaml` file. These scopes define the boundaries of what your app’s APIs can do and
are independent of Atlassian app scopes. Throughout this page, we refer to them as developer‑defined scopes.

To declare these scopes, you will:

* Create a `custom-scopes.yaml` file that defines your app’s scopes.
* Choose good, maintainable names for your scopes.
* Register scopes in a Forge environment and verify they were created.

### Create `custom-scopes.yaml`

Configure your editor to use the following JSON Schema for the `custom-scopes.yaml` file:

```
```
1
2
```



```
title: Custom Scopes Data
$schema: http://json-schema.org/draft-07/schema#
$comment: >-
  Note: schema.json is generated from schema.yaml
type: object
additionalProperties: false
properties:
  version:
    # This is a file version maintained by Atlassian. It cannot be changed.
    type: number
    exclusiveMinimum: 0
    enum:
      - 1
  scopes:
    type: object
    minProperties: 1
    maxProperties: 20
    additionalProperties: false
    patternProperties:
      "^[-.:_a-zA-Z0-9]{1,93}:custom$":
        type: object
        additionalProperties: false
        properties:
          description:
            type: string
            minLength: 1
            maxLength: 2048
            pattern: "^\\S[\\s\\S]*\\S$|^\\S$" # Allow newlines in the middle.
          displayName:
            type: string
            minLength: 1
            maxLength: 100
            pattern: "^\\S.*\\S$|^\\S$"
            $comment: >-
              Scope name suitable for displaying to end users.
        required:
          - description
required:
  - version
  - scopes
```
```

Example `custom-scopes.yaml`:

```
```
1
2
```



```
version: 1
scopes:
  read:employee:custom:
    displayName: Read Employee Info
    description: >-
      Read employee information such as name, date of joining, etc.
  write:employee:custom:
    displayName: Edit Employee Info
    description: >-
      Edit information related to an employee such as name, dob, payroll info, etc.
```
```

### Name your scopes

Every developer-defined scope name must end with the suffix `:custom`.

For guidance on scope naming, see
[Best practices](/platform/forge/app-rest-apis/#scopes).

Note that:

* Developer-defined scopes cannot be disabled or deleted.
* The `name` for a developer-defined scope cannot be updated.
* You can always register more developer-defined scopes in your Forge app, as long as the total
  number of scopes per environment is under 20.

Because of the above constraints, be very careful and deliberate when deciding the scopes for your
Forge app.

### Register scopes in an environment

Only Forge app admins have the required permissions to register developer-defined scopes. After
creating the `custom-scopes.yaml` file and defining your scopes, the admin can run the following
command to register your developer‑defined scopes in a specific environment:

```
```
1
2
```



```
$ forge custom-scopes create -e <env> -f <location of custom-scopes.yaml file>
```
```

Not specifying the environment will result in registration in the default (development) environment.

### Verify registered scopes

You can check the developer-defined scopes registered in an environment using the following CLI
command:

```
```
1
2
```



```
$ forge custom-scopes list -e <env>
```
```

This returns a list of all scopes that are registered in the specified environment. For example:

```
```
1
2
```



```
✔ Completed fetching custom scopes
┌───────────────────────┬────────────────────┐
│ Name                  │ Display name       │
├───────────────────────┼────────────────────┤
│ read:employee:custom  │ Read Employee Info │
├───────────────────────┼────────────────────┤
│ write:employee:custom │ Edit Employee Info │
└───────────────────────┴────────────────────┘
```
```

Once the developer-defined scopes are registered in the relevant environment, you’re ready to map
them to REST APIs and expose these APIs securely in your Forge app.

## Step 2: Add `apiRoute` entries to your manifest

The `apiRoute` module is used to expose REST APIs in a Forge app.

In your manifest, add the [`apiRoute` module](/platform/forge/manifest-reference/modules/api-route/)
under `modules`. For each REST API you want to expose, specify your function, the path, and the HTTP
method that you want to use.

In this example, we use `resolver` as the function, `/getEmployeeName` as the path, and `GET` as the HTTP method for
the call. The developer-defined scope being mapped to the `/getEmployeeName` API is
`read:employee:custom`. Note that we’d already registered this scope in the previous section.

```
```
1
2
```



```
modules:
  apiRoute:
    - key: employee-api-1
      path: /getEmployeeName
      operation: GET
      function: handler1
      accept:
        - application/json 
      scopes:
        - read:employee:custom
    - key: employee-api-2
      path: /editEmployeeName
      operation: POST
      function: handler2
      accept:
        - application/json 
      scopes:
        - read:employee:custom
        - write:employee:custom
```
```

## Step 3: Map `apiRoute` entries to functions

Map the function specified under `apiRoute` to a function in your code, such as `index.handler`:

```
```
1
2
```



```
function:
  function:
    - key: handler1
      handler: index.handler1
    - key: handler2
      handler: index.handler2
```
```

## Step 4: Implement your handlers

Add your function logic in the `handler` functions and import them in your `src/index.js` file.

Example `src/resolvers/index.js`:

```
```
1
2
```



```
export const handler1 = (req) => {
  return {
      "statusCode": 200,
      "customHeader": "done",
      "body": "Received request /getEmployeeName: ${JSON.stringify(req)}"
  }
}

export const handler2 = (req) => {
  return {
      "statusCode": 201,
      "customHeader": "done",
      "body": "Received request /editEmployeeName: ${JSON.stringify(req)}"
  }
}
```
```

Example `src/index.js`:

```
```
1
2
```



```
export { handler1, handler2 } from './resolvers';
```
```

## Step 5: Deploy your app

Navigate to the app's top-level directory and deploy your app:

Deploying an app creates REST API endpoints for each `path` you defined under `apiRoute`. For
example, for `/getEmployeeName` you’ll see endpoints like:

* `https://api.atlassian.com/svc/<product>/<cloud-id>/apps/<app-id>_<env-id>/getEmployeeName`
* `https://<site-name>/gateway/api/svc/<product>/apps/<appid>_<env-id>/getEmployeeName`

Both of these REST API endpoints point to the same function. The difference is that the first
includes the cloud ID, whereas the second has the client site name. You may use whichever endpoint
you would like.

If using the first URL, you can retrieve the `cloud-id` for your site through the `GET` API
`https://<site-name>/_edge/tenant_info`. Additionally, the `environment-id` for your Forge app can
be obtained from the Developer Console. Note that `environment-id` is not needed if your environment
is production.

For this example, and in case of a development environment, the URLs would be:

* `https://api.atlassian.com/svc/confluence/a12bc345-678d-9e1f-ghi0-1jkl112131m4/apps/zy2x11w1-0v1u-9876-ts54-3r210qponmlk_3aaa01b0-02cc-1d00-3eee-1f01g001h1i0/getEmployeeName`
* `https://sample.atlassian.com/gateway/api/svc/confluence/apps/zy2x11w1-0v1u-9876-ts54-3r210qponmlk_3aaa01b0-02cc-1d00-3eee-1f01g001h1i0/getEmployeeName`

## Step 6: Install the app

Install the app on your site so the REST APIs become available using the following command:

```
```
1
2
```



```
forge install -e <env>
```
```

If you are distributing this app to customers via Atlassian Marketplace, you will need to publish
developer documentation specifying the mapping between REST APIs and scopes for your Forge app.
This helps customers decide which scopes to grant when configuring access to your APIs.

## FAQs

| Question | Answer |
| --- | --- |
| Which HTTP methods can I use with `apiRoute`? | `GET`, `PUT`, `POST`, `DELETE`, and `PATCH`. |
| Why am I seeing an “Invocation failed” error? | This usually indicates an issue in your handler implementation. Check your app logs using `forge logs -e <env-id>` to see the underlying error. If you still can’t identify the problem, use the trace ID from the error message when contacting Atlassian for support. |

## Next steps
