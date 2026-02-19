# Forge changelog

We've introduced the `useTheme` hook for Forge UI Kit apps. This hook retrieves the current theme from the Atlassian app (Jira, Confluence, etc.) and reactively updates your Forge app when the theme changes.

The `useTheme` hook is now the preferred method for accessing theme information in UI Kit apps, replacing the previous approach of accessing `theme.colorMode` via `useProductContext`. Unlike `useProductContext`, the `useTheme` hook is reactive and automatically updates when the theme changes in the Atlassian app.

To use this hook, import `useTheme` from `@forge/react` and call it in your component. The hook returns a theme object containing the current theme configuration.

For implementation details and examples, see the [`useTheme` hook documentation](https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-theme/ "https://developer.atlassian.com/platform/forge/ui-kit/hooks/use-theme/").
