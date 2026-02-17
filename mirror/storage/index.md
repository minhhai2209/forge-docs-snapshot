# Storage

Forge provides three options for storing app data: Forge-hosted storage, Atlassian app REST APIs (for example, Jira or Confluence), and remote storage that you manage. Use these options to persist and retrieve data securely, at the scale your app needs.

## Forge Hosted Storage

Store your app data with Forge Storage so you can focus on solving customer problems instead of managing infrastructure.

### Start building your storage

Consider data shape and size limits when selecting the storage option that best fits your use case.

| API | Overview | Ideal for |
| --- | --- | --- |
| [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) | Simple storage for key/value pairs | User preferences, app configuration, simple data storage |
| [Custom entities store](/platform/forge/storage-reference/storage-api-custom-entities/) | Structured data storage with custom entities and query capabilities | Complex data structures, queryable data, relationships between entities |
| [SQL](/platform/forge/storage-reference/sql/) | Fully managed relational database | Complex data models, relationships, transactions, advanced queries |
| [Object Store (EAP)](/platform/forge/storage-reference/object-store/) | Large file and media storage | Binary data, files, media, large objects |

See [platform quotas and limits](/platform/forge/platform-quotas-and-limits/) and [storage options](/platform/forge/runtime-reference/storage-api/) for more details.

### Example code

Explore these code examples to see how to perform common storage operations with each Forge storage option.

Key-Value Store

Custom Entity Store

SQL

Object Store (EAP)

```
```
1
2
```



```
import { kvs } from '@forge/kvs';

// Store user preferences
export async function saveUserPreferences(userId, preferences) {
  await kvs.set(`user:${userId}:preferences`, preferences);
}

// Retrieve user preferences
export async function getUserPreferences(userId) {
  return await kvs.get(`user:${userId}:preferences`);
}

// Delete user preferences
export async function deleteUserPreferences(userId) {
  await kvs.delete(`user:${userId}:preferences`);
}
```
```

### Tutorials

Explore what's possible by use cases for various Atlassian products using Forge Hosted Storage by:

## Atlassian app REST APIs

Forge can also use Atlassian app-specific APIs to store and retrieve data for Atlassian Cloud sites and workspaces. This data is accessible to all apps installed within the site (as well as users). See [Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference/) for more details.

## Remote storage

Using the capabilities discussed in this section may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program. To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Forge also lets you integrate your app with services hosted on other platforms. This allows Forge apps to
store data remotely on self-hosted databases or third-party storage services. For more information about
integrating with remote services, see [Forge Remote](/platform/forge/remote/) and [Accessing Forge storage from a remote via REST API](/platform/forge/remote/accessing-storage/).

## Get help
