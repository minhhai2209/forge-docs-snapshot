# Example apps for Bitbucket

Before you begin exploring these example apps, you'll need to set up the Forge CLI first.
[Learn more about getting started](/platform/forge/getting-started/).

Once the Forge CLI is up and running, clone an example app repository to explore and customize it locally.
Each repository's `README.md` file contains quickstart instructions and other details about the app.

For more information, refer to our getting started guides for building
[Bitbucket](/platform/forge/build-a-hello-world-app-in-bitbucket/),
[Confluence](/platform/forge/build-a-hello-world-app-in-confluence/),
[Jira](/platform/forge/build-a-hello-world-app-in-jira/),
and [Jira Service Management](/platform/forge/build-a-hello-world-app-in-jira-service-management/) apps.
Our [tutorials](/platform/forge/tutorials-and-guides/) and [guides](/platform/forge/guides/)
also offer useful information for common tasks.

The `forge register` command creates a unique app ID in the `manifest.yml` file
and links the ID to the current developer. Forge apps can currently only be deployed
and installed by the developer who is linked to the app.

The content on this page is written with standard cloud development in mind. To learn about developing
for Atlassian Government Cloud, go to our
[Atlassian Government Cloud developer portal](/platform/framework/agc/).

This app adds a [pull request card](/platform/forge/manifest-reference/modules/bitbucket-repository-pull-request-card/) that displays pull requests related to the one you're viewing, based on the Jira tickets mentioned in the title of the current pull request.

* **Code:** [Related pull request app](https://bitbucket.org/atlassian/forge-bitbucket-related-prs/src/main/)
* **Atlassian app:** Bitbucket
* **Modules:** `bitbucket:repoPullRequestCard`
* **Custom UI:** none
* **UI Kit:**
  * `DynamicTable`, `Link`, `Lozenge`, and `Text` components
* **Other use-cases:**
  * Calls the Bitbucket REST API with `asApp` to retrieve relevant pull requests using BBQL (using `route` as well as `routeFromAbsolute`).

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/70df33c7-2f7f-4148-b923-bf8c15d7e874?signature=AYABeEISIzclVWrl1S3oNZ%2FAdSYAAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YB4jajVLNDKiiCJ00Q6f%2F7EAAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDA6G3Cc5iFLa23t%2FUwIBEIA7Eht64LD2mZPhE%2FegCfGNGeNVXBhYbLIqn7YdhsOQf6zI%2FyCvkPgDSYegUds%2FMCJbqZdJD9Jgci7UKZIAB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregEo1dZ493VFY1lJ0Ent3yMAAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMEJqlqNFAay6WOCEzAgEQgDvjF0N6O4Ar3yx%2FKQpCtybb3%2Bw3rJd54i2Y1o6ljdreBUYly2UoDnZPEmN2atCea5QplN%2BNDJLrG6CNhgAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCAV6uhQbWQoLUDq6%2B4hZraHMAAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAyDWeE08xkKH4cfxsMCARCAO476tVrFhFMcDswbdM%2ByRLdvisfxEGoU4rdlCUYFroYkTO68paWy%2F8o%2FYuAd0xvHBZu3Qk2wPglR2DVsAgAAAAAMAAAQAAAAAAAAAAAAAAAAAGK4dzKnPlnd1GkOO%2BTiiPj%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADIoZ6KMOFdnSS%2FLfm22GN%2Fd5aF5uLSUPnQu2vbf7KJs1Adje3OM5QHs0C9cDI25y8JSlQvFv21rG4zGhIHGhvW5Xh8%3D&product=bitbucket).

This app adds a [repository settings page](/platform/forge/manifest-reference/modules/bitbucket-repository-settings-menu-page/) that displays metadata changes to your repository.
To capture changes to the repository, it subscribes to the [Bitbucket repository updated event](/platform/forge/events-reference/bitbucket/#repository-updated).

* **Code:** [Repository metadata audit log](https://bitbucket.org/atlassian/forge-bitbucket-repository-metadata-audit-log/src/main/)
* **Atlassian app:** Bitbucket
* **Modules:** `bitbucket:repoSettingsMenuPage`, `trigger`
* **Events:** `avi:bitbucket:updated:repository`
* **Custom UI:** none
* **UI Kit:**
  * `Code`, `DynamicTable`, `Inline`, `Spinner`, `Strong`, `Text`, and `User` components
* **Other use-cases:**
  * Uses Forge hosted storage to store repository metadata changelog entries.

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/942aaacd-ca0f-4366-ba20-e897c53f79c9?signature=AYABeOjhTUVo9kJqLaSLULx1yzoAAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YBh3v2cS3q7D3ZAyzw8n6pzAAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDBWfleR4CLlwtps%2FdgIBEIA7veUCbyN5UFpqcsbEp8SZbgljm%2FP37ZNoUPHwVY%2FSKXzPavn%2F5dZq%2F4o94w7ZB%2Frfe%2F1FlyhJg4caL24AB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregEEbdsliWEpkkBZU2Zmz2VwAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMYvEDkzB9hoDkztddAgEQgDuznSNqQ10UZy5npmCbcxssEtLfDl0xIoBlHIrrWlWyKi9hnrlMdKMuGP7ObW1s3V1D5bxqogZr45oviAAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCAeiaWbskJCHX3uNmG5bDxWkAAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwQYCTKI4R3GoXdkB8CARCAO9znUnOwsBFHcUIsXHmrRL3r0SmIb191NVG5HdzO%2BACz7PD8ikuyqbeox9avgRaRf2goLCU1YFGDsG0gAgAAAAAMAAAQAAAAAAAAAAAAAAAAAHdR4c3VEiadUf4jtDlxv%2B7%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADJmXLQs7%2Fb8rleOpVbWHWoEIjTe7kcPsNd8kqCOoO3WU6bo79LP87QeuSw5BO%2BVymtcvhPl5IY%2F%2Fv%2B3jx4DxkCXjpA%3D&product=bitbucket).

## Classic merge checks as custom merge checks

This app implements Bitbucket's [classic merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/#Merge-checks)
as [custom merge checks](/platform/forge/manifest-reference/modules/bitbucket-merge-check/).
It uses a [repository settings page](/platform/forge/manifest-reference/modules/bitbucket-repository-settings-menu-page/) to configure merge check conditions.

This app does not replace Bitbucket's existing merge checks.
It demonstrates how existing merge checks can be seamlessly transformed into custom merge checks.

* **Code:** [Bitbucket official merge checks](https://bitbucket.org/atlassian/bitbucket-official-merge-checks/src/main/)
* **Atlassian app:** Bitbucket
* **Modules:**: `bitbucket:mergeCheck`, `bitbucket:repoSettingsMenuPage`
* **Custom UI:** none
* **UI Kit:**
  * `Box`, `ErrorMessage`, `Form`, `FormFooter`, `FormHeader`, `FormSection`, `Inline`, `Label`, `LoadingButton`,
    `RequiredAsterisk`, `SectionMessage`, `Spinner`, `Strong`, `Text`, and `Textfield` components
* **Other use-cases:**
  * Calls the Bitbucket REST API with `asApp` to retrieve data required to evaluate merge checks.
  * Uses Forge hosted storage to store the check configuration for each repository.

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/7ce7b774-dc57-45b6-b81c-cd4f8c9d54bd?signature=AYABeM38ouYzSr7AxXnn2hiSwRoAAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YBeEo%2Bu9Y259tDoxo5if%2FU2QAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDFiLOivyhDdwtgQspgIBEIA73ajKWVKPaU5%2BH23AxM6BmDpm0t27PF%2Bxf%2FpsGFZlrf1oR7J8CMFuDQLuTh9hxkfZRiFsNWg1BpIdtIoAB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregHJ%2FjU9lDwewABnUHYvxet%2FAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMJ0wBoU5RabzWkPvTAgEQgDs2sVx%2B0vhhtmXWjQ7qrdnFwqmqbduZ7ihERROsnwqtDWiEoEF9zdcENfRt7pdKl%2F%2BpQaoOiJGshfz4HwAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCATaU0Td5uDZkEBQd67H5WfMAAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAyOvLxvLT4vfAH1YZECARCAOwlNUBMOWZuqHhf8R6rjHLw4ODLD1XrV3zWqqDDwVtkkPzuPTW1tmPapr6pKobxRMov6Fnez%2FXETCN16AgAAAAAMAAAQAAAAAAAAAAAAAAAAAIKdkN4JoiaEFdGKPOcy37D%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADITQ9f5Bn1qdRj0GM2%2FBKk%2F9uXpCQyJC9gvRTU4JatQ8CN8n0BlU32v84jEaF4yYW1MQMb716t1eRttxVIyn2wcpR4%3D&product=bitbucket).

## Pull request title validator with custom merge checks

This app creates a [custom merge check](/platform/forge/manifest-reference/modules/bitbucket-merge-check/)
that can block a pull request from being merged if the title does not contain a string configured in the
[repository settings page](/platform/forge/manifest-reference/modules/bitbucket-repository-settings-menu-page/).

* **Code:** [Pull request title validator](https://bitbucket.org/atlassian/forge-bitbucket-pull-request-title-validator/src/main/)
* **Atlassian app:** Bitbucket
* **Modules:**: `bitbucket:mergeCheck`, `bitbucket:repoSettingsMenuPage`
* **Custom UI:** none
* **UI Kit:**
  * `ErrorMessage`, `Form`, `FormFooter`, `Inline`, `Label`, `LoadingButton`, `RequiredAsterisk`, `Spinner`, `Text`, and `Textfield` components
* **Other use-cases:**
  * Calls the Bitbucket REST API with `asApp` to retrieve the pull request the check was invoked for.
  * Uses Forge hosted storage to configure the expected prefix.

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/95aae29f-91fa-4473-976a-aa6c62a9ab87?signature=AYABeClp44BsyW4ykB8Bexf0nPIAAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YBgxaHnh9lgu6LFcRpLoxQ1QAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDIc3CxNNZRNJSLEOOgIBEIA7yA444hpvU9y0LjylblXdShAu%2FEysCisCl3cI4eYACPAdFVbUycf3SjiKeDFp%2BgfvTeTTR3JKOrVA%2F14AB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregFFh2e5AP5AxLqCW8BoqT%2BFAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMNKqHVKNCiRtARNixAgEQgDu91yusCeo5QImlBi8MPDh7YEjiQJSLmMfQStIimx4xefQDtl41Vw%2FPlP27KCai2JQB%2Bx%2FPHlXvQc%2FV6QAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCAd2aD%2FB3EGeBUqOmciM219wAAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwlKZNa8t9XPeWuMkYCARCAO2kg8ocpIFosdBzh%2FCR7CG6P93UEmIh2QBxu2nTfh7JajdjANc1ULfTKjJ%2FZn0cmfs9XBaESXdi8wXq7AgAAAAAMAAAQAAAAAAAAAAAAAAAAACJHtTimiHYkGup5irF%2BDDz%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADKti7ouLlon9H4NyqmllMqUhWvtWteNXHsFEkUY%2BbocjVqrI7eTPBDRxyNO0OpVjyFYJQ3AxvidtRgVtdlfQbqkD1U%3D&product=bitbucket).

## Pull request secrets scanner with custom merge checks

This app creates a [custom merge check](/platform/forge/manifest-reference/modules/bitbucket-merge-check/)
that can block a pull request from being merged when there are secrets detected in your repository.

* **Code:** [Pull request secrets scanner](https://bitbucket.org/atlassian/forge-bitbucket-secrets-scanner/src/main/)
* **Atlassian app:** Bitbucket
* **Modules:**: `bitbucket:mergeCheck`
* **Custom UI:** none
* **UI Kit:** none
* **Other use-cases:**
  * Uses [Bitbucket Security Secret Scanner pipe](https://bitbucket.org/atlassian/git-secrets-scan/src/master/README.md) to detect secrets in your repository.
  * Uses the `asApp` method to invoke the Bitbucket REST API, retrieving the pull request associated with the initiated check.
  * Uses the `asApp` method to invoke the Bitbucket REST API, aiming to fetch the code insights report produced by the Bitbucket Security Secret Scanner.

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/6775e812-af1d-4f21-a4bb-239592238106?signature=AYABeDDZr6Ctr6jEDwsynVgsG0oAAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YBlFxPcufzqiFCxzt5pqyyAgAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDM%2F94x72HdroUoYWQAIBEIA7%2BrfZwuCyg%2BTDwZKOjW8818wgkDEHJixATiJKyb7WBPW4i0lMuDeaRIGCpq0I4wiCc5Cz323h7mQQujkAB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregHLndg9ZvQnxwIteFX0cbH9AAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMKXqgG2nlhxPNkLIoAgEQgDtPVy9ElT5ShwULwRMS3nflAaKF1sIHDzC0mZnhdyA%2FF8skl7GMBEJYwGgVVimaVmuMEYdLcU%2BbwNqabAAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCATj%2BKCE%2B%2Be5g0d9I8VY1uvQAAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAy0OcqGpop1UebibJ8CARCAO2nHzlSfCO1zfAYCKdM7x%2F%2B1RVYrzL6EnB3IDw94jHVw3S0yi2Holvm7b3ex2hWy924DWNya%2FM7Z710mAgAAAAAMAAAQAAAAAAAAAAAAAAAAADVQr5L5836kS28rmIJOc5n%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADKnvsMJXCxLJYY74119vXNKOqKozaUCtavnQLHGU3DVD9kBeIcjFIf%2BrUj%2BZqzMJuiq4qjBVzwNd3hKeEVmWls49vc%3D&product=bitbucket).

## Dynamic Pipelines provider tutorial app

This app is a reference implementation of [Orchestrate your builds using Dynamic Pipelines](/platform/forge/orchestrate-your-builds-using-dynamic-pipelines)
tutorial, it adds a step to the `default` pipeline.

* **Code:** [Dynamic Pipelines provider tutorial app](https://bitbucket.org/atlassian/forge-bbc-dynamic-pipelines-provider-tutorial)
* **Atlassian app:** Bitbucket
* **Modules:**: `bitbucket:dynamicPipelinesProvider`
* **Custom UI:** none
* **UI Kit:** none
* **Other use-cases:**
  * Uses the `asApp` method to invoke the Bitbucket REST API, retrieving the diff stat for a commit the pipeline is requested to run at.

To try this app out, you can [install it into your workspace](https://developer.atlassian.com/console/install/6b1b78bc-4a1d-4018-bfc9-e9be2381b4e9?signature=AYABeDo3ZchCqqUEV8XW8R6bSQ8AAAADAAdhd3Mta21zAEthcm46YXdzOmttczp1cy1lYXN0LTE6NzA5NTg3ODM1MjQzOmtleS83ZjcxNzcxZC02OWM4LTRlOWItYWU5Ny05MzJkMmNhZjM0NDIAuAECAQB4KZa3ByJMxgsvFlMeMgRb2S0t8rnCLHGz2RGbmY8aB5YBX61yF6Qf1zZqhcUV2a3WoQAAAH4wfAYJKoZIhvcNAQcGoG8wbQIBADBoBgkqhkiG9w0BBwEwHgYJYIZIAWUDBAEuMBEEDH4OEhvXhRmb%2B1OY7gIBEIA7hGvsZGUCBmBunEIwsUHEMjethw8YO5rldo%2Btn81LpPtRAn2sOV8a5pqOMlgRL7mvqiSRXPlkyvNlJJoAB2F3cy1rbXMAS2Fybjphd3M6a21zOmV1LXdlc3QtMTo3MDk1ODc4MzUyNDM6a2V5LzU1OWQ0NTE2LWE3OTEtNDdkZi1iYmVkLTAyNjFlODY4ZWE1YwC4AQICAHhHSGfAZiYvvl%2F9LQQFkXnRjF1ris3bi0pNob1s2MiregGeaHACb7omGmejslf3U4hiAAAAfjB8BgkqhkiG9w0BBwagbzBtAgEAMGgGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQM8s5vf%2BmgAnR967LxAgEQgDsGSj8cuRNIM4tphbNOGno4Jrklcs6RABSEv2XlxDSABH6EXpxi7gIgkxUMDaASPJxe4lRETC%2FC1E2wnwAHYXdzLWttcwBLYXJuOmF3czprbXM6dXMtd2VzdC0yOjcwOTU4NzgzNTI0MzprZXkvM2M0YjQzMzctYTQzOS00ZmNhLWEwZDItNDcyYzE2ZWRhZmRjALgBAgIAePadDOCfSw%2BMRVmOIDQhHhGooaxQ%2FiwGaLB334n1X9RCAcd07pJ%2F7EgDlQIP5nLOUp8AAAB%2BMHwGCSqGSIb3DQEHBqBvMG0CAQAwaAYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAzCdXtNF6LMzQSK2pQCARCAO9%2Flt136SQavqNI3%2F6NaKnwlu0Pr%2F3rL51GKprgy8K24uKXMtNBDdEiZ3j4MpLtfKABI1edsszb8SrDxAgAAAAAMAAAQAAAAAAAAAAAAAAAAAHNyS0fekyeLSJmHN3asttP%2F%2F%2F%2F%2FAAAAAQAAAAAAAAAAAAAAAQAAADJ02IXgQNEsG4YPpBGlPurmJLOGdJ3wlHX3tsjs3Z8Kc5VXc%2BgB%2BVR858qDlgzFotj5WURz1JZRHYT%2BtcD2SZGYv5Y%3D&product=bitbucket).
