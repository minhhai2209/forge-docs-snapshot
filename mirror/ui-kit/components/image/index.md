# Image

To add the `Image` component to your app:

```
1
import { Image } from '@forge/react';
```

## Description

An image component to display images.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `alt` | `string` | Yes | The alternative text displayed if the image is not loaded. |
| `src` | `string` | Yes | The remote URL of the image or a reference to a local import (see  [local image](#local-image)). |
| `size` | `'xsmall'`,`'small'`, `'medium'`, `'large'` or `'xlarge'` | No | The size of the image. Defaults to `xlarge`. |
| `width` | `string` or `number` | No | The width of the image. Setting this prop will override the `size` prop. Setting only the `width` will result in the `height` scaling to the original image aspect ratio.  `width` can be given in pixels (ie. `50px`) or percentage (ie. `50%`). If a number value is given, it will default to pixels. |
| `height` | `string` or `number` | No | The height of the image. Setting this prop will override the `size` prop. Setting only the `height` will result in the `width` scaling to the original image aspect ratio.  The unit can be in pixels (i.e. `height="50px"`) or percentage (i.e.: `height="50%"`). If a number value is given, it will default to pixels. |

## Image permissions

If you are using a URL for the image `src`, make sure that the image URL is added to the app's manifest file to load the image.
For more information on how to declare image sources in an application's manifest file, see [image permissions](/platform/forge/manifest-reference/permissions/#images) documentation.

**Example to add an image URL in the manifest**

```
```
1
2
```



```
permissions:
  external:
    images:
      - address: <ImageURL>
```
```

## Examples

### Image size

The image `size` property is relative to the container.
Here's an example with different image `size` props, to help illustrate how to use the image component in an app.

![Examples of different image sizes that include xsmall, small, medium, large, xlarge to optimize images for different devices](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/image-sizes.png?_v=1.5800.1742)

If using percentage values for `width` and `height`, the image size will also be relative to the container, whereas
using pixel values for `width` and `height` will change the size of the image to the pixel values provided.

### Local image

```
```
1
2
```



```
import React from 'react';
import { Image } from '@forge/react';
// Importing the 'myCat' image from the project's folder for use in the component.
import myCat from './myCat.png'

export const App = () => (
   <Image
     src={myCat}
     alt="black and white cat lying on brown bamboo chair inside room"
   />
);
```
```

![black and white cat sitting on a bamboo chair, smirking as if to say, "This room is my fluffy kingdom"](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/image-default.png?_v=1.5800.1742)

### Static image

```
```
1
2
```



```
import React from 'react';
import { Image } from '@forge/react';

export const App = () => (
   <Image
     src="<ImageURL>"
     alt="black and white cat lying on brown bamboo chair inside room"
   />
);
```
```

![black and white cat sitting on a bamboo chair, smirking as if to say, "This room is my fluffy kingdom"](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/image-default.png?_v=1.5800.1742)

### GIF

```
```
1
2
```



```
import React from 'react';
import { Image } from '@forge/react';

export const App = () => (
    <Image
      src="https://media.giphy.com/media/jUwpNzg9IcyrK/source.gif"
      alt="Example of an animated GIF depicting Homer Simpson retreating into bushes, referencing the popular 'Homer Simpson disappearing' meme"
    />
);
```
```

![Example of an animated GIF depicting Homer Simpson retreating into bushes, referencing the popular 'Homer Simpson disappearing' meme](https://dac-static.atlassian.com/platform/forge/images/homer.gif?_v=1.5800.1742)

## Accessibility considerations

Text Alternatives (alt text) are an important factor in digital accessibility as they provide an easy way for [non-text content (as per WCAG success criterion)](https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html) to be perceived through various methods including Assistive Technology. Alt text is informative content which conveys the meaning of non-decorative images, and also provides content when images are slow or fail to load.

This helps users who use:

* Screen readers
* Braille display
* Text-to-speech technology

In order to first apply alt text correctly, we need to determine whether an image conveys any meaning (non-decorative) or whether it is purely for presentation purposes (decorative).

**Non-decorative images**

Require image descriptions as they convey meaning or add context to the content. In order to write the most appropriate alt text (image description) for an image, keep the following in mind:

* Describe the message the image is conveying, not what the image is. For example, for an image of a clock that points to 2pm, appropriate alt text would be: “Analog clock with a white face and black arms pointing to 2pm”. Inappropriate alt text would be: “clock”.
* Keep alt text to no more than ~100 characters. This allows for a streamlined experience for screen reader users.
* Avoid using “image of…” or “picture of…” assistive technology will add this for you when encountering the image element.

**Decorative images**

Do not require image descriptions because they are purely presentational and part of the overall design.

* Ensure that the decorative images have an EMPTY alt text attribute: `alt=""`.
