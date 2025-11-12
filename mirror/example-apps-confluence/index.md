# Example apps for Confluence

Before you begin exploring these example apps, you'll need to set up the Forge CLI first.
[Learn more about getting started](/platform/forge/getting-started/).

Once the Forge CLI is up and running, clone an example app repository to explore and customize it locally.
Each repository's `README.md` file contains quickstart instructions and other details about the app.

For more information, refer to our getting started guides for building
[Bitbucket](/platform/forge/build-a-hello-world-app-in-bitbucket/),
[Confluence](/platform/forge/build-a-hello-world-app-in-confluence/),
[Jira](/platform/forge/build-a-hello-world-app-in-jira/),
and [Jira Service Management](/platform/forge/build-a-hello-world-app-in-jira-service-management/) apps.
Our [tutorials](/platform/forge/tutorials-and-guides/) and [guides](/platform/forge/guides/)
also offer useful information for common tasks.

The `forge register` command creates a unique app ID in the `manifest.yml` file
and links the ID to the current developer. Forge apps can currently only be deployed
and installed by the developer who is linked to the app.

The content on this page is written with standard cloud development in mind. To learn about developing
for Atlassian Government Cloud, go to our
[Atlassian Government Cloud developer portal](/platform/framework/agc/).

## Question generator app with UI Kit and internationalization

A Confluence macro that displays questions in various languages based on a user’s locale. This app
uses UI Kit and [internationalization](/platform/forge/internationalization).

### Details

* **Code**: [Question generator app - i18n for UI Kit](https://bitbucket.org/atlassian/question-generator-app-i18n-for-ui-kit/src/master/)
* **Atlassian app**: Confluence
* **Modules**: `macro`
* **Custom UI**: none
* **UI Kit**:
  * `Text`, `Button`, `SectionMessage`, `Stack`, `Inline`, `Lozenge`, `Heading` and `Spinner` components from `@forge/react` library
  * `useTranslation` function and `I18nProvider` React context provider from `@forge/react` library
  * `useCallback` and `useState` hooks from `react` library
* **Runtime**: none

## Question generator app with Custom UI and and internationalization

A Confluence macro that displays questions in various languages based on a user’s locale. This app
uses Custom UI and [internationalization](/platform/forge/internationalization).

### Details

* **Code**: [Question generator app - i18n for Custom UI](https://bitbucket.org/atlassian/question-generator-app-i18n-for-custom-ui/src/master/)
* **Atlassian app**: Confluence
* **Modules**: `macro`
* **Custom UI**:
  * `Text`, `Button`, `SectionMessage`, `Stack`, `Inline`, `Lozenge`, `Heading` and `Spinner` components from `@atlaskit` library
  * `i18n` and `view` module from `@forge/bridge` library
  * `useState`, `useCallback` and `useEffect` hooks from `react` library
* **UI Kit**: none
* **Runtime**: none

## Page approver app with UI Kit

Allows the easy approval or rejection of a Confluence page through the
[Confluence content byline item](/platform/forge/manifest-reference/modules/confluence-content-byline-item) module.

### Details

* **Code**: [Page Approver](https://bitbucket.org/atlassian/forge-ui-kit-2-page-approver/src/main/)
* **Atlassian app**: Confluence
* **Modules**: `confluence:contentBylineItem`
* **Custom UI**: `@forge/bridge`
* **UI Kit**:
  * `Button` and `Text` components from `@forge/react` library
  * `useEffect` and `useState` components and hooks from `react` library
* **Runtime**: `@forge/resolver`, `@forge/api`
* **Other**:
  * Uses Confluence content properties to store data.
  * Uses the [dynamicProperties](/platform/forge/manifest-reference/modules/confluence-content-byline-item/#dynamic-properties) property.

## Quiz app with UI Kit

A simple quiz app that uses Confluence page through the [Global page](/platform/forge/manifest-reference/modules/confluence-global-page/) module.

### Details

* **Code**: [Quiz](https://bitbucket.org/atlassian/forge-quiz-app/src/main/)
* **Atlassian app**: Confluence
* **Modules**: [confluence:globalPage](/platform/forge/manifest-reference/modules/confluence-global-page/)
* **Custom UI**: none
* **UI Kit**:
* **Runtime**: `@forge/resolver`, `@forge/api`

## External authentication with various auth providers

Displays user profile information retrieved from various authentication providers,
including AWS Cognito, Dropbox, Figma, GitHub, Google, Microsoft, and Slack,
in a Confluence code block using external authentication for the API requests.

### Details

* **Code:** [External authentication with various auth providers repository](https://bitbucket.org/atlassian/forge-external-auth-examples/src/main/)
* **Atlassian app:** Confluence
* **Modules:** `macro`
* **Custom UI:** none
* **UI Kit:**
  * `CodeBlock` and `Text` components.
  * `useState` and `useEffect` hooks from `react` library
* **Runtime:**
  * `@forge/resolver`, `@forge/api`
* **Other:**
  * Uses external authentication to authenticate with the provider's REST APIs.
  * Shows how to retrieve user profile information from the provider.
