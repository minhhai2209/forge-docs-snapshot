# Forge bridge showFlag

**Normal info flag:**

```
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
