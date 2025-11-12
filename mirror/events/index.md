# Events

Your app can subscribe to events or set up an HTTP endpoint to invoke a function within your app
without any user interaction.

This enables your app to respond to activities occurring on the back end of Atlassian apps and
the Forge platform whether
they resulted from any user's interaction with the Atlassian app or other processing behind
the scenes, such as a REST API based script that made bulk updates to your projects.

Examples of the many Atlassian app and platform events your app can listen for include:

* a site upgrading a Forge app to a new major version
* any user updating a Jira issue
* any user creating a Confluence space
* a batch import process adding new Confluence pages
* an app being added to a data security policy

See [Types of event modules](#types-of-event-modules) for more information about the events
available in Forge.

Some use cases for apps that respond to events include:

* An app that maintains and publishes to Confluence up-to-date custom statistics about Jira issue
  activities, which might subscribe to events related to the Jira issues and aggregate that
  information for publication.
* "Pushing" new and updated data from an Atlassian app to another platform for external reporting.
  This is an alternative to running a client app on the other platform that periodically polls the
  Atlassian app using REST APIs and pulls the data to the other platform.

## Considerations for apps that respond to events

Some special considerations apply when developing an app that responds to events, that do not apply
to apps that run within a user's interactive session.

Forge app code that responds to events cannot access the Atlassian app’s user interface and is not
linked to any user’s session. Therefore, if you try to retrieve additional data about the event
from the `useProductContext` hook, you'll find that it includes a limited amount of information
compared to the Atlassian app context for interactive sessions.

However, your app can include separate UI modules that respond to the current user's Atlassian app
interactions, if desired.

Additionally, app code that responds to events runs under the identity of the app system user,
rather than an Atlassian interactive user account. If you have specified permissions for a
resource such as a Confluence page or Jira project that only allow certain Atlassian user accounts
access to it, your application may not be able to access that resource when handling a received
event because the app system user may not have permission to do so.

## Configuring your app for events

To configure your app to respond to events:

* Add a module to your manifest that specifies the events your app will respond to, and what it
  will do when it receives those events. For a quick start, you can specify a
  `Atlassian-app-trigger`, `scheduled-trigger` or `webtrigger` template when running `forge create`.
* Add functionality to your Forge app to process the incoming event according to the details
  on the event's reference page. The table in this section contains links to the event reference pages.

Events are categorised by the module type used to configure them in the `manifest.yml` file,
as described below.

### Types of event modules

| Module type | Used to... |
| --- | --- |
| [trigger](/platform/forge/manifest-reference/modules/trigger/) | Notify your app when selected Atlassian app and platform events occur.  To learn about specific Atlassian app and platform events your application can respond to using a trigger module, see:  If you are using `forge create` to create an app that includes a trigger module, choose the `Atlassian-app-trigger` template even when defining a module to respond to a lifecycle or data security policy event. |
| [scheduled trigger](/platform/forge/events-reference/scheduled-trigger) | Invoke your app on a periodic basis, such as once per hour. |
| [web trigger](/platform/forge/events-reference/web-trigger) | Register an endpoint that can accept HTTP requests, including third party requests, made to your app's registered URL. |

### Data associated with each module type

Each of the event module types has:

* A set of properties specific to that module type, that you use to configure the module in the manifest.

  For example, the `trigger` module requires that you specify a key that uniquely
  identifies that module in the manifest, a function or endpoint
  (for [Forge Remote](/platform/forge/remote)) to run when the event occurs, and the list of events
  that module is subscribing to.

  For more information, see the
  [Scheduled Trigger](/platform/forge/manifest-reference/modules/scheduled-trigger),
  [Trigger](/platform/forge/manifest-reference/modules/trigger), and
  [Web trigger](/platform/forge/manifest-reference/modules/web-trigger) manifest reference topics.
* (Atlassian app, data security policy, and lifecycle events only) An additional set of properties
  specific to the event being configured.

  For example, when an event notifies your app about comments added in Confluence, it includes
  the name of the event, the atlassian ID of the user whose action prompted the event, and an
  object representing the comment, including the page ID and space of the page being commented on.

  See the event-specific topics in the Events reference area for more information.
* A context object that provides more information about the context the event occurred in, such as
  the installation ID of the Atlassian site the app is installed in.

## Handling cascading events in Jira

In Jira events, the relationship between entities is hierarchical, structured as follows:

* **Project**: The top-level entity.
  * **Issue**: Child of project.
    * **Worklog**: Child of issue.
    * **Comment**: Child of issue.
    * **Attachment**: Child of issue.
  * **Board**: Associated with project through board location.
  * **Component**: Child of project.
  * **Version**: Child of project.
  * **Issue type**: Child of team-managed project.

Understanding this hierarchy is key to managing events, especially delete events, which cascade down
the hierarchy.

### Handling delete events

When a project is deleted in Jira, all its descendants (issues, worklogs, comments, attachments)
or associated entities (eg. boards) are also removed. However, it's important to note:

**We only emit a delete event for top-level entities.**

When a project is deleted, we won't emit separate delete events for its child issues, associated
boards, versions, components or issue types.

The same applies to the descendants of an issue (worklogs, comments, attachments) when its parent
is deleted.

This means that if your app relies on receiving delete events for individual issues, worklogs,
comments, attachments, boards, versions, components, and issue types you'll need to implement
a workaround to handle cascading deletes at the project or issue level.

### Workaround for handling cascading deletes

To effectively manage cascading deletes and ensure your app can react to these events, you should
store an up-to-date copy of the entire project hierarchy structure. To achieve this consider
the following approach:

1. Listen for delete events of higher-level entities if you want to be notified about removal
   of lower-level entites: Initially, ensure your app is set up to listen for delete events
   at the project and issue levels. This will be your trigger to check for cascading deletes.
2. Fetch and save entity structure before deletion: Before a project or issue is deleted,
   store a list of all associations between entities that your app needs to track. This can be done
   by using Jira's REST API to query for all issues under a project and subsequently all worklogs,
   comments, and attachments for those issues.
3. Handle deletes manually in your app: Once you have the list of all entities that will be deleted,
   your app can then manually process these deletions in a way that suits your application's needs.
   This could involve removing references to these entities from your app's database, triggering
   specific cleanup processes, or logging the deletions for audit purposes.

Example pseudocode for handling cascading deletes:

```
```
1
2
```



```
// Example function to handle project deletion
function onProjectDelete(projectId) {
  // Read all issues for the project based on previously stored association
  const issues = readCachedIssuesForProject(projectId);

  // For each issue, read and handle descendants
  issues.forEach(issue => {
    const worklogs = readCachedWorklogsForIssue(issue.id);
    const comments = readCachedCommentsForIssue(issue.id);
    const attachments = readCachedAttachmentsForIssue(issue.id);

    // Handle deletion of worklogs, comments, and attachments here
    // For example, remove references from your app's DB
    handleDelete(worklogs, comments, attachments);
  });

  // Finally, handle the deletion of issues at your app level
  handleDelete(issues);
}

// Note: `readCachedIssuesForProject`, `readCachedWorklogsForIssue`, `readCachedCommentsForIssue`,
// `readCachedAttachmentsForIssue`, and `handleDelete` are placeholders for functions you would need
// to implement based on your app's architecture and the specifics of the Jira REST API calls. 
// These functions are intended to demonstrate the logical flow for handling cascading deletes.
```
```

### Best practices

* Implement robust error handling: When dealing with cascading deletes, ensure your app gracefully
  handles errors. For instance, if fetching descendants of an issue fails, your app should log this
  error and proceed with the next steps cautiously.
* Optimize API calls: Fetching a large number of entities can be resource-intensive. Optimize your
  API calls by using bulk operations (like Jira expressions) wherever possible and by limiting
  the fields returned to only those necessary for your deletion logic.
* Keep track of dependencies: If your app creates additional entities or relationships based on
  issues, worklogs, comments, attachments, boards, versions, components, or issue types,
  ensure you have a mechanism in place to track and handle these dependencies when the parent entities
  are deleted.
* Regularly review API changes: Jira's REST API and Forge platform are continually evolving.
  Regularly review Atlassian's documentation for any changes that might affect how delete events
  and entity hierarchies are managed.

## Handling cascading events in Confluence

In Confluence events, the relationship between entities is hierarchical, structured as follows:

* **Space**: The top-level entity.
  * **Page**: Child of space.
    * **Comment**: Child of page.
    * **Attachment**: Child of page.
    * **Custom content**: Child of page (Forge or Connect app custom content).
      * **Comment**: Child of custom content.
      * **Attachment**: Child of custom content.
      * **Custom content**: Child of custom content.
  * **Whiteboard**: Child of space.
  * **Database**: Child of space.
  * **Smart link**: Child of space.
  * **Folder**: Child of space.
  * **Blog post**: Child of space.
    * **Comment**: Child of blog post.
    * **Attachment**: Child of blog post.
    * **Custom content**: Child of blog post (Forge or Connect app custom content).
      * **Comment**: Child of custom content.
      * **Attachment**: Child of custom content.
      * **Custom content**: Child of custom content.
  * **Custom content**: Child of space (Forge or Connect app space-level custom content).
    * **Comment**: Child of custom content.
    * **Attachment**: Child of custom content.
    * **Custom content**: Child of custom content.

In addition, entities of the following types can create a tree-like parent-child relationship
between each other creating, for example, a page can be a parent of another page, a database
can be a parent of a folder, and so on:

* Page
* Whiteboard
* Database
* Smart link
* Folder

Entities of these types are the ones that a user sees in the UI as a structure called "content tree."
Comments, attachments, and custom content are not part of the content tree, but they are still
part of the hierarchy as children of pages, or blog posts.

Understanding this hierarchy is essential for managing events, particularly delete events,
which cascade down the hierarchy.

### Handling delete events

When a space is deleted in Confluence, all its descendants are also removed. This includes entities
from a content tree (pages, whiteboards, databases, smart links, folders) as well as blog posts,
and child entities: comments, attachments, and custom content. However, it's important to note:

**We only emit a delete event for top-level entities.**

When a space is deleted, we won't emit separate delete events for its children, which include pages,
blog posts, whiteboards, databases, smart links, folders, custom content, comments, attachments,
or child custom content.

The same applies to the descendants of a page or blog post (comments, attachments, custom content)
when their parent is deleted. It's different, however, for content tree entities. When an individual
content tree entity is trashed, it gets detached from a content tree hierarchy, so all individually
deleted entities will receive delete events.

This means that if your app relies on receiving delete events for individual entities,
you'll need to implement a workaround to handle cascading deletes at the space, page, blog post,
or custom content level.

### Workaround for handling cascading deletes

To effectively manage cascading deletes and ensure your app can react to these events,
you should store an up-to-date copy of the entire space hierarchy structure. To achieve this,
consider the following approach:

1. **Listen for delete events of higher-level entities**: Ensure your app is set up to listen
   for delete events at the space, page, blog post, and custom content levels. This will be your
   trigger to check for cascading deletes.
2. **Fetch and save entity structure before deletion**: Before a space, page, blog post,
   or custom content is deleted, store a list of all associations between entities that your app needs
   to track. This can be done by using Confluence's REST API to query for all content tree entities
   and blog posts under a space, and subsequently all comments, attachments, and custom content
   for those entities.
3. **Handle deletes manually in your app**: Once you have the list of all entities that
   will be deleted, your app can then manually process these deletions in a way that suits your
   application's needs. This could involve removing references to these entities from
   your app's database, triggering specific cleanup processes, or logging the deletions
   for audit purposes.

Example pseudocode for handling cascading deletes:

```
```
1
2
```



```
// Example function to handle space deletion
function onSpaceDelete(spaceId) {
  // Read all content tree entities, blog posts, and space-level custom content for the space
  const contentTreeEntities = readCachedContentTreeEntitiesForSpace(spaceId);
  const blogPosts = readCachedBlogPostsForSpace(spaceId);
  const spaceCustomContents = readCachedCustomContentForSpace(spaceId);

  // For each content tree entity, handle deletion
  contentTreeEntities.forEach(entity => {
    onContentTreeEntityDelete(entity.id);
  });

  // For each blog post, read and handle descendants
  blogPosts.forEach(blogPost => {
    onBlogPostDelete(blogPost.id);
  });
  
  // For each space-level custom content, read and handle descendants
  spaceCustomContents.forEach(spaceCustomContent => {
    onCustomContentDelete(spaceCustomContent.id);
  });
  
  // Handle deletion of space-level entities
  handleDelete(contentTreeEntities, blogPosts, spaceCustomContents);
}

// Example function to handle content tree entity deletion
function onContentTreeEntityDelete(entity) {
  if (entity.type === 'page') {
    onPageDelete(entity.id);
  }
  
  // Recursively handle descendants of a content tree entity
  const childEntities = readCachedContentTreeEntitiesForEntity(entity.id);
  childEntities.forEach(childEntity => {
    onContentTreeEntityDelete(childEntity);
  });

  // Handle deletion of child entities
  handleDelete(childEntities);
}

// Example function to handle page deletion
function onPageDelete(pageId) {
  // Read all descendants for the page
  const comments = readCachedCommentsForPage(pageId);
  const attachments = readCachedAttachmentsForPage(pageId);
  const customContents = readCachedCustomContentForPage(pageId);

  // Recursively handle child custom contents
  customContents.forEach(customContent => {
    onCustomContentDelete(customContent.id);
  });

  // Handle deletion of page descendants
  handleDelete(comments, attachments, customContent);
}

// Example function to handle blog post deletion
function onBlogPostDelete(blogPostId) {
  // Read all descendants for the blog post
  const comments = readCachedCommentsForBlogPost(blogPostId);
  const attachments = readCachedAttachmentsForBlogPost(blogPostId);
  const customContents = readCachedCustomContentForPage(blogPostId);

  // Recursively handle child custom contents
  customContents.forEach(customContent => {
    onCustomContentDelete(customContent.id);
  });

  // Handle deletion of blog post descendants
  handleDelete(comments, attachments, customContents);
}

function onCustomContentDelete(customContentId) {
  // Read all descendants for the custom content
  const comments = readCachedCommentsForCustomContent(customContentId);
  const attachments = readCachedAttachmentsForCustomContent(customContentId);
  const childCustomContents = readCachedChildCustomContentForCustomContent(customContentId);

  // Recursively handle child custom contents
  childCustomContents.forEach(childCustomContent => {
    onCustomContentDelete(childCustomContent.id);
  });

  // Handle deletion of custom content descendants
  handleDelete(comments, attachments, childCustomContents);
}
```
```

### Best practices

* **Implement robust error handling**: When dealing with cascading deletes, ensure your app
  gracefully handles errors. For instance, if fetching descendants of a page fails, your app should
  log this error and proceed with the next steps cautiously.
* **Optimize API calls**: Fetching a large number of entities can be resource-intensive.
  Optimize your API calls by using bulk operations wherever possible and by limiting the fields
  returned to only those necessary for your deletion logic.
* **Handle page hierarchy carefully**: Confluence pages can have complex parent-child relationships.
  When handling content deletions, ensure you properly traverse the content tree to identify all
  affected descendants.
* **Keep track of dependencies**: If your app creates additional entities or relationships
  based on spaces, pages, blog posts, comments, attachments, or custom content, ensure you have
  a mechanism in place to track and handle these dependencies when the parent entities are deleted.
* **Regularly review API changes**: Confluence's REST API and Forge platform are continually evolving.
  Regularly review Atlassian's documentation for any changes that might affect how delete events
  and entity hierarchies are managed.
