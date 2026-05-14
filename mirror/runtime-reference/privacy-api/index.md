# Privacy API

Forge Privacy API provides functions to help app developers comply with Atlassian's [user privacy requirements](/platform/forge/user-privacy-guidelines/).

Import the Privacy API package in your app, as follows:

```
1
import { privacy } from '@forge/api';
```

The `reportPersonalData` function returns updates on whether a user account needs to be updated or erased. This helper function calls the 3LO [/report-accounts](https://developer.atlassian.com/cloud/jira/platform/user-privacy-developer-guide/#report-accounts-for-oauth-2-0-authorization-code-grants--3lo--apps) endpoint and handles requests with more than 90 accounts.

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
const updates = await privacy.reportPersonalData([
  {
    accountId: 'account-id-a',
    updatedAt: '2018-10-25T23:08:51.382Z'
  },
  {
    accountId: 'account-id-b',
    updatedAt: '2018-10-25T23:14:44.231Z'
  },
  {
    accountId: 'account-id-c',
    updatedAt: '2018-12-01T02:44:21.020Z'
  }
]);

console.log(updates)
// [{
//   "accountId": "account-id-a",
//   "status": "closed"
// },
// {
//   "accountId": "account-id-c",
//   "status": "updated"
// }]
```

## Method signature

```
```
1
2
```



```
reportPersonalData(
  accounts: Array<{ accountId: string; updatedAt: string }>
) => Promise<Array<{ accountId: string; status: 'updated' | 'closed' }>>;
```
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `accounts` | `Array<{ accountId: string; updatedAt: string }>` | A list of the accounts to get updates for. Returns updates to the account after the `updatedAt` time. |
