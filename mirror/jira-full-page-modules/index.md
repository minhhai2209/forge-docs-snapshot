# Jira full-page modules

As an app developer, you can use the following Jira full-page modules to create full-page
experiences in your Forge app:

## Global pages

Use the [Jira global page module](/platform/forge/manifest-reference/modules/jira-global-page/)
for larger apps that span multiple projects and entities. The module provides a full-page experience
for all app users who use the instance.

### Example

Learn how to build a dashboard app using the global page module in this tutorial: [Build a dashboard app with the Jira full page module](/platform/forge/build-a-dashboard-app-with-the-jira-full-page-module/).

### Navigation

You can access the global pages created by the app via **Apps** in the header. If an app has multiple
global pages, clicking the app in the **Apps** menu navigates to the path `/`.

![Apps navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/global-pages-navigation.png?_v=1.5800.1813)

### Apps with a single global page

From the header, select **Apps**, then select the app.

Apps with a single global page don't display a sidebar.

![Apps with a single global page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/global-single-page-app.png?_v=1.5800.1813)

### Apps with multiple global pages

Clicking an app in the **Apps** menu navigates to the path `/`. The sidebar displays the name of the app, as well as the app's global pages.

![Apps with multiple global pages - dividers](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/global-multipage-app-dividers.png?_v=1.5800.1813)

![Apps with multiple global pages - dividers](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/global-multipage-app-sections.png?_v=1.5800.1813)

## Full page (Preview)

Use the [Jira full page module](/platform/forge/manifest-reference/modules/jira-full-page/) to create fully customized app experiences with Custom UI. The full page module provides greater flexibility with custom routing and is ideal for apps that need complete control over the page experience.

### Example

Learn how to build a dashboard app using the full page module: [Build a dashboard app with the Jira full page module](/platform/forge/build-a-dashboard-app-with-the-jira-full-page-module/).

### Navigation

Full page modules can be accessed using this URL format:

```
```
1
2
```



```
https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/<app-route>
```
```

**Where to find each value:**

* **`<your-site>`**: Your site name
* **`<app-id>`**: The UUID from your `app.id` in `manifest.yml` (if in ARI format like `ari:cloud:ecosystem::app/UUID`, use only the UUID section)
* **`<forge-environment-id>`**: The UUID of the environment that the app is installed on.
  Run `forge environments list` to find the UUID of the desired environment.
* **`<route-prefix>`**: Defined in your manifest under `routePrefix`
* **`<app-route>`**: Optional - if your app code contains routing, it will appear under the `<app-route>` section of the URL.

**Example:**

```
```
1
2
```



```
https://example.atlassian.net/forge-apps/a/21e590df-79e6-40dd-9ee4-ba2c7b678f26/e/9f699e8b-33f1-4fa7-bd48-c5fdc44fa4c2/r/ui-kit
```
```

Unlike global pages that appear in the **Apps** menu, full page modules don't have automatic navigation entries. You control how users access them through URLs or links in your app.

### Apps with a single full page

When an app has a single full page module, users navigate directly to the route URL to access the full-page experience. You can add client-side routing within this module to create multiple views within your app. See [Add routing to a full page app](/platform/forge/add-routing-to-a-full-page-app/) for guidance.

### Apps with multiple full pages

Apps can define multiple full page modules by using different `routePrefix` values in the manifest. Each module is accessed via its own URL. To navigate between modules programmatically, use the [router bridge API](/platform/forge/apis-reference/ui-api-bridge/router/):

```
```
1
2
```



```
router.navigate({ target: "module", moduleKey: "my-full-page-module" });
```
```

## Personal settings pages

Use the [Jira personal settings page module](/platform/forge/manifest-reference/modules/jira-personal-settings-page/) to create a page where users can change their personal settings related to your app.

### Navigation

You can access personal settings pages from the profile menu in the main navigation. Apps that create a personal settings page have a menu item in the personal settings menu, in the **Apps** section. The **Apps** section is displayed below the native sections of the personal settings.

![Personal settings pages navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/personal-settings-nav.png?_v=1.5800.1813)

### Apps with a single personal settings page

Clicking the app in the profile menu opens up the personal settings page.

![Single personal settings page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/personal-settings-single-page-app.png?_v=1.5800.1813)

### Apps with multiple personal settings pages

Clicking the app in the personal settings sidebar displays a contextual sidebar, which then displays the app name and its multiple personal settings pages below.

![Multiple personal settings page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/personal-settings-multipage-app.png?_v=1.5800.1813)

## Project pages

Most users do their work in the project context, whether it’s on the board, queue, or issue view. Use the [Jira project page module](/platform/forge/manifest-reference/modules/jira-project-page/) to bring your app closer to where users do their work.
Project pages are most suitable for the full-page apps in a single project.

### Navigation

Within Atlassian apps, project pages can be accessed via the project sidebar in the **Apps** section, which appears below the native sections of the project. In Jira Work Management, however, project pages are accessed from the project view's horizontal navigation, under the **Apps** dropdown.
![Project pages navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-pages-navigation.png?_v=1.5800.1813)

### Apps with a single project page

Clicking the app in the project sidebar opens up the project page.

![Project pages navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-single-page-app.png?_v=1.5800.1813)

### Apps with multiple project pages

Clicking the app in the project sidebar displays a contextual sidebar, which then displays the app name and its multiple project pages below. App users can navigate to these project pages.

![Project pages navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-multipage-app.png?_v=1.5800.1813)

## Project settings pages

Use the [Jira project settings page module](/platform/forge/manifest-reference/modules/jira-project-settings-page/) to build a settings page that only project admins can access.

### Navigation

You can access project settings pages from the project settings sidebar. Apps that create a project settings page have a menu item in the project settings sidebar, in the **Apps** section. The **Apps** section is displayed below the native sections of the project settings.

![Project pages navigation](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-settings-nav.png?_v=1.5800.1813)

### Apps with a single project settings page

Clicking the app in the project settings sidebar opens up the project page.

![Single project settings page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-settings-single-page-app.png?_v=1.5800.1813)

### Apps with multiple project settings pages

Clicking the app in the project sidebar displays a contextual sidebar, which then displays the app name and its multiple project pages below.
Project admins can navigate to these project settings pages.

![Multiple project settings page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/project-settings-multipage-app.png?_v=1.5800.1813)

## Admin pages

The [Jira admin page module](/platform/forge/manifest-reference/modules/jira-admin-page/) works best for the following use cases:

* creating apps with full-page experiences for the admin of an instance
* providing the global settings of an app

### Navigation

You can access the admin page of an app from the **Apps** administration sidebar, below the native sections.

![Apps with single admin page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/nav-admin-pages.png?_v=1.5800.1813)

### Apps with a single admin page

1. From the header, select **Apps**, and then select **Manage apps**.
2. Select the app from the **Apps** section. The app's page is displayed.

![Apps with single admin page](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/admin-single-page.png?_v=1.5800.1813)

### Apps with multiple admin pages

1. From the header, select **Apps**, and then select **Manage apps**.
2. Select the app from the **Apps** section. The app's pages are displayed.

![Apps with multiple admin pages](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/admin-multi-page.png?_v=1.5800.1813)

## Building your page

The building blocks of full-page experiences in Forge apps are:

### Page content

Forge has two options for building the user interface of your apps:
[UI kit](/platform/forge/ui-kit/) and [Custom UI](/platform/forge/custom-ui/).
The user interface essentially becomes the page content of your app.

The UI kit lets you quickly and easily build a user interface for your app. It's made up of
three main concepts: components, hooks, and event handlers.

Custom UI lets you define your own user interface using static resources, such as HTML, CSS, JavaScript,
and images. Forge hosts your static resources, letting your app display custom UI on Atlassian apps.

### Layout

We have three layout types:

1. Native: Suits simple pages that don’t need multiple items in the header. Use the native layout to get the header styled like an Atlassian page.
2. Basic: Suits pages that need several items in the header, like actions, branding, and more. Use the basic layout to get more surface area in the header.
3. Blank: Suits pages which need a completely custom look. There are no margins or breadcrumbs and no header.

Custom UI apps support:

* native
* blank
* basic (deprecated)

UI kit apps support:

### Contextual navigation

A contextual sidebar is available when your app has multiple pages of the same kind.
From the contextual sidebar you can:

* display the app name and icon
* navigate to the subpages and sections

#### App name and app icon

You can use the name and icon of an app as branding for your app. We recommend using a colored icon for your app icon.

![App icon](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/app-icon.png?_v=1.5800.1813)

#### Menu label and icon

Menu labels and their corresponding icons are key for users to find their way when using an app. A menu label and its icon should clearly describe the functionality of a particular page, as well as reflect your branding.

![Single menu item](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/menu-single-item.png?_v=1.5800.1813)

#### Sections

Sections provide the ability to group two or more pages in the contextual sidebar. This helps users find relevant items when navigating the sidebar.
We discourage using sections for a single page.

![Multiple menu items](https://dac-static.atlassian.com/platform/forge/images/page-guidelines/menu-multiple-items.png?_v=1.5800.1813)
