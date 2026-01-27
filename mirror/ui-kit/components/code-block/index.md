# Code block

To add the `CodeBlock` component to your app:

```
1
import { CodeBlock } from '@forge/react';
```

## Description

A code block highlights an entire block of code and keeps the formatting.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `highlight` | `string` | No | Comma delimited lines to highlight. |
| `highlightedEndText` | `string` | No | Screen reader text for the end of a highlighted line. |
| `highlightedStartText` | `string` | No | Screen reader text for the start of a highlighted line. |
| `language` | `"text" | "PHP" | "php" | "php3" | "php4" | "php5" | "Java" | "java" | "CSharp" | "csharp" | "c#" | "Python" | "python" | "py" | "JavaScript" | "javascript" | "js" | "Html" | "html" | ... 224 more ... | "proto"` | No | Language grammars from [PrismJS](https://prismjs.com/#supported-languages) . When set to `text` will not perform highlighting. If an unsupported language is provided, code will be treated as `text` with no highlighting. Defaults to `text`. |
| `shouldWrapLongLines` | `boolean` | No | Sets whether long lines will create a horizontally scrolling container. When set to `true`, these lines will visually wrap instead. Defaults to `false`. |
| `showLineNumbers` | `boolean` | No | Sets whether to display code line numbers or not. Defaults to `true`. |
| `text` | `string` | No | The code to be formatted. |

## Examples

### Default

A code block highlights an entire block of code and keeps the formatting.

![Example image of a code block with line numbers](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code-block/code-block-line-numbers.png?_v=1.5800.1800)

```
```
1
2
```



```
const exampleCodeBlock = `// Forge App
const App = () => {
  const [name, setName] = React.useState('world');

  return (
    <Box>
      <Text>{\`Hello \${name}!\`}</Text>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;

const CodeBlockLineNumbersExample = () => {
  return (
    <CodeBlock
      language="jsx"
      text={exampleCodeBlock}
    />
  );
};
```
```

### Line highlighting

You can highlight lines in a code block.

* To highlight one line, input the line number: `highlight="3"`.
* To highlight a group of lines, input the line numbers as a range: `highlight="1-5"`.
* To highlight multiple groups, separate the individual lines and ranges with a comma: `highlight="1-5,7,10,15-20"`.

![Example image of a code block with line highlights](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code-block/code-block-highlights.png?_v=1.5800.1800)

```
```
1
2
```



```
const exampleCodeBlock = `// Forge App
const App = () => {
  const [name, setName] = React.useState('world');

  return (
    <Box>
      <Text>{\`Hello \${name}!\`}</Text>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;

const CodeBlockLineHighlightExample = () => {
  return (
    <CodeBlock
      language="jsx"
      text={exampleCodeBlock}
      highlight="2,5-7"
    />
  );
};
```
```

### Wrapping

By default, long lines will result in a horizontal-scrolling code block. You can use the `shouldWrapLongLines` prop to make the long lines wrap instead.

![Example image of a code block with default appearance](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code-block/code-block-wrapping.png?_v=1.5800.1800)

```
```
1
2
```



```
const exampleCodeBlockWithLongLines = `// This is an example of a comment that is going to create a long line of code, where you may want to use the \`shouldWrapLongLines\` prop. When this prop is set to false, the CodeBlock container will scroll horizontally. When it is set to true, the CodeBlock content will wrap to the next line. As you can see from this line, the 'highlight' and 'shouldWrapLongLines' props work well in tandem.

const ExtremelyLongApplicationNameThatMightNormallyForceTheCodeBlockToScrollHorizontally = () => {
  const [name, setName] = React.useState('world');

  return (
    <Box>
      <Text>{\`Hello \${name}!\`}</Text>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <ExtremelyLongApplicationNameThatMightNormallyForceTheCodeBlockToScrollHorizontally />
  </React.StrictMode>
);`;

const CodeBlockShouldWrapLongLinesExample = () => {
  return (
    <CodeBlock
      language="jsx"
      text={exampleCodeBlockWithLongLines}
      shouldWrapLongLines={true}
    />
  );
};
```
```

### Hide line numbers

Line numbers can be hidden by setting the `showLineNumbers` prop to `false`.

![Example image of a code block with no line numbers](https://dac-static.atlassian.com/platform/forge/ui-kit/images/code-block/code-block-line-numbers.png?_v=1.5800.1800)

```
```
1
2
```



```
const exampleCodeBlock = `// Forge App
const App = () => {
  const [name, setName] = React.useState('world');

  return (
    <Box>
      <Text>{\`Hello \${name}!\`}</Text>
    </Box>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;

const CodeBlockDefaultExample = () => {
  return (
    <CodeBlock
      language="jsx"
      text={exampleCodeBlock}
      showLineNumbers={false}
    />
  );
};
```
```
