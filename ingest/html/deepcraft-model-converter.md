---
source_url: "https://developer.imagimob.com/deepcraft-model-converter"
fetched_at: "2026-03-10T15:52:04Z"
title: "DEEPCRAFT™ Model Converter"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter"]
---

### DEEPCRAFT™ Model Converter

DEEPCRAFT™ Model Converter is a comprehensive solution designed to facilitate the conversion of pre-trained models for deployment on an Infineon target platforms. By leveraging Model Converter, users can generate code for existing models, optimize pre-trained models for specific target devices through configurable optimization parameters, and validate model performance on the desktop prior to actual device deployment.

DEEPCRAFT™ Model Converter is available in both **Graphical User Interface (GUI)** and **Command-Line Interface (CLI)** versions, providing flexibility and convenience for developers working in a variety of workflows. Model Converter is fully compatible with **Windows**, **macOS**, and **Linux** operating systems allowing users to integrate the models into the preferred development environments. Whether you are a researcher or a developer, DEEPCRAFT™ Model Converter simplifies the process of importing, optimizing, and validating your pre-trained models for Infineon devices.

#### Key Features

### Model Compatibility

Generate code for multiple model formats

- - •TensorFlow Keras (.h5)
- - •TensorFlow Lite (.tflite)
- - •PyTorch (.pt2)

### Input/Output Flexibility

Streamlined model architecture support

- - •Single input support
- - •Single output support
- - •Optimized for edge deployment

### Target Platform

Designed for Infineon microcontrollers

- - •PSOC™ 6
- - •PSOC™ Edge M55+U55
- - •PSOC™ Edge M33+NNLite

### Quantization

Optimize models for edge deployment

- - •Reduce model size significantly
- - •Improve inference speed
- - •Maintain accuracy for edge devices

### Validate on Desktop

Ensure model performance before deployment

- - •Validate quantized and non-quantizedmodels
- - •Performance and accuracy verification

#### Understanding DEEPCRAFT™ Model Converter

The intended use of DEEPCRAFT™ Model Converter is to generate code files that enable the execution of Neural Networks (in .h5, .tflite, .pt2 formats) on an an Infineon PSOC™ 6 or PSOC™ Edge target. The Model Converter accepts the network file, along with optional calibration or validation data, as input and generates model.c and model.h files that can be imported into a ModusToolbox™ project to perform inference (with optimizations for the selected target SoC). This workflow assumes that you already have implemented the necessary pre and post-processing steps, as well as any required sensor data acquisition code, to ensure that the data is in the proper format for passing to the network. The generated code depends on the following ModusToolbox™ assets or libraries that can be imported through the ModusToolbox™ Eclipse IDE library manager.For Infineon PSOC™ 6 target, the generated code relies on ml-middleware 3.0.1 and ml-tflite-micro 3.0.1 libraries, while for PSOC™ Edge target, the generated code relies on ml-middleware 3.1.0 and ml-tflite-micro 3.1.0 libraries,understanding these dependencies is crucial for successful model deployment and execution.

![](https://developer.imagimob.com/Images/model-converter/mc-user-journey.svg)

#### Supported Models and Quantization

DEEPCRAFT™ Model Converter generates code for TensorFlow, Keras, and PyTorch models that meet the required specifications. It also supports multiple quantization configurations. Refer to [Supported Models and Quantization](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-model-formats) section for detailed information.

#### Whats Next?

Let’s install the DEEPCRAFT™ Model Converter and launch the Graphical User Interface and Command Line Interface. Refer to [Install and Launch DEEPCRAFT™ Model Converter](https://developer.imagimob.com/deepcraft-model-converter/install-launch).

**DEEPCRAFT™ Model Converter** will replace the **ModusToolbox ML Configurator**. Both applications will be available side by side for a six-month transition period from launch to allow customers to transition to Model Converter and to provide a grace period for migrating any missing functionality from ML Configurator. In case, you need to install ML Configurator, see [here](https://softwaretools.infineon.com/assets/com.ifx.tb.tool.modustoolboxpackmachinelearning).
