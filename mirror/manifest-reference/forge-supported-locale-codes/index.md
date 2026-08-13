# Forge supported locale codes

Locale codes are standardized identifiers used in the `manifest.yml` file to determine the languages supported by your Forge app. We use the [BCP-47](https://en.wikipedia.org/wiki/IETF_language_tag) format, which consists of a two-letter language code and a two-letter region code separated by a dash. For example, the locale code for Portuguese (Brazil) is `pt-BR` and the locale code for Portuguese (Portugal) is `pt-PT`.

Internationalization for Forge apps supports the following languages and locale codes:

| Name | Language | Supported locale code |
| --- | --- | --- |
| Chinese (Simplified, People's Republic of China) | `中文 (简体)` | `zh-CN` |
| Chinese (Traditional, Taiwan) | `中文 (繁體)` | `zh-TW` |
| Czech | `Čeština` | `cs-CZ` |
| Danish | `Dansk` | `da-DK` |
| Dutch | `Nederlands` | `nl-NL` |
| English (United States) | `English (US)` | `en-US` |
| English (United Kingdom) | `English (UK)` | `en-GB` |
| Estonian | `Eesti` | `et-EE` |
| Finnish | `Suomi` | `fi-FI` |
| French | `Français` | `fr-FR` |
| German | `Deutsch` | `de-DE` |
| Hungarian | `Magyar` | `hu-HU` |
| Icelandic | `Íslenska` | `is-IS` |
| Italian | `Italiano` | `it-IT` |
| Japanese | `日本語` | `ja-JP` |
| Korean | `한국어` | `ko-KR` |
| Norwegian (Bokmål) | `Norsk` | `no-NO` |
| Polish | `Polski` | `pl-PL` |
| Portuguese (Brazil) | `Português (Brasil)` | `pt-BR` |
| Portuguese (Portugal)\* | `Português (Portugal)` | `pt-PT` |
| Romanian | `Română` | `ro-RO` |
| Russian | `Русский` | `ru-RU` |
| Slovak | `Slovenčina` | `sk-SK` |
| Turkish | `Türkçe` | `tr-TR` |
| Spanish | `Español` | `es-ES` |
| Swedish | `Svenska` | `sv-SE` |

\*Portuguese (Portugal), `pt-PT`, is not supported by Confluence. If a user’s locale is `pt-PT`, in Confluence it will fallback to Portuguese (Brazil), `pt-BR`, if configured. If `pt-BR` is not configured, the fallback language will be based on the app’s [fallback configurations](/platform/forge/internationalization/#fallback-configurations).

A user’s locale is determined by their browser language or the language preference configured in
their [settings](https://support.atlassian.com/atlassian-account/docs/manage-your-language-preferences/). It can be returned using the functions [view.getContext](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/view/#getcontext) or [useProductContext](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-product-context/).

To understand how locale codes are used in the `manifest.yml` file, see [Translations](/platform/forge/manifest-reference/translations).
