# Use Forge hosted storage in a Confluence macro

#### Having trouble?

Ask for help on our Developer Community

[Get help](https://community.developer.atlassian.com/session/sso?return_path=%2Fnew-topic%3Fcategory_id%3D45%26tags%3Ddac-get-help%2Cforge-create-confluence-macro-with-storage-api)

This tutorial describes how to build an app for sharing definitions for
terminology and acronyms across an entire Confluence site.
The app uses Forge hostes storage to store definitions, which allows them to be
shared between several macros and accessed from the site administration.

In this tutorial you will learn how to persist and retrieve data from Forge hosted storage
(specifically, the [Key-Value Store](/platform/forge/runtime-reference/storage-api))
and display the results in a table.

This tutorial has an accompanying [Bitbucket repository](https://bitbucket.org/atlassian/definitions-macro-tutorial/src/master/).
You'll find a link to a git tag at the end of each step which you can use to compare
with your code or to skip ahead.

If you are cloning this repository, use `forge register` before you begin to create a new ID
for the app under your account.

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

To complete this tutorial, you need the latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
on the command line.

### Set up a cloud developer site

An Atlassian cloud developer site lets you install and test your app on
Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:

1. Go to <http://go.atlassian.com/cloud-dev> and
   create a site using the email address associated with your Atlassian account.
2. Once your site is ready, log in and complete the setup wizard.

You can install your app to multiple Atlassian sites. However, app
data won't be shared between separate Atlassian apps, sites,
or Forge environments.

The limits on the numbers of users you can create are as follows:

* Confluence: 5 users
* Jira Service Management: 1 agent
* Jira Software and Jira Work Management: 5 users

## Step 1: Create your app

Create an app based on the Hello world template. Using your terminal complete
the following:

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Enter a name for the app. For example, *definitions-macro*.
4. Select *UI Kit*.
5. Select *Confluence*.
6. Select the *confluence-macro* template.
7. Your app has been created in a directory with the same name as your app, for example
   *definitions-macro*. Open the app directory to see the files associated with your app.
8. Install the latest version of the Forge KVS package to be able to use Forge Storage features.

   ```
   ```
   1
   2
   ```



   ```
   npm install --save @forge/kvs@latest
   ```
   ```
9. Enable the Key-Value Store by adding the `storage:app` scope to the `manifest.yml`
   file. [Learn more about adding scopes to call an Atlassian REST API]
   (/platform/forge/add-scopes-to-call-an-atlassian-rest-api/).

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     scopes:
       - storage:app
   ```
   ```
10. Enable the [config](/platform/forge/add-configuration-to-a-macro-with-ui-kit/) so that it can appear in the macro by adding `config: true` under `macro`.

    ```
    ```
    1
    2
    ```



    ```
    modules:
      macro:
        ...
        config: true
    ```
    ```

You can check your app against [the tutorial repository](https://bitbucket.org/atlassian/definitions-macro-tutorial/src/master/manifest.yml#lines-9).

## Step 2: Deploy and install your app

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

Next, add your new Confluence macro to a page. To view log invocations, start a [tunnel](/platform/forge/tunneling/) to your app:

You can check your app against [the tutorial repository](https://bitbucket.org/atlassian/definitions-macro-tutorial/src/master).

## Step 3: Add a configuration dialog to the macro

1. Within the `src/frontend/index.jsx` file, add a new component named `Config` containing [TextArea](/platform/forge/ui-kit/components/text-area/) and Label from the `@forge/react` library. This configuration form allows a user of the macro to specify a set of definitions to show in a table.

   ```
   ```
   1
   2
   ```



   ```
   const Config = () => {
     return (
       <>
         <Label labelFor="terms">Terms to include (one per line)</Label>
         <TextArea name="terms" id="terms" defaultValue="" isRequired />
       </>
     )
   };
   ```
   ```
2. Add the `Config` function to the `ForgeReconciler` to allow for configuration changes, under the existing `ForgeReconciler.render()` for `App`.

   ```
   ```
   1
   2
   ```



   ```
   ForgeReconciler.render(
     <React.StrictMode>
       <App />
     </React.StrictMode>
   );

   ForgeReconciler.addConfig(<Config />);
   ```
   ```
3. Add the [`useConfig`](/platform/forge/ui-kit/hooks/use-config/) hook to the `App` component. This hook allows the app
   to access configuration set by the user in the macro configuration dialog, and defaults to an empty object if undefined.
   If there is no list of terms found in config, `terms` defaults to an empty array.
   App currently returns the information wrapped in the [Text](/platform/forge/ui-kit/components/text/) component.

   ```
   ```
   1
   2
   ```



   ```
   const App = () => {
     const config = useConfig() || {};
     const terms = config.terms ? config.terms.split("\n") : [];

     if (terms.length === 0) {
       return (
         <Text>No Terms</Text>
       );
     }

     return (
       <Text>{terms.join(",")}</Text>
     );
   };
   ```
   ```

## Step 4: Fetch a list of definitions from storage

Your app makes use of the `@forge/kvs` package to interact with the Key-Value Store. This package provides methods for reading, writing, and querying data.

This tutorial starts with reading a list of definitions from the Key-Value Store.
Initially the results are empty; adding definitions is covered in a later stage.

The app stores key entities based on the term, with the following format:

```
```
1
2
```



```
interface Term {
  definition: string;
  term: string;
}
```
```

1. Within `src/resolvers/index.js`, add a `getTermDefinition` function to load a definition given a term.

   ```
   ```
   1
   2
   ```



   ```
   import Resolver from '@forge/resolver';
   import { kvs } from '@forge/kvs';

   const resolver = new Resolver();

   // Create a key composed from the term
   function termKey(term) { 
     return `term-${term}`;
   }

   async function getTermDefinition(term) {
     const value = await kvs.get(termKey(term));
     return value ? value.definition : "";
   }

   export const handler = resolver.getDefinitions();
   ```
   ```
2. Also create a `getTermDefinitions` function using `resolver` to turn a list of terms into a list of definitions.

   ```
   ```
   1
   2
   ```



   ```
   resolver.define('getTermDefinitions', async(req) => {
     const pendingDefinitions = req.payload.terms.map((term) => getTermDefinition(term));
     return await Promise.all(pendingDefinitions);
   })
   ```
   ```

   This function makes use of the `Promise.all` operation to turn a list
   of pending promises into a single promise. The resulting promise resolves to an
   array of definitions when awaited.
3. Inside the `src/frontend/index.jsx` file, add a new hook within the `App` component for `definitions`.

   ```
   ```
   1
   2
   ```



   ```
   const [definitions, setDefinitions] = useState([]);
   ```
   ```
4. In the `src/frontend/index.jsx` file, define an async helper function called `populateDefinitions` inside the `App` component using [useEffect](https://developer.atlassian.com/platform/forge/ui-kit-hooks-reference/#useeffect). This invokes the resolver with key `getTermDefinitions`.

   ```
   ```
   1
   2
   ```



   ```
     useEffect(() => {
       const populateDefinitions = async() => {
         if (terms.length !== 0) {
           const data = await invoke('getTermDefinitions', { terms: terms });
           setDefinitions(data);
         }
       }

       populateDefinitions();
     }, [terms, invoke, setDefinitions]);
   ```
   ```
5. Change the return of the `App` component to load the
   definitions for the provided terms list. Since no definitions have been provided yet, definitions should be empty.

   ```
   ```
   1
   2
   ```



   ```
   const App = () => {
     const [definitions, setDefinitions] = useState([]);
     const config = useConfig() || {};
     const terms = config.terms ? config.terms.split("\n") : [];

     useEffect(() => {
       const populateDefinitions = async() => {
         if (terms.length !== 0) {
           const data = await invoke('getTermDefinitions', { terms: terms });
           setDefinitions(data);
         }
       }

       populateDefinitions();
     }, [terms, invoke, setDefinitions]);

     return (
       <>
         <Text>{terms.join(",")}</Text>
         <Text>{definitions.join(",")}</Text>
       </>
     );
   };
   ```
   ```

## Step 5: Create the definitions table

![The definition table](https://dac-static.atlassian.com/platform/forge/images/definition-macro-step-5.png?_v=1.5800.1742)

In this step, you'll add a [Dynamic Table](/platform/forge/ui-kit/components/dynamic-table/) to the definitions macro to show the list of terms side by side with a list of definitions.

It can be useful when building a UI Kit app to group elements together into reusable components.
For this app, we will add a `DefinitionTable` component.

1. Create a new file named `definition-table.jsx` in `src/frontend`.
2. In this file, create a component named `DefinitionTable`. This component renders a list of definitions in a table. Also add an object called `head`, which will contain the data for the headers of `DefinitionTable`. Also remember to import `invoke` for later.

   ```
   ```
   1
   2
   ```



   ```
   import React from 'react';
   import { DynamicTable } from "@forge/react";
   import { invoke } from '@forge/bridge';

   // Render the table headers
   const head = {
     cells: [
       {
         key: "term",
         content: "Term",
         isSortable: true,
       },
       {
         key: "definition",
         content: "Definition",
         shouldTruncate: true,
         isSortable: true,
       },
       {
         key: "buttons", // Additional column for buttons on each row
         content: "",
         shouldTruncate: true,
         isSortable: true,
       },
     ],
   };

   // Render the Definition Table
   export const DefinitionTable = ({ terms, definitions }) => {
     return (
       <DynamicTable
         head={head}
         emptyView="No terms provided, please press Edit on the app and add terms in the Configuration box"
       />
     );
   };
   ```
   ```
3. In the same file, add an object called `row` - this will be used to render each row in the definitions table. Also add a `createKey` function that generates a key for each term in the row.

   ```
   ```
   1
   2
   ```



   ```
   // create a key for each term
   const createKey = (input) => {
     return input ? input.replace(/\s/g, "") : input; // remove whitespace
   }

   // Render the Definition Table
   export const DefinitionTable = ({ terms, definitions }) => {
     const rows = terms.map((term, index) => ({
       key: `row-${index}-${term}`,
       cells: [
         {
           key: createKey(term),
           content: term
         },
         {
           key: index,
           content: definitions[index],
           colSpan: 2,
         },
       ],
     }));

     return (
       <DynamicTable
         head={head}
         rows={rows}
         emptyView="No terms provided, please press Edit on the app and add terms in the Configuration box"
       />
     );
   }
   ```
   ```
4. Add an import for the `DefinitionTable` component in `src/frontend/index.jsx`.

   ```
   ```
   1
   2
   ```



   ```
   import { DefinitionTable } from './definition-table';
   ```
   ```
5. Add this table to your existing macro in `src/frontend/index.jsx`.

   ```
   ```
   1
   2
   ```



   ```
   return (
     <>
       <DefinitionTable terms={terms} definitions={definitions}/>
     </>
   );
   ```
   ```

For reference, a finished version of the `src/frontend/definition-table.jsx` file is available on [the tutorial repository](https://bitbucket.org/atlassian/definitions-macro-tutorial/src/master/src/frontend/definition-table.jsx).

## Step 6: Allow a user to add a definition

![The usable definition table](https://dac-static.atlassian.com/platform/forge/images/definition-macro-step-6a.png?_v=1.5800.1742)

At this stage, there's still no data stored for the app. In this step, you'll add the
ability to store a definition for a term.

1. Add a `saveDefinition` method to the `src/resolvers/index.js` file.

   ```
   ```
   1
   2
   ```



   ```
   resolver.define('saveDefinition', async(req) => {
     const { term, definition } = req.payload;
     await kvs.set(termKey(term), { term, definition });
   })
   ```
   ```
2. Add a `removeDefinition` method to the `src/resolvers/index.js` file.

   ```
   ```
   1
   2
   ```



   ```
   resolver.define('removeDefinition', async(req) => {
     let term = req.payload.term;
     await kvs.delete(termKey(term)); 
   })
   ```
   ```
3. In `src/frontend/definition-table.jsx`, within the `DefinitionTable` component, set up React hooks that will be used to open an input modal. This enables a user to provide a definition for a term.

   ```
   ```
   1
   2
   ```



   ```
   const { handleSubmit, register, getFieldId } = useForm();
   const [term, setTerm] = useState('');
   const [definition, setDefinition] = useState('');
   const [loadingState, setLoadingState] = useState(false);

   const [inputIsOpen, setInputIsOpen] = useState(false);
   const openInputModal = () => setInputIsOpen(true);
   const closeInputModal = () => setInputIsOpen(false);
   ```
   ```
4. Also set up React hooks that will be used to open a delete confirmation modal as well. This enables a user to delete a provided definition for a term.

   ```
   ```
   1
   2
   ```



   ```
   const [deleteIsOpen, setDeleteIsOpen] = useState(false);
   const openDeleteModal = () => setDeleteIsOpen(true);
   const closeDeleteModal = () => setDeleteIsOpen(false);
   ```
   ```
5. Add two [Modals](https://developer.atlassian.com/platform/forge/ui-kit/components/modal/) in the return statement of the `DefinitionTable` component. When the user clicks submit for the input modal, the `saveDefinition` resolver callback is invoked in the [Form](https://developer.atlassian.com/platform/forge/ui-kit/components/form/) component and then the modal closed. When the user clicks submit for the delete modal, the `removeDefinition` resolver callback is invoked.

   ```
   ```
   1
   2
   ```



   ```
   return (
     <>
       <DynamicTable
         head={head}
         rows={rows}
         emptyView="No terms provided, please press Edit on the app and add terms in the Configuration box"
         isLoading={loadingState}
       />

       <ModalTransition>
         {inputIsOpen && (
           <Modal onClose={closeInputModal}>
             <Form
                 onSubmit={handleSubmit(submitInput)}
               >
               <ModalHeader>
                 <ModalTitle>{`Add definition for ${term}`}</ModalTitle>
               </ModalHeader>
               <ModalBody>
                 <Label labelFor={getFieldId("definition")}>{`Definition for ${term}`}</Label>
                   <TextArea name="definition" id="definition" defaultValue={definition} {...register("definition", {
                     required: true
                   })} />
               </ModalBody>
               <ModalFooter>
                 <Button appearance="subtle" onClick={closeInputModal}>
                   Cancel
                 </Button>
                 <Button appearance="primary" onClick={closeInputModal} type="submit">
                   Submit
                 </Button> 
               </ModalFooter>
             </Form>
           </Modal>
         )}
       </ModalTransition>

       <ModalTransition>
         {deleteIsOpen && (
           <Modal onClose={closeDeleteModal}>
             <Form
                 onSubmit={handleSubmit(submitDelete)}
               >
               <ModalHeader>
                 <ModalTitle>{`Delete definition for ${term}?`}</ModalTitle>
               </ModalHeader>
               <ModalFooter>
                 <Button appearance="subtle" onClick={closeDeleteModal}>
                   Cancel
                 </Button>
                 <Button appearance="danger" onClick={closeDeleteModal} type="submit">
                   Delete
                 </Button> 
               </ModalFooter>
             </Form>
           </Modal>
         )}
       </ModalTransition>
     </>
   );
   ```
   ```
6. Add two submit functions for the input and delete modals respectively within the `DefinitionTable` component.

   ```
   ```
   1
   2
   ```



   ```
   const submitInput = async({ definition }) => {
     setLoadingState(true);
     await invoke('saveDefinition', { term: term, definition: definition })
     setLoadingState(false);
   };

   const submitDelete = async() => {
     setLoadingState(true);
     await invoke('removeDefinition', { term: term })
     setLoadingState(false);
   };
   ```
   ```
7. Create a `generateRow` function that uses [useCallback](https://developer.atlassian.com/platform/forge/ui-kit/#supported-hook-types). This will return the definition of a term if it exists, along with an `Edit` and `Delete` button for modifying the definition. This is formatted using [Inline](https://developer.atlassian.com/platform/forge/ui-kit/components/inline/). If the definition for the term does not exist, it will render an `Add Definition` button. Otherwise, it will render a [Spinner](https://developer.atlassian.com/platform/forge/ui-kit/components/spinner/).

   ```
   ```
   1
   2
   ```



   ```
   const generateRow = useCallback(
   (index, term, generatedDefinition) => {
     let definitionContent = <Spinner />;
     if (generatedDefinition === "") {
       definitionContent = 
         <Button appearance="default" onClick={() => {
           setTerm(term);
           setDefinition("");
           openInputModal();
         }}>
           Add Definition
         </Button>
     } else if (generatedDefinition) {
       definitionContent = 
       <Inline spread="space-between">
         <Text>{generatedDefinition}</Text>
         <ButtonGroup>
           <Button appearance="default" spacing="compact" onClick={() => {
             setTerm(term);
             setDefinition(generatedDefinition);
             openInputModal();
           }}>
             Edit
           </Button>
           <Button appearance="danger" spacing="compact" onClick={() => {
             setTerm(term);
             openDeleteModal();
           }}>
             Delete
           </Button>
         </ButtonGroup>
       </Inline>
     }

     return ({
       key: `row-${index}-${term}`,
       cells: [
         {
           key: createKey(term),
           content: term
         },
         {
           key: index,
           content: definitionContent,
           colSpan: 2,
         },
       ],
     })
   },
   [setTerm, setDefinition, openInputModal, openDeleteModal, createKey, setTerm, setDefinition, openInputModal, openDeleteModal]);
   ```
   ```
8. Add `generateRow` function to the rows variable, so it will be rendered in `<DynamicTable>`.

   ```
   ```
   1
   2
   ```



   ```
   const rows = terms.map((term, index) => (
     generateRow(index, term, definitions[index])
   ));
   ```
   ```
9. Stop tunneling your app and deploy it by running:

## Next steps

At this point your app is able display a list of terms and their associated definitions.
The app stores definitions in the storage service, and shares these across all
the instances of the macro in the site.

Explore Forge storage in further detail over the following pages:

* Read [App storage options](/platform/forge/storage/) for an overview of the different ways Forge
  apps can store data
* Read about the [Key-Value Store](/platform/forge/runtime-reference/storage-api) which
  details the JavaScript API.
* Learn more about how [Queries](/platform/forge/runtime-reference/storage-api-query) can
  be run against data stored in the Key-Value Store.
* View the [Limits](/platform/forge/platform-quotas-and-limits/#storage-quotas) that apply
  to apps using Forge hosted storage.
