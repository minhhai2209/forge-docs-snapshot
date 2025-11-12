# CreateIssueModal

While subtask issue type is not supported now, it may be added in the future.

The `CreateIssueModal` class enables your Custom UI app to open an issue create modal pre-filled with data you supply.

## Class signature

```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
interface CreateIssueModalOptions {
  context?: {
    projectId?: string;
    issueTypeId?: string;
    requestType?: string;
    parentId?: string;
    summary?: string;
    description?: Record<string, any>;
    environment?: Record<string, any>;
    assignee?: string;
    reporter?: string;
    labels?: string[];
    duedate?: string;
    priority?: string;
    components?: string[];
    versions?: string[];
    fixVersions?: string[];
    [customFieldKey: string]: any;
  };
  onClose?: (args: {
    payload: {
      issueId: string;
    }[];
  }) => void;
}

class CreateIssueModal {
  constructor(opts?: CreateIssueModalOptions);
  open(): Promise<void>;
}
```

## Arguments

* **onClose**: A callback function that runs when the issue create modal is closed.
  The function is called with a list of the issues created.
* **context**: Custom context that contains fields to pre-fill when the issue create modal opens.

The `description` and `environment` fields must be in an [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/).

## Example

This example shows how to open an issue create modal with pre-filled fields.

```
```
1
2
```



```
import { CreateIssueModal } from '@forge/jira-bridge';

const createIssueModal = new CreateIssueModal({
  onClose: (payload) => {
    console.log('CreateIssueModal is closed with', payload);
  },
  context: {
    projectId: '10114',
    issueTypeId: '10004',
    requestType: 'jism/newaccount',
    parentId: '10152', // epic id
    summary: 'Issue summary',
    description: { version: 1, type: "doc", content: [] },
    environment: { version: 1, type: "doc", content: [] },
    assignee: '5cfa7fca3fa1890e7f17075e',
    reporter: '5cfa7fca3fa1890e7f17075e',
    labels: ['label-one', 'label-two'],
    duedate: '2022-02-28',
    priority: '2',
    components: ['10294', '10295'],
    versions: ['10039'],
    fixVersions: ['10039'],
    customfield_10010: 'custom value', 
  },
});

createIssueModal.open();
```
```

### Custom fields pre-filling

#### Group fields

Use group ID, for instance `{"customfield_10061": "30cf4713-876b-4a49-a40b-fba48fcc806a"}`.

#### User fields

Use account ID, full name or user email. For instance `{"customfield_10062": "712020:7b6adff9-f903-4e45-a25e-b3595df3d9fc"}` or `{"customfield_10062": "John Smith"}` or `{"customfield_10062": "john.smith@example.com"}`.

## Supported modules

`CreateIssueModal` can be used in these modules:
