# Teamwork Graph connector (EAP)

The Teamwork Graph connector module is now available through Forge's Early Access Program (EAP).

EAPs are offered to selected users for testing and feedback purposes. We are currently working with
a select group of EAP participants to get their apps production-ready and available for publishing on Marketplace.

You must be part of the Forge connector EAP to use this module and the
[Connector SDK](/platform/teamwork-graph/connector-reference/overview/). You can express interest in
joining this EAP through [this form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18836).

The `graph:connector` module allows your app to import data from external tools into Atlassian's Teamwork Graph.
Once the data is integrated into the Graph, it becomes accessible across various Atlassian experiences, including
Search, Rovo Chat, Rovo Agents, and Atlassian Analytics.

This module works in conjunction with the [Teamwork Graph connector SDK](/platform/teamwork-graph/connector-reference/overview/).
To install, run:

```
1
npm i @forge/teamwork-graph
```

## Manifest structure

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
31
32
33
34
modules {}
└─ graph:connector
   ├─ key (string) [Required]
   ├─ name (string) [Required]
   ├─ icons (object) [Required]
   │  ├─ light (string) [Required]
   │  └─ dark (string) [Required]
   ├─ objectTypes (array of string) [Required]
   ├─ auth (object) [Optional]
   │  └─ provider (AuthProvider) [Required]
   └─ datasource (object) [Required]
      ├─ formConfiguration (object) [Optional]
      │  ├─ instructions (array of string) [Optional]
      │  ├─ form (array of FormSection) [Required]
      │  │  ├─ key (string) [Required]
      │  │  ├─ type (string) [Required]
      │  │  ├─ title (string) [Required]
      │  │  ├─ description (string) [Required]
      │  │  └─ properties (array of FormProperty) [Required]
      │  │     ├─ key (string) [Required]
      │  │     ├─ label (string) [Required]
      │  │     ├─ type (string) [Required]
      │  │     ├─ isRequired (boolean) [Optional]
      │  │     ├─ isSensitive (boolean) [Optional]
      │  │     └─ hideInEditView (boolean) [Optional]
      │  └─ validateConnection (object) [Required]
      │     └─ function (Function) [Required]
      └─ onConnectionChange (object) [Required]
         └─ function (Function) [Required]

function []
├─ key (string) [Mandatory]
└─ handler (string) [Mandatory]
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the connector. Must be unique within the manifest. Regex: `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The display name of the connector shown to customers. |
| `icons` | `object` | Yes | All connectors require a light and dark icon to allow change of theme. These icons are used in the admin experience of connector configuration as well as the end user experience in Search, where users can filter search results by connector. |
| `icons.light` | `string` | Yes | Icon to display when theme is set to light. |
| `icons.dark` | `string` | Yes | Icon to display when theme is set to dark. |
| `objectTypes` | `Array(string)` | Yes | List of object types ingested by the connector.  See supported [Object types](/platform/teamwork-graph/object-types/overview). |
| `auth` | `object` | No | If the Atlassian user must be authenticated with the source system to see the ingested data, the Auth Provider to authenticate end users needs to be specified.  Contains a `provider` property specifying the authentication provider. |
| `auth.provider` | `AuthProvider` | Yes | The authentication provider to use for end-user authentication. |
| `datasource` | `object` | Yes | This section contains all the related data to enable Datasource configuration by Admin Users. |
| `datasource.formConfiguration` | `FormConfiguration` | No | This section is to configure the Admin Connector Configuration screens. It includes the ability to add test instructions on how to fill in the Connector Configuration Form, the fields that need to be captured in the Form as well as functions to validate the configuration and get default form data. |
| `datasource.onConnectionChange` | `object` | Yes | Function to handle connection creation, update, or deletion events.  Must specify a `function` property referencing a function key. |
| `onConnectionChange.function` | `Function` | Yes | Function key to handle connection change events. |

### Form configuration

Defines the fields and layout shown to admins when configuring this connector in the admin experience.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `instructions` | `Array(string)` | No | A list of messages that will be displayed to the Admin at the top of the Configuration Form. |
| `form` | `Array(FormSection)` | Yes | The form consists of sections, each capturing configuration from the Admin. |
| `form.key` | `string` | Yes | Unique identifier for the form section. |
| `form.type` | `string` | Yes | Type of the form section. |
| `form.title` | `string` | Yes | Title displayed for the form section. |
| `form.description` | `string` | Yes | Description displayed for the form section. |
| `form.properties` | `Array(FormProperty)` | Yes | Form properties within the section for collecting specific connection details. |
| `form.properties.key` | `string` | Yes | Unique identifier for the form property. |
| `form.properties.label` | `string` | Yes | Label displayed for the form property. |
| `form.properties.type` | `string` | Yes | Type of the form property. Supported values: `string`, `number`, `boolean`. |
| `form.properties.isRequired` | `boolean` | No | Whether the form property is required for submission. |
| `form.properties.isSensitive` | `boolean` | No | Whether the form property contains sensitive data that should be masked. |
| `form.properties.hideInEditView` | `boolean` | No | Whether the form property should be hidden when editing an existing connection. |
| `validateConnection` | `object` | Yes | Function to validate the connection details entered in the form.  Must specify a `function` property referencing a function key. |
| `validateConnection.function` | `Function` | Yes | Function key to validate the connection. |

## Scopes required

To enable data ingestion and retrieval, you will also need to enable the following scopes in your manifest:

```
```
1
2
```



```
permissions:
  scopes:
    - write:object:jira
    - read:object:jira
    - delete:object:jira
```
```

## Configuration in Atlassian Administration

Admins will be able to configure and manage the Teamwork Graph connectors available in your app in
Atlassian Administration through **Connected apps**.

The Connected apps screen can be accessed within Atlassian Administration by navigating to
*Apps > Site > Connected apps*.

After selecting the app, all available Teamwork Graph connectors will be shown
in the **Connections** tab.

![Connections tab within Marketplace app showing one Teamwork Graph connector that has not yet been configured](https://dac-static.atlassian.com/platform/forge/images/teamwork-graph/teamwork-graph-connector-not-configured.svg?_v=1.5800.1877)

Admins must configure the connector before it can start providing data to Teamwork Graph. To
do this, the admin will click the **Connect** button, which opens a configuration modal.

![Basic modal for configuring Teamwork Graph connector](https://dac-static.atlassian.com/platform/forge/images/teamwork-graph/teamwork-graph-connector-modal.svg?_v=1.5800.1877)

### Configuration details

The configuration screens in Rovo and Connected apps include the same content. There is some
Atlassian-defined information, such as legal and privacy declarations, and a required field for
the admin to enter a connector nickname.

Using the properties that are defined in the manifest under the `formConfiguration` section,
you can add to and customize this screen. You can provide additional details to admins in the **Before you begin**
section with the `instructions` property, and add fields for admins to provide any further information
you require for the connector, such as API keys, with the `form` property.

## Supported functions

### validateConnection

The `validateConnection` function is required, only if the connector requires the admin to
provide additional configuration, via the Form input properties. The Forge app will be called to validate the data entered by the Admin User to ensure it can successfully connect to the
remote system. Atlassian will only proceed to set up the data source for ingestion into Teamwork
Graph after the connection has been validated.

If the connector does not require any additional configuration properties, i.e Form Configuration,
the `validateConnection` function should not be supplied and will not be called.

#### Request Payload

```
```
1
2
```



```
{
  name: string;
  configProperties: Record<string,string>;
}
```
```

##### Example

```
```
1
2
```



```
{
  "name" : "My Connection",
  "configProperties" : {
    "secret" : "jane",
    "username" : "joe"
  }
}
```
```

#### Response

If the connection is not valid, the function must `throw` an `Error("Reason for error")`.
If successful, the function should return with a `HTTP 200` response.

### onConnectionChange

The `onConnectionChange` function is required. Whenever a connection is created, updated,
or disconnected (deleted), Atlassian notifies the Forge app by invoking the `onConnectionChange`
function. This enables your app to start data synchronization, update sync parameters, or halt data
ingestion when a connection is removed.

The `onConnectionChange` function will be executed when there is any change to the
configuration of a connection. The possible values for action are `CREATED`,
`UPDATED`, and `DELETED`.

Note that Atlassian will automatically take care of deleting the data assocociated with the Connection. No data deletion logic is required to remove the data from Teamwork Graph by the App when a Connection is deleted.

#### Request

```
```
1
2
```



```
{
  action: CREATED | UPDATED | DELETED;
  name: string;
  connectionId: string;
  configProperties: Record<string,string>?;
}
```
```

##### Example

```
```
1
2
```



```
"body": {
  "action": "CREATED",
  "name" : "My Connection",
  "connectionId": "edc0ce33-2f67-4997-8c0f-c5f38923e33f",
  "configProperties" : {
    "secret" : "jane",
    "username" : "joe"
    }
}
```
```

#### Response

To acknowledge receipt of the change notification, the function should return a Success response.

# Managing when a connector is disconnected

When an admin disconnects a connector instance, the Forge app is notified of this change
through the `onConnectionChange` function with the action type `DELETED`. This
enables your app to perform any necessary cleanup, such as stopping data ingestion if it is managed
by the Forge app.

## Manifest examples

### Connector with no end-user OAuth or configuration properties

In this example, the Teamwork Graph connector does not require end-user authentication on the remote system,
so the `auth.provider` property is omitted. Note that because there is no end-user authentication, the object permissions will need to be scoped to the Atlassian Workspace (e.g ATLASSIAN\_WORKSPACE permission). Without the end-user OAuth authentication, Atlassian can not reliably link the external user account to the Atlassian user and apply permissions.

Furthermore, in this example the connector does not require any additional admin configuration, beyond the required connector
nickname.

This scenario represents an app that operates entirely within Atlassian boundaries,
with all data residing on the same site as the app installation. As a result, no additional
connection details are needed.

When the admin creates the connection, the app will not be prompted to validate it. However, the app
will still be notified when the connection is established so that data ingestion can begin. The app
will also receive notifications if the connector is disconnected, allowing it to handle cleanup as
needed.

```
```
1
2
```



```
permissions:
  scopes:
    - write:object:jira
    - read:object:jira
    - delete:object:jira
  external:
    fetch:
      backend:
        - "https://www.remote-service.com"

graph:connector:
  - key: example-connector
    name: Example Connector
    icons: 
     light: https://static.example-hello-world.com/favicon-light.ico
     dark: https://static.example-hello-world.com/favicon-dark.ico
    objectTypes:
      - atlassian:document
      - atlassian:feature-flag
    datasource:
        onConnectionChange:
          function: onConnectionChangeFn 

function:
    - key: onConnectionChangeFn
       handler: index.onConnectionChange
```
```

### Connector requiring end-user OAuth and configuration properties

In this example, this app has defined a set of properties that the admin must provide to configure
the connection. When the admin submits the configuration, the app is prompted to validate the
connection using the `validateConnection` function.

Once validation succeeds, Atlassian sets up the connection for data ingestion and notifies the app
when the connection is fully established and ready for use via the `onConnectionChange` function.

```
```
1
2
```



```
permissions:
  scopes:
    - write:object:jira
    - read:object:jira
    - delete:object:jira
  external:
    fetch:
      backend:
        - "https://www.remote-service.com"

graph:connector:
  - key: example-connector
    name: Example Connector
    icons: 
     light: https://static.example-hello-world.com/favicon-light.ico
     dark: https://static.example-hello-world.com/favicon-dark.ico
    objectTypes:
      - atlassian:document
    auth:
        provider: myAuthProviderKey
    datasource:
      formConfiguration:
        form:
          - key: exampleSection1
            type: header
            title: Connection Details
            description: Please provide your API Key
            properties:
              - key: apiKey
                label: Api Key
                type: string
                isRequired: true
        validateConnection:
          function: validateConnectionFn
      onConnectionChange:
        function: onConnectionChangeFn 
function:
    - key: onConnectionChangeFn
       handler: index.onConnectionChange
    - key: validateConnectionFn
       handler: index.validateConnection
```
```

## Guidelines

To ensure a consistent and user-friendly experience across Atlassian surfaces,
such as Rovo Search, please ensure your connector adheres to the following guidelines:

### Logo usage

* Use the official logo of the service for your connector. For example, if you are building a ServiceNow
  connector, use the official ServiceNow logo.
* Do not modify or combine the official logo with your company or developer logo. The connector
  logo should remain the unaltered, official logo of the service.

### Connector naming

* Use the official service name as the connector name. For example, "Service Now".
* Do not add prefixes, suffixes, or descriptors. For example, avoid names like “ServiceNow Demand
  Connector” or "ServiceNow by Your Name". The connector should simply be named after the service.

### Differentiation between Atlassian-built and Partner-built connectors

* Admins will be able to differentiate connectors built by Atlassian and those built by Partners in
  the configuration UI, where the developer name and app name is displayed.
* End users will see a “connector nickname” as a subfilter within Rovo Search to distinguish between
  connectors, including multiple connectors of the same tool.

### Forge app branding

For your Forge app itself, outside of the connector, you may use your own name and logo.
The above guidelines apply only to the connector configuration.

## Object types and connector SDK

## Example app
