# Jira global permission

The `jira:globalPermission` module allows you to define custom global permissions for Jira.
Global permissions are not related to any particular entity and are useful if you need to manage permissions for operations performed on global objects.

A custom global permission behaves as any other Jira permission. Administrators may manage it in the UI and your add-on can access it through REST APIs.

The format of the permission key is: `ari:cloud:ecosystem::extension/[App ID]/[Environment ID]/static/[Permission key]`.

Note that there is a similar module for [project permissions](/platform/forge/manifest-reference/modules/jira-project-permission/).

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the permission.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | Yes | Description of the global permission. It will be displayed under the permission's name.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `anonymousAllowed` | `boolean` | Yes | Specifies if this permission can be granted to anonymous users. |
| `defaultGrants` | `string` | No | Specifies the group of users that will be granted this permissions when the add-on is first installed. Please note that existing permission configuration won't be overwritten during add-on upgrades or re-installations. Allowed values:   * `all` - if `anonymousAllowed` is set to true, every user,   both logged in and anonymous, will be granted the permission.   Otherwise, the permission will be granted to every user with an application role assigned. * `jira-administrators` - every user with the Jira administration permission will be granted this   permission. * `none` - by default, the permission will not be granted to anyone. |
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
  jira:globalPermission:
    - key: "administer-timesheets"
      name: "Administer Timesheets"
      description: "Users with this permission can administer timesheet data provided by this app"
      anonymousAllowed: false
      defaultGrants:
        - "jira-administrators"
```
```
