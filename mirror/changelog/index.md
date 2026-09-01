# Forge changelog

## Which apps are affected?

All apps using Macros. Learn more about app macros at the following links.

## What’s changing?

### In 6 months on Feb 25, 2027, app macros will only appear in one category in the **modal element browser, and the** `categories ([string])` property will be fully replaced by a new `category (string)` property for Forge app macros

Today, app macros can set an optional `categories ([string])` property that defines which categories (potentially multiple) the app macro should appear in within the **modal element browser** (not the **slash menu element browser**).

In 6 months on Feb 25, 2027, all app macros will only be able to appear in one category in the **modal element browser** instead of multiple categories like they can today, to improve end users' browsing experience.

#### **For Forge app macros**

Since we are moving toward one category per app macro to improve the browsing experience, we have introduced a new `category (string)` property, where developers can define one valid category string to determine where their app macro shows up in both the **modal element browser** and **slash menu element browser**. Valid category inputs for this field will be:

* `structure` *(Native examples: Action item, Table, Status)*
* `media` *(Native examples: Image, video, or file, Link, Emoji)*
* `embed` *(Native examples: like Google Drive, Figma, Dropbox)*
* `text-formatting` *(Native examples: Bullet list, Heading 1, Quote)*
* `data-and-charts` *(Native examples: Database, Jira work items, Child items)*

*To learn more about these new categories, read the second part of this announcement.*

On Feb 25, 2027, the `categories ([string])` property will no longer be recognized by Forge app macros. It will effectively be fully replaced by this new `category (string)` field, making it so Forge app macros only appear in one category. Make sure to update the `category (string)` property by then to explicitly set which category you’d like your app macro to live in. Otherwise, if there is no valid entry in the `category (string)` property by then, your app macro will appear in an “Other elements” category as well as the default “All” category.

#### **For Connect app macros**

On Feb 25, 2027, Connect app macros will only appear in the **first** category listed in their `categories ([string])` property with the below mapping. Connect app macros will not gain access to the new `category (string)` property.

* `formatting`, `confluence content`, `navigation`, `admin` → `structure`
* `reporting`, `development` → `data-and-charts`
* `media`, `visuals`, `communication` → `media`
* `external-content` → `embed`
* **No valid categories provided** → Other elements (as well as the default "All" category)

### Modernizing categories in the **slash menu element browser** and **modal element browser**

Before the above deprecation on Feb 25, 2027, we will also be updating the categories & appearance of the **slash menu element browser** and **modal element browser** to improve discoverability of our shared offerings, expected to begin rollout on Oct 6, 2026. We will be:

* Updating the set of categories we have to better capture our shared offerings.
* Updating the slash menu element browser to actually show the categories.
* Updating the modal element browser to show the new categories.
* Cosmetically modernizing the slash menu and modal element browser.

*Example of new categories in slash menu element browser*

*Example of new categories in modal element browser*

Before this release, the valid set of categories app macros could use were:

* Formatting - `formatting`
* Confluence content - `confluence-content`
* Navigation - `navigation`
* Admin - `admin`
* Reporting - `reporting`
* Development - `development`
* External content - `external-content`
* Media - `media`
* Visuals and images - `visuals`
* Communication - `communication`

After this release, the new valid set of categories app macros can use will be the following. Any of the above categories not listed below will be considered legacy categories.

* Structure - `structure` *(Native examples: Action item, Table, Status)*
* Media - `media` *(Native examples: Image, video, or file, Link, Emoji)*
* Embed - `embed` *(Native examples: like Google Drive, Figma, Dropbox)*
* Text formatting - `text-formatting` *(Native examples: Bullet list, Heading 1, Quote)*
* Data and charts - `data-and-charts` *(Native examples: Database, Jira work items, Child items)*

Any app macros with legacy categories still listed in their `categories` property on Oct 6, 2026 will have their categories automatically mapped to new categories in product with the below mapping.

* `formatting`, `confluence content`, `navigation`, `admin` → `structure`
* `reporting`, `development` → `data-and-charts`
* `media`, `visuals`, `communication` → `media`
* `external-content` → `embed`
* **No valid categories provided** → Other elements (as well as the default "All" category)

If, however, you would like your app macro to appear in different categories than it would automatically be mapped to, update the new aforementioned `category (string)` property with any one of the new categories (available only for Forge app macros) by Oct 6, 2026.

As mentioned in the first part of this announcement, app macros will continue to be able to appear in multiple categories in the **modal element browser** for 6 months until Feb 25, 2027,when app macros will begin to appear in only one category.

**In the slash menu element browser, however, with very limited screen real estate, app macros will only appear in one category upon release on** Oct 6, 2026**.** Furthermore, we plan to show up to 30 items per category in the slash menu element browser. If there are more items, we’ll show a “View more” CTA that leads to the modal element browser where all items appear. However, to ensure app macro discoverability, we will always show up to 10 app macros (if they exist) in a category *in addition* to the 30 item maximum. In the future, we will explore more dynamic behavior here.

* For Forge app macros, this category will be determined by the `category (string)` property if available, or the first category listed in `categories ([string])` as a fallback until Feb 25, 2027, when `categories ([string])` will no longer work.
* For Connect app macros, this category will be determined by the first category listed in `categories ([string])` as Connect app macros will not gain access to the new `category (string)` property.

## Action required from developers of app macros

#### For Forge app macros

To ensure your app macro appears in an accurate category as we roll out these changes, we strongly recommend updating the new `category (string)` property (available for use by developers now) with one of the new valid categories below by Oct 6, 2026, when we begin to rollout the modernized element browser experience.

If not by Oct 6, 2026, be sure to update the new `category (string)` property by Feb 25, 2027 to ensure your app is assigned a category when `categories [(string)]` is no longer recognized. Otherwise, it will be shown in “Other elements” as well as the default “All” category.

Valid categories:

* Structure - `structure` *(Native examples: Action item, Table, Status)*
* Media - `media` *(Native examples: Image, video, or file, Link, Emoji)*
* Embed - `embed` *(Native examples: like Google Drive, Figma, Dropbox)*
* Text formatting - `text-formatting` *(Native examples: Bullet list, Heading 1, Quote)*
* Data and charts - `data-and-charts` *(Native examples: Database, Jira work items, Child items)*

To help developers plan, here is a simplified timeline of the upcoming changes.

**Between now and** Oct 6, 2026**:**

* In the **slash element browser:** All app macros will continue to appear as they do today.
* In the **modal element browser:** All app macros will continue to appear in the **macro element browser** in any valid legacy categories listed in `categories ([string])`. The new `category (string)` property will not be used in product until then.

**On and after** Oct 6, 2026**, and before** Feb 25, 2027**:**

* Forge app macros will:

  * In the **slash element browser**: Appear only in one category determined by the `category (string)` property – or, the first category listed in `categories ([string])` as a fallback if no valid `category (string)` is set.
  * In the **modal element browser**: Appear either in one category determined by the `category (string)` property – OR in one or multiple categories listed in `categories ([string])` as a fallback (with above mapping between legacy and new categories) if no valid `category (string)` is set.
* Connect app macros will:

  * In the **slash element browser**: Appear only in one category determined by the first category listed in `categories ([string])` as Connect app macros will not gain access to the new `category (string)` property.
  * In the **modal element browser**: Appear in one or multiple categories listed in `categories ([string])` as Connect app macros will not gain access to the new `category (string)` property.

**On and after** Feb 25, 2027**:**

* Forge app macros will:

  * In the **slash element browser**: Appear only in one category determined by the `category (string)` property. `categories ([string])`will no longer work or be recognized.
  * In the **modal element browser**: Appear only in one category determined by the `category (string)` property. `categories ([string])`will no longer work or be recognized.
* Connect app macros will:

  * In the **slash element browser**: Appear only in one category determined by the first category listed in `categories ([string])` as Connect app macros will not gain access to the new `category (string)` property.
  * In the **modal element browser**: Appear only in one category determined by the first category listed in `categories ([string])` as Connect app macros will not gain access to the new `category (string)` property.

#### For Connect app macros

We highly recommend moving to Forge and following the above steps for Forge apps. Otherwise, no work is required for Connect apps, as Connect app macros will not gain access to the new `category (string)` property nor be able to update their `categories ([string])` property.

## Thank you

Lastly, thank you for giving valuable feedback on [RFC-140: Updating categories in the editor’s element browser](https://community.developer.atlassian.com/t/rfc-140-updating-categories-in-the-editors-element-browser/101855 "https://community.developer.atlassian.com/t/rfc-140-updating-categories-in-the-editors-element-browser/101855") about this topic.
