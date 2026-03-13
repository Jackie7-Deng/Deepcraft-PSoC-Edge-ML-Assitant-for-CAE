---
source_url: "https://developer.imagimob.com/deepcraft-studio/other-pages/iar-embedded-workbench"
fetched_at: "2026-03-10T15:51:58Z"
title: "Iar Embedded Workbench"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "other-pages", "iar-embedded-workbench"]
---

### IAR Embedded Workbench

This section provides step-by step instructions to setup Imagimob Commandline Tool inside IAR Embedded Workbench. The IAR Embedded Workbench automatically compiles TensorFlow .h5 files into .c and .h files. The Imagimob Commandline Tool is compatible with Tensorflow/Keras .h5 models generated with a Tensorflow backend of version 2.x. To know the supported layers and activation functions in Studio refer to [Supported layers and functions](https://developer.imagimob.com/edge-optimization/supported-layers).

The models that contain unsupported layers will fail to convert.

#### Pre-requisite

Make sure you have installed DEEPCRAFT™ Studio.

#### Sample project

Here is a pre-configured sample project that can be loaded in IAR Embedded Workbench. [Click to download sample project](https://developer.imagimob.com/data/imagimob-iar-demo.zip)

#### Setup Imagimob Commandline Tool for IAR Embedded Workbench Sample Project

To setup the Imagimob Commandline Tool for new or existing projects, follow the steps:

1. - Go to **Project** → **Options** → **Custom Build**.
2. - In **Filename extensions**, enter *.h5*.
3. - In **Command line**, enter *imc $FILE\_PATH$ -oc $FILE\_BNAME$.c -oh $FILE\_BNAME$.h*
4. - In **Output files**, enter *$FILE\_BNAME$.c $FILE\_BNAME$.h*

  ![](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fiar-custom-tool-configuration.528fb28f.png&w=1200&q=75)
5. - Add the .h5 file that you want to convert to the project.
6. - Make project (make sure that the project contains a file named main.c)

  You can now find the generated .c and .h files under **Files** → **Model.h5** → **Output**.

  ![](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fiar-generated-files.beecd22f.png&w=640&q=75)
