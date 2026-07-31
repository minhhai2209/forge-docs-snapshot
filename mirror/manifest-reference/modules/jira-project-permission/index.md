# Jira project permission

The `jira:projectPermission` module allows you to define custom project permissions for Jira.
Project permissions are scoped to projects and are useful if you need to manage permissions for operations performed on objects related to projects, like issues, comments, worklogs or your add-on's project-scoped entities.

A custom project permission behaves as any other Jira permission. Administrators may manage it in the UI, and your add-on can access it through REST APIs.

The format of the permission key is: `ari:cloud:ecosystem::extension/[App ID]/[Environment ID]/static/[Permission key]`.

Note that there is a similar module for [global permissions](/platform/forge/manifest-reference/modules/jira-global-permission/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the permission.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | Description of the project permission. It will be displayed under the permission's name.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `category` | `string` | No | The category of the project permission. This determines in which section the permission will be displayed. Allowed values:   * `attachments` * `comments` * `issues` * `other` * `projects` * `time_tracking` * `voters_and_watchers`   *Default:* `other` |
| `migratedFromConnect` | `boolean` | No | This optional field relates to migrating from a Connect app. See [here](https://developer.atlassian.com/platform/adopting-forge-from-connect/migrate-jira-global-project-permissions/) for more information.  *Default:* `false` |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Example

```
```
1
2
```



```
modules:
  jira:projectPermission:
    - key: "forge-project-permission"
      name: "Forge project permission"
      description: "Forge custom project permission"
      category: attachments
```
```
