# Jira Software events

Forge apps can subscribe to Jira Software events for:

Your Forge app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

## Board events

You can subscribe to the following Jira Software board events in Forge apps:

### Board created, updated, deleted

An event with the name `avi:jira-software:created:board` / `avi:jira-software:updated:board` / `avi:jira-software:deleted:board` is sent when a board is `created` / `updated` / `deleted` respectively.

Keep in mind that cascading events for deleted boards are not emitted.
  
For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`, `read:jira-user`

**Granular**: `read:board-scope:jira-software`, `read:issue-details:jira`, `read:project:jira`, `read:user:jira`

The payload for all of these events is the same.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI, one of: `avi:jira-software:created:board`, `avi:jira-software:updated:board`, `avi:jira-software:deleted:board`. |
| board | `Board` | The board the event relates to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

#### Type reference

```
```
1
2
```



```
interface Board {
    id: string;
    name: string;
    type: "simple" | "scrum" | "kanban";
}
```
```

#### Example

This is an example of a payload for a newly created board.

```
```
1
2
```



```
{
  "eventType": "avi:jira-software:created:board",
  "board": {
    "id": 11,
    "name": "Some SCRUM board",
    "type": "scrum"
  },
  "atlassianId": "5c37e3bdb393bf4ce95658d5"
}
```
```

### Board configuration changed

An event with the name `avi:jira-software:configuration-changed:board` is sent when board configuration is changed.

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`, `read:jira-user`

**Granular**: `read:board-scope.admin:jira-software`, `read:project:jira`, `read:user:jira`

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI: `avi:jira-software:configuration-changed:board`. |
| configuration | `Board configuration` | The configuration of board the event relates to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

#### Type reference

```
```
1
2
```



```
interface Configuration {
    id: number; // id of the board
    name: string; // name of the board
    type: "simple" | "scrum" | "kanban";
    location?: Location;
    filter: Filter;
    subQuery?: Subquery;
    columnConfig: ColumnConfig;
    estimation?: Estimation;
    ranking: Ranking;
}

interface Location {
    type: "project" | "user";
    id: string;
    key?: string;
    name?: string;
}

interface Filter {
    id: string;
}

interface Subquery {
    query: string;
}

interface ColumnConfig {
    constraintType: "none" | "issueCount" | "issueCountExclSubs";   
    columns: Column[];
}

interface Column {
    name: string;
    statuses: Status[];
    min?: number;
    max?: number;
}

interface Status {
    id: string;
}

interface Estimation {
    type: string;
    field: EstimationField;
}

interface EstimationField {
    fieldId: string;
    displayName: string;
}

interface Ranking {
    rankCustomFieldId?: number;
}
```
```

#### Example

This is an example of a payload for changing configuration for a board.

```
```
1
2
```



```
{
  "eventType": "avi:jira-software:configuration-changed:board",
  "configuration": {
    "id": 11,
    "name": "CMPSCRUM board",
    "type": "scrum",
    "location": {
      "type": "project",
      "key": "CMPSCRUM",
      "id": "10005",
      "name": "cmpscrum"
    },
    "filter": {
      "id": "10007"
    },
    "columnConfig": {
      "columns": [
        {
          "name": "To Do",
          "statuses": [
            {
              "id": "10006"
            }
          ]
        },
        {
          "name": "In Progress",
          "statuses": [
            {
              "id": "3"
            }
          ]
        },
        {
          "name": "Done",
          "statuses": [
            {
              "id": "10007"
            }
          ]
        }
      ],
      "constraintType": "none"
    },
    "estimation": {
      "type": "field",
      "field": {
        "fieldId": "customfield_10214",
        "displayName": "Story Points"
      }
    },
    "ranking": {
      "rankCustomFieldId": 10019
    }
  },
  "atlassianId": "655363:f4dec1e8-6b1a-48aa-a9bf-e03d10b4abba"
}
```
```

## Sprint events

You can subscribe to the following Jira Software sprint events in Forge apps:

* Sprint created: `avi:jira-software:created:sprint`
* Sprint started: `avi:jira-software:started:sprint`
* Sprint updated: `avi:jira-software:updated:sprint`
* Sprint closed: `avi:jira-software:closed:sprint`
* Sprint deleted: `avi:jira-software:deleted:sprint`

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular**: `read:sprint:jira-software`

The payload for all of these events is the same.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event AVI. |
| sprint | `Sprint` | The sprint the event is related to. |
| oldValue? | `Sprint` | [Optional] The sprint values from before the change. Present for the sprint updated event. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

#### Type reference

```
```
1
2
```



```
interface Sprint {
    id: string;
    originBoardId?: string;
    name: string; // limited to 30 characters
    goal?: string; // limited to 10000 characters
    state: string;
    createDate?: string;
    startDate?: string;
    endDate?: string;
    completeDate?: string;
}
```
```

#### Examples

This is an example of a payload for a sprint update:

```
```
1
2
```



```
{
  "eventType": "avi:jira-software:updated:sprint",
  "sprint": {
    "id": "6",
    "originBoardId": "12",
    "name": "EX1 Sprint 1",
    "goal": "The new goal",
    "state": "future",
    "createDate": "2024-09-24T10:59:20.334+0200",
    "startDate": "2024-10-05T00:00:00.000+0200",
    "endDate": "2024-10-12T00:00:00.000+0200"
  },
  "oldValue": {
    "goal": "The goal",
    "startDate": "2024-10-03T00:00:00.000+0200",
    "endDate": "2024-10-05T00:00:00.000+0200"
  },
  "atlassianId": "5c37e3bdb393bf4ce95658d5"
}
```
```
