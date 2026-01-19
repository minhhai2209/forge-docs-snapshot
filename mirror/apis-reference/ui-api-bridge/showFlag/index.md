# Forge bridge showFlag

**Normal info flag:**

```
```
1
2
```



```
import { showFlag } from "@forge/bridge";
showFlag({
  id: "info-normal",
  title: "Information",
  type: "info",
  description: "This is an informational message.",
  isAutoDismiss: true,
});
```
```

**Bold info flag:**

```
```
1
2
```



```
import { showFlag } from "@forge/bridge";
showFlag({
  id: "info-bold",
  title: "No team members found",
  type: "info",
  appearance: "info", // Bold appearance, no dismiss button with a close icon
  description: "Add teammates to get started.",
  actions: [
    {
      text: "Add teammates",
      onClick: () => console.log("Navigate to team page"),
    },
    {
      text: "Skip",
      onClick: () => console.log("User skipped"),
    },
  ],
});
```
```
