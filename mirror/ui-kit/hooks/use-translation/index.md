# useTranslation

This page explains the [useTranslation](#usetranslation) hook which can be used to internationalize
[UI Kit](/platform/forge/ui-kit/) apps. To internationalize a [Custom UI](/platform/forge/custom-ui/) app, see [i18n](/platform/forge/apis-reference/ui-api-bridge/i18n).

Note that internationalization does not support the legacy version of UI Kit, UI Kit 1. If you have
a UI Kit 1 app that you would like to internationalize, you will first have to upgrade to the
[latest version of UI Kit](/platform/forge/ui-kit/upgrade-to-ui-kit-latest/).

The [useTranslation](#usetranslation) hook and [I18nProvider](#i18nprovider) are React-specific APIs that allow you to access the
translation resources configured in [Translations](/platform/forge/manifest-reference/translations/).
These tools enable your UI Kit app to adapt based on a user’s language and locale.

## useTranslation

The `useTranslation` hook provides the current i18n context value. This includes the translation
function, known as the `t` function, which is bound to a specified [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) through the `I18nProvider`.

### Usage

To add the `useTranslation` hook to your app:

```
1
import { useTranslation, I18nProvider } from "@forge/react";
```

Ensure that the `useTranslation` hook is used within components that have the [I18nProvider](#i18nprovider) correctly configured at the top of the component hierarchy.

Here is an example of an app that displays translated content with `useTranslation`:

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
import React from 'react';
import ForgeReconciler, { Text, useTranslation, I18nProvider } from '@forge/react';

const App = () => {
  const { ready, t } = useTranslation();
  if (!ready) {
    return null;
  }

  // usage of the `t` function to resolve translation for 'app.message'
  return <Text>{t('app.message')}</Text>;
};

ForgeReconciler.render(
  <React.StrictMode>
    <I18nProvider>
      <App />
    </I18nProvider>
  </React.StrictMode>
);
```

### Function signature

```
```
1
2
```



```
function useTranslation(): I18nContextValue;

type I18nContextValue =
  | {
      ready: false;
      t: TranslationFunction;
    }
  | {
      ready: true;
      t: TranslationFunction;
      locale: ForgeSupportedLocaleCode;
    };

type TranslationFunction = (i18nKey: string, defaultValue?: string) => string;
```
```

### Arguments

None.

### Returns

* **ready**: A boolean value that indicates whether the i18n context is fully initialized.
* **t**: The translation function, known as the `t` function, which performs translations by
  replacing the translation key with the translation value. It uses the assigned locale code and
  fallback configuration, if required, to determine the appropriate translation.
  * **Arguments**:
    * **i18nKey**: The key to be translated. The key should correspond to a string value in the
      translation files.
    * **defaultValue**: The default value to return if the translation key cannot be resolved.
  * **Returns**:
    * The translated string. This is the translation value that corresponds to the provided
      translation key. If the key is not found, the function returns the `defaultValue` if provided.
      If the key is not found and no `defaultValue` is provided, it returns the translation key itself
      to help identify which translations are missing.
* **locale**: The [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the desired translation determined by the `I18nProvider`.
  This is either explicitly provided through the `locale` parameter or defaults to the user’s preferred
  locale, which is retrieved from [view.getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext)
  after the i18n context has been initialized (that is, when ready is set to `true`).

## I18nProvider

The `I18nProvider` is a [React Context Provider](https://react.dev/learn/passing-data-deeply-with-context)
designed to support internationalization for [UI Kit](/platform/forge/ui-kit/) apps. It initializes and provides an i18n context,
which includes the user’s locale and the `t` function,
making them accessible to any components that consume this context.

### Component signature

```
```
1
2
```



```
type I18nProvider = React.FC<{
 locale?: ForgeSupportedLocaleCode;
 children?: React.ReactNode
}>
```
```

### Properties

* **locale**: The target [locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) for the i18n context being initialized. If left unspecified or
  set to undefined, the locale will default to the user's preferred locale retrieved from
  [view.getContext](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext).
* **children**: The components nested within the `I18nProvider` will inherit its i18n context. This
  allows the components to effectively utilize translation functions and locale configurations via
  [useTranslation](#usetranslation).
