```
# Macro

{{% warning %}}
With the [release of](/platform/forge/changelog/#CHANGE-2381) `@forge/react` version 11.0.0, enhancements have been made
to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook to improve performance in [macro config](/platform/forge/manifest-reference/modules/macro/) apps when receiving configuration value changes.

Confluence macro config apps relying on the **[useProductContext](/platform/forge/ui-kit/hooks/use-product-context/)**
hook or **[view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext)** need to
transition to the [useConfig](/platform/forge/ui-kit/hooks/use-config/) hook before upgrading to
`@forge/react` version 11.0.0 or higher in order to properly access the latest values after the configuration updates.

Confluence macro config apps using the **[useConfig](/platform/forge/ui-kit/hooks/use-config/)** hook
should upgrade to `@forge/react` version 11.0.0 for improved performance.
{{% /warning %}}

The `macro` module inserts dynamic content into the user interface via an editor. Editor macros are
only compatible with the Atlassian editor. All cloud sites use the Atlassian editor by default.

The `macro` module works in Confluence, where the macro is inserted by typing `/` and selecting
from the quick insert menu of the editor. The `macro` module is implemented by a Forge function.

{{% warning %}}
On apps that use Custom UI, module content is displayed inside a [special Forge iframe](/platform/forge/custom-ui/iframe/) which has the [sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#sandbox) attribute configured. This means that HTML links (for example, `<a href="https://domain.tld/path">...</a>`) in this iframe won't be clickable. To make them clickable, use the [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate) API from the `@forge/bridge` package.
{{% /warning %}}

![Example of a macro](/platform/forge/snippets/images/macro-example.png)

## Manifest structure

```yml
modules {}
└─ macro []
   ├─ key (string) [Mandatory]
   ├─ resource (string) [Mandatory]
   ├─ render (string) [Optional]
   ├─ resolver {} [Optional]
   ├─ viewportSize (string) [Optional]
   ├─ title (string | i18n) [Mandatory]
   ├─ icon (string) [Optional]
   ├─ categories (string[]) [Optional]
   ├─ unlicesedAccess (List<string>) [Optional]
   ├─ description (string | i18n) [Optional]
   ├─ hidden (boolean) [Optional]
   └─ config (boolean | {} | config object) [Optional]
     ├─ icon (string) [Optional]
     ├─ title (string | i18n) [Optional]
     ├─ resource (string) [Mandatory]
     ├─ render (string) [Optional]
     ├─ viewportSize (string) [Optional]
     └─ openOnInsert (boolean) [Optional]
   ├─ adfExport {} [Optional]
   ├─ layout (string) [Optional]
   └─ autoConvert [] [Optional]
     └─ matchers [] [Mandatory]
        └─ pattern (string) [Mandatory]

resources []
├─ key (string) [Mandatory]
└─ path (string) [Mandatory]
```

## Properties

<table>
<thead>
<tr>
<th>Property</th>
<th>Type</th>
<th>Required</th>
<th>Description</th>
</tr>
</thead>
<tbody>

<tr>
<td><code>key</code></td>
<td><p><code>string</code></p></td>
<td>Yes</td>
<td>
<p>A key for the module, which other modules can refer to. Must be unique within the manifest.</p>
<p><i>Regex:</i> <code>^[a-zA-Z0-9_-]+$</code></p>
</td>
</tr>
<tr>
<td><code>resource</code></td>
<td><code>string</code></td>
<td>If using <a href="/platform/forge/custom-ui/">Custom UI</a> or modern versions of <a href="/platform/forge/ui-kit/">UI Kit</a></td>
<td>The key of a static <code>resources</code> entry that your module will display. See <a href="/platform/forge/manifest-reference/resources">resources</a> for more details.</td>
</tr>
<tr>
<td><code>render</code></td>
<td><code>'native'</code></td>
<td>If using modern versions of <a href="/platform/forge/ui-kit/components/">UI Kit</a></td>
<td>Indicates the module uses <a href="/platform/forge/ui-kit/components/">UI Kit</a>.</td>
</tr>
<tr>
<td><code>resolver</code></td>
<td><code>{ function: string }</code> or<br><code>{ endpoint: string }</code></td>
<td></td>
<td>
<p>Set the <code>function</code> property if you are using a hosted <code>function</code> module for your resolver.</p>
<p>Set the <code>endpoint</code> property if you are using <a href="/platform/forge/forge-remote-overview">Forge Remote</a> to integrate with a remote back end.</p>
</td>
</tr>

<tr>

<td><code>viewportSize</code></td>
<td><code>'small'</code>, <code>'medium'</code>, <code>'large'</code>, <code>'xlarge'</code> or <code>'max'</code></td>
<td></td>
<td>The <a href="/platform/forge/manifest-reference/resources">display size</a> of <code>resource</code>. Can only be set if the module is using the <code>resource</code> property. Remove this property to enable automatic resizing of the module.</td>

</tr>
<tr>
<td><code>title</code></td>
<td>

<code>string</code> or <code>i18n object</code>

</td>
<td>Yes</td>
<td>
<p>The title of the macro. In Confluence, this is displayed in the editor.</p>
<p>

The <code>i18n object</code> allows for translation. See <a href="#i18n-object">i18n object</a>.

</p>
</td>
</tr>
<tr>
<td><code>icon</code></td>
<td><code>string</code></td>
<td></td>
<td>

<p>The icon displayed next to the <code>title</code>.</p>

<br>
<p>For Custom UI and UI Kit apps, the <code>icon</code> property accepts a relative path from a
declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See
<a href="/platform/forge/custom-ui/#icons">Icons</a> for more information.</p>

<p>If no icon is provided, or if there's an issue preventing the icon from loading, a
generic app icon will be displayed.</p>

</td>
</tr>
<tr>
<td><code>categories</code></td>
<td><code>string[]</code></td>
<td></td>
<td>The categories of the macro. In Confluence, this is used for categorisation in the macro browser.
<br />
<ul>
<li><code>formatting</code></li>
<li><code>confluence-content</code></li>
<li><code>media</code></li>
<li><code>visuals</code></li>
<li><code>navigation</code></li>
<li><code>external-content</code></li>
<li><code>communication</code></li>
<li><code>reporting</code></li>
<li><code>admin</code></li>
<li><code>development</code></li>
</ul>
</td>
</tr>
<tr>
<td><code>description</code></td>
<td>

<code>string</code> or <code>i18n object</code>

</td>
<td></td>
<td>
<p>The description of the macro. In Confluence, this is displayed in the editor.</p>
<p>

The <code>i18n object</code> allows for translation. See <a href="#i18n-object">i18n object</a>.

</p>
</td>
</tr>
<tr>
<td><code>hidden</code></td>
<td><code>boolean</code></td>
<td></td>
<td>
<p>Defaults to <code>false</code>. When set to <code>true</code>, hides the macro from the quick insert menu and macro browser in Confluence. This prevents users from inserting new instances of the macro through these interfaces.</p>
<p>Existing macros on pages continue to render normally, even when this property is set to <code>true</code>.</p>
</td>
</tr>
<tr>
<td><code>config</code></td>
<td><code>boolean</code>, <code>{ function: string }</code>, <code>{ openOnInsert: boolean }</code> or <code>config object</code></td>
<td></td>
<td>
<p>Set <code>config</code> to <code>true</code> if you are using <a href="/platform/forge/add-configuration-to-a-macro/">classic macro configuration</a> without needing <code>openOnInsert</code>.</p>
<p>Set <code>config</code> with the <code>openOnInsert</code> property if you are using <a href="/platform/forge/add-configuration-to-a-macro/">classic macro configuration</a> and need the <code>openOnInsert</code> feature. <code>openOnInsert</code> defaults to false.</p>
<p>Set <code>config</code> to the <a href="/platform/forge/manifest-reference/modules/macro/#config-object">config object</a> if you are using a <a href="/platform/forge/add-custom-configuration-to-a-macro/">custom macro configuration</a>.<p>
</td>
<tr>
<td><code>config.icon</code></td>
<td><code>string</code></td>
<td></td>
<td>
The icon displayed next to the title in the custom config modal.

<br>
<p>For Custom UI and UI Kit apps, the <code>icon</code> property accepts a relative path from a
declared resource. Alternatively, you can also use an absolute URL to a self-hosted icon. See
<a href="/platform/forge/custom-ui/#icons">Icons</a> for more information.</p>

<p>If no icon is provided, or if there's an issue preventing the icon from loading, a
generic app icon will be displayed.</p>

</td>
</tr>
<tr>
<td><code>config.title</code></td>
<td>

<code>string</code> or <code>i18n object</code>

</td>
<td></td>
<td>A title for the config. If the viewport size is <code>fullscreen</code>*, then the title rendered in the modal header will be this title.</td>
</tr>
<tr>
<td><code>config.resource</code></td>
<td><code>string</code></td>
<td>Required if using <a href="/platform/forge/custom-ui/">Custom UI</a> or the latest version of <a href="/platform/forge/ui-kit/">UI Kit.</a></td>
<td>A reference to the static <code>resources</code> entry that your context menu app wants to display. See <a href="/platform/forge/manifest-reference/resources">resources</a> for more details.</td>
</tr>
<tr>
<td><code>config.render</code></td>
<td><code>'native'</code></td>
<td>Yes for <a href="/platform/forge/ui-kit/components/">UI Kit</a></td>
<td>Indicates the module uses <a href="/platform/forge/ui-kit/components/">UI Kit</a>.</td>
</tr>
<tr>
<td><code>config.viewportSize</code></td>
<td><code>'small'</code>, <code>'medium'</code>, <code>'large'</code>, <code>'xlarge'</code>, <code>'max'</code> or <code>'fullscreen'</code>*</td>
<td></td>
<td>The <a href="/platform/forge/manifest-reference/resources">display size</a> of <code>resource</code>. Can only be set if the module is using the <code>resource</code> property. Remove this property to enable automatic resizing of the module.</td>
</tr>
<tr>
<td><code>config.openOnInsert</code></td>
<td><code>boolean</code></td>
<td></td>
<td>Defaults to <code>false</code> for classic configuration, defaults to <code>true</code> for custom configuration. An optional configuration to control if the classic configuration sidepanel or the custom configuration modal is automatically opened when first inserted.</td>
</tr>
<tr>
<td><code>adfExport</code></td>
<td><code>{ function: string }</code></td>
<td></td>
<td><b>For UI Kit and Custom UI use only</b>. Contains a <code>function</code> property, which references the <code>function</code> module that defines the export view of the macro, specified in <a href="/cloud/jira/platform/apis/document/structure/">Atlassian document format</a>.
The specified function can consume the <code>exportType</code> directly from the function's payload in order to specify different views per export type. The <code>exportType</code> can be one of <code>pdf</code>, <code>word</code>, or <code>other</code>. See this <a href="/platform/forge/change-the-confluence-frontend-with-the-ui-kit/#specify-the-export-view">tutorial</a> for more information.
</tr>
<tr>
<td><code>layout</code></td>
<td><code>'block'</code>, <code>'inline'</code> or <code>'bodied'</code></td>
<td></td>
<td>
<p><code>'block'</code> type is used by default.</p>
<p>
<code>'inline'</code> shows the element inline with existing text.
<ul>
<li>For UI Kit apps, inline macros dynamically resize to wrap the content.</li>
<li>A limitation exists for Custom UI apps that prevents inline macros from dynamically resizing when the content of the macro is changed.</li>
</ul>
</p>
<p>
<code>'bodied'</code> sets the macro to have a rich text body.
<ul>
<li>This allows users to insert and edit rich content (such as images and tables) within the macro using the Confluence editor, and allows your app to insert a body using a custom editor.</li>
<li>Please see the link to the tutorial <a href="/platform/forge/using-rich-text-bodied-macros">here</a>.</li>
</ul>
</p>
</td>
</tr>
<tr>
<td><code>autoConvert</code></td>
<td><code>autoConvert object</code></td>
<td></td>
<td>
Inserts a macro into the editor when a recognised URL is pasted in by the user.
See <a href="#macro-autoconvert">Macro autoconvert.</a>
</td>
</tr>
<tr>
<td><code>autoConvert.matchers</code></td>
<td><code>[matcher, ...]</code></td>
<td>Yes, if using <code>autoConvert</code></td>
<td>The list of patterns that define what URLs should be matched.</td>
</tr>
<tr>
<td><code>autoConvert.matchers.pattern</code></td>
<td><code>string</code></td>
<td>Yes, if using <code>autoConvert</code></td>
<td>
A string that defines a specific URL pattern to be matched, using wildcards for variable
parts of the URL, such as unique IDs.
<ul>
<li>Use multiple wildcards to match multiple sub-paths. Do not include all sub-paths with a single wildcard.</li>
<li>Ensure URLs do not contain whitespace unless it is URL encoded.</li>
<li>Wildcards cannot be used in place of a protocol. Custom URL Schemes are supported See <a href="#matching-custom-url-schemes">examples</a></li>
<li>Maximum length of the pattern is 1024 characters.</li>
</ul>
</td>
</tr>
<tr>
<td><code>emitsReadyEvent</code></td>
<td>boolean</td>
<td>No</td>
<td>Defaults to <code>false</code>. An optional configuration to notify Confluence that the macro will send a <code>emitReadyEvent</code> when it has completed loading and is ready for export or further processing. This should be used with <code>view.emitReadyEvent()</code>. See the <a href="/platform/forge/apis-reference/ui-api-bridge/view/#emitreadyevent">view bridge function</a> for more information.</td>
</tr>

<tr>
<td><code>unlicensedAccess</code></td>
<td>List&lt;string&gt;</td>
<td></td>
<td>
A list of unlicensed user types that can access this module. Valid values are: <code>unlicensed</code> (Guests Users), and <code>anonymous</code>. For more information, see
<a href="/platform/forge/access-to-forge-apps-for-unlicensed-users/#confluence-forge-modules">Access to Forge apps for unlicensed Confluence users</a>.
</td>
</tr>

  </tbody>
</table>

\* 

{{% warning %}}
`fullscreen` viewport sizing is now available as part of our Early Access Program (EAP). This allows your macro configuration modal to fill the entire viewport. You can also provide a `title` and an `icon` to display in the header. To start testing, [sign up here](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18983).

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge Full Page Modals is governed by the [Atlassian Developer Terms](https://developer.atlassian.com/platform/marketplace/atlassian-developer-terms/). The Forge Full Page Modals are considered “Early Access Materials”, as set forth in Section 10 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).
{{% /warning %}}

 

### i18n object

<table>
<thead>
<tr>
<th>Key</th>
<th>Type</th>
<th>Required</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>i18n</code></td>
<td><code>string</code></td>
<td>Yes</td>
<td>A key referencing a translated string in the translation files. For more details, see <a href="/platform/forge/manifest-reference/translations">Translations</a>.</td>
</tr>
</tbody>
</table>

## Extension context

### UI Kit and Custom UI

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>type</code></td>
      <td><code>string</code></td>
      <td>The type of the module (<code>macro</code>).</td>
    </tr>
    <tr>
       <td><code>content.id</code></td>
      <td><code>string</code></td>
      <td>A string that represents the unique identifier of the <code>content</code> object.</td>
    </tr>
    <tr>
    <tr>
      <td><code>content.type</code></td>
      <td><code>"page"</code>, <code>"blogpost"</code> or <code>"space"</code></td>
      <td>A string that represents the type of the <code>content</code> object.</td>
    </tr>
    <tr>
    <tr>
      <td><code>content.subtype</code></td>
      <td><code>string</code> or <code>null</code></td>
      <td>A string that represents the subtype of the <code>content</code> object. <code>null</code> is returned if <code>subtype</code> does not apply.</td>
    </tr>
    <tr>
      <td><code>space.id</code></td>
      <td><code>string</code></td>
      <td>A string that represents the unique identifier of the <code>space</code> object.</td>
    </tr>
        <tr>
      <td><code>space.key</code></td>
      <td><code>string</code></td>
      <td>A string that represents the unique key of the <code>space</code> object.</td>
    </tr>
    <tr>
      <td><code>isEditing</code></td>
      <td><code>boolean</code></td>
      <td>Indicates whether the macro is opened in the editor or not.</td>
    </tr>
    <tr>
      <td><code>references</code></td>
      <td><a href="https://bitbucket.org/atlassian/atlassian-frontend-mirror/src/71638af3b28e29e6f3f72c3e36cf5524149402ff/editor/editor-common/src/extensions/types/extension-handler.ts#lines-75">ReferenceEntity[]</a></td>
      <td>An array of reference entities (if any). Reference entities are a list of any other ADF nodes on the page that are referenced by this macro.</td>
    </tr>
    <tr>
      <td><code>config</code></td>
      <td><code>object</code></td>
      <td>The configuration parameters saved in this macro.</td>
    </tr>
    <tr>
      <td><code>macro.body</code></td>
      <td><a href="/cloud/jira/platform/apis/document/structure/">ADF document</a></td>
      <td>The rich text body of the macro. Available for <code>layout: bodied</code> macros only.</td>
    </tr>
    <tr>
      <td><code>autoConvertLink</code></td>
      <td><code>string</code></td>
      <td>The link pasted by a user that has matched an AutoConvert app.</td>
    </tr>
    <tr>
      <td><code>template.id</code></td>
      <td><code>string</code></td>
      <td>A string that represents the unique identifier of the template. This value is only available when the macro is in a saved template.</td>
    </tr>
  </tbody>
</table>

## Macro autoconvert

Macro autoconvert allows your app to automatically insert a macro into the editor when a user pastes
a recognized URL. This is achieved by defining URL patterns in the manifest using the `matchers`
property. These `matchers`are registered in the editor when the app is installed.

### Example

```yml
modules:
  macro:
    - key: autoconvert-app
      resource: main
      render: native
      resolver:
        function: resolver
      title: Forge app for autoconvert
      description: Example for autoconvert manifest
      autoConvert:
        matchers:
          - pattern: https://www.example.com/*/about
          - pattern: https://www.example.com/*/music
          - pattern: https://*.example.com/*/movies/*
          - pattern: https://example.com/gifs/*/
          - pattern: http://*.example.com/media/*/.gif
          - pattern: customScheme:\\example:custom
          - pattern: customScheme:example:*
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: "<your app id>"
```

The URL patterns use wildcards to match parts of the URL that can vary, such as unique IDs. Wildcards are
defined using `*`.

Use a new `*` for each segment in the URL you want a wildcard for. For example, `https://www.example.com/*` will match `https://www.example.com/about` but will not match `https://www.example.com/about/contact`. To match this path as well you need to include `https://www.example.com/*/*` as one of your `matchers`.

You'll need to define a separate `matcher` for each relevant internet protocol, such as `http` and `https`.

Creating custom URL schemes is also supported. For example, `customScheme:*` can be used to match any URL that starts with that custom scheme such as`customScheme:\\example:custom`. Any custom schemes will have to be registered on the system they will be used on, such as iOS, Windows or Android. Either `:\\` or just `:` can be used as the initial separator in the URL scheme then `:` thereon.

### Example patterns

###### Wildcard path

```yml
- "pattern": "https://www.example.com/*/about"
```

###### Wildcard in subdomain

```yml
- "pattern": "https://www.*.example.com/help"
```

###### Matching wildcard paths

```yml
- "pattern": "https://bitbucket.org/*/*/*"
```

###### Matching custom URL schemes

```yml
- "pattern": "customScheme:example:custom"
- "pattern": "customScheme:\\example:custom"
```

###### Matching custom URL scheme wildcard

```yml
- "pattern": "customScheme:example:*"
- "pattern": "customScheme:\\example:*"
```

When a pasted URL matches a defined pattern, the macro is created in the editor, and the URL is
captured and inserted as a parameter into the macro body. This parameter can be accessed using the
`autoConvertLink` property.

{{% card %}}
  title: Example app: Macro autoconvert for UI Kit
  description: Learn how to configure auto convert in your manifest.yml file, including pattern matching and setting permissions for API calls.
  link: https://bitbucket.org/atlassian/macro-auto-convert-app-for-ui-kit/src/master/
  {{% /card %}}

## Macro custom configuration

### Extension context in the macro editor

There are two additional extension context parameters available when you are in macro configuration editor context.

<table>
  <thead>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Details</th>
  </tr>
  </thead>
  <tbody>
      <tr>
        <td><code>macro.isConfiguring</code></td>
        <td><code>boolean</code></td>
        <td><code>true</code> if the currently rendered resource is the <code>config</code> resource, <code>false</code> if it is the macro's default resource</td>
      </tr>
      <tr>
        <td><code>macro.isInserting</code></td>
        <td><code>boolean</code></td>
        <td><code>true</code> if a new macro is being inserted, <code>false</code> if an existing macro is being edited</td>
      </tr>
  </tbody>
</table>

### Options for submitting the configuration

This table details the options supported by [view.submit()](/platform/forge/apis-reference/ui-api-bridge/view/#submit)
in the context of custom macro configuration.

<table>
  <thead>
  <tr>
    <th>Parameter</th>
    <th>Type</th>
    <th>Required</th>
    <th>Details</th>
    <th>Code</th>
  </tr>
  </thead>
  <tbody>
      <tr>
        <td><code>config</code></td>
        <td><a href="#supported-config-payload-format">Config payload</a></td>
        <td>Yes</td>
        <td>Sets the config properties of the macro.</td>
        <td>
<pre>
view.submit({
  config: {
    param1: "test",
    param2: [1, 2, 3]
  }
})
</pre>
        </td>
      </tr>
      <tr>
        <td><code>body</code></td>
        <td><a href="/cloud/jira/platform/apis/document/structure/">ADF document</a></td>
        <td>No</td>
        <td>Sets the rich text body of the macro. Can only be used with <code>layout: bodied</code> macros.</td>
        <td>
<pre>
view.submit({
  config: {},
  body: {
    type: "doc",
    version: 1,
    content: [
      // ADF content
    ]
  }
})
</pre>
        </td>
      </tr>
      <tr>
        <td><code>keepEditing</code></td>
        <td><code>boolean</code></td>
        <td>No</td>
        <td>Defaults to <code>false</code>, which automatically closes the config modal on submit. Set this to <code>true</code> to keep the modal open.</td>
        <td>
<pre>
view.submit({
  config: {},
  keepEditing: true
})
</pre>
        </td>
      </tr>
  </tbody>
</table>

### Supported config payload format

The `config` payload only supports values that can be serialised to JSON.

The following types are allowed on the payload:

1. `undefined`
1. `string`
1. `number`
1. `boolean`
1. `object` (can contain any of the allowed types, including nested objects)
1. `array` (can contain strings, numbers, booleans, and objects; all items in the array must be of the same type).

The following types are not allowed:

- Nested arrays (arrays as direct children of arrays)
- `null`
- Any data types that are not serializable to JSON (e.g. `Map`, `Set`, etc.)

If you want greater control over the storage format of your configuration, such as being able to store nested arrays and nulls, we recommend serializing your configuration to JSON upfront, and storing it as a string.

### Error code guide

This table details the possible error codes that may be thrown by `view.submit()`:

<table>
  <thead>
  <tr>
    <th>Error code</th>
    <th>Details</th>
  </tr>
  </thead>
  <tbody>
      <tr>
        <td><code>INVALID_PAYLOAD</code></td>
        <td>The top-level parameter passed to <code>view.submit()</code> must be an object.</td>
      </tr>
      <tr>
        <td><code>INVALID_CONFIG</code></td>
        <td>The <code>config</code> prop provided must be an object that is compliant with the <a href="#supported-config-payload-format">config payload format</a> above.</td>
      </tr>
      <tr>
        <td><code>INVALID_EXTENSION_TYPE</code></td>
        <td>When providing a <code>body</code>, the macro must be a rich text macro (<code>layout: "bodied"</code>).</td>
      </tr>
      <tr>
        <td><code>INVALID_BODY</code></td>
        <td>The provided <code>body</code> is not a valid <a href="/cloud/jira/platform/apis/document/nodes/doc/">ADF document node</a>.</td>
      </tr>
       <tr>
        <td><code>MACRO_NOT_FOUND</code></td>
        <td>The macro that you are attempting to update no longer exists. It may have been deleted by another user editing the page.</td>
      </tr>
  </tbody>
</table>

## Tutorials

{{% layout %}}{{% content %}}
{{% /content %}},{{% content %}}{{% card %}}
  title: Add configuration to a macro with UI Kit
  description: The app allows you to customize what the macro displays by adjusting settings in a form.
  link: /platform/forge/add-configuration-to-a-macro-with-ui-kit/
  {{% /card %}}{{% /content %}},{{% content %}}
{{% /content %}}{{% /layout %}}

{{% layout %}}{{% content %}}
{{% /content %}},{{% content %}}{{% card %}}
  title: Add custom configuration to a macro
  description: The app’s configuration can be edited using a custom configuration modal.
  link: /platform/forge/add-custom-configuration-to-a-macro/
  {{% /card %}}{{% /content %}},{{% content %}}
{{% /content %}}{{% /layout %}}

{{% layout %}}{{% content %}}
{{% /content %}},{{% content %}}{{% card %}}
  title: Using rich-text bodied macros
  description: How to configure the manifest and render rich text body content.
  link: /platform/forge/using-rich-text-bodied-macros/
  {{% /card %}}{{% /content %}},{{% content %}}
{{% /content %}}{{% /layout %}}
```
