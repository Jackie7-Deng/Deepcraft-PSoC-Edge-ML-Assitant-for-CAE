---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/release-notes"
fetched_at: "2026-03-10T15:52:04Z"
title: "Release Notes"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "release-notes"]
---

# Release Notes

### Release Notes 5.8

This section lists the new functionality, improvements and some of the major changes related to DEEPCRAFT™ Model Converter.

#### New Features and Enhancements

**Interpreterless Mode**

DEEPCRAFT™ Model Converter now offers Interpreterless mode that pre-interprets the model to generate the static C++ code that executes the neural network directly, removing the need for the TensorFlow Lite Micro interpreter at runtime. When this option is enabled, the runtime, memory planner and unused operator code are not compiled into the final application, reducing the ROM footprint. This can provide memory savings for very small models (under 400 KB) that use a limited set of operator types. Refer to [Graphical User Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-gui#general) or
[Command Line Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-cli#command-line-syntax) to know how to use the Interpreterless mode.

#### Fixes

Overall bug fixes and increased stability.
