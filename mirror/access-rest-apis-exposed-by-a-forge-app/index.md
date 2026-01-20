# Access REST APIs exposed by a Forge app (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge apps can expose REST APIs, allowing external systems to call the app’s logic over HTTP.
This tutorial demonstrates how to enable APIs for a site and call them using 3LO (OAuth 2.0).
For more information, see [Forge app REST APIs](/platform/forge/app-rest-apis/).

If you’re looking to expose app REST APIs from your own app, see [Expose Forge app REST APIs](/platform/forge/expose-forge-app-rest-apis/).

## Before you begin

Before you start, make sure:

* The Forge app you want to call **exposes app REST APIs**.
* The app developer has published documentation that maps **API endpoints to scopes**.
* You have access to:

## Step 1: Enable app REST APIs in Connected apps

Forge app REST APIs are **disabled by default** for each site and must be explicitly enabled by a
site or organization admin.

To enable app REST APIs for a site:

1. Go to [Atlassian Administration](https://admin.atlassian.com/) and select your organization.
2. In the left-hand navigation, go to **Apps**, then **Sites** and select the site where the Forge app is installed.
3. In the left-hand navigation for that site, select **Connected apps**.
4. Find the Forge app that exposes REST APIs and click **View app details**.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/admin-hub-connected-apps-details.png?_v=1.5800.1783)
5. On the app details page, open the **Details** tab and locate the **App REST APIs** section.
   There, there is a button that you can use to enable or disable app REST APIs - you can do so at any
   time. Disabling it will immediately block API calls to this app’s REST endpoints for that site.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/admin-hub-connected-apps-rest-api-toggle.png?_v=1.5800.1783)

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/admin-hub-connected-apps-enable-rest-apis.png?_v=1.5800.1783)

App REST APIs on Forge are **disabled by default**.
If the site or organization admin doesn’t enable this feature in **Connected apps**, app REST APIs
won’t be accessible to members of the site.

## Step 2: Create a 3LO integration for the app

Forge app REST APIs use 3LO (OAuth 2.0) for authentication and authorization. To call an app
REST API, you must first create a 3LO integration and grant it access to the appropriate scopes.

Only members of the site where the Forge app is installed can create a 3LO integration that connects
to that app’s REST APIs.

### Create a 3LO app

1. Go to the [Developer Console](https://developer.atlassian.com/console).
2. Click **Create** and select **OAuth 2.0 integration**.
3. Follow the prompts to name and create your 3LO app.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-create-3lo-integration.png?_v=1.5800.1783)

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-name-3lo-integration.png?_v=1.5800.1783)

### Connect the 3LO app to the Forge app

1. In your 3LO app, open the **Permissions** section.
2. On the right side, click **Add Marketplace or custom app**.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-3lo-add-forge-app-button.png?_v=1.5800.1783)
3. In the modal that opens, first select the **site** where the Forge app is installed.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-modal-with-site.png?_v=1.5800.1783)
4. After you select the site, you’ll see a list of Forge apps installed on that site. Choose the
   Forge app (and environment) that exposes the REST APIs you want to access.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-modal-with-app.png?_v=1.5800.1783)
5. Select the **scopes** that your integration needs, based on the app developer’s documentation. You must select at least one scope.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-forge-app-scopes-modal.png?_v=1.5800.1783)

   Select only the scopes that you need in order to access the APIs.
   For example, if you only need to use the `/getEmployeeName` API, select the scope mapped to it,
   such as `read:employee:custom`, and do **not** select `write:employee:custom`.
6. Select **Add**. The Forge app will then appear in the **Permissions** tab for your 3LO integration. You
   can always edit the scopes later as needed.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-permissions-tab-with-forge-app.png?_v=1.5800.1783)
7. In addition to these app-defined scopes, add the **Forge app product scopes** required for the
   relevant Atlassian apps (currently Jira and Confluence). For example:

   * Jira: `read:forge-app:jira`
   * Confluence: `read:forge-app:confluence`

### Configure authorization and obtain an access token

1. Navigate to the **Authorization** section of your 3LO app and configure the **callback URL**. This URL
   is required to complete the OAuth 2.0 flow and obtain an authorization code.
2. After you configure the callback, the Developer Console will show an **authorization URL** for
   your 3LO app under the Forge app entry.
   This URL already includes the app-defined scopes and Atlassian app-level Forge scopes you selected.

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-authorization-tab.png?_v=1.5800.1783)

   ![Screenshot](https://dac-static.atlassian.com/platform/forge/images/forge-rest-apis/dev-console-auth-url.png?_v=1.5800.1783)
3. Use the authorization URL to obtain an access token. In a production setup, this flow is usually
   handled by your integration code, but you can perform it manually for testing:

   1. Paste the authorization URL into your browser and press **Enter**.
   2. On the 3LO consent screen, choose the site where the Forge app is installed and click **Accept**.
   3. After consent, you'll be redirected to the callback URL with a `code` query parameter. Copy this
      authorization code.
   4. Exchange the authorization code for an access token by following the instructions in
      [Exchange authorization code for access token](https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/#2--exchange-authorization-code-for-access-token).

## Step 3: Call the app REST APIs

App REST API calls must include the 3LO access token in the `Authorization` header.

### Example request

```
```
1
2
```



```
curl --request GET \
  --url <REQUEST_URL> \
  --header "Authorization: Bearer ACCESS_TOKEN" \
  --header "Accept: application/json"
```
```

* Replace `<REQUEST_URL>` with one of the app’s REST API endpoints.
* Replace `ACCESS_TOKEN` with the token you obtained in Step 2.

The app documentation should list the exact URLs and methods for each endpoint. In general, app
REST API URLs follow one of these patterns:

* `https://api.atlassian.com/svc/<product>/<cloud-id>/apps/<app-id>_<env-id>/<path>`
* `https://<site-name>/gateway/api/svc/<product>/apps/<app-id>_<env-id>/<path>`

Both URLs invoke the same function: the first uses the cloud ID, and the second uses the site name.
Choose whichever form best fits your integration or existing URL handling

### Dynamic paths and parameters

App REST APIs support dynamic paths and query parameters, depending on how the `path` is defined in
the app’s `apiRoute` configuration. For example, given this base URL:

```
```
1
2
```



```
https://api.atlassian.com/svc/confluence/a12bc345-678d-9e1f-ghi0-1jkl112131m4/apps/zy2x11w1-0v1u-9876-ts54-3r210qponmlk_3aaa01b0-02cc-1d00-3eee-1f01g001h1i0/getEmployeeName
```
```

These requests might map to the following `path` values:

| Example URL | `path` declared in `apiRoute` |
| --- | --- |
| `.../getEmployeeName?id=1234` | `/getEmployeeName` |
| `.../getEmployeeName/1234` | `/getEmployeeName/*` |
| `.../getEmployeeName/new` | `/getEmployeeName/*` |
| `.../getEmployeeName/new/1234` | `/getEmployeeName/**` |

Refer to the app developer’s documentation for the exact paths, parameters, and URL patterns
supported by each REST API.

You can also pass custom headers when calling app REST APIs, for example:

```
```
1
2
```



```
curl --request GET \
  --url "https://api.atlassian.com/svc/confluence/a12bc345-678d-9e1f-ghi0-1jkl112131m4/apps/zy2x11w1-0v1u-9876-ts54-3r210qponmlk_3aaa01b0-02cc-1d00-3eee-1f01g001h1i0/getEmployeeName" \
  --header "Authorization: Bearer ACCESS_TOKEN" \
  --header "Accept: application/json" \
  --header "id: 1234"
```
```

Replace `ACCESS_TOKEN` and any custom headers with values appropriate for your integration.
