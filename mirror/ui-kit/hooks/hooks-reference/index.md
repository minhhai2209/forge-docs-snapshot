# UI Kit hooks

Custom hooks and other React hooks can be used but may not behave the same in UI Kit's lifecycle.

Hooks that require direct DOM access, such as `useRef` for DOM elements, `useLayoutEffect`, `useImperativeHandle` and `useInsertionEffect`,
will have limited functionality since UI Kit does not have access to the underlying DOM nodes.
