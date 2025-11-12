# Variables

You can use environment variables in your manifest for entire or partial field values. The Forge CLI
reads these values from the process environment when executing any command.

Manifest variables are only available during manifest parsing by the Forge CLI toolchain and are NOT available to your app code at runtime. For runtime environment variables that your app can access, use the [`forge variables set`](/platform/forge/cli-reference/variables-set/) command.

An environment variable must first be declared in `environment.variables` before it can be used elsewhere in the manifest file:

```
1
2
3
4
environment:
  variables:
    - VARIABLE
    - VARIABLE2
```

or using default values:

```
1
2
3
4
5
6
environment:
  variables:
    - key: VARIABLE
      default: "default value"
    - key: VARIABLE2
      default: "default value 2"
```

## Manifest variables vs runtime variables

Understanding the difference between these two types of variables is crucial:

| Aspect | Manifest Variables (This Page) | Runtime Variables |
| --- | --- | --- |
| **When available** | During CLI commands (build-time) | App execution (runtime) |
| **How to set** | `export VAR=value` in terminal | `forge variables set VAR value` |
| **How to access** | `${VAR}` in manifest.yml | `process.env.VAR` in app code |
| **Use cases** | App IDs, module configuration | API tokens, secrets, runtime config |

Note that environment variables are not presently supported for the `forge build` command.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `variables` | `Array` of [Variables](#Variables) | No | A list of strings or objects, with the key each matching the regex `^[a-zA-Z_][a-zA-Z0-9_]*$` that indicate which substrings used throughout the `manifest.yml` can be replaced with the corresponding environment variable value from the current process or defined as the default value to use. |

### Variables

| Type | Required | Description |
| --- | --- | --- |
| `string` | No | A list of strings, each matching the regex `^[a-zA-Z_][a-zA-Z0-9_]*$` that indicate which substrings used throughout the `manifest.yml` can be replaced with the corresponding environment variable value from the current process. |
| `{ key: string; default: string }` | No | A list of objects, the `key` of which each matching the regex `^[a-zA-Z_][a-zA-Z0-9_]*$` that indicate which substrings used throughout the `manifest.yml` can be replaced with the corresponding environment variable value from the current process. If there is no matching environment variable in the current process, the `default` value defined will be used instead. |

## Examples

### Using a list of environment variable strings

If you want to use your `APP_ID` in the manifest (not in app code), you can export it as an environment variable **without** default values:

```
```
1
2
```



```
export APP_ID=406d303d-0393-4ec4-ad7c-1435be94583a
```
```

Afterwards, you can specify it in your manifest file:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/${APP_ID}"
environment:
  variables:
    - APP_ID
```
```

Forge CLI commands that read the manifest will convert the variable `APP_ID` as follows:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"
environment:
  variables:
    - APP_ID
```
```

### Using a list of environment variable objects

Alternatively, if you want to export your `APP_ID` as a list of environment variable objects, you can define your manifest file with a variable object that **includes** a default value:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/${APP_ID}"
environment:
  variables:
    - key: APP_ID
      default: 406d303d-0393-4ec4-ad7c-1435be94583a
```
```

Forge CLI commands that read the manifest will convert the variable `APP_ID` as follows:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/406d303d-0393-4ec4-ad7c-1435be94583a"
environment:
  variables:
    - key: APP_ID
      default: 406d303d-0393-4ec4-ad7c-1435be94583a
```
```

Exported environment variables will always take precedence over the `default` values defined in the manifest file.

Suppose you had exported the `APP_ID` environment variable as follows:

```
```
1
2
```



```
export APP_ID=12345678-1234-1234-1234-123456789012
```
```

Then, Forge CLI commands that read the manifest will convert the variable `APP_ID` as follows:

```
```
1
2
```



```
app:
  id: "ari:cloud:ecosystem::app/12345678-1234-1234-1234-123456789012"
environment:
  variables:
    - key: APP_ID
      default: 406d303d-0393-4ec4-ad7c-1435be94583a
```
```
