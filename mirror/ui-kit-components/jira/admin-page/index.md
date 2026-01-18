# UI Kit components

You must be on `@forge/react` major version 10 or higher to use the latest version of
UI Kit components.

To upgrade your app to the latest version, run `npm install --save @forge/react@latest` in your terminal.

Upgrading to the latest version may contain [breaking changes](/platform/forge/ui-kit/version-10-changes/) for **existing UI Kit apps**, *as all existing component APIs have been updated*.

UI Kit offers a wide range of pre-built and customizable components that align with Atlassian's design standards.

## Action

Use action components to initiate or execute specific tasks within your app.

| Components | Description |
| --- | --- |
| [Button](/platform/forge/ui-kit/components/button) | A button that triggers an event or action. |
| [Button group](/platform/forge/ui-kit/components/button-group) | A button group displays multiple buttons together. |
| [Link](/platform/forge/ui-kit/components/link/) | A component for displaying inline links. |

## Content & image

Use content and image components to display text, visuals, and other data in your app.

| Components | Description |
| --- | --- |
| [ADF renderer](/platform/forge/ui-kit/components/adf-renderer/) | A renderer for ADF documents. |
| [Code](/platform/forge/ui-kit/components/code/) | A code highlight for short strings in the body text. |
|
| [Code block](/platform/forge/ui-kit/components/code-block/) | A code block highlights an entire block of code and keeps the formatting. |
|
| [Comment (Preview)](/platform/forge/ui-kit/components/comment-editor/) | A comment displays discussions and user feedback. |
| [Dynamic table](/platform/forge/ui-kit/components/dynamic-table/) | A table that displays rows of data with built-in pagination, sorting, and re-ordering functionality. |
| [Image](/platform/forge/ui-kit/components/image/) | An image, which functions similarly to a native `img` element. |
| [Icon](/platform/forge/ui-kit/components/icon/) | A visual representation for actions or other items. |
| [User](/platform/forge/ui-kit/components/user/) | A representation of a user, displaying details such as name and profile picture. |
| [User group](/platform/forge/ui-kit/components/user-group/) | A stack-like entity that encompasses multiple users, including their names and profile pictures. |

## Feedback

Use feedback components to provide users with responses or notifications based on their actions in your app.

| Components | Description |
| --- | --- |
| [Badge](/platform/forge/ui-kit/components/badge/) | A visual indicator for numeric values, such as tallies and scores. |
| [Empty state (Preview)](/platform/forge/ui-kit/components/empty-state/) | An empty state appears when there is no data to display and describes what the user can do next. |
| [Lozenge](/platform/forge/ui-kit/components/lozenge/) | A visual indicator to display different status types or states. |
| [Progress bar](/platform/forge/ui-kit/components/progress-bar/) | A progress bar communicates the status of a system process. |
| [Progress tracker](/platform/forge/ui-kit/components/progress-tracker/) | A progress tracker displays the steps and progress through a journey. |
| [Section message](/platform/forge/ui-kit/components/section-message/) | A text callout to alert users to important information. |
| [Spinner](/platform/forge/ui-kit/components/spinner/) | A spinner is an animated spinning icon that lets users know content is being loaded. |
| [Tag](/platform/forge/ui-kit/components/tag/) | A visual indicator for UI objects for quick recognition. |
| [Tag group](/platform/forge/ui-kit/components/tag-group/) | A group of tag components. |
| [Tooltip](/platform/forge/ui-kit/components/tooltip/) | A floating, non-actionable label used to explain a user interface element or feature. |

## Primitives

Use layout components to structure and organize elements within your app.

| Components | Description |
| --- | --- |
| [Box](/platform/forge/ui-kit/components/box) | A box is a generic container that provides managed access to design tokens. |
| [Inline](/platform/forge/ui-kit/components/inline) | An inline manages the horizontal layout of direct children using flexbox. |
| [Pressable (Preview)](/platform/forge/ui-kit/components/pressable) | A pressable is a primitive for building custom buttons. |
| [Stack](/platform/forge/ui-kit/components/stack) | A stack manages the vertical layout of direct children using flexbox. |
| [XCSS](/platform/forge/ui-kit/components/xcss) | A styling API that integrates with Atlassian's design tokens and primitives. |

## Navigation

Use navigation components to assist users in navigating and interacting with different sections of your app.

| Components | Description |
| --- | --- |
| [Empty state](/platform/forge/ui-kit/components/empty-state/) | An empty state appears when there is no data to display and describes what the user can do next. |
| [Tabs](/platform/forge/ui-kit/components/tabs/) | Tabs are used to organize content by grouping similar information on the same page. |

## Overlays

Use overlay components to highlight certain areas or display additional information in your app.

| Components | Description |
| --- | --- |
| [Modal](/platform/forge/ui-kit/components/modal/) | A dialog that appears in a layer above the app’s UI and requires user interaction. |
| [Popup (Preview)](/platform/forge/ui-kit/components/popup/) | A popup displays brief content in an overlay. |

## Selection & input

Use selection and input components to allow users to enter information or choose options in your app.

| Components | Description |
| --- | --- |
| [Calendar (Preview)](/platform/forge/ui-kit/components/calendar/) | An interactive calendar for date selection experiences. |
| [Checkbox](/platform/forge/ui-kit/components/checkbox/) | An input control that allows a user to select one or more options from a number of choices. |
| [Checkbox group](/platform/forge/ui-kit/components/checkbox-group/) | A list of options where one or more choices can be selected. |
| [Date picker](/platform/forge/ui-kit/components/date-picker/) | A date picker allows the user to select a particular date. |
| [File picker (EAP)](/platform/forge/ui-kit/components/file-picker/) | A file picker allows the user to select files. |
| [File card (EAP)](/platform/forge/ui-kit/components/file-card/) | A file card component used to display and manage selected files. |
| [Form](/platform/forge/ui-kit/components/form/) | A form component that allows for the inclusion of a list of components, a submit button, and a function that handles the submit event. |
| [Inline edit (Preview)](/platform/forge/ui-kit/components/inline-edit/) | An inline edit displays a custom input component that switches between reading and editing on the same page. |
| [Radio](/platform/forge/ui-kit/components/radio/) | A radio input allows users to select only one option from a number of choices. |
| [Radio group](/platform/forge/ui-kit/components/radio-group/) | A radio group presents a list of options where only one choice can be selected. |
| [Range](/platform/forge/ui-kit/components/range/) | A range lets users choose an approximate value on a slider. |
| [Select](/platform/forge/ui-kit/components/select/) | A dropdown field that allows users to select an option from a list. |
| [Time picker (Preview)](/platform/forge/ui-kit/components/time-picker/) | A time picker allows the user to select a specific time. |
| [Text area](/platform/forge/ui-kit/components/text-area/) | An input field that lets users enter long form text, which spans over multiple lines. |
| [Text field](/platform/forge/ui-kit/components/textfield/) | An input field that allows a user to write or edit text. |
| [Toggle](/platform/forge/ui-kit/components/toggle/) | A component that allows users to switch between two states, such as on/off or true/false. |
| [User Picker](/platform/forge/ui-kit/components/user-picker/) | A dropdown field that allows users to search and select users from a list. |

## Typography

Use typography components to manage the style and appearance of text within your app.

| Components | Description |
| --- | --- |
| [Heading](/platform/forge/ui-kit/components/heading/) | A typography component used to display text in different sizes and formats. |
| [List (Preview)](/platform/forge/ui-kit/components/list/) | A typography component used to display dot points or numbered lists. |
| [Text](/platform/forge/ui-kit/components/text/) | A typography component used to display body text. |

## Data visualizations

Use these components to create visual representations of your data, making it easier to understand at a glance.

| Charts | Description |
| --- | --- |
| [Bar chart](/platform/forge/ui-kit/components/bar-chart/) | A visual representation of data using rectangular bars of varying heights to compare different categories or values. |
| [Donut chart](/platform/forge/ui-kit/components/donut-chart/) | A visual representation of data in a donut format. |
| [Horizontal bar chart](/platform/forge/ui-kit/components/horizontal-bar-chart/) | A visual representation of data using horizontal rectangular bars of varying lengths to compare different categories or values. |
| [Stack bar chart](/platform/forge/ui-kit/components/stack-bar-chart/) | A visual representation of data using rectangular bars of varying heights to demonstrate comparisons between categories of data. |
| [Horizontal stack bar chart](/platform/forge/ui-kit/components/horizontal-stack-bar-chart/) | A visual representation of data using horizontal rectangular bars of varying lengths to demonstrate comparisons between categories of data. |
| [Line chart](/platform/forge/ui-kit/components/line-chart/) | A visual representation of data showing trends over time. |
| [Pie chart](/platform/forge/ui-kit/components/pie-chart/) | A visual representation of data proportions in a circular format. |
