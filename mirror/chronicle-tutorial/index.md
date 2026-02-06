# Build a work and knowledge capture app with Global UI Kit component

EXPERIMENTAL

**EXPERIMENTAL:** Global UI Kit components are currently in an experimental phase. The APIs and features are subject to change without notice and are not recommended for production use. Use these components for testing and feedback purposes only.

This tutorial shows you how to build Chronicle, a work and knowledge capture app for Confluence using Global UI Kit components and the [`confluence:fullPage`](/platform/forge/manifest-reference/modules/confluence-full-page/) module. You'll learn how to:

* Create a full-page Confluence app with sidebar navigation
* Implement CRUD operations with Forge Storage
* Build reusable UI components and custom hooks
* Add client-side search functionality
* Handle routing between views
* Create modal forms for data entry

This tutorial builds a functional subset of the Chronicle app. The [complete Chronicle example app](https://bitbucket.org/atlassian/full-page-module-apps/src/main/Global-component-example/) includes additional features such as Jira and Confluence API integration, browse-by-category and browse-by-tags pages, summary reports, edit and knowledge-capture modals, and advanced filtering.

## What you'll build

Chronicle is a productivity app that helps teams log and track work entries in an organized timeline. In this tutorial, you'll build the core features:

* **Log work entries** — Create entries with categories and tags through a modal form
* **View a timeline** — See entries grouped by date with category badges
* **Search instantly** — Filter entries across titles, descriptions, categories, and tags
* **Delete entries** — Remove entries you no longer need
* **Navigate with a sidebar** — Use the Global sidebar component with expandable menu sections for navigation between views

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development. If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

To complete this tutorial, you need:

* The latest version of the Forge CLI: `npm install -g @forge/cli@latest`
* Node.js 18 or later
* An Atlassian cloud developer site

### Set up a cloud developer site

An Atlassian cloud developer site lets you install and test your app. If you don't have one yet:

1. Go to <http://go.atlassian.com/cloud-dev> and create a site using your Atlassian account email.
2. Once your site is ready, log in and complete the setup wizard.

## Create your app

Make sure you run `forge login` before creating your app.

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Enter a name for your app: **chronicle**
4. Select the **UI Kit** category.
5. Select the **Confluence** product.
6. Select the **confluence-global-page-ui-kit** template.
7. Change to the app subdirectory:

## Configure the app manifest

The `manifest.yml` file defines your app's modules, permissions, and resources. Replace the contents of `manifest.yml` with the following:

```
```
1
2
```



```
modules:
  confluence:fullPage:
    - key: chronicle-app
      resource: main
      render: native
      resolver:
        function: resolver
      title: Chronicle
      routePrefix: chronicle
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
permissions:
  scopes:
    - storage:app
```
```

Here's what each section does:

* **`confluence:fullPage`** — Registers a full-page module in Confluence with its own URL route.
* **`routePrefix`** — Sets the URL path prefix for your app (e.g., `/chronicle/timeline`).
* **`function`** — Defines the backend resolver function that handles `invoke()` calls from the frontend.
* **`resources`** — Points to your frontend entry file.
* **`permissions.scopes`** — Grants access to Forge Storage for persisting data.

## Set up the project structure

Create a clean architecture with separated concerns:

1. Create the folder structure:

   ```
   ```
   1
   2
   ```



   ```
   mkdir -p src/frontend/{hooks,utils,constants,ui-components,features/{timeline,modals}}
   ```
   ```
2. Your structure should look like:

   ```
   ```
   1
   2
   ```



   ```
   src/
   ├── index.js
   ├── frontend/
   │   ├── App.jsx
   │   ├── index.jsx
   │   ├── hooks/
   │   │   ├── useTimeline.js
   │   │   └── useRouting.js
   │   ├── constants/
   │   │   └── categories.js
   │   ├── utils/
   │   │   └── dateUtils.js
   │   ├── ui-components/
   │   │   └── EmptyState.jsx
   │   └── features/
   │       ├── timeline/
   │       │   ├── TimelineCard.jsx
   │       │   └── TimelineView.jsx
   │       └── modals/
   │           └── LogWorkModal.jsx
   └── resolvers/
       └── index.js
   ```
   ```

## Create the resolver entry point

The manifest references `index.handler`, which resolves to `src/index.js`. This file re-exports the resolver handler.

Create `src/index.js`:

```
```
1
2
```



```
export { handler } from './resolvers';
```
```

## Create backend resolvers

Backend resolvers handle data storage using the Forge Storage API. They are called from the frontend using `invoke()` from `@forge/bridge`.

Replace `src/resolvers/index.js` with:

```
```
1
2
```



```
import Resolver from '@forge/resolver';
import { storage } from '@forge/api';

const resolver = new Resolver();

/**
 * Get user-specific storage key.
 * Scoping storage per user ensures data isolation.
 */
const getUserStorageKey = (accountId) => `timeline_entries_${accountId}`;

/**
 * Get all timeline entries for the current user.
 * Returns entries sorted by timestamp (newest first).
 */
resolver.define('getTimelineEntries', async (req) => {
  try {
    const accountId = req.context.accountId;
    const storageKey = getUserStorageKey(accountId);
    const entries = await storage.get(storageKey) || [];

    return entries.sort((a, b) =>
      new Date(b.timestamp) - new Date(a.timestamp)
    );
  } catch (error) {
    console.error('Error fetching timeline entries:', error);
    return [];
  }
});

/**
 * Save a new timeline entry.
 * Generates an ID and timestamp if not provided.
 */
resolver.define('saveTimelineEntry', async (req) => {
  const { entry } = req.payload;
  const accountId = req.context.accountId;
  const storageKey = getUserStorageKey(accountId);

  if (!entry || !entry.title || !entry.description || !entry.category) {
    throw new Error('Invalid entry: missing required fields');
  }

  const existingEntries = await storage.get(storageKey) || [];

  const newEntry = {
    ...entry,
    id: entry.id || Date.now().toString(),
    timestamp: entry.timestamp || new Date().toISOString()
  };

  existingEntries.unshift(newEntry);
  await storage.set(storageKey, existingEntries);

  return newEntry;
});

/**
 * Update an existing timeline entry.
 * Preserves the original timestamp.
 */
resolver.define('updateTimelineEntry', async (req) => {
  const { entry } = req.payload;
  const accountId = req.context.accountId;
  const storageKey = getUserStorageKey(accountId);

  const entries = await storage.get(storageKey) || [];
  const index = entries.findIndex(e => e.id === entry.id);

  if (index === -1) {
    throw new Error('Entry not found');
  }

  entries[index] = { ...entry, timestamp: entries[index].timestamp };
  await storage.set(storageKey, entries);

  return entries[index];
});

/**
 * Delete a timeline entry by ID.
 */
resolver.define('deleteTimelineEntry', async (req) => {
  const { entryId } = req.payload;
  const accountId = req.context.accountId;
  const storageKey = getUserStorageKey(accountId);

  const entries = await storage.get(storageKey) || [];
  const filtered = entries.filter(e => e.id !== entryId);
  await storage.set(storageKey, filtered);

  return { success: true, entryId };
});

export const handler = resolver.getDefinitions();
```
```

Key patterns in this resolver code:

* **User-scoped storage** — Each user's entries are stored under a unique key (`timeline_entries_{accountId}`), providing data isolation.
* **`storage.get()` and `storage.set()`** — Read and write data using the Forge Storage API.
* **`req.context.accountId`** — Access the current user's Atlassian account ID from the request context.

## Create constants

### Category constants

Create `src/frontend/constants/categories.js`:

```
```
1
2
```



```
/**
 * Category Constants
 * Defines available categories for work and knowledge entries.
 */

export const WORK_CATEGORIES = [
  'Documentation',
  'Review',
  'Bug Fix',
  'Feature',
  'Research',
  'Automation'
];

export const KNOWLEDGE_CATEGORIES = [
  'Learning',
  'Decision',
  'Blocker',
  'Idea'
];

export const ALL_CATEGORIES = [
  ...WORK_CATEGORIES,
  ...KNOWLEDGE_CATEGORIES
];
```
```

## Create date utilities

Create `src/frontend/utils/dateUtils.js`:

```
```
1
2
```



```
/**
 * Format an ISO timestamp to a readable string.
 * Example: "Jan 23, 3:45 PM"
 */
export const formatTimestamp = (isoString) => {
  const date = new Date(isoString);
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const month = months[date.getMonth()];
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours % 12 || 12;

  return `${month} ${day}, ${displayHours}:${minutes} ${ampm}`;
};

/**
 * Format a Date object as "DD MM YYYY".
 */
export const formatDate = (date) => {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
};

/**
 * Group entries by date for timeline display.
 * Returns an array of { label, entries, sortDate } objects sorted newest first.
 */
export const groupEntriesByDate = (entries) => {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const grouped = {};

  entries.forEach((entry) => {
    const entryDate = new Date(entry.timestamp);
    const entryDay = new Date(
      entryDate.getFullYear(),
      entryDate.getMonth(),
      entryDate.getDate()
    );

    const label = entryDay.getTime() === today.getTime()
      ? 'TODAY'
      : formatDate(entryDay);

    if (!grouped[label]) {
      grouped[label] = { label, entries: [], sortDate: entryDay.getTime() };
    }
    grouped[label].entries.push(entry);
  });

  return Object.values(grouped).sort((a, b) => b.sortDate - a.sortDate);
};
```
```

## Create custom hooks

Custom hooks separate business logic from UI components, keeping your code maintainable and testable.

### useTimeline hook

This hook manages all timeline CRUD operations. It calls the backend resolvers via `invoke()` and manages local state.

Create `src/frontend/hooks/useTimeline.js`:

```
```
1
2
```



```
import { useState, useEffect, useCallback } from 'react';
import { invoke } from '@forge/bridge';

export const useTimeline = () => {
  const [entries, setEntries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  /** Load all timeline entries from backend storage. */
  const loadEntries = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await invoke('getTimelineEntries');
      setEntries(data || []);
    } catch (err) {
      console.error('Error loading timeline:', err);
      setError(err.message || 'Failed to load entries');
    } finally {
      setIsLoading(false);
    }
  }, []);

  /** Create a new timeline entry and add it to the top of the list. */
  const createEntry = useCallback(async (newEntry) => {
    setError(null);
    try {
      const savedEntry = await invoke('saveTimelineEntry', { entry: newEntry });
      setEntries(prev => [savedEntry, ...(prev || [])]);
      return savedEntry;
    } catch (err) {
      console.error('Error saving entry:', err);
      setError(err.message || 'Failed to save entry');
      throw err;
    }
  }, []);

  /** Update an existing entry in place. */
  const updateEntry = useCallback(async (updatedEntry) => {
    setError(null);
    try {
      const savedEntry = await invoke('updateTimelineEntry', { entry: updatedEntry });
      setEntries(prev =>
        prev.map(e => e.id === savedEntry.id ? savedEntry : e)
      );
      return savedEntry;
    } catch (err) {
      console.error('Error updating entry:', err);
      setError(err.message || 'Failed to update entry');
      throw err;
    }
  }, []);

  /** Delete an entry by ID and remove it from state. */
  const deleteEntry = useCallback(async (entryId) => {
    setError(null);
    try {
      await invoke('deleteTimelineEntry', { entryId });
      setEntries(prev => prev.filter(e => e.id !== entryId));
    } catch (err) {
      console.error('Error deleting entry:', err);
      setError(err.message || 'Failed to delete entry');
      throw err;
    }
  }, []);

  // Load entries on mount
  useEffect(() => {
    loadEntries();
  }, [loadEntries]);

  return { entries, isLoading, error, setError, createEntry, updateEntry, deleteEntry };
};
```
```

### useRouting hook

This hook manages navigation between views using the Forge `view.createHistory()` API. The `confluence:fullPage` module supports client-side routing through the `routePrefix` defined in the manifest.

Create `src/frontend/hooks/useRouting.js`:

```
```
1
2
```



```
import { useState, useEffect, useCallback } from 'react';
import { view } from '@forge/bridge';

const VALID_ROUTES = ['timeline', 'about', 'browse/categories', 'browse/tags'];

/** Extract a valid route name from a URL pathname. */
const getRouteFromPath = (pathname) => {
  const route = pathname.replace(/^\/+|\/+$/g, '') || 'timeline';
  return VALID_ROUTES.includes(route) ? route : 'timeline';
};

export const useRouting = () => {
  const [currentView, setCurrentView] = useState('timeline');

  /** Navigate to a specific route. */
  const navigateTo = useCallback(async (route) => {
    try {
      const history = await view.createHistory();
      history.push(route);
      setCurrentView(route);
    } catch (error) {
      console.error('Error navigating:', error);
      setCurrentView(route);
    }
  }, []);

  // Set up routing on mount: read the initial route and listen for changes
  useEffect(() => {
    const setupRouting = async () => {
      try {
        const history = await view.createHistory();

        // Set initial route from the current URL
        const initialRoute = getRouteFromPath(history.location.pathname);
        setCurrentView(initialRoute);

        // Listen for browser navigation (back/forward)
        history.listen((location) => {
          const route = getRouteFromPath(location.pathname);
          setCurrentView(route);
        });
      } catch (error) {
        console.error('Error setting up routing:', error);
        setCurrentView('timeline');
      }
    };

    setupRouting();
  }, []);

  return { currentView, navigateTo };
};
```
```

Key concepts:

* **`view.createHistory()`** — Creates a history object for managing routes within your app. This uses the `routePrefix` from the manifest to scope URLs.
* **`history.push(route)`** — Navigates to a new route without a full page reload.
* **`history.listen()`** — Listens for route changes triggered by browser back/forward buttons or sidebar navigation.

## Create UI components

### EmptyState component

This component displays when no entries exist, prompting the user to create their first entry.

Create `src/frontend/ui-components/EmptyState.jsx`:

```
```
1
2
```



```
import React from 'react';
import { Box, Stack, Text, Heading, Button, xcss } from '@forge/react';

export const EmptyState = ({
  title = 'No entries yet',
  message = 'Start by logging your first work entry!',
  onLogWork
}) => {
  return (
    <Box xcss={xcss({ padding: 'space.400', textAlign: 'center' })}>
      <Stack space="space.200" alignInline="center">
        <Text size="large">📋</Text>
        <Heading size="medium">{title}</Heading>
        <Text color="color.text.subtlest">{message}</Text>
        {onLogWork && (
          <Button appearance="primary" onClick={onLogWork}>
            Log Work
          </Button>
        )}
      </Stack>
    </Box>
  );
};
```
```

### TimelineCard component

Each timeline entry is rendered as a card with a category badge, timestamp, title, description, tags, and a delete action.

Create `src/frontend/features/timeline/TimelineCard.jsx`:

```
```
1
2
```



```
import React, { useState } from 'react';
import { Box, Stack, Inline, Text, Lozenge, Button, xcss } from '@forge/react';
import { formatTimestamp } from '../../utils/dateUtils';

/**
 * Map category names to Lozenge appearance values.
 */
const getCategoryAppearance = (category) => {
  const map = {
    'Documentation': 'inprogress',
    'Review': 'new',
    'Bug Fix': 'removed',
    'Feature': 'success',
    'Research': 'moved',
    'Automation': 'default',
    'Learning': 'success',
    'Decision': 'inprogress',
    'Blocker': 'removed',
    'Idea': 'new'
  };
  return map[category] || 'default';
};

const cardStyles = xcss({
  backgroundColor: 'elevation.surface',
  borderRadius: 'border.radius',
  borderColor: 'color.border',
  borderStyle: 'solid',
  borderWidth: 'border.width',
  padding: 'space.200',
  marginBottom: 'space.200'
});

export const TimelineCard = ({ entry, onDelete }) => {
  const [showActions, setShowActions] = useState(false);
  const categoryValue = typeof entry.category === 'object'
    ? entry.category.value
    : entry.category;

  return (
    <Box
      xcss={cardStyles}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <Stack space="space.100">
        {/* Header: category badge, timestamp, and actions */}
        <Inline space="space.100" spread="space-between" alignBlock="center">
          <Inline space="space.100" alignBlock="center">
            <Lozenge appearance={getCategoryAppearance(categoryValue)}>
              {categoryValue}
            </Lozenge>
            <Text size="small" color="color.text.subtlest">
              {formatTimestamp(entry.timestamp)}
            </Text>
          </Inline>
          {showActions && (
            <Button
              appearance="subtle"
              spacing="compact"
              onClick={() => onDelete && onDelete(entry)}
            >
              Delete
            </Button>
          )}
        </Inline>

        {/* Title */}
        <Text weight="medium">{entry.title}</Text>

        {/* Description (only if different from title) */}
        {entry.description && entry.description !== entry.title && (
          <Text>{entry.description}</Text>
        )}

        {/* Tags */}
        {entry.tags && entry.tags.length > 0 && (
          <Inline space="space.100">
            {entry.tags.map((tag) => (
              <Text key={tag} size="small" color="color.link">
                #{tag}
              </Text>
            ))}
          </Inline>
        )}
      </Stack>
    </Box>
  );
};
```
```

### TimelineView component

This component groups entries by date and renders a `TimelineCard` for each entry. It shows an `EmptyState` when there are no entries.

Create `src/frontend/features/timeline/TimelineView.jsx`:

```
```
1
2
```



```
import React, { useMemo } from 'react';
import { Stack, Text } from '@forge/react';
import { TimelineCard } from './TimelineCard';
import { EmptyState } from '../../ui-components/EmptyState';
import { groupEntriesByDate } from '../../utils/dateUtils';

export const TimelineView = ({ entries, onDelete, onLogWork }) => {
  // Show empty state when there are no entries
  if (entries.length === 0) {
    return (
      <EmptyState
        title="No entries found"
        message="Start by logging your first work entry!"
        onLogWork={onLogWork}
      />
    );
  }

  // Memoize grouped entries to avoid recalculating on every render
  const groupedByDate = useMemo(() => groupEntriesByDate(entries), [entries]);

  return (
    <Stack space="space.400">
      {groupedByDate.map((dateGroup) => (
        <Stack key={dateGroup.label} space="space.200">
          <Text size="small" weight="semibold" color="color.text.subtlest">
            {dateGroup.label}
          </Text>
          <Stack space="space.200">
            {dateGroup.entries.map((entry) => (
              <TimelineCard
                key={entry.id}
                entry={entry}
                onDelete={onDelete}
              />
            ))}
          </Stack>
        </Stack>
      ))}
    </Stack>
  );
};
```
```

## Create the Log Work modal

The modal uses Forge UI Kit form components (`Form`, `useForm`, `Label`, `Select`, `TextArea`) to create a structured entry form.

Create `src/frontend/features/modals/LogWorkModal.jsx`:

```
```
1
2
```



```
import React from 'react';
import {
  Modal,
  ModalHeader,
  ModalTitle,
  ModalBody,
  ModalFooter,
  ModalTransition,
  Form,
  Label,
  Textfield,
  TextArea,
  Select,
  Button,
  Stack,
  Text,
  RequiredAsterisk,
  useForm
} from '@forge/react';
import { WORK_CATEGORIES } from '../../constants/categories';

export const LogWorkModal = ({ isOpen, onClose, onSubmit }) => {
  const { handleSubmit, register, getFieldId } = useForm();

  const onFormSubmit = async (data) => {
    try {
      // Select returns { value, label } — extract the string value
      const categoryValue = typeof data.category === 'object'
        ? data.category.value
        : data.category;

      // Parse comma-separated tags
      const tags = data.tags
        ? data.tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
        : [];

      const entry = {
        id: Date.now().toString(),
        type: 'work',
        category: categoryValue,
        title: data.description.substring(0, 60),
        description: data.description,
        timestamp: new Date().toISOString(),
        tags: tags.length > 0 ? tags : undefined
      };

      if (onSubmit) {
        await onSubmit(entry);
      }
      onClose();
    } catch (error) {
      console.error('Error saving entry:', error);
    }
  };

  const categoryOptions = WORK_CATEGORIES.map(cat => ({
    label: cat,
    value: cat
  }));

  return (
    <ModalTransition>
      {isOpen && (
        <Modal onClose={onClose}>
          <ModalHeader>
            <ModalTitle>Log Work</ModalTitle>
          </ModalHeader>

          <Form onSubmit={handleSubmit(onFormSubmit)}>
            <ModalBody>
              <Stack space="space.200">
                {/* Description field */}
                <Stack space="space.100">
                  <Label labelFor={getFieldId('description')}>
                    Description <RequiredAsterisk />
                  </Label>
                  <TextArea
                    {...register('description', { required: true })}
                    placeholder="What are you working on?"
                  />
                </Stack>

                {/* Category field */}
                <Stack space="space.100">
                  <Label labelFor={getFieldId('category')}>
                    Category <RequiredAsterisk />
                  </Label>
                  <Select
                    {...register('category', { required: true })}
                    placeholder="Select Category"
                    options={categoryOptions}
                  />
                </Stack>

                {/* Tags field */}
                <Stack space="space.100">
                  <Label labelFor={getFieldId('tags')}>
                    Tags
                  </Label>
                  <Textfield
                    {...register('tags')}
                    placeholder="e.g. react, api, performance"
                  />
                  <Text size="small" color="color.text.subtlest">
                    Comma-separated keywords to categorize your work
                  </Text>
                </Stack>
              </Stack>
            </ModalBody>

            <ModalFooter>
              <Button appearance="subtle" onClick={onClose}>
                Cancel
              </Button>
              <Button appearance="primary" type="submit">
                Log Work
              </Button>
            </ModalFooter>
          </Form>
        </Modal>
      )}
    </ModalTransition>
  );
};
```
```

Key form patterns:

* **`useForm()`** — Forge UI Kit hook that provides `handleSubmit`, `register`, and `getFieldId` for form management.
* **`register('fieldName', { required: true })`** — Registers a form field with validation rules.
* **`getFieldId('fieldName')`** — Returns an ID to connect `<Label>` to its form field for accessibility.
* **`<Label>` component** — Forge UI Kit form fields don't have a built-in label prop. You must use the separate `<Label>` component with `labelFor`.

## Build the main App component

The `App` component brings everything together: sidebar navigation, routing, search, and the timeline view.

Create `src/frontend/App.jsx`:

```
```
1
2
```



```
import React, { useState, useMemo } from 'react';
import {
  Stack,
  Inline,
  Box,
  Text,
  Heading,
  Textfield,
  SectionMessage,
  Button,
  xcss,
  Global
} from '@forge/react';

// Custom Hooks
import { useTimeline } from './hooks/useTimeline';
import { useRouting } from './hooks/useRouting';

// Feature Components
import { TimelineView } from './features/timeline/TimelineView';
import { LogWorkModal } from './features/modals/LogWorkModal';

export const App = () => {
  // Business logic hooks
  const {
    entries,
    isLoading,
    error,
    setError,
    createEntry,
    deleteEntry
  } = useTimeline();

  const { currentView } = useRouting();

  // Local UI state
  const [searchText, setSearchText] = useState('');
  const [isLogWorkModalOpen, setIsLogWorkModalOpen] = useState(false);

  // Client-side search filtering
  const filteredEntries = useMemo(() => {
    if (!searchText || !searchText.trim()) return entries;
    const search = searchText.toLowerCase().trim();
    return entries.filter(entry =>
      entry.title?.toLowerCase().includes(search) ||
      entry.description?.toLowerCase().includes(search) ||
      entry.category?.toLowerCase().includes(search) ||
      entry.tags?.some(tag => tag.toLowerCase().includes(search))
    );
  }, [entries, searchText]);

  // Event handlers
  const handleSubmitEntry = async (newEntry) => {
    try {
      await createEntry(newEntry);
      setIsLogWorkModalOpen(false);
    } catch (err) {
      // Error already handled in hook
    }
  };

  const handleDeleteEntry = async (entry) => {
    try {
      await deleteEntry(entry.id);
    } catch (err) {
      // Error already handled in hook
    }
  };

  return (
    <Global>
      {/* Sidebar Navigation */}
      <Global.Sidebar forYouUrl={'timeline'}>
        {/* ExpandMenuItem creates a collapsible section with nested links */}
        <Global.ExpandMenuItem label="Browse">
          <Global.LinkMenuItem label="By Category" href="browse/categories" />
          <Global.LinkMenuItem label="By Tags" href="browse/tags" />
        </Global.ExpandMenuItem>
        <Global.LinkMenuItem label="About Chronicle" href="about" />
      </Global.Sidebar>

      {/* Main Content Area */}
      <Global.Main>
        <Box xcss={xcss({ padding: 'space.400' })}>
          <Stack space="space.400">
            {/* Error display */}
            {error && (
              <SectionMessage appearance="error">
                <Text>{error}</Text>
                <Button appearance="subtle" onClick={() => setError(null)}>
                  Dismiss
                </Button>
              </SectionMessage>
            )}

            {/* Route: About page */}
            {currentView === 'about' ? (
              <Stack space="space.200">
                <Heading size="large">About Chronicle</Heading>
                <Text>
                  Chronicle is a work and knowledge capture app built with
                  Forge UI Kit Global components. Use the sidebar to navigate
                  back to your Timeline.
                </Text>
              </Stack>

            /* Route: Browse by Category */
            ) : currentView === 'browse/categories' ? (
              <Stack space="space.200">
                <Heading size="large">Browse by Category</Heading>
                <Text>
                  View your work entries grouped by category. This page
                  demonstrates nested sidebar navigation using ExpandMenuItem.
                </Text>
              </Stack>

            /* Route: Browse by Tags */
            ) : currentView === 'browse/tags' ? (
              <Stack space="space.200">
                <Heading size="large">Browse by Tags</Heading>
                <Text>
                  Discover and filter entries by tags. This page demonstrates
                  nested sidebar navigation using ExpandMenuItem.
                </Text>
              </Stack>
            ) : (
              <>
                {/* Route: Timeline (default) */}
                {/* Header with search and add button */}
                <Inline spread="space-between" alignBlock="center">
                  <Heading size="large">Timeline</Heading>
                  <Inline space="space.200" alignBlock="center">
                    <Box xcss={xcss({ maxWidth: '250px' })}>
                      <Textfield
                        placeholder="Search entries..."
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                      />
                    </Box>
                    {searchText && searchText.trim().length > 0 && (
                      <Button
                        appearance="subtle"
                        onClick={() => setSearchText('')}
                      >
                        Clear
                      </Button>
                    )}
                    <Button
                      appearance="primary"
                      onClick={() => setIsLogWorkModalOpen(true)}
                    >
                      + Log Work
                    </Button>
                  </Inline>
                </Inline>

                {/* Timeline entries */}
                {isLoading ? (
                  <Text>Loading timeline...</Text>
                ) : (
                  <TimelineView
                    entries={filteredEntries}
                    onDelete={handleDeleteEntry}
                    onLogWork={() => setIsLogWorkModalOpen(true)}
                  />
                )}
              </>
            )}
          </Stack>

          {/* Log Work Modal */}
          <LogWorkModal
            isOpen={isLogWorkModalOpen}
            onClose={() => setIsLogWorkModalOpen(false)}
            onSubmit={handleSubmitEntry}
          />
        </Box>
      </Global.Main>
    </Global>
  );
};
```
```

Key concepts in the App component:

* **`<Global>`** — The root wrapper for apps using Global UI Kit components.
* **`<Global.Sidebar>`** — Renders a persistent sidebar. The `forYouUrl` prop sets the URL for the built-in "For You" tab.
* **`<Global.ExpandMenuItem>`** — Creates a collapsible section in the sidebar. It can only contain `<Global.LinkMenuItem>` children and cannot be nested inside another `ExpandMenuItem`.
* **`<Global.LinkMenuItem>`** — Adds a navigation link to the sidebar. The `href` corresponds to a route handled by `useRouting`.
* **`<Global.Main>`** — The main content area that adjusts alongside the sidebar.
* **`useMemo`** — Memoizes the search filter so entries are only recalculated when `entries` or `searchText` change.

## Create the frontend entry point

Update `src/frontend/index.jsx`:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler from '@forge/react';
import { App } from './App';

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Deploy and install your app

1. Deploy your app:

   ```
   ```
   1
   2
   ```



   ```
   forge deploy -e development
   ```
   ```
2. Install it to your Confluence site:

   ```
   ```
   1
   2
   ```



   ```
   forge install --site <your-site>.atlassian.net --product confluence -e development
   ```
   ```
3. Find your app's URL by running:

   ```
   ```
   1
   2
   ```



   ```
   forge environments list
   ```
   ```

   Full page modules can be accessed using this URL format:

```
```
1
2
```



```
https://<your-site>.atlassian.net/forge-apps/a/<app-id>/e/<forge-environment-id>/r/<route-prefix>/<app-route>
```
```

**Where to find each value:**

* **`<your-site>`**: Your site name
* **`<app-id>`**: The UUID from your `app.id` in `manifest.yml` (if in ARI format like `ari:cloud:ecosystem::app/UUID`, use only the UUID section)
* **`<forge-environment-id>`**: The UUID of the environment that the app is installed on.
  Run `forge environments list` to find the UUID of the desired environment.
* **`<route-prefix>`**: Defined in your manifest under `routePrefix`
* **`<app-route>`**: Optional - if your app code contains routing, it will appear under the `<app-route>` section of the URL.

**Example:**

```
```
1
2
```



```
https://example.atlassian.net/forge-apps/a/21e590df-79e6-40dd-9ee4-ba2c7b678f26/e/9f699e8b-33f1-4fa7-bd48-c5fdc44fa4c2/r/ui-kit
```
```

## Test your app

1. Navigate to your app URL in your browser.
2. You should see the Chronicle timeline with an empty state and a "Log Work" button.
3. Click **+ Log Work** to open the modal:
   * Enter a description (e.g., "Updated API documentation for v2 endpoints")
   * Select a category (e.g., "Documentation")
   * Add tags (e.g., "api, docs")
   * Click **Log Work** to save
4. Your entry should appear on the timeline under "TODAY".
5. Create a few more entries with different categories and tags.
6. Try the search bar:
   * Type a category name like "Bug" to filter entries
   * Type a tag to find matching entries
   * Click **Clear** to reset
7. Hover over a timeline card to reveal the **Delete** button.
8. In the sidebar, expand the **Browse** section to see nested links:
   * Click **By Category** to navigate to the category browsing page
   * Click **By Tags** to navigate to the tag browsing page
9. Click **About Chronicle** in the sidebar to test navigation, then navigate back using the **For You** tab.

## Explore the complete Chronicle app

This tutorial builds the core functionality of Chronicle. The [complete example app](https://bitbucket.org/atlassian/forge-chronicle-example) includes these additional features:

* **Edit entries** — Modal for updating existing work entries
* **Capture knowledge** — Separate modal for logging learnings, decisions, and blockers
* **Browse by category** — View entries grouped by work and knowledge categories
* **Browse by tags** — Discover and filter entries by tags
* **Summary reports** — Generate weekly and monthly reports with metrics, charts, and AI summaries
* **Jira integration** — Auto-fetch Jira issue details (summary, status, priority) when linking a ticket
* **Confluence integration** — Auto-fetch Confluence page metadata when linking a page
* **Advanced filtering** — Filter by category dropdown, date range, and tags with a filter banner
* **Quick action cards** — Shortcut cards for common actions
* **Expandable sidebar menus** — Nested navigation with `Global.ExpandMenuItem`

## Next steps

Now that you have the core of Chronicle working, try extending it:

1. **Add an edit modal** — Create an `EditWorkModal` component that pre-fills form fields with existing entry data using `useForm({ defaultValues })`.
2. **Add knowledge capture** — Create a `CaptureKnowledgeModal` that uses `KNOWLEDGE_CATEGORIES` for a separate entry type.
3. **Add browse views** — Create category and tag browsing pages and add them to the sidebar using `Global.ExpandMenuItem`.
4. **Integrate with Jira** — Use `api.asUser().requestJira()` in your resolvers to fetch issue details when a ticket ID is provided.
5. **Add summary reports** — Create a `generateReport` resolver that aggregates entries by date range and calculates metrics.

Or clone the [complete example app](https://bitbucket.org/atlassian/forge-chronicle-example) to see all of these features implemented.

## Troubleshooting

| Issue | Solution |
| --- | --- |
| App not loading | Check browser console for errors. Verify manifest syntax with `forge lint` |
| Storage not persisting | Ensure you're using user-scoped keys (`getUserStorageKey`) |
| Search not filtering | Verify `searchText` is included in the `useMemo` dependency array in `App.jsx` |
| Module not found errors | Check all import paths are correct relative to file location |
| Deployment fails | Run `npm install` to ensure dependencies are installed |
| Modal not opening | Ensure `isLogWorkModalOpen` state is toggled and `<LogWorkModal>` is rendered inside `<Global.Main>` |
| Route changes not reflected | Verify `useRouting` hook is calling `view.createHistory()` and `history.listen()` |

## Key learnings

* **Global UI Kit** — `<Global>`, `<Global.Sidebar>`, and `<Global.Main>` provide a full-page app layout with persistent navigation. `<Global.ExpandMenuItem>` adds collapsible menu sections for hierarchical navigation
* **Clean architecture** — Separating hooks, utilities, and components makes code maintainable
* **Custom hooks** — Business logic in hooks (`useTimeline`, `useRouting`) keeps components clean and reusable
* **Forge forms** — `useForm()`, `register()`, and `<Label>` with `getFieldId()` provide accessible form handling
* **Forge Storage** — User-scoped storage keys provide data isolation per user
* **Client-side search** — Filtering with `useMemo` provides instant results without backend queries
* **Routing** — `view.createHistory()` enables client-side navigation within a `confluence:fullPage` module

---
