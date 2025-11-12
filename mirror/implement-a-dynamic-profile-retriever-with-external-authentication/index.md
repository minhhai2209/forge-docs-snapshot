# Implement a dynamic profile retriever with external authentication

## Before you begin

This guide assumes you're already familiar with calling an external OAuth 2.0 API using the Forge
`fetch` function, with authentication handled by the Forge platform. If not, see the
[Use an external OAuth 2.0 API with fetch](/platform/forge/use-an-external-oauth-2.0-api-with-fetch/) guide first.

### Limitations

As you work with a dynamic profile retriever, keep in mind these limitations:

* The file containing a dynamic profile retriever cannot import `@forge/react`. When executed,
  the dynamic profile retriever is run in a different context outside of the UI.
* The `displayName` attribute is displayed to the user to help distinguish between
  multiple accounts. You should *not* use the name of the user as this may be common
  across multiple accounts. Use something more specific, such as a username or email address instead.

## Update the Forge function

Create a new file called `auth.ts` in the `src` folder with the code shown below.

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
``` typescript
import { AuthProfile } from '@forge/response';

interface ProfileRetrieverParameters {
  status: number;
  body: {
    [key: string]: any;
  };
}

export const retriever = (response:   ProfileRetrieverParameters): AuthProfile => {
  const { status, body: externalProfile } =   response;

  if (status === 200){
    return new AuthProfile({
      id: externalProfile.id,
      displayName: externalProfile.email ||   externalProfile.name,
      avatarUrl: externalProfile.picture,
    });
  } else {
    throw new Error(`Could not determine   profile information. HTTP ${status}`);
  }
}
```
```

See the
[AuthProfile](/platform/forge/runtime-reference/external-fetch-api/#authprofile)
reference documentation for more details.

## Update the manifest

1. Add the new function to the `manifest.yml` file.

   ```
   ```
   1
   2
   ```



   ```
   modules:
     function:
       ...
       - key: google-profile
         handler: auth.retriever
   ```
   ```
2. Change the `retrieveProfile` action to replace the `resolvers` with a `function`.

   ```
   ```
   1
   2
   ```



   ```
   providers:
     auth:
       - key: google
         ...
         actions:
           ...
           retrieveProfile:
             remote: google-apis
             path: /userinfo/v2/me
             function: google-profile
   ```
   ```

See the [Profile retriever](/platform/forge/manifest-reference/providers/#profile-retriever) reference for more details.

## Deploy the changes

Navigate to the app's top-level directory and deploy your app with the manifest changes.

This causes a major version upgrade of your app. Users are required to upgrade to the latest
version of the app.

[Learn more about Forge versions](/platform/forge/environments-and-versions#versions).

## Debug a profile retriever

Since the profile retriever is a Forge function, you can start a tunnel to troubleshoot issues by running:

The `AuthProfile` class validates the parameters passed into its constructor and raises an exception
in the logs.

### Common errors

To assist your debugging, below are some common errors and fixes when implementing
a dynamic profile retriever.

#### Could not retrieve profile information

**Error message**:

```
```
1
2
```



```
could not retrieve profile information: There was an error invoking
the function - Can't wrap a non-transferable value
```
```

**Action**: Check your function returns an `AuthProfile` class.
