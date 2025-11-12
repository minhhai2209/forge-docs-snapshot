# User privacy guide for app developers

This guide describes how app developers can comply with user privacy requirements, as detailed
by the [General Data Protection Regulation (GDPR)](https://ec.europa.eu/commission/priorities/justice-and-fundamental-rights/data-protection/2018-reform-eu-data-protection-rules_en).
On this page, you'll find information on your responsibilities as an app developer for Atlassian and
instructions on how to meet these responsibilities.

In addition to this guide, you should read
[Data privacy guidelines](/platform/marketplace/data-privacy-guidelines/) for general guidelines on
user privacy and Marketplace apps.

## GDPR responsibilities for app developers

The GDPR governs the processing of personal data of individuals by an individual, company, or organization.
As an app developer, you must ensure that your apps comply with the GDPR when handling the personal data
for users. This includes:

* [Right to erasure](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/)
  (also known as *Right to be Forgotten*): If your app stores the personal data for a user and the user
  requests for their data to be erased, your app must erase the data.
* [Right to rectification](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-rectification/):
  If your app stores the personal data for a user and the user changes their data, your app must
  either erase or update the data.
* [Right to be informed](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-be-informed):
  You must inform users if you collect and use their personal data.

In order to comply with these requirements, **we recommend that your apps do not store any user personal
data** and always retrieve current user data at the time of use using Atlassian APIs. This is the
simplest and most reliable solution, as you don't need to worry about managing and reporting user
personal data for your apps. If you choose this approach, you don't need to read the rest of this guide.

However, if you choose to store user personal data with your apps, Atlassian has built the following
capabilities to help you comply with the GDPR:

* The new *Personal data reporting API* lets you report the user accounts that your apps are storing
  personal data for.
* The reported data is made available to every user on their Atlassian Account profile, so that they
  can see which apps are storing their personal data.
* For each user account reported, the *Personal data reporting API* returns whether each user's personal
  data must be erased or refreshed. You must erase or refresh the personal data for your apps accordingly.

Read the following sections on [reporting data](#reportingdata) and [storing data](#storingdata) to
learn how to use these capabilities.

## Reporting user personal data for your apps

As an app developer, you are required to periodically report the user personal data that your apps are
storing. You must report each `accountId`, which is a short hand reference to an Atlassian Account ID.
An `accountId` uniquely identifies a user across all Atlassian apps. An `accountID` is 1-128 characters
long, and may contain alphanumeric characters, as well as `-` and `:` characters.

You must
use `accountIds` to report personal data usage, even if the API permits other identifiers.

At a high level, this is how to do reporting for your apps:

1. Compile the list of user accounts that your apps are storing personal data for.
2. Use the polling resources for the *Personal data reporting API* to report the
   user accounts for your apps. See the [reference documentation](#reportingapi) below for details.
3. Based on the response, you may need to update or erase the personal data for users accordingly.
4. Repeat this process each cycle period. By default, the cycle period is every
   **7 days**.

The cycle period defines the required period of time between sending reports for a given `accountId`.
You can think about it as the maximum allowable staleness of the reported data that is stored by Atlassian.

By default, the cycle period is **7 days**.

However, the polling resources may return a different cycle
period (in the `Cycle-Period` header) that you must follow instead.

You should not send reports more frequently than the cycle period for each `accountId`.

When setting up reporting for your apps, also consider the following recommendations:

* **Understand your reporting obligations**: All apps storing personal data must report user personal data,
  using the *Personal data reporting API*.  
  Your apps do not need to report when they proactively erase personal data for a user.
  Atlassian will apply a time to live (TTL) on the data reported by apps. This means an app may be
  listed in a user's profile for some period after the app has ceased storing personal data for that user.
* **Cater for interruptions**: The polling iteration period is the period over which an app will iterate
  over all the accountIds to send reports for personal data usage. The longer the polling iteration period,
  the more likely the polling will be interrupted by events, such as server restarts and app updates.  
  This means that apps need to keep track of where they are within a poll period and have
  a means of resuming a poll cycle from this information. If this is too complex to implement, consider
  using a shorter polling iteration period instead.
* **Schedule around potential conflicts**: Consider that scheduled actions by apps generally take place
  at particular times of the day, such as midnight or at the top of each hour. Don't schedule polling
  requests for your apps for specific times, so that there are not conflicts with other apps.
* **Handle account additions and deletions**: The iteration logic for your apps must handle account
  additions and deletions. This will mean adjusting the polling rate and/or batch sizes.

### Note about reporting personal data storage

* In various locations throughout the Jira Cloud REST APIs (all Atlassian apps), an account ID of
  *unknown* may be returned. Apps should not attempt to retrieve and store personal data for the
  account *unknown*, nor should they include *unknown* in the accounts when reporting personal
  data storage.

## Storing user personal data for your apps

In addition to reporting user personal data for your apps, you must ensure that you are storing user
personal data for your apps correctly:

* **Track the age of personal data**: Apps must track the age of the personal data retrieved from Atlassian.
  This must be sent in reports so that Atlassian can determine if the personal data is stale. If an
  app stores multiple aspects of personal data for an account, the age must correspond
  to the oldest time that the personal data was retrieved at.
* **Store a single copy of personal data**: It is imperative that apps are able to report personal
  data usage accurately and reliably. To ensure that all personal data is erased when necessary, we
  recommend that the app only stores a single copy of the personal data within this address
  space, and retrieves it when necessary. The obvious choice for an address space is a persistent store,
  such as a database table that supports efficient querying by accountId.
* **Erase personal data when uninstalled**: When an app is uninstalled, the app should erase personal data that is no longer needed.

## Testing

The following accountIds should be used by partners for testing:

* Active: `5be24ad8b1653240376955d2`
* Closed: `5be24ba3f91c106033269289`

There is no fixed accountId that can be used to test for the *updated* case.

### Invalid API calls and regression testing

Atlassian will be monitoring correct usage of the API detailed in this guide.
For example, our systems will detect the case of apps repeatedly checking the status
of a closed account beyond a reasonable time frame.
For this reason, repeated/regression testing of the closed account should only be done
using the closed test account provided above since we have added this accountid to the blocklist
from our anomaly detection logic.

## Personal data reporting API reference

The *personal data reporting API* is a RESTful API that allows apps to report the user accounts
for which they are storing personal data. For flexibility and efficiency, the API allows multiple
accounts to be reported on in a single request.

`POST https://api.atlassian.com/app/report-accounts/`

This endpoint is used by apps to report a list of user accounts, and returns information on whether
the personal data for each account needs to be updated or erased.

### Parameters

This operation has no parameters.

### Request

Content type: *application/json*

Each request allows up to 90 accounts to be reported on. For each account, the
`accountId` and time that the personal data was retrieved must be provided. The time format is
defined by
[RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6).

Example request (*application/json*):

```
```
1
2
```



```
{
"accounts": [{
    "accountId": "account-id-a",
    "updatedAt": "2018-10-25T23:08:51.382Z"
  }, {
    "accountId": "account-id-b",
    "updatedAt": "2018-10-25T23:14:44.231Z"
  }, {
    "accountId": "account-id-c",
    "updatedAt": "2018-12-01T02:44:21.020Z"
  }]
}
```
```

### Responses

* `200` (*application/json*): The request is successful and one or
  more personal data erasure actions are required.

  The information is contained in an `accounts` array, where:

  * each object identifies the `accountId`, and
  * whether the reason for the erasure is due to the closure of the account, or
    the app's copy of personal data has been invalidated due to the some update.

  In the case of the latter, the app is permitted to request personal data again.

  Example response (*application/json*):

  ```
  ```
  1
  2
  ```



  ```
  {
    "accounts": [{
      "accountId": "account-id-a",
      "status": "closed"
    }, {
      "accountId": "account-id-c",
      "status": "updated"
    }]
  }
  ```
  ```
* `204`: The request was successful and the app has no action to take for the
  accounts sent in the request.
* `400`: The request was malformed in some way. The response body contains
  an error message.

  Example response (*application/json*):

  ```
  ```
  1
  2
  ```



  ```
  {
    "errorType": "string",
    "errorMessage": "string"
  }
  ```
  ```
* `429`: Rate limiting applies. Delay by the time period is specified in the `Retry-After` header (in seconds)
  before making the API call again.
* `500`: An internal server error occurred. The response body contains an error message.

  Example response (*application/json*):

  ```
  ```
  1
  2
  ```



  ```
  {
    "errorType": "string",
    "errorMessage": "string"
  }
  ```
  ```
* `503`: The service is unavailable.

## Building your GDPR flow on Forge

The Forge modules and APIs available to you today can be combined together to provide GDPR capabilities
on top of the **Forge platform**. How these pieces are composed will likely depend on the situation
that your app is in, in regards to infrastructure and where the data is being stored.

### Sample implementation

We include a sample implementation [here](https://bitbucket.org/atlassian/forge-gdpr-polling-example/src/master/).

This targets the use case where personal data is only being stored in Forge storage or Atlassian app entity properties.

We use the following:

We assume data is being stored in Forge storage with the following shape:

```
```
1
2
```



```
interface Account {
    references: string[];
    accountId: string;
    displayName: string;
    emailAddress: string;
    updatedAt?: string;
}
```
```

This data is stored with an `account:${accountId}` key format, allowing us to retrieve all accounts
by finding all of the keys starting with `account:`

### Scheduled triggers

Forge includes the ability to schedule work at regular intervals using
[scheduled triggers](/platform/forge/manifest-reference/modules/scheduled-trigger/).
In the example above, we combine both a weekly and an hourly schedule to implement the flow.

#### Weekly schedule

The weekly schedule essentially performs an extract, transform, and load operation.

On a weekly cadence, the trigger fires and searches for all accounts present in Forge storage.
It then processes the accounts using the polling API to determine which ones to delete and to update.
These accounts are then put into an account processing "queue" built over the top of Forge's storage
mechanism.

We provide a sample queue implementation [here](https://bitbucket.org/atlassian/forge-gdpr-polling-example/src/master/src/queue.ts).

In the future, this should be replaced by a Forge solution to background processing, which is
being tracked on the [FRGE-242 ticket](https://ecosystem.atlassian.net/browse/FRGE-242).

#### Hourly schedule

The hourly schedule is used to perform account update or deletion operations, based on the results
of the weekly schedule.

### Alternative implementations

The implementation above combines the extraction of Atlassian accounts and their processing into one
call. You may find this is infeasible for your app, either due to the particular data shape in storage
or due to the nature of your app. These operations can be split apart - for example, maintaining
a list of all the `accountIds` you store in another storage entry that is processed by the weekly
schedule against the polling API.

### What if I store data outside of Atlassian?

If you are storing or processing data outside of Atlassian, we assume you have external infrastructure
available to help implement this flow (or can provision it as required).

While the examples above extract the list of accounts from Forge storage, the same sort of extraction
could be performed on external data stores using tooling, such as a cron job. This could be used
to generate a list of accounts that are fetched by the weekly schedule and then processed within
the Forge app.
