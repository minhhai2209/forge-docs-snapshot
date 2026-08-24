# CreateIssueModal

While subtask issue type is not supported now, it may be added in the future.

The `CreateIssueModal` class enables your Custom UI app to open an issue create modal pre-filled with data you supply.

## Class signature

```
1interface CreateIssueModalOptions {
2  context?: {
3    projectId?: string;
4    issueTypeId?: string;
5    requestType?: string;
6    parentId?: string;
7    summary?: string;
8    description?: Record<string, any>;
9    environment?: Record<string, any>;
10    assignee?: string;
11    reporter?: string;
12    labels?: string[];
13    duedate?: string;
14    priority?: string;
15    components?: string[];
16    versions?: string[];
17    fixVersions?: string[];
18    [customFieldKey: string]: any;
19  };
20  onClose?: (args: {
21    payload: {
22      issueId: string;
23    }[];
24  }) => void;
25}
26
27class CreateIssueModal {
28  constructor(opts?: CreateIssueModalOptions);
29  open(): Promise<void>;
30}
31
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
    customfield_10028: '2026-05-12T09:34:48',
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
