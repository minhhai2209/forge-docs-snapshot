# i18n

This page explains the [createTranslationFunction](#createtranslationfunction) and
[getTranslations](#gettranslations) functions which can be used to internationalize Forge apps.
While these functions can be used for both [Custom UI](/platform/forge/custom-ui/) and [UI Kit](/platform/forge/ui-kit/) apps,
we recommend using the [useTranslation](/platform/forge/ui-kit/hooks/use-translation) UI Kit hook to internationalize UI Kit apps.

The `i18n` APIs allow you to access the translation resources configured in [Translations](/platform/forge/manifest-reference/translations/) so that your app can adapt based on a user’s language and locale. There
are two functions available:

* [createTranslationFunction](#createtranslationfunction) which provides basic translation
  functionalities to internationalize your app.
* [getTranslations](#gettranslations) which allows you to integrate with third-party i18n frameworks,
  such as [i18next](https://www.i18next.com/). This allows you to access advanced translation features like interpolation, formatting, and plurals by preparing the translation resources for these
  i18n frameworks.

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
  locale: ForgeSupportedLocaleCode | null = null
): Promise<TranslationFunction>

type TranslationFunction = (i18nKey: string, defaultValue?: string) => string;
```

### Arguments

* **locale**: The target [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the translation. This should be left unspecified or set to
  `null` so that the locale will default to the user's preferred locale, which is retrieved from
  [view.getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext).

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
import React, { useState, useEffect } from "react";
import { i18n } from "@forge/bridge";

const App = () => {
  const [t, setT] = React.useState(null);
  useEffect(() => {
    const loadTranslator = async () => {
      const t = await i18n.createTranslationFunction();
      // Use the updater function in the React state setter to ensure t is set correctly.
      // Note, setT(t) would not work as expected, as t is a function. For more information, see
      // https://react.dev/reference/react/useState#im-trying-to-set-state-to-a-function-but-it-gets-called-instead
      setT(() => t);
    };
    loadTranslator();
  }, [setT]);

  if (!t) {
    return <div>loading...</div>;
  }

  return (
    <div>{t('page.content')}</div>
  );
};
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
  locale: ForgeSupportedLocaleCode | null = null,
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

* **locale**: The target [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the translation resource that will be fetched. This should
  be left unspecified or set to `null` so that the locale will default to the user's preferred locale,
  which is retrieved from [view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext).
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
import React, { useState, useEffect } from "react";
import { i18n } from "@forge/bridge";

const App = () => {
  const [translations, setTranslations] = React.useState(null);
  const [locale, setLocale] = React.useState(null);

  useEffect(() => {
    const loadTranslations = async () => {
      const { translations, locale } = await i18n.getTranslations();
      if (translations) {
        setTranslations(translations);
        setLocale(locale);
      }
    };
    loadTranslations();
  }, [setTranslations, setLocale]);

  if (!translations) {
    return <div>loading...</div>;
  }

  return (
    <>
      <div>locale: {locale}</div>
      <div>translations: {JSON.stringify(translations)}</div>
    </>
  );
};
```
```
