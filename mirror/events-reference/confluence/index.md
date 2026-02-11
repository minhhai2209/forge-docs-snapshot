# Confluence events

Forge apps can subscribe to Confluence events for:

Your Forge app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

## Pages, live docs, and blog posts

Forge apps can subscribe to the following page, live doc, and blog post events:

* **Pages and live docs**
  * Liked: `avi:confluence:liked:page`
  * Viewed: `avi:confluence:viewed:page`
  * Archived: `avi:confluence:archived:page`
  * Unarchived: `avi:confluence:unarchived:page`
  * Moved: `avi:confluence:moved:page`
  * Copied: `avi:confluence:copied:page`
  * Children reordered: `avi:confluence:children_reordered:page`
  * Permissions updated: `avi:confluence:permissions_updated:page`
  * Trashed: `avi:confluence:trashed:page`
  * Restored: `avi:confluence:restored:page`
  * Deleted: `avi:confluence:deleted:page`
* **Pages**
  * Created: `avi:confluence:created:page`
  * Updated: `avi:confluence:updated:page`
* **Live docs**
  * Created: `avi:confluence:initialized:page`
  * End of first edit session: `avi:confluence:started:page`
  * End of subsequent editing sessions: `avi:confluence:snapshotted:page`
  * Converted to page: `avi:confluence:published:page`
* **Blog posts**
  * Created: `avi:confluence:created:blogpost`
  * Updated: `avi:confluence:updated:blogpost`
  * Liked: `avi:confluence:liked:blogpost`
  * Viewed: `avi:confluence:viewed:blogpost`
  * Permissions updated: `avi:confluence:permissions_updated:blogpost`
  * Trashed: `avi:confluence:trashed:blogpost`
  * Restored: `avi:confluence:restored:blogpost`
  * Deleted: `avi:confluence:deleted:blogpost`

Page, live doc, and blog post events require the following OAuth scopes:

* `read:confluence-content.summary` - Required for all page, live doc, and blog post events
* `write:confluence-content` - Additionally required for trashed events (this requirement may be removed in the future)

Trashed and deleted events, in addition to the above, require the OAuth scope `write:confluence-content`. This requirement may be removed in the future.

Keep in mind that cascading deletion events aren’t emitted. For more information, see
[Cascading events guide](/platform/forge/events/#handling-cascading-events-in-confluence).

Events such as `avi:confluence:moved:page` which apply to both pages and live docs will have a `subType="live"` field added in their payload if emitted by a live doc.

Page, live doc, and blog post events share the same payload format, with the exception of some events that have additional fields (see below).

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:page`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| suppressNotifications | `boolean` | Indicates whether notifications for this event were suppressed. |
| updateTrigger | `string` | The reason that caused the update event to trigger. Included only for the following events:  * `avi:confluence:updated:page` * `avi:confluence:started:page` * `avi:confluence:snapshotted:page` * `avi:confluence:published:page` * `avi:confluence:updated:blogpost` |
| content | `Content` | An object representing the page, live doc or blog post. |
| prevContent | `Content` | Only for `avi:confluence:moved:page`. An object representing the old page. |
| originContentId | `string` | Only for `avi:confluence:copied:page`. The ID of the origin content that was copied. |
| oldSortedChildPageIds | `string[]` | Only for `avi:confluence:children_reordered:page`. The list of child page IDs before the reorder. |
| newSortedChildPageIds | `string[]` | Only for `avi:confluence:children_reordered:page`. The list of child page IDs after the reorder. |

### Type reference

```
```
1
2
```



```
interface Content {
  id: string;
  type: "blogpost" | "page";
  subType?: "live"; // Included only if the page is a live doc.
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  space: Space;
  history: History;
  version: Version;
}

/**
 * The space the page, live doc, or blog post is located in.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
}

/**
 * Information about the creator and owner of the page, live doc, or blog post that the event is related to,
 * as well as the date it was created.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Information about the current version of the page, live doc, or blog post.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a page is created.

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:page",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "suppressNotifications": false,
  "content": {
    "id": "838205441",
    "type": "page",
    "status": "current",
    "title": "A brand new page",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:29:21.707Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T06:29:21.707Z",
      "number": 1
    }
  }
}
```
```

## Whiteboards, databases, smart links, and folders

Forge apps can subscribe to the following whiteboard, database, smart link in the content tree, and folder events:

* **Whiteboards**
  * Created: `avi:confluence:created:whiteboard`
  * Moved: `avi:confluence:moved:whiteboard`
  * Copied: `avi:confluence:copied:whiteboard`
  * Permissions updated: `avi:confluence:permissions_updated:whiteboard`
* **Databases**
  * Created: `avi:confluence:created:database`
  * Moved: `avi:confluence:moved:database`
  * Copied: `avi:confluence:copied:database`
  * Permissions updated: `avi:confluence:permissions_updated:database`
* **Smart links in the content tree**
  * Created: `avi:confluence:created:embed`
  * Moved: `avi:confluence:moved:embed`
  * Copied: `avi:confluence:copied:embed`
* **Folders**
  * Created: `avi:confluence:created:folder`
  * Moved: `avi:confluence:moved:folder`
  * Copied: `avi:confluence:copied:folder`
  * Permissions updated: `avi:confluence:permissions_updated:folder`

These events share the same payload format as [page and blog post events](#pages--live-docs--and-blog-posts).
They also require the OAuth scope `read:confluence-content.summary`.

## Inline tasks

Forge apps can subscribe to the following inline task events:

* Created: `avi:confluence:created:task`
* Updated: `avi:confluence:updated:task`
* Removed: `avi:confluence:removed:task`

Task events require the OAuth scope `read:confluence-content.all` and share the same payload format,
with the exception of some events that have additional fields (see below).

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:task`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| suppressNotifications | `boolean` | Indicates whether notifications for this event were suppressed. |
| task | `Task` | An object representing the inline task. |
| oldTask | `Task` | Only for `avi:confluence:updated:task`. An object representing the previous version of the inline task. |
| content | `Content` | The page, live doc or blog post, that contains the inline task. |

### Type reference

```
```
1
2
```



```
interface Task {
  id: number;
  uuid: string | null; // The UUID of the task, or null if not available.
  status: "complete" | "incomplete";
  statusAsString: "CHECKED" | "UNCHECKED";
  assignee: string | null; // The account ID of the user assigned to the task, or null if not assigned.
  dueDate: string | null; // Date and time in ISO 8601 format, or null if no due date is set.
}

interface Content {
  id: string;
  type: "blogpost" | "page";
  subType?: "live"; // Included only if the page is a live doc.
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  space: Space;
  history: History;
  version: Version;
}

/**
 * The space the page, live doc, or blog post is located in.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
}

/**
 * Information about the creator and owner of the page, live doc, or blog post that the event is related to,
 * as well as the date it was created.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Information about the current version of the page, live doc, or blog post.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a task is updated (checked).

```
```
1
2
```



```
{
  "eventType": "avi:confluence:updated:task",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "task": {
    "id": 1,
    "uuid": "e0a0e71d-5575-4185-bf33-61364fb0960e",
    "status": "complete",
    "statusAsString": "CHECKED",
    "assignee": "4ad9aa0c52dc1b420a791d12",
    "dueDate": "2021-02-21T07:00:00Z"
  },
  "oldTask": {
    "id": 1,
    "uuid": "e0a0e71d-5575-4185-bf33-61364fb0960e",
    "status": "incomplete",
    "statusAsString": "UNCHECKED",
    "assignee": "4ad9aa0c52dc1b420a791d12",
    "dueDate": "2021-02-21T07:00:00Z"
  },
  "content": {
    "id": "838205441",
    "type": "page",
    "status": "current",
    "title": "A brand new page",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:29:21.707Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T06:29:21.707Z",
      "number": 1
    }
  }
}
```
```

Forge apps can subscribe to the following comment events:

* Created: `avi:confluence:created:comment`
* Updated: `avi:confluence:updated:comment`
* Liked: `avi:confluence:liked:comment`
* Deleted: `avi:confluence:deleted:comment`

Comment events require the OAuth scope `read:confluence-content.summary` and share the same
payload format.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:comment`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| suppressNotifications | `boolean` | Indicates whether notifications for this event were suppressed. |
| updateTrigger | `string` | Only for `avi:confluence:updated:comment`. The reason that caused the update event to trigger. |
| content | `Content` | An object representing the comment. |

### Type reference

```
```
1
2
```



```
interface Content {
  id: string;
  type: "comment";
  status: "current" | "trashed" | "historical" | "draft";
  title: string;
  space: Space;
  history: History;
  version: Version;
  ancestors: Ancestors;
  container: CommentContainer;
  extensions: {
    location: "footer" | "inline";
  };
}

/**
 * The space the comment is located in.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
}

/**
 * Information about the creator and owner of the comment, its container, or ancestor,
 * as well as the date it was created.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Information about the current version of the comment or its container.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * If this comment is part of a thread of replies, then this contains a list of all comments before
 * this particular comment, sorted from newest to oldest. Otherwise, it's an empty array.
 */
type Ancestors = Ancestor[];

/**
 * Represents a comment that is an ancestor of the current comment.
 */
interface Ancestor {
  id: string;
  type: "comment";
  status: "current" | "trashed" | "historical" | "draft";
  title: string;
  history: History;
}

/**
 * The page, blog post or custom content the comment is located in.
 */
interface CommentContainer {
  id: number;
  type: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  history: History;
  version: Version;
  space: Space;
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a new comment is posted on a page.

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:comment",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "suppressNotifications": false,
  "content": {
    "id": "838205455",
    "type": "comment",
    "status": "current",
    "title": "Re: A brand new page",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T07:10:41.070Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T08:35:00.100Z",
      "number": 1
    },
    "ancestors": [
      {
        "id": "838205415",
        "type": "comment",
        "status": "current",
        "title": "Re: A brand new page",
        "history": {
          "latest": true,
          "createdBy": {
            "type": "known",
            "username": "5df0ac136e39300e512d2ffa",
            "accountId": "5df0ac136e39300e512d2ffa",
            "accountType": "atlassian",
            "email": "5df0ac136e39300e512d2ffa",
            "publicName": "5df0ac136e39300e512d2ffa",
            "profilePicture": {
              "path": "/wiki/aa-avatar/5df0ac136e39300e512d2ffa",
              "width": 48,
              "height": 48,
              "isDefault": false
            },
            "displayName": "5df0ac136e39300e512d2ffa",
            "isExternalCollaborator": false
          },
          "ownedBy": {
            "type": "known",
            "username": "5df0ac136e39300e512d2ffa",
            "accountId": "5df0ac136e39300e512d2ffa",
            "accountType": "atlassian",
            "email": "5df0ac136e39300e512d2ffa",
            "publicName": "5df0ac136e39300e512d2ffa",
            "profilePicture": {
              "path": "/wiki/aa-avatar/5df0ac136e39300e512d2ffa",
              "width": 48,
              "height": 48,
              "isDefault": false
            },
            "displayName": "5df0ac136e39300e512d2ffa",
            "isExternalCollaborator": false
          },
          "createdDate": "2021-01-20T07:09:32.573Z"
        }
      }
    ],
    "container": {
      "id": "838205441",
      "type": "page",
      "status": "current",
      "title": "A brand new page",
      "history": {
        "latest": true,
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "ownedBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:29:21.707Z"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "when": "2021-01-20T06:29:21.707Z",
        "number": 1
      }
    },
    "extensions": {
      "location": "footer"
    }
  }
}
```
```

## Spaces

Forge apps can subscribe to the following space events:

* Created: `avi:confluence:created:space:V2`
* Updated: `avi:confluence:updated:space:V2`
* Permissions updated: `avi:confluence:permissions_updated:space:V2`
* Deleted: `avi:confluence:deleted:space:V2`

Space events require the following OAuth scopes:

* `read:confluence-space.summary` - Required for all space events
* `write:confluence-space` - Additionally required for `avi:confluence:permissions_updated:space:V2` event (this requirement may be removed in the future)

Events `avi:confluence:permissions_updated:space:V2` and `avi:confluence:deleted:space:V2`, in addition to the above,
require the OAuth scope `write:confluence-space`. This requirement may be removed in the future.

Keep in mind that cascading deletion events aren’t emitted. For more information, see
[Cascading events guide](/platform/forge/events/#handling-cascading-events-in-confluence).

All space events share the same payload format.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:space:V2`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| space | `Space` | An object representing the space. |

### Type reference

```
```
1
2
```



```
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
  history: History;
}

/**
 * Information about the creator of the space that the event is related to, as well as the date it was created.
 */
interface History {
  createdBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a space is created.

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:space:V2",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "space": {
    "id": 827392002,
    "key": "SP",
    "alias": "SP",
    "name": "Project: Sample Project",
    "icon": {
      "path": "/images/logo/default-space-logo-256.png",
      "width": 48,
      "height": 48,
      "isDefault": false
    },
    "type": "global",
    "status": "current",
    "history": {
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:29:20.501Z"
    }
  }
}
```
```

## Attachments

Forge apps can subscribe to the following attachment events:

* Created: `avi:confluence:created:attachment`
* Updated: `avi:confluence:updated:attachment`
* Viewed: `avi:confluence:viewed:attachment`
* Archived: `avi:confluence:archived:attachment`
* Unarchived: `avi:confluence:unarchived:attachment`
* Trashed: `avi:confluence:trashed:attachment`
* Restored: `avi:confluence:restored:attachment`
* Deleted: `avi:confluence:deleted:attachment`

Attachment events require the OAuth scope `read:confluence-content.summary` and share the same
payload format.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:attachment`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| suppressNotifications | `boolean` | Indicates whether notifications for this event were suppressed. |
| updateTrigger | `string` | Only for `avi:confluence:updated:attachment`. The reason that caused the update event to trigger. |
| attachment | `Attachment` | An object representing the attachment. |

### Type reference

```
```
1
2
```



```
interface Attachment {
  id: string;
  type: "attachment";
  status: "current" | "trashed" | "historical" | "archived";
  title: string;
  space: Space;
  history: History;
  version: Version;
  container: AttachmentContainer;
  extensions: Extensions;
}

/**
 * The space the attachment is located in.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
}

/**
 * Information about the creator and owner of the attachment or its container,
 * as well as the date it was created.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Information about the current version of the attachment or its container.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * The page, blog post or custom content the attachment is located in.
 */
interface AttachmentContainer {
  id: string;
  type: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  history: History;
  version: Version;
  space: Space;
}

/**
 * Represents an additional piece of information about the attachment.
 */
interface Extensions {
  mediaType: string;
  fileSize: number;
  mediaTypeDescription: string;
  fileId: string;
  downloadPath: string;
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when an attachment is created.

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:attachment",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "suppressNotifications": false,
  "attachment": {
    "id": "838205455",
    "type": "attachment",
    "status": "current",
    "title": "logo.png",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T07:10:41.070Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T08:35:00.100Z",
      "number": 1
    },
    "container": {
      "id": "838205441",
      "type": "page",
      "status": "current",
      "title": "A brand new page",
      "history": {
        "latest": true,
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "ownedBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:29:21.707Z"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "when": "2021-01-20T06:29:21.707Z",
        "number": 1
      }
    },
    "extensions": {
      "mediaType": "image/png",
      "fileSize": "3329",
      "mediaTypeDescription": "PNG Image",
      "fileId": "b23c8f6f-5b24-401f-9f97-3e83650d858e",
      "collectionName": "contentId-753665",
      "downloadPath": "https://example.atlassian.net/wiki/download/attachments/838205441/logo.png?version=5&cacheVersion=1&api=v2"
    }
  }
}
```
```

## Custom content

Forge apps can subscribe to the following custom content events:

* Created: `avi:confluence:created:custom_content`
* Updated: `avi:confluence:updated:custom_content`
* Permissions updated: `avi:confluence:permissions_updated:custom_content`
* Trashed: `avi:confluence:trashed:custom_content`
* Restored: `avi:confluence:restored:custom_content`
* Deleted: `avi:confluence:deleted:custom_content`

Custom content events are triggered when an action is performed on a Connect or Forge custom content.

Keep in mind that cascading deletion events aren’t emitted. For more information, see
[Cascading events guide](/platform/forge/events/#handling-cascading-events-in-confluence).

Custom content events require the OAuth scope `read:confluence-content.summary` and share the same payload format.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:custom_content`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| suppressNotifications | `boolean` | Indicates whether notifications for this event were suppressed. |
| updateTrigger | `string` | Only for `avi:confluence:updated:custom_content`. The reason that caused the update event to trigger. |
| content | `Content` | An object representing the custom content. |

### Type reference

```
```
1
2
```



```
interface Content {
  id: number;
  type: string; // Full Connect or Forge custom content type.
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  space: Space;
  history: History;
  container?: CustomContentContainer; // Absent for space-level custom content.
}

/**
 * The space the custom content is located in.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
}

/**
 * Information about the creator and owner of the custom content or its container, 
 * as well as the date it was created.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy: User;
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Information about the current version of the custom content.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * The page, blog post or another custom content this custom content is located in.
 */
interface CustomContentContainer {
  id: number;
  type: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  title: string;
  history: History;
  version: Version;
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents an image shown in the UI
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a Forge custom content is created as a child of a page.

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:custom_content",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:41.570Z",
  "suppressNotifications": false,
  "content": {
    "id": "838205552",
    "type": "forge:9149a1f2-9ed3-44ab-80e8-741adf4187fd:2edb9983-c665-4da2-a714-48572fb09cd0:my-custom-content",
    "status": "current",
    "title": "My custom content 001",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:29:41.070Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T06:29:41.070Z",
      "number": 1
    },
    "container": {
      "id": "838205441",
      "type": "page",
      "status": "current",
      "title": "A brand new page",
      "history": {
        "latest": true,
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "ownedBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:29:21.707Z"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "when": "2021-01-20T06:29:21.707Z",
        "number": 1
      }
    }
  }
}
```
```

## Labels

Forge apps can subscribe to the following label events:

* Created: `avi:confluence:created:label`
* Added: `avi:confluence:added:label`
* Removed: `avi:confluence:removed:label`
* Deleted: `avi:confluence:deleted:label`

Label events are triggered when a label is created, added to an entity, removed from an entity, or deleted.

A label can be associated with one of the following entities:

* Content (such as a page, blog post, database, etc.)
* Space
* Page template

Only one of the fields (`content`, `space`, or `template`) will be present in the event payload, depending on the
entity the label is associated with.

Label events require the following OAuth scopes:

* `read:confluence-content.summary`
* `read:confluence-space.summary`

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:added:label`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| label | `Label` | The label object. |
| content | `Content` | (Optional) The content the label is associated with. |
| space | `Space` | (Optional) The space the label is associated with. |
| template | `Template` | (Optional) The template the label is associated with. |

### Type reference

```
```
1
2
```



```
interface Label {
  id: string;
  name: string;
  prefix: string; // "global", "team", "my", etc.
}

interface Content {
  id: string;
  type: "page" | "blogpost" | "attachment" | "whiteboard" | "database" | "embed" | "folder";
  subType?: "live"; // Included only if "type" value is "page" and the page is a live doc
  title: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  space: Space;
  history: History;
  version: Version;
  labels: Label[]; // Existing labels on the content at the time of the event
}

interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
  history?: History; // Included only for space-level label events
  homepage?: Homepage; // Included only for space-level label events
  labels?: Label[]; // Existing labels on the space at the time of the event. Included only for space-level label events.
}

interface Template {
  templateId: string;
  name: string;
  description: string;
  templateType: "page" | "blueprint";
  space?: Space; // Included only for space-level page templates (as opposed to global templates)
  labels: Label[]; // Existing labels on the template at the time of the event
}

interface History {
  latest: boolean;
  createdBy: User;
  ownedBy?: User; // Included only for content-level label events
  createdDate: string;
}

interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

interface Homepage {
  id: string;
  type: "page";
  title: string;
  status: "current" | "archived";
}

interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a label is added to a live doc:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:added:label",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "label": {
    "id": "123456789",
    "name": "example-label",
    "prefix": "global"
  },
  "content": {
    "id": "838205441",
    "type": "page",
    "subType": "live",
    "title": "A brand new page",
    "status": "current",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "history": {
      "latest": true,
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "ownedBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:29:21.707Z"
    },
    "version": {
      "by": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "when": "2021-01-20T06:29:21.707Z",
      "number": 1
    },
    "labels": [
      {
        "id": "123456701",
        "name": "existing-label-1",
        "prefix": "global"
      },
      {
        "id": "123456702",
        "name": "existing-label-2",
        "prefix": "team"
      }
    ]
  }
}
```
```

### Example

This is an example of an event triggered when a label is added to a space:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:added:label",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "label": {
    "id": "123456789",
    "name": "example-label",
    "prefix": "global"
  },
  "space": {
    "id": 827392002,
    "key": "SP",
    "alias": "SP",
    "name": "Project: Sample Project",
    "icon": {
      "path": "/images/logo/default-space-logo-256.png",
      "width": 48,
      "height": 48,
      "isDefault": false
    },
    "type": "global",
    "status": "current",
    "history": {
      "createdBy": {
        "type": "known",
        "username": "4ad9aa0c52dc1b420a791d12",
        "accountId": "4ad9aa0c52dc1b420a791d12",
        "accountType": "atlassian",
        "email": "4ad9aa0c52dc1b420a791d12",
        "publicName": "4ad9aa0c52dc1b420a791d12",
        "profilePicture": {
          "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "displayName": "4ad9aa0c52dc1b420a791d12",
        "isExternalCollaborator": false
      },
      "createdDate": "2021-01-20T06:28:20.501Z"
    },
    "homepage": {
      "id": "827392004",
      "type": "page",
      "title": "SP Home",
      "status": "current"
    },
    "labels": [
      {
        "id": "123456701",
        "name": "existing-label-1",
        "prefix": "global"
      },
      {
        "id": "123456702",
        "name": "existing-label-2",
        "prefix": "team"
      }
    ]
  }
}
```
```

### Example

This is an example of an event triggered when a label is added to a space-level page template:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:added:label",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "label": {
    "id": "123456789",
    "name": "example-label",
    "prefix": "global"
  },
  "template": {
    "templateId": "123456789",
    "name": "Example Template",
    "description": "A template for demonstration purposes.",
    "templateType": "page",
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current"
    },
    "labels": [
      {
        "id": "123456701",
        "name": "existing-label-1",
        "prefix": "global"
      },
      {
        "id": "123456702",
        "name": "existing-label-2",
        "prefix": "team"
      }
    ]
  }
}
```
```

## Users

Forge apps can subscribe to the following user events:

* Created: `avi:confluence:created:user`
* Deleted: `avi:confluence:deleted:user`

User events are triggered when a user is created or deleted in Confluence.

User events require the OAuth scope `read:confluence-user`.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:user`. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| user | `User` | Object representing the user that was created or deleted. |

Note that `atlassianId` field is not included in the payload because user events are triggered via
an asynchronous process.

### Type reference

```
```
1
2
```



```
/**
 * Represents a user
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}
```
```

### Example

This is an example of an event triggered when a user is created:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:user",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "user": {
    "type": "known",
    "username": "4ad9aa0c52dc1b420a791d12",
    "accountId": "4ad9aa0c52dc1b420a791d12",
    "accountType": "atlassian",
    "email": "4ad9aa0c52dc1b420a791d12",
    "publicName": "4ad9aa0c52dc1b420a791d12",
    "profilePicture": {
      "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
      "width": 48,
      "height": 48,
      "isDefault": false
    },
    "displayName": "4ad9aa0c52dc1b420a791d12",
    "isExternalCollaborator": false
  }
}
```
```

## Groups

Forge apps can subscribe to the following group events:

* Created: `avi:confluence:created:group`
* Deleted: `avi:confluence:deleted:group`

Group events are triggered when a group is created or deleted in Confluence.

Group events require the OAuth scope `read:confluence-groups`.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:group`. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| group | `Group` | Object representing the group that was created or deleted. |

Note that `atlassianId` field is not included in the payload because group events are triggered via
an asynchronous process.

### Type reference

```
```
1
2
```



```
interface Group {
  id: string;
  name: string;
}
```
```

### Example

This is an example of an event triggered when a group is created:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:group",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "group": {
    "id": "ab1a3479-143a-456e-8853-d359e577863a",
    "name": "example-group"
  }
}
```
```

## Relations

Forge apps can subscribe to the following relation events:

* Created: `avi:confluence:created:relation`
* Deleted: `avi:confluence:deleted:relation`

Relation events are triggered when a relationship between two entities (source and target) is created or deleted
in Confluence. The following entities are allowed to be in a relationship:

* As a source: Content, Space, User
* As a target: Content, Space

Relation events require the following OAuth scopes:

* `read:confluence-content.summary`
* `read:confluence-space.summary`
* `read:confluence-user`

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:created:relation`. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| relationName | `string` | Name of the relation. |
| relationData | `RelationData` | (Optional) Information about a user who created the relationship and the date and time of the creation. Absent for relation types `like` and `favourite`. |
| source | `EntityWrapper` | Wrapper for the source entity. Depending on the relationship type, contains one of the following subfields: `content`, `space`, or `user`. |
| target | `EntityWrapper` | Wrapper for the target entity. Depending on the relationship type, contains one of the following subfields: `content`, `space`, or `user`. |

### Type reference

```
```
1
2
```



```
/**
 * Information about the user who created the relationship and the date and time of the creation.
 */
interface RelationData {
  createdBy: User;
  createdDate: string;  // Date and time in ISO 8601 format.
}

/**
 * Wrapper for the source or target entity.
 * Only one of the following fields may be present at the same time: 'content', 'space', or 'user'.
 */
interface EntityWrapper {
  content?: Content;
  space?: Space;
  user?: User;
}

/**
 * Represents content.
 */
interface Content {
  id: string;
  type: "page" | "blogpost" | "attachment" | "whiteboard" | "database" | "embed" | "folder";
  subType?: "live"; // Included only if "type" value is "page" and the page is a live doc
  title: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
  space: Space;
  history: History;
  version: Version;
}

/**
 * Represents a space.
 */
interface Space {
  id: number;
  key: string;
  alias: string;
  name: string;
  type: "global" | "personal";
  icon: Image;
  status: "current" | "archived";
  history?: History; // Included only if a space is a source or target entity
  homepage?: Homepage; // Included only if a space is a source or target entity
}

/**
 * Represents a user.
 *
 * Note that personally identifiable information (username, email,
 * publicName, and displayName) is populated with the accountId instead
 * for privacy reasons.
 */
interface User {
  type: "known" | "unknown" | "anonymous" | "user";
  username: string;
  accountId: string;
  accountType: "atlassian" | "app";
  email: string;
  profilePicture: Image;
  displayName: string;
  publicName: string;
  isExternalCollaborator: boolean;
}

/**
 * Represents content or space history.
 */
interface History {
  latest: boolean;
  createdBy: User;
  ownedBy?: User; // Included only for content history
  createdDate: string; // Date and time in ISO 8601 format.
}

/**
 * Represents a content version.
 */
interface Version {
  by: User;
  when: string; // Date and time in ISO 8601 format.
  number: number;
}

/**
 * Represents a home page of a space.
 */
interface Homepage {
  id: string;
  type: "page";
  title: string;
  status: "current" | "trashed" | "historical" | "draft" | "archived";
}

/**
 * Represents an image shown in the UI.
 */
interface Image {
  path: string;
  width: number;
  height: number;
  isDefault: boolean;
}
```
```

### Example

This is an example of an event triggered when a User-to-Content relationship is created:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:created:relation",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:21.970Z",
  "relationName": "watching",
  "relationData": {
    "createdBy": {
      "type": "known",
      "username": "4ad9aa0c52dc1b420a791d12",
      "accountId": "4ad9aa0c52dc1b420a791d12",
      "accountType": "atlassian",
      "email": "4ad9aa0c52dc1b420a791d12",
      "publicName": "4ad9aa0c52dc1b420a791d12",
      "profilePicture": {
        "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "displayName": "4ad9aa0c52dc1b420a791d12",
      "isExternalCollaborator": false
    },
    "createdDate": "2021-01-20T06:29:21.970Z"
  },
  "source": {
    "user": {
      "type": "known",
      "username": "4ad9aa0c52dc1b420a791d12",
      "accountId": "4ad9aa0c52dc1b420a791d12",
      "accountType": "atlassian",
      "email": "4ad9aa0c52dc1b420a791d12",
      "publicName": "4ad9aa0c52dc1b420a791d12",
      "profilePicture": {
        "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "displayName": "4ad9aa0c52dc1b420a791d12",
      "isExternalCollaborator": false
    }
  },
  "target": {
    "content": {
      "id": "838205441",
      "type": "page",
      "subType": "live",
      "title": "A brand new page",
      "status": "current",
      "space": {
        "id": 827392002,
        "key": "SP",
        "alias": "SP",
        "name": "Project: Sample Project",
        "icon": {
          "path": "/images/logo/default-space-logo-256.png",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "type": "global",
        "status": "current"
      },
      "history": {
        "latest": true,
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "ownedBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:29:21.707Z"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "when": "2021-01-20T06:29:21.707Z",
        "number": 1
      }
    }
  }
}
```
```

### Example

This is an example of an event triggered when a Content-to-Space relationship is deleted:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:deleted:relation",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "eventCreatedDate": "2021-01-20T06:29:41.070Z",
  "relationName": "summary",
  "relationData": {
    "createdBy": {
      "type": "known",
      "username": "4ad9aa0c52dc1b420a791d12",
      "accountId": "4ad9aa0c52dc1b420a791d12",
      "accountType": "atlassian",
      "email": "4ad9aa0c52dc1b420a791d12",
      "publicName": "4ad9aa0c52dc1b420a791d12",
      "profilePicture": {
        "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "displayName": "4ad9aa0c52dc1b420a791d12",
      "isExternalCollaborator": false
    },
    "createdDate": "2021-01-20T06:29:21.970Z"
  },
  "source": {
    "content": {
      "id": "838205441",
      "type": "page",
      "subType": "live",
      "title": "A brand new page",
      "status": "current",
      "space": {
        "id": 827392002,
        "key": "SP",
        "alias": "SP",
        "name": "Project: Sample Project",
        "icon": {
          "path": "/images/logo/default-space-logo-256.png",
          "width": 48,
          "height": 48,
          "isDefault": false
        },
        "type": "global",
        "status": "current"
      },
      "history": {
        "latest": true,
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "ownedBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:29:21.707Z"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "when": "2021-01-20T06:29:21.707Z",
        "number": 1
      }
    }
  },
  "target": {
    "space": {
      "id": 827392002,
      "key": "SP",
      "alias": "SP",
      "name": "Project: Sample Project",
      "icon": {
        "path": "/images/logo/default-space-logo-256.png",
        "width": 48,
        "height": 48,
        "isDefault": false
      },
      "type": "global",
      "status": "current",
      "homepage": {
        "id": "827392004",
        "type": "page",
        "title": "SP Home",
        "status": "current"
      },
      "history": {
        "createdBy": {
          "type": "known",
          "username": "4ad9aa0c52dc1b420a791d12",
          "accountId": "4ad9aa0c52dc1b420a791d12",
          "accountType": "atlassian",
          "email": "4ad9aa0c52dc1b420a791d12",
          "publicName": "4ad9aa0c52dc1b420a791d12",
          "profilePicture": {
            "path": "/wiki/aa-avatar/4ad9aa0c52dc1b420a791d12",
            "width": 48,
            "height": 48,
            "isDefault": false
          },
          "displayName": "4ad9aa0c52dc1b420a791d12",
          "isExternalCollaborator": false
        },
        "createdDate": "2021-01-20T06:28:20.501Z"
      }
    }
  }
}
```
```

## Search

Forge apps can subscribe to the following search events:

* Performed: `avi:confluence:performed:search`

Search events are triggered after Confluence search results are returned for the search query.

Search events require the following OAuth scopes:

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:confluence:performed:search`. |
| eventCreatedDate | `string` | Date and time of the event in ISO 8601 format. |
| atlassianId | `string` | The ID of the user that caused the event. Absent if the event was triggered by an anonymous user. |
| query | `string` | The search query string. |
| accountType | `string` | The type of account of the User who performed the search. |
| results | `integer` | The number of search results returned. |

### Example

This is an example of an event triggered when a user performs a Confluence search:

```
```
1
2
```



```
{
  "eventType": "avi:confluence:performed:search",
  "eventCreatedDate": "2021-01-20T06:29:21.907Z",
  "atlassianId": "4ad9aa0c52dc1b420a791d12",
  "query": "test search",
  "accountType": "atlassian",
  "results": 2
}
```
```
