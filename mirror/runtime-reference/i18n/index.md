# i18n API

This page explains [createTranslationFunction](#createtranslationfunction) and
[getTranslations](#gettranslations) which can be used to internationalize [Forge functions](/platform/forge/function-reference/index/). To add internationalization support for your app's frontend,
see the [useTranslation](/platform/forge/ui-kit/hooks/use-translation) hook for UI Kit apps or the [Forge bridge i18n](/platform/forge/apis-reference/ui-api-bridge/i18n/#i18n) function for Custom UI apps.

The `i18n` APIs allow you to access the translation resources configured in [Translations](/platform/forge/manifest-reference/translations/) so that your app can adapt based on a user’s language and locale. There
are two functions available:

* [createTranslationFunction](#createtranslationfunction), which provides basic translation
  functionalities to internationalize your app.
* [getTranslations](#gettranslations), which allows you to integrate with third-party i18n frameworks,
  such as [i18next](https://www.i18next.com/). This allows you to access advanced translation features like interpolation, formatting, and plurals by preparing the translation resources for these i18n frameworks.

## createTranslationFunction

`createTranslationFunction()` allows you to generate a translation function, referred to as the `t`
function, bound to a specified [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/). This function performs translations by replacing
the requested translation key with its respective localized string based on the translation files specified
in the app manifest.

### Function signature

```
1
2
3
4
5
const createTranslationFunction = (
  locale: ForgeSupportedLocaleCode
): Promise<TranslationFunction>

type TranslationFunction = (i18nKey: string, defaultValue?: string) => string;
```

### Arguments

* **locale**: The target [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the translation. Please refer to [here](#accessing-locale-information-on-the-forge-function-side) for more information on how to access the locale information on the Forge function side.

### Returns

* **translation function**: The translation function, known as the `t` function, which
  performs translations by replacing the translation key with the translation value. It uses the
  assigned locale code and fallback settings, if required, to determine the appropriate translation.
  * **Arguments**:
    * **i18nKey**: The key to be translated. The key should correspond to a string value in the
      translation files.
    * **defaultValue**: The default value to return if the translation key cannot be resolved.
  * **Returns**:
    * The translated string. This is the translation value that corresponds to the provided
      translation key. If the key is not found, the function returns the `defaultValue` if provided.
      If the key is not found and no `defaultValue` is provided, it returns the translation key itself
      to help identify which translations are missing.

### Example

```
```
1
2
```



```
import api, { i18n } from "@forge/api";

const resolver = new Resolver();

resolver.define("getText", async (req) => {
  const t = await i18n.createTranslationFunction('en-US');
  return JSON.stringify({
    text: t("page.content"),
  });
});

export const handler = resolver.getDefinitions();
```
```

## getTranslations

`getTranslations()` retrieves the content of a translation file for a specified `locale` code.

### Function signature

```
```
1
2
```



```
const getTranslations = (
  locale: ForgeSupportedLocaleCode,
  options: GetTranslationsOptions = { fallback: true }
): Promise<GetTranslationsResult>

interface GetTranslationsOptions {
    fallback: boolean;
}

interface GetTranslationsResult {
  locale: ForgeSupportedLocaleCode;
  translations: TranslationResourceContent | null;
}

interface TranslationResourceContent {
  [key: string]: string | TranslationResourceContent;
}
```
```

### Arguments

* **locale**: The target [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the translation resource that will be fetched. Please refer to [here](#accessing-locale-information-on-the-forge-function-side) for more information on how to access the locale information on the Forge function side.
* **options**:
  * **fallback**: Specifies whether the [fallback configuration](/platform/forge/manifest-reference/translations/#fallback-configuration) will be taken into account during the retrieval of the translation resource.

### Returns

* **locale**: The [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) of the translation resource returned within the payload. If the
  `fallback` option is enabled and the translation resource for the requested locale is unavailable,
  the returned locale might differ from the requested one as the function retrieves the translation
  resource from the corresponding fallback locale instead.
* **translations**: The parsed content of the translation file for the specified locale. If the
  translation file and fallback can't be found for the given locale, the function returns `null`. The
  `getTranslations()` function retrieves the complete content of the specified translation file. In
  this process, the `fallback` setting is not implemented at the specific translation key level.
  Therefore, if the intended translation key is absent from the designated translation file, you might
  need to obtain the required content for that key by requesting an alternative translation file.

### Example

```
```
1
2
```



```
import api, { i18n } from "@forge/api";

const resolver = new Resolver();

resolver.define("getText", async (req) => {
  const { translations, locale } = await i18n.getTranslations("en-US");
  return JSON.stringify({
    translations,
    locale,
  });
});

export const handler = resolver.getDefinitions();
```
```

## Accessing locale information in Forge functions

A user's `locale` information is not directly available to Forge functions. This is because:

* The Forge function runtime is shared across users.
* Not all Forge functions are user-specific, such as [web triggers](/platform/forge/runtime-reference/web-trigger/#web-triggers).

There are several ways for Forge functions to access a user's locale information. This includes:

* Passing the locale information from the frontend to the backend via the request payload.
* Using the [Atlassian app fetch API](/platform/forge/runtime-reference/fetch-api/#fetch-api) to retrieve the locale information from the Atlassian app API.
  * For Confluence, you can use the [getCurrentUser](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-users/#api-wiki-rest-api-user-current-get) API to get the locale information for the current user.

    ```
    ```
    1
    2
    ```



    ```
    const getConfluenceLocale = async () => {
      const response = await api
        .asUser()
        .requestConfluence(route`/wiki/rest/api/user/current`, {
          headers: {
            Accept: "application/json",
          },
        });
      const confluence = await response.json();

      return confluence.locale;
    };
    ```
    ```
  * For Jira, you can use the [getLocale](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-myself/#api-rest-api-3-mypreferences-locale-get) API to get the locale information for the current user.

    ```
    ```
    1
    2
    ```



    ```
    const getJiraLocale = async () => {
      const response = await api
        .asUser()
        .requestJira(route`/rest/api/3/mypreferences/locale`, {
          headers: {
            Accept: "application/json",
          },
        });
      const jira = await response.json();

      return jira.locale;
    };
    ```
    ```
