# Privacy API

Forge Privacy API provides functions to help app developers comply with Atlassian's [user privacy requirements](/platform/forge/user-privacy-guidelines/).

Import the Privacy API package in your app, as follows:

```
1import { privacy } from '@forge/api';
2
```

The `reportPersonalData` function returns updates on whether a user account needs to be updated or erased. This helper function calls the 3LO [/report-accounts](https://developer.atlassian.com/cloud/jira/platform/user-privacy-developer-guide/#report-accounts-for-oauth-2-0-authorization-code-grants--3lo--apps) endpoint and handles requests with more than 90 accounts.

```
1const updates = await privacy.reportPersonalData([
2  {
3    accountId: 'account-id-a',
4    updatedAt: '2018-10-25T23:08:51.382Z'
5  },
6  {
7    accountId: 'account-id-b',
8    updatedAt: '2018-10-25T23:14:44.231Z'
9  },
10  {
11    accountId: 'account-id-c',
12    updatedAt: '2018-12-01T02:44:21.020Z'
13  }
14]);
15
16console.log(updates)
17// [{
18//   "accountId": "account-id-a",
19//   "status": "closed"
20// },
21// {
22//   "accountId": "account-id-c",
23//   "status": "updated"
24// }]
25
```

## Method signature

```
```
1
2
3
4
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
