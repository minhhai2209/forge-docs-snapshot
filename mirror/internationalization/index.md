# Internationalization

With internationalization (i18n), you can make your Forge app available in multiple languages. Once internationalized, your app can translate it's content based on a user’s language and locale. Note that you need to choose the languages you want your app to support and configure the corresponding translation files. For a full list of supported languages and their locale codes, see [Forge supported locale codes](/platform/forge/manifest-reference/forge-supported-locale-codes).

Internationalization can be used by [UI Kit](/platform/forge/ui-kit/) apps, including apps using the [Frame component](/platform/forge/ui-kit/components/frame), as well as [Custom UI](/platform/forge/custom-ui/) apps. The internationalization capability in Forge supports both:

* **Module properties:** Elements of the UI defined in the app [manifest](/platform/forge/manifest-reference/translations/#manifest-structure) that are displayed in Atlassian apps. For example, a label for your app in the top menu.
* **App frontend:** Elements of the UI that are defined in the frontend code of your app. For example, the content within your app.

## Prerequisites

Internationalization does not support UI Kit 1, the legacy version of UI Kit. If you have a UI Kit 1 app that you would like to internationalize, you will first have to [upgrade to the latest version of UI Kit](/platform/forge/ui-kit/upgrade-to-ui-kit-latest/).

You must also update to the latest Forge CLI version. To do this:

1. Install the Forge CLI globally by running:

   ```
   1
   npm install -g @forge/cli@latest
   ```
2. Verify that the CLI is installed correctly by running:

   You should be on version `11.3.0` or higher.

Additionally, if you'd like to add internationalization support to your app frontend code using the [i18n](/platform/forge/apis-reference/ui-api-bridge/i18n/) functions or the [useTranslation](/platform/forge/ui-kit/hooks/use-translation/) UI Kit hook, ensure that you are using the latest version of `@forge/bridge` and `@forge/react`.

1. Install the latest `@forge/bridge` package to the project by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/bridge@latest
   ```
   ```
2. Install the latest `@forge/react` package to the project by running:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/react@latest
   ```
   ```

## Setting up internationalization for your Forge app

Internationalizing your Forge app involves creating translation files, updating your manifest, and updating your app code. Here's an overview of what is required:

* **Create translation files:** Create JSON files that define translation keys and their corresponding translated strings. You need a translation file for each language your app supports. For configuration details, see [Translation files](/platform/forge/manifest-reference/translations/#translation-files).
* **Configure your manifest:** Configure your app’s `manifest.yml` file to specify the path to the translation files. Additionally, you must define the [fallback configurations](#fallback-configurations) for your app in the manifest. For more information, see [Translations](/platform/forge/manifest-reference/translations).
* **Add translatable keys to the module properties:** Use translation resources to configure translatable module properties in the `manifest.yml` file. For guidance, see [Translatable module properties](/platform/forge/manifest-reference/translations/#translatable-module-properties).
* **Add internationalization support to your app frontend code using APIs and UI hooks:** To make UI elements in your app's frontend code translatable, add translation resources to your app's code. You can use the Forge internationalization hooks and APIs to translate this content based on a user’s locale. For UI Kit apps, we recommend using the [useTranslation](/platform/forge/ui-kit/hooks/use-translation/) UI Kit hook. Both UI Kit and Custom UI apps can use the [i18n](/platform/forge/apis-reference/ui-api-bridge/i18n/) function.
* **Add internationalization support for Forge functions:** Additionally, i18n support can be implemented
  for Forge functions using the [i18n API](/platform/forge/runtime-reference/i18n/).

## Fallback configurations

Translation fallback is essential to guarantee that users can still access meaningful content in cases where translations for their preferred locale are unavailable. It ensures a consistent and user-friendly experience, stepping in when the desired locale is not supported, translations are incomplete, or only partial translations are available.

There are two fallback configurations available when internationalizing your Forge app:

1. **Default fallback (required):** Your app must have an overall default fallback locale. This locale will be used if the user’s locale is not found in your configured translation files. The translation file for the default fallback locale must contain all translation keys used in your app.
2. **Locale-specific fallback configurations (optional):** You also have the option to add fallback configurations specific to given target locales. For example, if `English (US)` is your default fallback and the user’s locale is `Portuguese (Brazil)`, you might prefer `Portuguese (Portugal)` as a fallback instead of `English (US)`. In this case, you could configure `English (US)` as the overall default fallback and `Portuguese (Portugal)` as the fallback for the target locale `Portuguese (Brazil)`.

For more information on configuring translation fallbacks in the manifest, see [Fallback configuration](/platform/forge/manifest-reference/translations/#fallback-configuration).

## Get started

[Tutorial: Create a question generator app using internationalization

Follow a step-by-step tutorial to see how we created a question generator app that uses internationalization and UI Kit.](/platform/forge/create-a-question-generator-app-in-multiple-languages-using-i18n)

## Supported modules

Internationalization support can be added to the following modules:

## Moving internationalized Connect apps to Forge

Internationalization for Forge is backwards compatible with internationalized Connect apps. This means you can seamlessly transition your existing translation keys and translation files from Connect to Forge, maintaining the language support of your app.

For more information, see [Moving internationalized Connect apps to Forge](/platform/adopting-forge-from-connect/moving-internationalized-connect-apps-to-forge).
