# Translations

You can [internationalize your Forge app](/platform/forge/internationalization) by defining
translation resources in your app’s `manifest.yml` file. This allows your app to support multiple
languages and adapt based on a user’s language and locale.

Internationalization can be utilized by
[UI Kit](/platform/forge/ui-kit/) apps (including apps using the
[Frame component](/platform/forge/ui-kit/components/frame/)) as well as
[Custom UI](/platform/forge/custom-ui/) apps. The internationalization capability in Forge supports both:

* Elements of the UI defined in the app [manifest](#manifest-structure) that are displayed
  in Atlassian apps. For example, the title of your app.
* Elements of the UI defined in the frontend code of your Forge app. For more information on adding
  translation resources to your frontend code, see the [useTranslation](/platform/forge/ui-kit/hooks/use-translation/) hook for
  UI Kit, the [i18n](/platform/forge/apis-reference/ui-api-bridge/i18n#createTranslationFunction) `@forge/bridge` API for Custom UI, and
  the [i18n](/platform/forge/runtime-reference/i18n/) `@forge/api` for Forge functions.

The `translations` configuration specified in this section is shared across the modules defined in the `manifest.yml` file.

## Manifest structure

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
modules {}
└─ confluence:globalPage []
   ├─ key: my-page
   ├─ resource: main
   ├─ render: native
   ├─ route: my-page
   └─ title: (string | i18n)
   │  └─ i18n: page.title (string)
translations: {}
└─ resources: {}
   ├─ key: en-US (string)
   └─ path: locales/en-US.json (string)
└─ fallback: {}
   ├─ default: en-US (string)
   └─ zh-CN: []
   │  ├─ zh-TW
   │  └─ ja-JP
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `resources` | [Translation resources](#translation-resources) | Yes | Specifies the locales supported by your Forge app, along with the respective file paths for each translation file. |
| `fallback` | [Translation fallback](#translation-fallback) | Yes | Fallback rules for resolving missing translations for any given locale. |

### Translation resources

Translation resources define the locales and translated content supported by your Forge app. Each resource entry includes the locale code and the file path for the respective locale's [translation file](#translation-files).

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | [Forge supported locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) | Yes | One of the Forge supported locale codes. For example, `en-US`. |
| `path` | `string` | Yes | The relative path from the top-level directory of your app to the translation file containing the translated strings. For example, `locales/en-US.json`. |

### Translation fallback

Translation fallback is essential to guarantee that users can still access meaningful content when translations for their
locale are unavailable. It ensures a consistent and user-friendly experience, stepping in when the desired locale is not supported, translations are incomplete, or only partial translations are available.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `default` | [Forge supported locale code](/platform/forge/manifest-reference/forge-supported-locale-codes/) | Yes | The default locale that is used when the given target locale cannot be resolved. It must:  * be one of the Forge supported locale codes * be defined in the `resources` section * be linked with a translation file that contains all translation keys defined in the manifest file |
| target locale |  | No | A rule that specifies the fallback locales to use if the target locale is missing. This means that if a translation for the target locale is not available, it will attempt to use the specified fallback locales, following the order listed, before resorting to the `default` fallback locale. For example, the below [example fallback configuration](#fallback-configuration) sets `de-DE` and `zh-CN` as the designated fallback locales for `ja-JP`. |

## Example

##### manifest.yml

```
```
1
2
```



```
modules:
  confluence:globalPage:
    - key: my-page
      resource: main
      render: native
      route: my-page
      title:
        i18n: page.title
    - key: my-app
      resource: main
      render: native
      route: my-app
      title:
        i18n: appName
    - key: my-header
      resource: main
      render: native
      route: my-header
      title:
        i18n: header
translations:
  resources:
    - key: en-US
      path: locales/en-US.json
    - key: zh-CN
      path: src/frontend/locales/zh-CN.json
    - key: zh-TW
      path: locales/zh-TW.json
    - key: de-DE
      path: locales/de-DE.json
  fallback:
    default: en-US
    zh-TW:
      - zh-CN
    ja-JP:
      - de-DE
      - zh-CN
```
```

##### Translation files

```
```
1
2
```



```
// locales/en-US.json
{
  "appName": "My cool app",
  "header": "My header",
  "page": {
    "title": "My page title"
  },
  "custom.content": "used within the app not manifest.yml"
}
```
```

```
```
1
2
```



```
// src/frontend/locales/zh-CN.json
{
  "page.title": "我的页面标题 (zh-CN)",
  "page": {
    "title": "我的页面标题 (not used)"
  },
  "header": "我的标题 (zh-CN)"
}
```
```

```
```
1
2
```



```
// locales/zh-TW.json
{
  "page": {
    "title": "我的頁面標題 (zh-TW)"
  }
}
```
```

```
```
1
2
```



```
// locales/de-DE.json
{
  "header": "Meine Kopfzeile (de-DE)"
}
```
```

## Explanation

Let’s examine the `manifest.yml` file and the associated translation files to understand how this setup works.

### Translatable module properties

In the `manifest.yml` file some `module` properties, such as the `title` of the `confluence:globalPage` module, support translations.

```
```
1
2
```



```
modules:
  confluence:globalPage:
    - key: my-page
      resource: main
      render: native
      route: my-page
      title:
        i18n: page.title
    - key: my-app
      resource: main
      render: native
      route: my-app
      title:
        i18n: appName
    - key: my-header
      resource: main
      render: native
      route: my-header
      title:
        i18n: header
```
```

To enable translation support, change the attribute type from a `string` to an `i18n object`.

For example, before adding translation support, this looks like:

After adding translation support, this looks like:

```
```
1
2
```



```
title:
  i18n: page.title
```
```

When you change the module property from a `string` to an `i18n object`, Forge can use
the translation key `page.title` to retrieve the value for the `title` property from the translation
files.

### Path to the translation files

The `manifest.yml` section outlining the locale code and its corresponding translation file path is found under
`translations.resources`.

Each translation resource has a key and path. The key is one of the
[supported locale codes](/platform/forge/manifest-reference/forge-supported-locale-codes/). The path
is the relative path from the top-level directory of your app to the translation file.
It is good practice to name the file in the format `<locale-code>.json`, where the locale code is
one of the [supported locales](/platform/forge/manifest-reference/forge-supported-locale-codes/).

```
```
1
2
```



```
translations:
  resources:
    - key: en-US
      path: locales/en-US.json
    - key: zh-CN
      path: src/frontend/locales/zh-CN.json
    - key: zh-TW
      path: locales/zh-TW.json
    - key: de-DE
      path: locales/de-DE.json
```
```

These files can be located within the UI Kit frontend source code (for example,
`src/frontend/locales/zh-CN.json`), in the project root directory (for example, `locales/en-US.json`),
or in other specified locations within the project. If a translation file needs to be shared across
multiple frontend code bundles, it is best to store the translation files in the project root directory.

### Fallback configuration

The `manifest.yml` file also specifies the fallback configurations, including the default and target fallback locales. If the target fallback rules fail to resolve the translation, the content from the default fallback will be used.

```
```
1
2
```



```
fallback:
  default: en-US
  zh-TW:
    - zh-CN
  ja-JP:
    - de-DE
    - zh-CN
```
```

You need to configure translation files for the fallback locales in the `translation.resources`
section of the manifest. In the example above, these locales are `en-US`, `de-DE`, and `zh-CN`.
If file paths for any of these locales are not configured, a validation error will be thrown when
you attempt to deploy the app.

The translation file for the default fallback is required to include translations for **all exposed translation keys** in the app manifest. If any of these i18n keys cannot be resolved in the default fallback translation file, a validation error will be thrown. The app cannot be deployed until this has been resolved.

The table below explains the fallback logic for this example:

```
```
1
2
```



```
// locales/en-US.json
{
  "appName": "My cool app",
  "header": "My header",
  "page": {
    "title": "My page title"
  },
  "custom.content": "used within the app not manifest.yml"
}
```
```

```
```
1
2
```



```
// src/frontend/locales/zh-CN.json
{
  "page.title": "我的页面标题 (zh-CN)",
  "page": {
    "title": "我的页面标题 (not used)"
  },
  "header": "我的标题 (zh-CN)"
}
```
```

```
```
1
2
```



```
// locales/zh-TW.json
{
  "page": {
    "title": "我的頁面標題 (zh-TW)"
  }
}
```
```

```
```
1
2
```



```
// locales/de-DE.json
{
  "header": "Meine Kopfzeile (de-DE)"
}
```
```

| Case | Result | Explanation |
| --- | --- | --- |
| `page.title` [`en-US`] | My Page Title | Translation is directly resolvable in `en-US`. No fallback required. |
| `page.title` [`zh-CN`] | 我的页面标题 (zh-CN) | Translation is directly resolvable in `zh-CN`. No fallback required. The translation associated with the flattened key is used over the nested one. |
| `page.title` [`zh-TW`] | 我的頁面標題 (zh-TW) | Translation is directly resolvable in `zh-TW`. No fallback required. The translation is associated with the nested key format. |
| `page.title` [`ja-JP`] | 我的页面标题 (zh-CN) | `ja-JP` → `de-DE` → `zh-CN`. A translation resource for `ja-JP` is not configured in `translations.resource`, and the translation is not resolvable using the matching fallback `de-DE`.The translation in the subsequent fallback, `zh-CN`, is used. |
| `page.title` [`fr-FR`] | My Page Title | `fr-FR` → `en-US` (default). A translation resource for `fr-FR` is not configured in `translations.resource`, and there is no matching fallback configured for `fr-FR` in `translations.fallback`. The translation from the default fallback, `en-US`, is used. |
| `appName` [`en-US`] | My cool app | Translation is directly resolvable in `en-US`. No fallback required. |
| `appName` [`zh-CN`] | My cool app | `zh-CN` → `en-US` (default). Translation is not resolvable in `zh-CN`. The translation from the default fallback, `en-US`, is used. |
| `appName` [`zh-TW`] | My cool app | `zh-TW` → `zh-CN` → `en-US` (default). Translation is not resolvable using `zh-TW` or the matching fallback `zh-CN`. The translation from the default fallback, `en-US`, is used. |
| `appName` [`ja-JP`] | My cool app | `ja-JP` → `de-DE` → `zh-CN` → `en-US` (default). A translation resource for `ja-JP` is not configured in `translations.resource`, and the translation is not resolvable using the matching fallback `de-DE` and `zh-CN`. The translation from the default fallback, `en-US`, is used. |
| `appName` [`fr-FR`] | My cool app | `fr-FR` → `en-US` (default). A translation resource for `fr-FR` is not configured in `translations.resource`, and there is no matching fallback configured for `fr-FR` in `translations.fallback`. The translation from the default fallback, `en-US`, is used. |
| `header` [`en-US`] | My header | Content is directly resolvable in `en-US`. No fallback required. |
| `header` [`zh-CN`] | 我的标题 (zh-CN) | Content is directly resolvable in `zh-CN`. No fallback required. |
| `header` [`zh-TW`] | 我的标题 (zh-CN) | `zh-TW` → `zh-CN`. The translation is not resolvable in `zh-TW`. The content from the matching fallback, `zh-CN`, is used. |
| `header` [`ja-JP`] | Meine Kopfzeile (de-DE) | `ja-JP` → `de-DE`. A translation resource for `ja-JP` is not configured in `translations.resource`. The translation from the first fallback, `de-DE`, is used. |
| `header` [`fr-FR`] | My header | `fr-FR` → `en-US` (default). A translation resource for `fr-FR` is not configured in `translations.resource`, and there is no matching fallback configured for `fr-FR` in `translations.fallback`. The translation from the default fallback, `en-US`, is used. |

### Translation files

Translation files referenced in your manifest.yml have a combined size limit of 100 KB. However, translations handled directly in your app's frontend code (using the `useTranslation()` hook or `i18n` from `@forge/bridge`) have no size restrictions since they're bundled with your app code.

The translation files provide key-value pairs to be used by
Forge to execute the translation. Each key represents a unique identifier, such as `header` or `page.title`, while the corresponding value is the translation to be displayed, such as "My header" or "My page title".

```
```
1
2
```



```
// locales/en-US.json
{
  "appName": "My cool app",
  "header": "My header",
  "page": {
    "title": "My page title"
  },
  "custom.content": "used within the app not manifest.yml"
}
```
```

The content of the translation files supports both nested and flattened key formats.

For example, a nested key format looks like:

```
```
1
2
```



```
{
  "page": {
    "title": "My page title"
  }
}
```
```

A flattened key format looks like:

```
```
1
2
```



```
{
  "page.title": "My page title"
}
```
```

The support for both formats ensures portability with [Connect apps](https://developer.atlassian.com/cloud/jira/platform/internationalization-for-connect-apps/#example). When both methods are used to define a key-value pair, the flattened key is prioritized over a nested key lookup.

For example, in the `src/frontend/locales/zh-CN.json` file mentioned earlier, when resolving the translation for the key `page.title`, the content (`我的页面标题 (zh-CN)`) associated with the flattened key `page.title` will be used, instead of the content (`我的页面标题 (not used)`) linked to the corresponding nested key.

We recommend using the nested key format as it typically results in a more compact file size and improved maintainability.
