# The Bitbucket Cloud REST API

The purpose of this section is to describe how to authenticate when making API calls using the Bitbucket REST API.

---



---

### Access tokens

Access tokens are passwords (or tokens) that provide access to a *single* repository, project or workspace.
These tokens can authenticate with Bitbucket APIs for scripting, CI/CD tools, Bitbucket Cloud-connected apps,
and Bitbucket Cloud integrations.

Access tokens are linked to a repository, project, or workspace, not a user account.
The level of access provided by the token is set when a repository, or workspace admin creates it,
by setting privilege scopes.

There are three types of access token:

* **Repository access tokens** can connect to a single repository, preventing them from accessing any other repositories or workspaces.
* **Project access tokens** can connect to a single project, providing access to any repositories within the project.
* **Workspace access tokens** can connect to a single workspace and have access to any projects and repositories within that workspace.

When using Bitbucket APIs with an access token, the token will be treated as the "user" in the
Bitbucket UI and Bitbucket logs. This includes when using the access token to leave a comment on a pull request,
push a commit, or merge a pull request. The Bitbucket UI and API responses will show the
repository/project/workspace access token as a user. The username shown in the Bitbucket UI is the Access
Token *name*, and a custom icon is used to differentiate it from a regular user in the UI.

#### Considerations for using access tokens

* After creation, an access token can't be viewed or modified. The token's name, created date,
  last accessed date, and scopes are visible on the repository, project, or workspace **access tokens** page.
* Access tokens can access a limited set of Bitbucket's privilege scopes.
* Provided you set the correct privilege scopes, you can use an access token to clone (`repository`)
  and push (`repository:write`) code to the token's repository or the repositories the token can access.
* You can't use an access token to log into the Bitbucket website.
* Access tokens don't require two-step verification.
* You can set privilege scopes (specific access rights) for each access token.
* You can't use an access token to manipulate or query repository, project, or workspace permissions.
* Access tokens are not listed in any repository or workspace permission API response.
* Access tokens are deactivated when deleting the resource tied to it (a repository, project, or workspace).
* Repository access tokens are also revoked when transferring the repository to another workspace.
* Any content created by the access token will persist after the access token has been revoked.
* Access tokens can interact with branch restriction APIs, but the token can't be configured as a user with merge access when using branch restrictions.

There are some APIs which are inaccessible for Access tokens, these are:

#### Repository access tokens

For details on creating, managing, and using repository access tokens, visit
[Repository access tokens](https://support.atlassian.com/bitbucket-cloud/docs/repository-access-tokens/).

The available scopes for repository access tokens are:

#### Project access tokens

For details on creating, managing, and using project access tokens, visit
[Project access tokens](https://support.atlassian.com/bitbucket-cloud/docs/project-access-tokens/).

The available scopes for project access tokens are:

#### Workspace access tokens

For details on creating, managing, and using workspace access tokens, visit
[Workspace access tokens](https://support.atlassian.com/bitbucket-cloud/docs/workspace-access-tokens/).

The available scopes for workspace access tokens are:

### App passwords

App passwords are deprecated. Use [API tokens](#api-tokens).

### API tokens

API Tokens are personal access tokens that users can create to authenticate with Bitbucket's REST APIs
or interact with Git. They are designed as a long term replacement for app passwords, while retaining a
lot of the functionality you are already familiar with.

Some important points about API tokens:

* To authenticate with an API token, use Basic HTTP Authentication as per [RFC-2617](https://tools.ietf.org/html/rfc2617), where
  the username is your Atlassian email and password is the API token.
* You cannot view an API token or adjust permissions after you create the API token. They are
  designed to be disposable. If you need to change the scopes or you've lost the token, you should just create a new one.
* API token require an expiry date at creation, with a maximum duration of 1 year.
* You cannot use them to log into Bitbucket website.
* API tokens are tied to an individual account's credentials and should not be shared. If you're sharing your API token
  you're giving direct, authenticated access to everything that the token has been scoped
  to do with Bitbucket's APIs.
* You can set privilege scopes (specific access rights) for each API token.

For details on creating, managing, and using API tokens, visit
[API tokens](https://support.atlassian.com/bitbucket-cloud/docs/api-tokens/).

### OAuth 2.0

Our OAuth 2 implementation is merged in with our existing OAuth 1 in
such a way that existing OAuth 1 consumers automatically become
valid OAuth 2 clients. The only thing you need to do is edit your
existing consumer and configure a callback URL.

Once that is in place, you'll have the following 2 URLs:

```
```
1
2
```



```
https://bitbucket.org/site/oauth2/authorize
https://bitbucket.org/site/oauth2/access_token
```
```

For obtaining access/bearer tokens, we support three of RFC-6749's grant
flows, plus a custom Bitbucket flow for exchanging JWT tokens for access tokens.
Note that Resource Owner Password Credentials Grant (4.3) is no longer supported.

#### 1. Authorization Code Grant (4.1)

The full-blown 3-LO flow. Request authorization from the end user by
sending their browser to:

```
```
1
2
```



```
https://bitbucket.org/site/oauth2/authorize?client_id={client_id}&response_type=code
```
```

The callback includes the `?code={}` query parameter that you can swap
for an access token:

```
```
1
2
```



```
$ curl -X POST -u "client_id:secret" \
  https://bitbucket.org/site/oauth2/access_token \
  -d grant_type=authorization_code -d code={code}
```
```

#### 2. Implicit Grant (4.2)

This flow is useful for browser-based add-ons that operate without server-side backends.

Request the end user for authorization by directing the browser to:

```
```
1
2
```



```
https://bitbucket.org/site/oauth2/authorize?client_id={client_id}&response_type=token
```
```

That will redirect to your preconfigured callback URL with a fragment
containing the access token
(`#access_token={token}&token_type=bearer`) where your page's js can
pull it out of the URL.

#### 3. Client Credentials Grant (4.4)

Somewhat like our existing "2-LO" flow for OAuth 1. Obtain an access
token that represents not an end user, but the owner of the
client/consumer:

```
```
1
2
```



```
$ curl -X POST -u "client_id:secret" \
  https://bitbucket.org/site/oauth2/access_token \
  -d grant_type=client_credentials
```
```

#### 4. Bitbucket Cloud JWT Grant (urn:bitbucket:oauth2:jwt)

If your Atlassian Connect add-on uses JWT authentication, you can swap a
JWT for an OAuth access token. The resulting access token represents the
account for which the add-on is installed.

Make sure you send the JWT token in the Authorization request header
using the "JWT" scheme (case sensitive). Note that this custom scheme
makes this different from HTTP Basic Auth (and so you cannot use "curl
-u").

```
```
1
2
```



```
$ curl -X POST -H "Authorization: JWT {jwt_token}" \
  https://bitbucket.org/site/oauth2/access_token \
  -d grant_type=urn:bitbucket:oauth2:jwt
```
```

#### Making Requests

Once you have an access token, as per RFC-6750, you can use it in a request in any of
the following ways (in decreasing order of desirability):

1. Send it in a request header: `Authorization: Bearer {access_token}`
2. Include it in a (application/x-www-form-urlencoded) POST body as `access_token={access_token}`
3. Put it in the query string of a non-POST: `?access_token={access_token}`

#### Repository Cloning

Since add-ons will not be able to upload their own SSH keys to clone
with, access tokens can be used as Basic HTTP Auth credentials to
clone securely over HTTPS. This is much like GitHub, yet slightly
different:

```
```
1
2
```



```
$ git clone https://x-token-auth:{access_token}@bitbucket.org/user/repo.git
```
```

The literal string `x-token-auth` as a substitute for username is
required (note the difference with GitHub where the actual token is in
the username field).

#### Refresh Tokens

Our access tokens expire in one hour. When this happens you'll get 401
responses.

Most access tokens grant responses (Implicit and JWT excluded). Therefore, you should include a
refresh token that can then be used to generate a new access token,
without the need for end user participation:

```
```
1
2
```



```
$ curl -X POST -u "client_id:secret" \
  https://bitbucket.org/site/oauth2/access_token \
  -d grant_type=refresh_token -d refresh_token={refresh_token}
```
```

### Bitbucket OAuth 2.0 scopes

Bitbucket's API applies a number of privilege scopes to endpoints. In order to access an
endpoint, a request will need to have the necessary scopes.

OAuth 2.0 Scopes are applicable for OAuth 2 and access tokens
auth mechanisms as well as Bitbucket Connect apps.

Scopes are declared in the descriptor as a list of strings, with each string being the name of a unique scope.

A descriptor lacking the `scopes` element is implicitly assumed to require all scopes and as a result,
Bitbucket will require end users authorizing/installing the add-on to explicitly accept all scopes.

Our best practice suggests you add only the scopes your add-on needs, but no more than it needs.

Invalid scope strings will cause the descriptor to be rejected and the installation to fail.

The available scopes are:

#### project

Provides access to view the project or projects.
This scope implies the [`repository`](#repository) scope, giving read access to all the repositories in a project or projects.

#### project:write

This scope is deprecated, and has been made obsolete by `project:admin`. Please see the deprecation notice [here](/cloud/bitbucket/deprecation-notice-project-write-scope).

#### project:admin

Provides admin access to a project or projects. No distinction is made between public and private projects. This scope doesn't implicitly grant the [`project`](#project) scope or the [`repository:write`](#repository-write) scope on any repositories under the project. It gives access to the admin features of a project only, not direct access to its repositories' contents.

* ability to create the project
* ability to update the project
* ability to delete the project

#### repository

Provides read access to a repository or repositories.
Note that this scope does not give access to a repository's pull requests.

* access to the repo's source code
* clone over HTTPS
* access the file browsing API
* download zip archives of the repo's contents
* the ability to view and use the issue tracker on any repo (created issues, comment, vote, etc)
* the ability to view and use the wiki on any repo (create/edit pages)

#### repository:write

Provides write (not admin) access to a repository or repositories. No distinction is made between public and private repositories. This scope implicitly grants the [`repository`](#repository) scope, which does not need to be requested separately.
This scope alone does not give access to the pull requests API.

* push access over HTTPS
* fork repos

#### repository:admin

Provides admin access to a repository or repositories. No distinction is made between public and private repositories. This scope doesn't implicitly grant the [`repository`](#repository) or the [`repository:write`](#repository-write) scopes. It gives access to the admin features of a repo only, not direct access to its contents. This scope can be used or misused to grant read access to other users, who can then clone the repo, but users that need to read and write source code would also request explicit read or write.
This scope comes with access to the following functionality:

* View and manipulate committer mappings
* List and edit deploy keys
* Ability to delete the repo
* View and edit repo permissions
* View and edit branch permissions
* Import and export the issue tracker
* Enable and disable the issue tracker
* List and edit issue tracker version, milestones and components
* Enable and disable the wiki
* List and edit default reviewers
* List and edit repo links (Jira/Bamboo/Custom)
* List and edit the repository webhooks
* Initiate a repo ownership transfer

#### repository:delete

Provides access to delete a repository or repositories.

#### pullrequest

Provides read access to pull requests.
This scope implies the [`repository`](#repository) scope, giving read access to the pull request's destination repository.

* see and list pull requests
* create and resolve tasks
* comment on pull requests

#### pullrequest:write

Implicitly grants the [`pullrequest`](#pullrequest) scope and adds the ability to create, merge and decline pull requests.
This scope also implicitly grants the [`repository:write`](#repository-write) scope, giving write access to the pull request's destination repository. This is necessary to allow merging.

* merge pull requests
* decline pull requests
* create pull requests
* approve pull requests

#### issue

Ability to interact with issue trackers the way non-repo members can.
This scope doesn't implicitly grant any other scopes and doesn't give implicit access to the repository.

* view, list and search issues
* create new issues
* comment on issues
* watch issues
* vote for issues

#### issue:write

This scope implicitly grants the [`issue`](#issue) scope and adds the ability to transition and delete issues.
This scope doesn't implicitly grant any other scopes and doesn't give implicit access to the repository.

* transition issues
* delete issues

#### wiki

Provides access to wikis. This scope provides both read and write access (wikis are always editable by anyone with access to them).
This scope doesn't implicitly grant any other scopes and doesn't give implicit access to the repository.

* view wikis
* create pages
* edit pages
* push to wikis
* clone wikis

#### webhook

Gives access to webhooks. This scope is required for any webhook-related operation.

This scope gives read access to existing webhook subscriptions on all
resources the authorization mechanism can access, without needing further scopes.
For example:

* A client can list all existing webhook subscriptions on a repository. The [`repository`](#repository) scope is not required.
* Existing webhook subscriptions for the issue tracker on a repo can be retrieved without the [`issue`](#issue) scope. All that is required is the `webhook` scope.

To create webhooks, the client will need read access to the resource. Such as: for [`issue:created`](#issue-created), the client will need to
have both the `webhook` and the [`issue`](#issue) scope.

* list webhook subscriptions on any accessible repository, user, team, or snippet
* create/update/delete webhook subscriptions.

#### snippet

Provides read access to snippets.
No distinction is made between public and private snippets (public snippets are accessible without any form of authentication).

* view any snippet
* create snippet comments

#### snippet:write

Provides write access to snippets.
No distinction is made between public and private snippets (public snippets are accessible without any form of authentication).
This scope implicitly grants the [`snippet`](#snippet) scope which does not need to be requested separately.

* create snippets
* edit snippets
* delete snippets

#### email

Ability to see the user's primary email address. This should make it easier to use Bitbucket Cloud as a login provider for apps or external applications.

#### account

When used for:

* **user-related APIs** — Gives read-only access to the user's account information.
  Note that this doesn't include any ability to change any of the data. This scope allows you to view the user's:
  * email addresses
  * language
  * location
  * website
  * full name
  * SSH keys
  * user groups
* **workspace-related APIs** — Grants access to view the workspace's:
  * users
  * user permissions
  * projects

#### account:write

Ability to change properties on the user's account.

* delete the authorizing user's account
* manage the user's groups
* change a user's email addresses
* change username, display name and avatar

#### pipeline

Gives read-only access to pipelines, steps, deployment environments and variables.

#### pipeline:write

Gives write access to pipelines. This scope allows a user to:

* Stop pipelines
* Rerun failed pipelines
* Resume halted pipelines
* Trigger manual pipelines.

This scope is not needed to trigger a build using a push. Performing a `git push` (or equivalent actions) will trigger the build. The token doing the push only needs the [`repository:write`](#repository-write) scope.

This doesn't give write access to create variables.

#### pipeline:variable

Gives write access to create variables in pipelines at the various levels:

* Workspace
* Repository
* Deployment

#### runner

Gives read-only access to pipelines runners setup against a workspace or repository.

#### runner:write

Gives write access to create/edit/disable/delete pipelines runners setup against a workspace or repository.

### Forge app and API token scopes

In order for a Forge app integration or an API token to access Bitbucket API endpoints, it needs to include certain privilege scopes. These are different from Bitbucket OAuth 2.0 scopes.

In the case of a Forge app, the privilege scopes need to be included in the app manifest.

Unlike OAuth 2.0 scopes, Forge app and API token scopes do not implicitly grant access to other scopes, for example, `write:repository:bitbucket` does not implicitly grant access to `read:repository:bitbucket`.

It's important to note that only a subset of all API endpoints are currently available for Forge app integrations. Each endpoint is clearly labeled, indicating whether it is available for Forge apps.

Our best practice recommends adhering to the principle of least privilege. You should only add the scopes that are necessary for your needs.

The available scopes are:

#### read:repository:bitbucket

Allows viewing of repository data. Note that this scope does not give access to a repository's pull requests.

* access to the repository's source code
* access the file browsing API
* access to certain repository configurations such as branching model, default reviewers, etc.

#### write:repository:bitbucket

Allows modification of repository data. No distinction is made between public and private repositories. This scope does not imply the `read:repository:bitbucket` scope, so you need to request that separately if required. This scope alone does not give access to the pull request API.

* update/delete source, branches, tags, etc.
* fork repositories

#### admin:repository:bitbucket

Allows admin activities on repositories. No distinction is made between public and private repositories. This scope does not implicitly grant the `read:repository:bitbucket` or the `write:repository:bitbucket` scopes. It gives access to the admin features of a repository only, not direct access to its contents. This scope does not allow modification of repository permissions. This scope comes with access to the following functionality:

* create repository
* view repository permissions
* view and edit branch restrictions
* edit branching model settings
* edit default reviewers
* view and edit inheritance state for repository settings

#### delete:repository:bitbucket

Allows deletion of repositories.

#### read:pullrequest:bitbucket

Allows viewing of pull requests, plus the ability to comment on pull requests.

This scope does not imply the `read:repository:bitbucket` scope. With this scope, you could retrieve some data specific to the source/destination repositories of a pull request using pull request endpoints, but it does not give access to repository API endpoints.

#### write:pullrequest:bitbucket

Allows the ability to create, update, approve, decline, and merge pull requests.

This scope does not imply the `write:repository:bitbucket` scope.

#### read:project:bitbucket

Allows viewing of project and project permission data.

#### admin:project:bitbucket

Allows the ability to create, update, and delete project. No distinction is made between public and private projects.

This scope does not implicitly grant the `read:project:bitbucket` scope or any repository scopes. It gives access to the admin features of a project only, not direct access to its repositories' contents.

#### read:workspace:bitbucket

Allows viewing of workspace and workspace permission data.

#### admin:workspace:bitbucket

Allows the ability to create, update and delete the workspace. This scope does not implicitly grant the `read:workspace:bitbucket` scope or any repository scopes. It gives access to the admin features of a workspace only, not direct access to its workspaces' contents.

#### read:user:bitbucket

Allows viewing of data related to the current user.

#### write:user:bitbucket

Allows the ability to update data related to the current user.

This scope does not imply the `read:user:bitbucket` scope.

#### read:pipeline:bitbucket

Allows read access to all pipeline information (pipelines, steps, caches, artifacts, logs, tests, code-insights).

#### write:pipeline:bitbucket

Allows running pipelines (i.e., start/stop/create pipeline) and uploading tests/code-insights.

This scope does not imply the `read:pipeline:bitbucket` scope.

#### admin:pipeline:bitbucket

Allows admin activities, such as creating pipeline variables.

This scope does not implicitly grant the `read:pipeline:bitbucket` or the `write:pipeline:bitbucket` scopes.

#### read:runner:bitbucket

Allows viewing of runners information.

#### write:runner:bitbucket

Allows runners management.

This scope does not imply the `read:runners:bitbucket` scope.

#### read:issue:bitbucket

Allows the viewing of issues.

#### write:issue:bitbucket

Allows the ability to create and update issues.

This scope does not implicitly grant the `read:issue:bitbucket` scope.

#### delete:issue:bitbucket

Allows the deletion of issues.

#### read:webhook:bitbucket

Allows read access to webhooks information.

#### write:webhook:bitbucket

Allows the ability to create and update webhooks.

This scope does not implicitly grant the `read:webhook:bitbucket` scope.

#### delete:webhook:bitbucket

Allows the deletion of webhooks.

#### read:snippet:bitbucket

Allows the viewing of snippets.

#### write:snippet:bitbucket

Allows the ability to create and update snippets.

This scope does not implicitly grant the `read:snippet:bitbucket` scope.

#### delete:snippet:bitbucket

Allows the deletion of snippets.

#### read:ssh-key:bitbucket

Allows read access to information related to deploy keys and SSH keys.

#### write:ssh-key:bitbucket

Allows the ability to create and update deploy keys and SSH keys.

This scope does not implicitly grant the `read:ssh-key:bitbucket` scope.

#### delete:ssh-key:bitbucket

Allows the deletion of deploy keys and SSH keys.

#### read:gpg-key:bitbucket

Allows read access to information related to GPG keys.

#### write:gpg-key:bitbucket

Allows the ability to create and update GPG keys.

This scope does not implicitly grant the `read:gpg-key:bitbucket` scope.

#### delete:gpg-key:bitbucket

Allows the deletion of GPG keys.

#### read:permission:bitbucket

Allows read access to permissions data.

#### write:permission:bitbucket

Allows the ability to create and modify permissions related data.

This scope does not implicitly grant the `read:permission:bitbucket` scope.

#### delete:permission:bitbucket

Allows the deletion of permissions related data.
