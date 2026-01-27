# Bitbucket dynamic pipelines provider

The `bitbucket:dynamicPipelinesProvider` module defines a Dynamic Pipelines provider that can be
configured in the context of a repository or a workspace. Dynamic Pipelines provider generates
pipeline definition at runtime using dynamic logic, as opposed to the static Pipelines configuration file.

## System hierarchy

For the purpose of this explanation, the term “resources” refers to either a Repository or a Workspace;
Projects are not currently supported, but will be added in the future. Resources exist hierarchically,
e.g. a Repository exists “under” a Workspace. Dynamic pipelines leverages this hierarchy in order to
enable flexibility to be added to pipeline workflows at every level.

For any given Workspace, there can be many `bitbucket:dynamicPipelinesProvider` modules installed.
However, each resource within that workspace can only have a single `dynamicPipelinesProvider`
selected to execute for that resource.

**For example:**

* You may have four separate repositories within a workspace - Repos A, B, C, & D
  * Those repositories may all have unique `bitbucket:dynamicPipelinesProvider` modules configured
    for each of them (Providers A, B, C, & D), or they may share/reuse providers in any configuration
    the user wants.
  * However, each **individual** repository can only have a **single**
    `bitbucket:dynamicPipelinesProvider` module configured for it.
* In **addition**, a `bitbucket:dynamicPipelinesProvider` module can **also** be configured against
  other resources above those repositories in the hierarchy (e.g. the parent workspace).
  * Just like at the repository level, only a single `bitbucket:dynamicPipelinesProvider` can be
    configured for those resources (e.g. the parent workspace).
* At runtime, these `bitbucket:dynamicPipelinesProvider` modules at different levels of the hierarchy
  create a chain, all of which will be executed for the respective pipeline run.
  * This allows multiple levels of dynamic execution to occur, in a specific order, one at each
    level of the hierarchy.

Each Dynamic Pipelines provider acts as a transforming function of the pipeline configuration: it
takes a valid pipeline configuration along with pipeline metadata as input, and generates a valid
pipeline configuration as output. This *“Pipeline-In|Pipeline-Out”* design is what enables multiple
providers to be chained together up the hierarchy.

This chain will always be executed in a *“bottom up”* order, starting with the static `.yml` configuration
stored in the repository, then the repository level `bitbucket:dynamicPipelinesProvider` and finally,
the workspace level `bitbucket:dynamicPipelinesProvider`. This ensures that policies and rules put
in place “higher” in the hierarchy are able to take precedence over ones implemented “lower” in the hierarchy.

![Dynamic Pipeline execution hierarchy](https://dac-static.atlassian.com/platform/forge/images/bitbucket-dynamic-pipelines-provider-execution-hierarchy.png?_v=1.5800.1800)

* initial workflow is read from the static `bitbucket-pipelines.yml` file.
* if [shared workflow](https://support.atlassian.com/bitbucket-cloud/docs/share-pipelines-configurations/)
  is used, `import` statements are resolved from the static `bitbucket-pipelines.yml` files of the
  external repositories.
* if a repository-level dynamic pipeline is configured, it is executed and transforms the workflow.
* if a workspace-level dynamic pipeline is configured, it is executed and transforms the workflow.

The output of this chain is the final pipeline workflow which is then consumed by Bitbucket Pipelines
to generate and run a pipeline using that definition.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` or `i18n object` | Yes | The name of the provider which is displayed throughout the UI.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `function` | `string` | Required if `endpoint` is not set | A reference to the `key` of the `function` that defines the dynamic pipeline behavior.  *This function must return a [dynamic pipelines configuration result](#response-payload).* |
| `endpoint` | `string` | Required if `function` is not set | A reference to the `endpoint` that specifies the remote back end to invoke a dynamic pipeline if you are using [Forge Remote](/platform/forge/remote) to integrate with a remote back end.  *This endpoint must return a [dynamic pipelines configuration result](#response-payload).* |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

### Example

The snippet below defines a Dynamic Pipelines provider.

```
```
1
2
```



```
modules:
  bitbucket:dynamicPipelinesProvider:
    - key: my-bitbucket-dynamic-pipelines-provider
      name: My first Dynamic Pipelines provider
      description: This is my first provider
      function: dynamic-pipelines-provider
  function:
    - key: dynamic-pipelines-provider
      handler: index.dynamicPipelinesProviderFunction
```
```

## Invocation scenarios

Whenever a `bitbucket:dynamicPipelinesProvider` module is invoked, an event payload will be provided
as an argument to the Forge function. This payload provides the identifiers of the workspace,
repository, pipeline configuration, and some additional metadata.

A `bitbucket:dynamicPipelinesProvider` module is invoked by Bitbucket Pipelines in two scenarios:

* To generate a list of available pipeline definitions that a user can run against a particular branch or tag.
* To generate the configuration for a pipeline in order to run it in response to a particular event.

The only responsibility of the function registered against the `bitbucket:dynamicPipelinesProvider`
module is that it returns a well-defined response payload every time the Bitbucket Forge
infrastructure invokes it.

This result produced by each invocation of the `bitbucket:dynamicPipelinesProvider` module is handled
and stored by the Bitbucket infrastructure, there is no requirement for the Forge app to store it,
or send the response back to a specific Bitbucket API. The Dynamic Pipelines provider is only expected
to calculate and return result in the correct response format.

If any exceptions are thrown when executing the Dynamic Pipelines provider logic, the result will be
treated as a failure. Bitbucket Pipelines may retry the request to the Dynamic Pipelines provider
in such case.

## Get pipeline definitions

This scenario is triggered, for example, when user opens the **Run pipeline** dialog in the UI and
selects a branch.

![The list of pipeline definitions in the Run pipeline dialog](https://dac-static.atlassian.com/platform/forge/images/bitbucket-dynamic-pipelines-provider-run-pipeline-dialog.png?_v=1.5800.1800)

The Dynamic Pipelines provider is expected to return all pipeline definitions applicable for the
provided context. From this set of results, the user can then select a definition to run.

### Invocation payload

| Parameter | Type | Description |
| --- | --- | --- |
| `workspace` | `string` | The Bitbucket UUID of the workspace which contains the repository the pipeline definitions are being requested for. |
| `repository` | `string` | The Bitbucket UUID of the repository the pipeline definitions are being requested for. |
| `creator` | `string` | The Bitbucket UUID of the user who is requesting pipeline definitions. |
| `trigger` | `string` | Equals to `definitions` when requesting pipeline definitions. |
| `target` | [`PipelineTarget`](#pipelinetarget) | The information about the entity the pipeline definitions are being requested against: commit, ref (branch or tag), or pull request. |
| `pipelines_configuration` | [`PipelinesConfiguration`](#pipelinesconfiguration) | The pipelines configuration populated from previous steps in the process. |

#### Example

Request to get pipeline definitions with a single resolved `default` definition:

```
```
1
2
```



```
{
  "workspace": "{308ce669-576d-4fa7-b4d4-15e8171f0c8c}",
  "repository": "{2fc883c6-3dee-4e73-a354-ccee4bd77938}",
  "creator": "{cda97709-b1a9-4544-9a8d-750f1b3a12c4}",
  "trigger": "definitions",
  "target": {
    "type": "pipeline_commit_target",
    "commit": {
      "hash": "e34ad324d1e4334777dca3e56c04eba36c2a68c6"
    }
  },
  "pipelines_configuration": {
    "pipelines": {
      "default": [
        {
          "step": {
            "name": "Foo",
            "script": [
              "echo Bar"
            ]
          }
        }
      ]
    }
  }
}
```
```

### `PipelineTarget`

| Parameter | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the pipeline target:   * `pipeline_commit_target` – target pointing at a commit * `pipeline_ref_target` – target pointing at a ref (branch or tag) * `pipeline_pullrequest_target` – target pointing at a pull request |
| `commit` | [`Commit`](#commit) | The Git commit the target is pointing at. |
| `ref_type`  *Only for **ref target*** | `string` | The type of the ref: |
| `ref_name`  *Only for **ref target*** | `string` | The name of the branch or tag. |
| `source`  *Only for **pull request target*** | `string` | The name of the source branch of the pull request. |
| `destination`  *Only for **pull request target*** | `string` | The name of the destination branch of the pull request. |
| `destination_commit`  *Only for **pull request target*** | [`Commit`](#commit) | The tip commit of the destination branch of the pull request. |
| `pullrequest`  *Only for **pull request target*** | [`PullRequest`](#pullrequest) | The pull request the target is pointing at. |

#### `Commit`

| Parameter | Type | Description |
| --- | --- | --- |
| `hash` | `string` | The SHA-1 hash identifying the Git commit. |

#### `PullRequest`

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `integer` | The id of the pull request identifying it within the repository. |

#### Examples

Commit target:

```
```
1
2
```



```
{
  "type": "pipeline_commit_target",
  "commit": {
    "hash": "ca0beaeaf9c4d6ef07e9abf2de0d262014f23dd5"
  }
}
```
```

Ref target:

```
```
1
2
```



```
{
  "type": "pipeline_ref_target",
  "commit": {
    "hash": "ca0beaeaf9c4d6ef07e9abf2de0d262014f23dd5"
  },
  "ref_type": "branch",
  "ref_name": "master"
}
```
```

Pull request target:

```
```
1
2
```



```
{
  "type": "pipeline_pullrequest_target",
  "commit": {
    "hash": "6486ba02730e5a90394cbd5d3f27aa84ccabb1e4"
  },
  "source": "feature",
  "destination": "master",
  "destination_commit": {
    "hash": "ca0beaeaf9c4d6ef07e9abf2de0d262014f23dd5"
  },
  "pullrequest": {
    "id": 239
  }
}
```
```

### `PipelinesConfiguration`

This is a complex type which covers all the features and properties supported in the
[Bitbucket Pipelines YML configuration file](https://support.atlassian.com/bitbucket-cloud/docs/bitbucket-pipelines-configuration-reference/).
Simply speaking, this is a JSON version of what you can possibly configure in `bitbucket-pipelines.yml`
file, with some minor nuances.

| Parameter | Type | Description |
| --- | --- | --- |
| `image` | [`Image`](#image) | The parameters of the Docker image to use when running steps of the pipeline. |
| `options` | [`Options`](#options) | Overrides for the default values applied to all steps in all declared pipelines. |
| `clone` | [`Clone`](#clone) | Settings for cloning a repository into a container. |
| `definitions` | [`Definitions`](#definitions) | The definitions of caches and services used in the declared pipelines. |
| `pipelines` | [`Pipelines`](#pipelines) | The pipeline definitions, grouped by the trigger type. |
| `labels` | [`Labels`](#labels) | Additional key value data supplied in the configuration YAML. |

### `Image`

The parameters of the Docker image.

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `string` | The name of the Docker image which may or may not include registry URL, tag, and digest value. |
| `run-as-user` | `integer` | The UID of a user in the docker image to run as. Overrides image's default user, specified user UID must be an existing user in the image with a valid home directory. |
| `username` | `string` | The username to use when fetching the Docker image. |
| `password` | `string` | The password to use when fetching the Docker image. |
| `aws` | [`AwsImageProperties`](#awsimageproperties) | The properties specific to images stored in Amazon Elastic Container Registry (AWS ECR). |

#### `AwsImageProperties`

The properties specific to images stored in Amazon Elastic Container Registry (AWS ECR).

| Parameter | Type | Description |
| --- | --- | --- |
| `access-key` | `string` | The access key for Amazon Elastic Container Registry (AWS ECR). |
| `secret-key` | `string` | The secret key for Amazon Elastic Container Registry (AWS ECR). |
| `oidc-role` | `string` | OIDC role with access to private Docker images hosted in Amazon Elastic Container Registry (AWS ECR). |

#### Examples

Simple image:

```
```
1
2
```



```
{
  "name": "atlassian/default-image:3",
  "run-as-user": 1001
}
```
```

Image with basic authentication:

```
```
1
2
```



```
{
  "name": "my.docker.registry/my-project/my-repo/test-image:latest",
  "username": "$DOCKER_REGISTRY_USERNAME",
  "password": "$DOCKER_REGISTRY_PASSWORD"
}
```
```

AWS ECR image with credentials:

```
```
1
2
```



```
{
  "name": "aws_account_id.dkr.ecr.us-west-2.amazonaws.com/my-repository:tag",
  "aws": {
    "access-key": "$AWS_ACCESS_KEY",
    "secret-key": "$AWS_SECRET_KEY"
  }
}
```
```

AWS ECR image with OpenID Connect:

```
```
1
2
```



```
{
  "name": "aws_account_id.dkr.ecr.us-west-2.amazonaws.com/my-repository:tag",
  "aws": {
    "oidc-role": "arn:aws:iam::aws_account_id:role/pipelines-ecr-access"
  }
}
```
```

### `Options`

Global options allow to override the default values applied to all steps in all declared pipelines.

| Parameter | Type | Description |
| --- | --- | --- |
| `docker` | `boolean` | Enables Docker service for every step. |
| `max-time` | `integer` | The maximum time a step can execute for, in minutes. |
| `size` | `string` | The size of the step, sets the amount of resources allocated: |

#### Example

```
```
1
2
```



```
{
  "docker": true,
  "max-time": 60,
  "size": "2x"
}
```
```

### `Clone`

Settings for cloning a repository into a container.

| Parameter | Type | Description |
| --- | --- | --- |
| `enabled` | `boolean` | Enables cloning of the repository. |
| `depth` | `string` | The depth argument of Git clone operation.  It can be either a number or `full` value. |
| `lfs` | `boolean` | Enables the download of files from LFS storage when cloning. |
| `tags` | `boolean` | Enables fetching tags when cloning. |
| `strategy` | `string` | Set the Git clone strategy to use:   * `fetch` is the new default strategy * `clone` is the legacy strategy |
| `filter` | `string` | The partial clone filter argument of Git fetch operation.  It can be either `blob:none` or `tree:<n>` value. |
| `sparse-checkout` | [`SparseCheckout`](#sparsecheckout) | Git sparse checkout settings |
| `skip-ssl-verify` | `boolean` | Disables SSL verification during Git clone operation, allowing the use of self-signed certificates. |

#### `SparseCheckout`

The properties of Git sparse checkout mode.

| Parameter | Type | Description |
| --- | --- | --- |
| `enabled` | `boolean` | Enables sparse checkout. |
| `cone-mode` | `boolean` | Controls whether to use cone-mode or non-cone-mode. |
| `patterns` | `array` | List of `string` patterns to include in sparse checkout. The patterns should be directories or gitignore-style patterns based on the cone-mode settings. |

#### Example

```
```
1
2
```



```
{
  "depth": "3",
  "enabled": true,
  "lfs": true,
  "skip-ssl-verify": true
}
```
```

### `Definitions`

The definitions of caches and services used in the declared pipelines.

| Parameter | Type | Description |
| --- | --- | --- |
| `caches` | `map` | A map of custom cache definitions.  In each map record, the key is the cache *name*, the value is an object of type [`Cache`](#cache). |
| `services` | `map` | A map of custom service definitions.  In each map record, the key is the service *name*, the value is an object of type [`Service`](#service). |

#### `Cache`

A definition of a custom cache.

| Parameter | Type | Description |
| --- | --- | --- |
| `path` | `string` | Path to the directory to be cached, can be absolute or relative to the clone directory. |
| `key` | [`CacheKey`](#cachekey) | Cache key properties. |

#### `CacheKey`

Describes the set of files to generate the cache key.

| Parameter | Type | Description |
| --- | --- | --- |
| `files` | `array` | Checksum of these file paths will be used to generate the cache key.  Each item is a `string` path to a file or glob pattern of files in the repository which form the cache key. |

#### `Service`

A definition of a custom service.

| Parameter | Type | Description |
| --- | --- | --- |
| `image` | [`Image`](#image) | The parameters of the Docker image to use for the service. |
| `memory` | `integer` | Memory limit for the service container, in megabytes. |
| `variables` | `map` | A map of environment variables passed to the service container.  In each map record, the key is the environment variable *name*, the value is its *value* to assign. |
| `type` | `string` | The type of the service container:   * `docker` — specifies Docker service container to run Docker-in-Docker. |

#### Examples

Definitions of caches:

```
```
1
2
```



```
{
  "caches": {
    "simple-cache": {
      "path": "/cache/a"
    },
    "cache-with-key": {
      "key": {
        "files": [
          "dependencies.lock"
        ]
      },
      "path": "/cache/b"
    }
  }
}
```
```

Definitions of services:

```
```
1
2
```



```
{
  "services": {
    "service-a": {
      "image": {
        "name": "my.docker.registry/service-a-image:latest",
        "username": "$DOCKER_REGISTRY_USERNAME",
        "password": "$DOCKER_REGISTRY_PASSWORD",
        "run-as-user": 1111
      },
      "memory": 128,
      "type": "docker",
      "variables": {
        "FOO": "BAR",
        "BAZ": "QUX"
      }
    },
    "service-b": {
      "image": {
        "name": "sample/service-b-image:latest"
      },
      "variables": {
        "HELLO": "WORLD"
      }
    }
  }
}
```
```

### `Pipelines`

The pipeline definitions, grouped by the trigger type.

| Parameter | Type | Description |
| --- | --- | --- |
| `default` | [`Pipeline`](#pipeline) | Default pipeline runs on every push except for tags unless a branch-specific pipeline is defined. |
| `branches` | `map` | A map of branch-specific build pipelines.  In each map record, the key is the branch *glob pattern*, the value is an object of type [`Pipeline`](#pipeline). |
| `tags` | `map` | A map of tag-specific build pipelines.  In each map record, the key is the tag *glob pattern*, the value is an object of type [`Pipeline`](#pipeline). |
| `pull-requests` | `map` | A map of pull-request-specific build pipelines.  In each map record, the key is the pull request source branch *glob pattern*, the value is an object of type [`Pipeline`](#pipeline). |
| `custom` | `map` | A map of pipelines that can only be triggered manually or be scheduled.  In each map record, the key is the custom pipeline *name*, the value is an object of type [`CustomPipeline`](#custompipeline). |

### `Pipeline`

Pipeline definition is an `array` of objects wrapped into a single-value map with their type as the key:

* [`step`](#step) — individual pipeline step
* [`parallel`](#parallel) — declares steps in the parallel group to run concurrently
* [`stage`](#stage) — a logical group of steps to run sequentially

#### Example

A pipeline with a step, followed by a stage with two steps, followed by a parallel group with two steps:

```
```
1
2
```



```
[
  {
    "step": {
      "name": "Just a step",
      "script": [
        "echo This is just a step"
      ]
    }
  },
  {
    "stage": {
      "name": "A stage",
      "steps": [
        {
          "step": {
            "name": "Step 1 in stage",
            "script": [
              "echo This is the first step of a stage"
            ]
          }
        },
        {
          "step": {
            "name": "Step 2 in stage",
            "script": [
              "echo This is the second step of a stage"
            ]
          }
        }
      ]
    }
  },
  {
    "parallel": {
      "steps": [
        {
          "step": {
            "name": "Parallel step 1",
            "script": [
              "echo This is the first step of a parallel group"
            ]
          }
        },
        {
          "step": {
            "name": "Parallel step 2",
            "script": [
              "echo This is the second step of a parallel group"
            ]
          }
        }
      ]
    }
  }
]
```
```

### `CustomPipeline`

Custom pipeline definition additionally allows another named item to be declared in the array before
all steps and/or stages of the pipeline:

* [`variables`](#custompipelinevariables) — variables for the custom pipeline

#### `CustomPipelineVariables`

An `array` of variables for the custom pipeline, each item of which is of
[CustomPipelineVariable](#custompipelinevariable) type.

#### `CustomPipelineVariable`

Properties of the custom pipeline variable.

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `string` | The name of the variable. |
| `allowed-values` | `array` | A list of values that are allowed for the variable.  Each item is a `string` variable value. |
| `default` | `string` | The default value of the variable. |
| `description` | `string` | The description of the variable shown to the user. |

#### Example

A custom pipeline with variables declaration and a step that uses these variables:

```
```
1
2
```



```
[
  {
    "variables": [
      {
        "name": "Var"
      },
      {
        "name": "VarWithDefaultValue",
        "default": "Fallback value when user didn't provide one",
        "description": "Example of a variable with default value"
      },
      {
        "name": "VarWithAllowedValues",
        "default": "foo",
        "allowed-values": [
          "foo",
          "bar",
          "baz"
        ]
      }
    ]
  },
  {
    "step": {
      "name": "Print variables",
      "script": [
        "echo Var: $Var",
        "echo VarWithDefaultValue: $VarWithDefaultValue",
        "echo VarWithAllowedValues: $VarWithAllowedValues"
      ]
    }
  }
]
```
```

### `Step`

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `string` | The name of the step. |
| `max-time` | `string` | The maximum time a step can execute for, in minutes. |
| `size` | `string` | The size of the step, sets the amount of resources allocated: |
| `runs-on` | `array` | Required labels of a runner to run the step.  Each item is a `string` label of a runner. |
| `trigger` | `string` | The trigger used for the pipeline step: |
| `image` | [`Image`](#image) | The parameters of the Docker image to use when running a step. |
| `condition` | [`Condition`](#condition) | The condition to execute the step. |
| `clone` | [`Clone`](#clone) | Settings for cloning a repository into a container. |
| `artifacts` | [`Artifacts`](#artifacts) | Step artifacts settings. |
| `caches` | `array` | List of caches enabled for the step  Each item is a *cache name* referring to a cache defined under global `definitions`. |
| `services` | `array` | List of services enabled for the step  Each item is a *service name* referring to a service defined under global `definitions`. |
| `deployment` | `string` | The deployment environment for the step. |
| `fail-fast` | `boolean` | Stop the parent parallel group in case this step fails. |
| `oidc` | `boolean` | Enables the use of OpenID Connect to connect a pipeline step to a resource server. |
| `script` | `array` | List of commands that are executed in sequence.  Each item is either a `string` shell command, or an object of type [`Pipe`](#pipe). |
| `after-script` | `array` | List of commands to execute after the step succeeds or fails.  Each item is either a `string` shell command, or an object of type [`Pipe`](#pipe). |

#### `Condition`

The condition to execute a step or a stage.

| Parameter | Type | Description |
| --- | --- | --- |
| `changesets` | [`ChangesetsCondition`](#changesetscondition) | Condition on the changesets involved in the pipeline. |

#### `ChangesetsCondition`

| Parameter | Type | Description |
| --- | --- | --- |
| `includePaths` | `array` | Condition which holds only if any of the modified files match any of the specified patterns.  Each item is a glob pattern to match the file path. |

#### `Artifacts`

| Parameter | Type | Description |
| --- | --- | --- |
| `download` | `boolean` | Enables downloading of all available artifacts at the start of a step. |
| `paths` | `array` | List of step artifacts.  Each item is a `string` glob pattern for the path to the artifacts. |

#### `Pipe`

| Parameter | Type | Description |
| --- | --- | --- |
| `pipe` | `string` | The full pipe identifier. |
| `variables` | `map` | A map of environment variables passed to the pipe container.  In each map record, the key is the environment variable *name*, the value is either a `string` value or an `array` of values to assign to it. |

#### Examples

A manually triggered step which uses custom caches and services:

```
```
1
2
```



```
{
  "name": "Manually triggered deployment step with caches and services",
  "trigger": "manual",
  "deployment": "test",
  "caches": [
    "simple-cache",
    "cache-with-key"
  ],
  "services": [
    "service-a",
    "service-b"
  ],
  "script": [
    "echo Deploying to test environment..."
  ]
}
```
```

A step with custom size which makes use of a pipe and after-script:

```
```
1
2
```



```
{
  "step": {
    "name": "A step with custom size, a pipe call, and after-script",
    "size": "2x",
    "script": [
      "echo I will call a pipe now...",
      {
        "pipe": "atlassian/slack-notify:2.2.0",
        "variables": {
          "FOO": "BAR"
        }
      }
    ],
    "after-script": [
      "echo This step is about to finish"
    ]
  }
}
```
```

A step which conditionally runs if certain files have been updated:

```
```
1
2
```



```
{
  "step": {
    "name": "Conditional step",
    "condition": {
      "changesets": {
        "includePaths": [
          "foo/*.bar",
          "qux/**"
        ]
      }
    },
    "script": [
      "echo Some interesting files have been changed"
    ]
  }
}
```
```

### `Parallel`

| Parameter | Type | Description |
| --- | --- | --- |
| `fail-fast` | `boolean` | Stop the whole parallel group in case one of its steps fails. |
| `steps` | `array` | List of steps in the parallel group to run concurrently.  Each item is an object of type [`Step`](#step) wrapped into a single-value map with `step` as the key. |

#### Example

```
```
1
2
```



```
{
  "parallel": {
    "fail-fast": true,
    "steps": [
      {
        "step": {
          "name": "Parallel step 1",
          "script": [
            "echo Run first parallel operation..."
          ]
        }
      },
      {
        "step": {
          "name": "Parallel step 2",
          "script": [
            "echo Run second parallel operation..."
          ]
        }
      }
    ]
  }
}
```
```

### `Stage`

| Parameter | Type | Description |
| --- | --- | --- |
| `name` | `string` | The name of the stage. |
| `condition` | [`Condition`](#condition) | The condition to execute the stage. |
| `deployment` | `string` | The deployment environment for the stage. |
| `trigger` | `string` | The trigger used for the pipeline stage: |
| `steps` | `array` | List of steps in the stage.  Each item is an object of type [`Step`](#step) wrapped into a single-value map with `step` as the key. |

#### Example

A conditional deployment stage with two steps:

```
```
1
2
```



```
{
  "name": "Conditional deployment stage",
  "deployment": "staging",
  "trigger": "automatic",
  "condition": {
    "changesets": {
      "includePaths": [
        "staging/*.conf",
        "global/**"
      ]
    }
  },
  "steps": [
    {
      "step": {
        "name": "Stage step 1",
        "script": [
          "echo Run first stage operation..."
        ]
      }
    },
    {
      "step": {
        "name": "Stage step 2",
        "script": [
          "echo Run second stage operation..."
        ]
      }
    }
  ]
}
```
```

### `Labels`

Labels represent additional free-form key-value data supplied in the configuration YAML.

The total size of `labels` map should not exceed 10 KB.

#### Example

A 3 levels deep map declaring 4 labels.

```
```
1
2
```



```
{
  "label": "foo",
  "bar": {
    "sub_label": "baz",
    "qux": {
      "sub_sub_label": "quux"
    },
    "another_sub_label": "corge"
  }
}
```
```

### Response payload

The Dynamic Pipelines provider is expected to modify (or retain) the configuration passed in the
`pipelines_configuration` parameter and then return the outcome back. Returning exactly what was
passed to the dynamic pipeline provider is a valid response, and is the expected behaviour when
no modifications are required.

| Parameter | Type | Description |
| --- | --- | --- |
| `pipelines_configuration` | [`PipelinesConfiguration`](#pipelinesconfiguration) | The pipelines configuration to be returned. |

## Get configuration for a pipeline

This scenario is triggered in response to an event, such as:

* commit pushed
* pull request created or updated
* user requested to run specific pipeline manually
* a pipeline was requested to run on user-configured schedule

The Dynamic Pipelines provider is expected to return a pipeline configuration containing a definition
matching the provided selector. In certain cases Dynamic Pipelines provider may return a configuration
with no matching definitions.

### Invocation payload

| Parameter | Type | Description |
| --- | --- | --- |
| `workspace` | `string` | The Bitbucket UUID of the workspace which contains the repository the pipeline configuration is being requested for. |
| `repository` | `string` | The Bitbucket UUID of the repository the pipeline configuration is being requested for. |
| `creator` | `string` | The Bitbucket UUID of the user who is requesting to run a pipeline. |
| `trigger` | `string` | The type of the trigger which initiated the request to run a pipeline, one of:   * `push` — commit was pushed to the repository, or a pull request was created or updated * `manual` — user manually requested to run a pipeline * `schedule` — a pipeline requested to run on user-configured schedule * `parent_step` - a pipeline requested to run from another pipeline (a parent step) |
| `trigger_context` | [`TriggerContext`](#triggercontext) | Additional information relating to the trigger that initiated the request to run a pipeline. |
| `target` | [`PipelineTargetWithSelector`](#pipelinetarget-with-selector) | The information about the entity the pipeline configuration is being requested against: commit, ref (branch or tag), or pull request. |
| `pipeline` | `string` | The Bitbucket UUID of the pipeline the configuration is being requested for. |
| `build_number`  *Only for **manual** and **schedule** trigger* | `integer` | The build number of the pipeline.  *Not included when `trigger` equals `push`.* |
| `created_on` | `date-time` | The date and time when the pipeline was created, in ISO 8601 timestamp format. |
| `pipelines_configuration` | [`PipelinesConfiguration`](#filtered-pipelinesconfiguration) | The pipelines configuration filtered down to just the pipeline definition matching the specified `target`. It is possible for this to be empty if there are no existing pipeline configurations that match the specified `target`. |

#### Example

Request to get definition of a pipeline in response to a commit pushed to `master` branch of the
repository and with a single matched branch-specific `mas*` pipeline definition from the previously
discovered configuration (e.g. in the static `bitbucket-pipelines.yml` file):

```
```
1
2
```



```
{
  "workspace": "{308ce669-576d-4fa7-b4d4-15e8171f0c8c}",
  "repository": "{2fc883c6-3dee-4e73-a354-ccee4bd77938}",
  "creator": "{cda97709-b1a9-4544-9a8d-750f1b3a12c4}",
  "trigger": "push",
  "build_number": 239,
  "pipeline": "{0ac5e5c0-a233-4cb5-88b9-bcffc5fa4925}",
  "created_on": "2024-04-22T02:42:19.807Z",
  "target": {
    "type": "pipeline_ref_target",
    "selector": {
      "type": "branches",
      "pattern": "mas*"
    },
    "commit": {
      "hash": "e34ad324d1e4334777dca3e56c04eba36c2a68c6"
    },
    "ref_type": "branch",
    "ref_name": "master"
  },
  "pipelines_configuration": {
    "pipelines": {
      "branches": {
        "mas*": [
          {
            "step": {
              "name": "A step",
              "script": [
                "echo Running job..."
              ]
            }
          }
        ]
      }
    }
  }
}
```
```

### `PipelineTarget` with selector

| Parameter | Type | Description |
| --- | --- | --- |
| `selector` | [`PipelineSelector`](#pipelineselector) | The selector which identifies the pipeline definition from `pipelines_configuration` which matched the specified `target`.  *Optional, present only if a pipeline definition did match the `target`.* |

#### `PipelineSelector`

| Parameter | Type | Description |
| --- | --- | --- |
| `type` | `string` | Type of the selector, refers to the section the matched pipeline definition is declared in, one of:   * `default` * `branches` * `tags` * `pull-requests` * `custom` |
| `pattern` | `string` | The name of the matching pipeline definition.  *Optional, present for all types other than `default`.* |
| `imported_from` | [`ImportedFrom`](#importedfrom) | The details about an import (see [shared configurations](https://support.atlassian.com/bitbucket-cloud/docs/share-pipelines-configurations/)) which has been resolved for the selected pipeline definition.  *Optional, present only if an `import` has been resolved earlier.* |

#### `ImportedFrom`

| Parameter | Type | Description |
| --- | --- | --- |
| `repo_uuid` | `string` | The Bitbucket UUID of the repository the pipeline definition was imported from. |
| `revision` | `string` | The branch or tag name the pipeline definition was imported from. |
| `pipelineName` | `string` | The name of the pipeline definition that was imported. |

#### Example

Commit target with a selector of a custom `build-and-test` pipeline definition and resolved
import metadata:

```
```
1
2
```



```
{
  "type": "pipeline_commit_target",
  "selector": {
    "type": "custom",
    "pattern": "build-and-test",
    "imported_from": {
      "repo_uuid": "{9d6433db-fbd2-4fcf-a7e0-621526b3161e}",
      "revision": "master",
      "pipelineName": "generic-build"
    }
  },
  "commit": {
    "hash": "82dec1c48c8d3aa75e9e246646894ed952216f3d"
  }
}
```
```

### Filtered `PipelinesConfiguration`

The only difference is that in the request to the Dynamic Pipelines provider the definitions are
filtered down to just the one matching the specified `target`, or none in case no pipelines matched
that `target`.

### Response payload

The Dynamic Pipelines provider is expected to modify (or retain) the configuration passed in the
`pipelines_configuration` property and then return the outcome back.

Alternatively, provider may return an error message in the `error` property. In this case, the pipeline
run will be considered failed, and the error message will be surfaced as the cause of the failure.

#### Response target behaviours

In order for a returned `PipelinesConfiguration` to be executed, it must contain a pipeline definition
that meets the criteria necessary for it to match the `target` specified in the initial request.
If this does not occur, there are two potential outcomes, depending on the `trigger` that initiated the process.

If the `trigger == 'push'` and the returned `PipelinesConfiguration` does not match the `target`
specified in the initial request, the pipelines system will simply ignore the response and
no pipeline run will be generated.

If the `trigger == 'manual'` or `trigger == 'schedule'` and the returned `PipelinesConfiguration`
does not match the `target` specified in the initial request, the pipelines system would generate
and display a “failed” pipeline run.

#### `ProviderError`

If provided, the error message will be shown to the user in the UI on the pipeline result screen.

![The custom error message returned by the Dynamic Pipelines provider](https://dac-static.atlassian.com/platform/forge/images/bitbucket-dynamic-pipelines-provider-error-message.png?_v=1.5800.1800)

| Parameter | Type | Description |
| --- | --- | --- |
| `key` | `string` | The identifier of the Dynamic Pipelines provider error. |
| `message` | `string` | The message describing the error which can be shown to the user in the UI. |

#### `TriggerContext`

If provided, provides additional context relating to the trigger that requested the pipeline.
Currently only provided when trigger type = `parent_step`.

| Parameter | Type | Description |
| --- | --- | --- |
| `parent_pipeline_uuid` | `string` | The UUID of the pipeline that contains the parent step that triggered this pipeline. |
| `parent_pipeline_run_uuid` | `string` | The UUID of the pipeline run that contains the parent step that triggered this pipeline. |
| `parent_step_uuid` | `string` | The UUID of the parent step that triggered this pipeline. |

#### Examples

A response with a modified pipeline definition:

```
```
1
2
```



```
{
  "pipelines_configuration": {
    "image": {
      "name": "enforced/image:latest"
    },
    "pipelines": {
      "branches": {
        "master": [
          {
            "step": {
              "name": "Updated step",
              "script": [
                "echo Running updated job..."
              ]
            }
          }
        ]
      }
    }
  }
}
```
```

A response with an error:

```
```
1
2
```



```
{
  "error": {
    "key": "provider.error.example",
    "message": "This error message was provided by Dynamic Pipelines provider"
  }
}
```
```
