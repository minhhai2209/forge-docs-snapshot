# Build an app with Teamwork Graph Smart Links

In this tutorial, you'll learn how to build a Forge app that generates custom [Smart Links](/platform/forge/manifest-reference/modules/teamwork-graph-smart-link/). We'll
cover the fundamentals of app setup and generate an example Smart Link. Note, that this tutorial does not cover
integration with external systems.

![](https://dac-static.atlassian.com/platform/forge/snippets/images/graph/screenshot.png?_v=1.5800.1739)

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development. If you're not, see
[Getting started with Forge](https://developer.atlassian.com/platform/forge/set-up-forge/) for a detailed tutorial.

You will also need to ensure you are using the latest version of the Forge CLI.

To install, run:

```
1
npm install -g @forge/cli@latest
```

### Set up a cloud developer site

Currently, apps that use Teamwork Graph modules will need to be installed into to Jira. This means
that in order to test your Teamwork Graph app, you will need a Jira site. If you do not have one of
these already, see below for information on how to create a new Atlassian cloud developer site.

An Atlassian cloud developer site lets you install and test your app on Confluence and Jira. If you don't have one yet, set it up now:

Go to <http://go.atlassian.com/cloud-dev> and create a site using the email address associated with your Atlassian account.
Once your site is ready, log in and complete the setup wizard.
You can install your app to multiple Atlassian sites. However, app data won't be shared between separate Atlassian sites, products, or Forge environments.

The limits on the numbers of users you can create are as follows:

Confluence: 5 users
Jira Service Management: 1 agent
Jira Software and Jira Work Management: 5 users

## Step 1: Create your app

In this step we will create a blank Forge app and then in the following steps, we will add the required
modules and logic to the app.

1. Create your app by running:
2. Enter a name for your app (up to 50 characters). For example, *my-first-smartlink-app*.
3. Select *Show All* as the context.
4. Select the *Show All* category.
5. Select the *blank* template.
6. Change to the app subdirectory to see the app files:

   ```
   ```
   1
   2
   ```



   ```
   cd my-first-smartlink-app
   ```
   ```

The Forge app uses Node.js and has the following structure:

```
```
1
2
```



```
├── manifest.yml
├── package.json
└── src
    └── index.js
```
```

### manifest.yml

Your `manifest.yml` file should look like the following with app ID:

```
```
1
2
```



```
modules:
  function:
    - key: my-function
      handler: index.run
app:
  runtime:
    name: nodejs24.x
    memoryMB: 256
    architecture: arm64
  id: <your app id>
```
```

## Step 2: Install Typescript

Installing Typescript is a development dependency for apps utilizing the Smart Links module.

To install, run:

```
```
1
2
```



```
  npm install typescript --save-dev
```
```

Then, create a `tsconfig.json` file containing the following configuration:

```
```
1
2
```



```
{
  "compilerOptions": {
    "target": "es2016", // Specifies the target JavaScript version for compilation
    "module": "commonjs", // Specifies the module system to use (e.g., commonjs, esnext)
    "outDir": "./dist", // Specifies the output directory for compiled JavaScript files
    "strict": true, // Enables a wide range of type-checking validation rules
    "esModuleInterop": true // Enables interoperability between CommonJS and ES Modules
  },
  "include": [
    "src/**/*.ts" // Specifies files to include in the compilation
  ],
  "exclude": [
    "node_modules" // Specifies files/directories to exclude from the compilation
  ]
}
```
```

## Step 3: Configure the app manifest

In the app's top-level directory, open the `manifest.yml` file and update the modules section to:

```
```
1
2
```



```
modules:
  graph:smartLink:
    - key: my-first-smartlink
      icon: https://static.my-first-smartlink.com/favicon.ico
      name: My first Smart Links
      function: getEntityByUrlFn
      domains:
        - my-first-smartlink.com
        - www.my-first-smartlink.com
      subdomains: true
      patterns:
        - >-
          https:\/\/([\w\.-]+\.)?my-first-smartlink\.com\/([0-9a-zA-Z]{4,128})(?:\/.*)?$

  function:
    - key: getEntityByUrlFn
      handler: index.resolveSmartLinks
```
```

In this step we've added the `graph:smartLink` module, which contains:

* Domains the app supports and whether to allow sub-domains.
* The URL patterns that are supported by the app.
* The function to call when a Link matches a domain and one of our URL patterns.

For a detailed understanding of the manifest structure, refer to the
[Smart Link module](/platform/forge/manifest-reference/modules/teamwork-graph-smart-link).

### Step 4: Configure Smart Link logic

Now that we have the `manifest` configured, let's add the code logic.

Rename `index.js` to `index.ts` and replace the content with the following:

```
```
1
2
```



```
// SOME HELPER OBJECTS
export interface ResolveSmartLinkRequest {
    type: 'resolve';
    payload: {
        urls: string[];
    }
}

export interface ResolveSmartLinkResponse {
    entities: ResolveUrlEntityResult[];
}

export type Identifier = { url : string}

export interface ResolveUrlEntityResult  {
    identifier: Identifier
    meta: {
        access: string,
        visibility: string
    };
    entity?: any;
}

export const buildResolveSmartLinksResponse = (entities: ResolveUrlEntityResult[]): ResolveSmartLinkResponse => {
    return {
        entities: entities,
    };
}

/**
 * This is the entrypoint for the Smart Link function.
 * It receives a request containing a list of URLs to resolve and returns a list of entities.
 * The function uses async processing to resolve all URLs concurrently.
 */
export async function resolveSmartLinks(request: ResolveSmartLinkRequest):Promise<ResolveSmartLinkResponse>  {
    console.log(request);
    const urls = request.payload.urls;

    const processedEntities = await Promise.all(
        urls.map(url => {
            return processUrl(url);
        }),
    );

    return buildResolveSmartLinksResponse(processedEntities);

}

/**
 * This function processes a single URL.
 * It extracts the fileId from the URL and then pulls the file information from Google using the user authenticated OAuth2 token.
 */
async function processUrl(url: string) : Promise<ResolveUrlEntityResult> {

    return  {
        identifier: {
            url: url
        },
        meta: {
            access: 'granted',
            visibility: 'public'
        },
        entity: {
            schemaVersion: '2.0',
            id: '1231321',
            updateSequenceNumber: 1111,
            displayName: "Hello World!",
            description: "Well done you created your first Smart Link!",
            url,
            'atlassian:remote-link': {
                type: 'document',
            },
            createdAt: new Date().toISOString(),
            lastUpdatedAt: new Date().toISOString(),
            thumbnail: {
                externalUrl: `https://picsum.photos/200`,
            },
            createdBy: {
                accountId: '6076c075c642ff0070ef3787',
            }
        }
    };
}
```
```

Ensure you import all dependencies.

## Step 5: Install the app

To use your app, it must be installed onto an Atlassian site. The `forge deploy` command builds,
compiles, and deploys your code; it'll also report any compilation errors. The `forge install` command
then installs the deployed app onto an Atlassian site with the required API access.

Currently, apps that use Teamwork Graph modules will need to be installed into to Jira.

You must run the `forge deploy` command before `forge install` because an installation links your deployed app to an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app into your Jira instance by running:
3. Select your *Jira* using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, example.atlassian.net.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the successful installation message appears, your app is installed and ready to use on the
specified site. You can always delete your app from the site by running the forge uninstall command.

Running the `forge install` command only installs your app onto the selected organization. To install
onto multiple organizations, repeat these steps again, selecting another organization each time.
You must run `forge deploy` before running `forge install` in any of the Forge environments.

## Test the app

To test the app, open up Jira, create an Jira issue, and paste `https://www.my-first-smartlink.com/12346`
into the description. If your setup is correct, your Smart Link will appear; otherwise, it will
display as a regular link.

These links can now be added to any Smart Link-enabled surface such as Jira issues, Confluence pages,
Confluence whiteboards, and more.
