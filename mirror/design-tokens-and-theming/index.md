# Design tokens and theming

This feature involves using Atlassian Design tokens for developing Forge apps for Jira and Confluence.

When developing Forge apps, incorporating Atlassian's design tokens can be highly beneficial. To familiarize yourself with design tokens, refer to the [Atlassian Design System documentation](https://atlassian.design/foundations/design-tokens/). This describes the naming conventions used, as well as the advantages they offer.

In addition to enabling features like dark theme and improved accessibility, design tokens make it easy for you to design and build apps that match the parent Atlassian app, such as Jira or Confluence — and do it once.

Colors in your app will mirror and react to the active theme of the parent Atlassian app to appear closely integrated and provide a consistent, familiar experience for customers. But not only that, as the Atlassian Design System is continually improved upon and colors iterated on, you'll easily benefit from them too.

Design tokens enabled features are automatically enabled in [Forge UI kit](/platform/forge/ui-kit-components/) apps. For [Forge Custom UI](/platform/forge/custom-ui/iframe), you can enable the opt-in theming API by using design tokens by following the steps below.

## Opt-in theming API

The opt-in API allows you to test and iterate on your experience, while only enabling it for customers when the migration is complete, and you’re ready to ship to your customers.

### Activate theming

To activate theming in your Forge Custom UI app, call `view.theme.enable()` function.

This will fetch the current active theme from the host environment (example, Jira)
and apply it in your app. It will also reactively apply theme changes that occur in the host environment so that your app and the host are always in sync.

```
```
1
2
```



```
import { view } from "@forge/bridge";

await view.theme.enable();
```
```

## Using design tokens

Verify that design tokens are enabled by inspecting the HTML of your application while shown in the parent Atlassian app.

```
```
1
2
```



```
<html data-theme="dark:dark light:light" data-color-mode="dark">
  <head>
    <style data-theme="dark">
      /* Dark theme CSS */
    </style>
  </head>
  <body>
    <!-- Your app here -->
  </body>
</html>
```
```

Pay special attention to the `data-color-mode="dark"` attribute, and also note the `data-theme="dark:dark light:light"` attribute. These reflect the current theme state of the parent Atlassian app (Jira or Confluence). They also match CSS selectors within the theme files so the appropriate CSS variables can be activated in response to theme changes.

* `data-color-mode="dark"` represents the color “mode” of the theme, with possible values today being `light`, `dark` or `auto`. This attribute tells your application what “type” of theme is active on the page, so that images and theme overrides may be applied consistently.
* `data-theme="dark:dark light:light"` represents the active theme(s), but this is *internal behavior* and *should not be read or modified in any way*, since the names and shape of this attribute may change at any time as we add more themes.
* For example, if an additional theme `high-contrast-light` is introduced, the color mode will still be `light`, telling your application that it should respect a “light” color scheme and render light image variants accordingly. Hence please only rely on `data-color-mode` as above.

## Update colors, spacing and typography to design tokens

All that is left is to use tokens in place of colors, spacing and typography throughout your application.

To view, search and filter through the available design tokens, visit the [“All design tokens” section](https://atlassian.design/components/tokens/all-tokens) on [atlassian.design](https://atlassian.design/). This page includes a “Token picker” tool which, through a series of questions, will help you find the right token for your use case.

For examples of how design tokens can be used in components, and common pairings of background and text colors, view the [design token examples](https://atlassian.design/components/tokens/examples).

Design tokens are CSS custom properties so for **vanilla CSS, Sass and Less**, we recommend accessing design tokens in the following way:

```
```
1
2
```



```
.example {
  background: var(--ds-surface-raised);
  padding: var(--ds-space-100);
  font: var(--ds-font-heading-large);
}
```
```

For **CSS-in-JS**, we strongly recommend you install `@atlaskit/tokens` as a dependency and use the `tokens()` function, which provides additional type safety.

```
```
1
2
```



```
import { token } from "@atlaskit/tokens";

const example = {
  color: token("color.background.selected.bold"),
  margin: token("space.150"),
  font: token("font.body"),
};
```
```

Make sure to keep the `@atlaskit/tokens` package up to date to ensure the tokens suggested are accurate and match the version of tokens injected into your application from the parent Atlassian app.

For more details, read the [tokens migration guide on atlassian.design](https://atlassian.design/components/tokens/migration-guide#changes-for-engineers).

## Custom color schemes

If your application uses colors that correspond to your unique brand, it is still possible to theme your app by querying the `html[data-color-mode]` attribute and styling your applications with your own tokens.

```
```
1
2
```



```
html[data-color-mode="light"] {
  --my-custom-background-token: white;
  --my-custom-text-token: black;
}

html[data-color-mode="dark"] {
  --my-custom-background-token: black;
  --my-custom-text-token: white;
}
```
```

If you have an existing dark mode implementation this attribute can be used to turn it on or off to match the parent application.

This may cause color discrepancies between your app and the parent Atlassian app, so it's recommended to use it sparingly.

## Surface background colors

In some scenarios you may find that the background color of the element your application is rendered on does not match or differs between different locations and themes. For example, if your app is rendered inside of a modal or elevated card and dark mode is enabled.

To work around this, we make a special css variable available to your application with the appropriate background color reflecting the current surface your app is rendered on. This variable is updated whenever the surface changes, so you can use it to style your app accordingly.

```
```
1
2
```



```
import { token } from "@atlaskit/tokens";

const AppStyles = {
  backgroundColor: token("utility.elevation.surface.current"),
};
```
```

## Staying up to date

Our design tokens are designed to evolve over time, moving through a lifecycle of `active`, `deprecated`, and `deleted`, eventually being fully removed from the theme (no longer functional). Tokens will be marked as `deprecated` in a minor version, soft-deleted (functional but will raise errors) in the following minor, and deleted in the next `major` release of the tokens library. All breaking changes to APIs and design tokens will be communicated well in advance, with clear cut-off dates for deprecations.

To simplify the migration and to simplify continuous adoption, we recommend you install and configure the following linters:

These linters will `warn` and `error` for `deprecated` and `deleted` tokens respectively. They also have built-in auto-fixers that allow you to update your entire app to the latest tokens automatically via `eslint --fix` and `stylelint "**/*.css" --fix`.

For the full design tokens reference, please refer to the [Design Tokens documentation on atlassian.design](https://atlassian.design/components/tokens).
