# Storage

Forge provides three options for storing app data: Forge-hosted storage, Atlassian app REST APIs (for example, Jira or Confluence), and remote storage that you manage. Use these options to persist and retrieve data securely, at the scale your app needs.

## Hosted storage (recommended)

Store your app data with Forge Storage so you can focus on solving customer problems instead of managing infrastructure.

### Start building your storage

Consider data shape and size limits when selecting the storage option that best fits your use case.

| API | Overview | Ideal for |
| --- | --- | --- |
| [Key-Value Store](/platform/forge/storage-reference/kvs/) | Simple storage for key/value pairs | User preferences, app configuration, simple data storage |
| [Custom entities store](/platform/forge/storage-reference/entities/) | Structured data storage with custom entities and query capabilities | Complex data structures, queryable data, relationships between entities |
| [SQL](/platform/forge/storage-reference/sql/) | Fully managed relational database | Complex data models, relationships, transactions, advanced queries |
| [Object Store (Preview)](/platform/forge/storage-reference/object-store/) | Large file and media storage | Binary data, files, media, large objects |

See [platform quotas and limits](/platform/forge/platform-quotas-and-limits/) and [storage options](/platform/forge/storage-reference/) for more details.

### Example code

Explore these code examples to see how to perform common storage operations with each Forge storage option.

Key-Value Store

Custom Entity Store

SQL

Object Store (Preview)

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

Each storage option has different cost characteristics. For pricing and free monthly allowances, see [Forge platform pricing](/platform/forge/forge-platform-pricing/).

For recommendations on reducing storage costs (such as caching, batching, and querying instead of iterating), see [Storage optimisations](/platform/forge/optimise-forge-costs/#storage-optimisations).

## Remote storage

Forge also lets you integrate your app with services hosted on other platforms. This allows Forge apps to
store data remotely on self-hosted databases or third-party storage services. For more information about
integrating with remote services, see [Forge Remote](/platform/forge/remote/) and [Accessing Forge storage from a remote via REST API](/platform/forge/remote/accessing-storage/).

### Tenant safety in remote storage

Forge data is scoped per app installation to provide basic tenant safety.
However, you still need to avoid storing tenant data in *module-level variables or in-memory caches*
to prevent cross-tenant data leaks.

See [Tenant data isolation in Forge apps](/platform/forge/tenant-data-isolation/)
for unsafe patterns to avoid and safe alternatives.
