---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/deploy-model-using-code-example"
fetched_at: "2026-03-10T15:52:06Z"
title: "Deploy Model Using Code Example"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "deploy-model-using-code-example"]
---

# Deploy Model Using Code Example

### Deploy code on PSOC™ Edge boards using the Code Example

This section explains how to deploy the code generated from DEEPCRAFT™ Model Converter onto the PSOC™ Edge boards using the **PSOC™ Edge MCU: Machine learning DEEPCRAFT™ profiler** code example.

#### PSOC™ Edge MCU: Machine learning DEEPCRAFT™ profiler

This code example demonstrates how to use the DEEPCRAFT™ development flow on PSOC™ Edge MCU, where you can have a pre-trained neural network (NN) model, which can be profiled and validated the target device.

Import a pre-trained model using the DEEPCRAFT™ Model Converter (installed through the Infineon Developer Center), create an embedded and optimized version of this model. After generation, the passed in validation data files can be integrated with this code example, so you can run the same validation data and profile performance when the ML model is deployed on the PSOC™ Edge MCU.

You can also select where to deploy and run the model:

- - High-performance domain: Uses the Arm® Cortex®-M55 and the Ethos-U55 processor
- - Low-power domain: Uses the Arm® Cortex®-M33 and the NNLITE processor

**Refer to the README.md in the Code Example for hardware and software setup and other detailed instructions.**

#### Pre-requisites:

- - Download and Install [ModusToolbox™](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox) (recommended v3.6 or later)
- - Supported kits::
  * [PSOC™ Edge E84 Evaluation Kit (KIT\_PSE84\_EVAL\_EPC2)](https://www.infineon.com/KIT_PSE84_EVAL)
  * [PSOC™ Edge E84 Evaluation Kit (KIT\_PSE84\_EVAL\_EPC4)](https://www.infineon.com/KIT_PSE84_EVAL)
  * [PSOC™ Edge E84 AI Kit (KIT\_PSE84\_AI)](https://www.infineon.com/KIT_PSE84_AI)

#### Creating Code Example for PSOC™ Edge

The ModusToolbox™ tools package provides the Project Creator as both a GUI tool and a command line tool. Refer to the *using\_the\_code\_example.md* file in the docs folder for detailed instructions.

After the application is created successfully, the code example directory appears.

### Open the project and Launch Model Converter

After the project has been created, you can open it in your preferred development environment. Refer to *using\_the\_code\_example.md* file in the docs folder for detailed instructions.

After creating the application, let’s generate the code for the model using the Model Converter.
The code example directory contains the following *project.byom* files: *proj\_cm55/project.byom* and *proj\_cm33\_ns/project.byom*

1. - Double-click the *project.byom* file for the desired core to open the DEEPCRAFT™ Model Converter. You can also open the Model Converter in the **Quick Panel** under the configuration.
2. - Configure the parameters in the project.byom to generate, optimize and validate the code. To know about the parameters, refer to the [Graphical User Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-gui).
3. - Click the Start button to generate the code for the model. The code (model.c/.h files) is generated in the Output Directory defined earlier along with the code generation report.

Refer to the README.md and *design\_and\_implementation.md* and file in the docs folder for detailed instructions.

If you use the interpreterless mode when generating the code, you need to update the Makefile in your project with the following code:

```
NN_INFERENCE_ENGINE=tflm_less

ifeq (tflm, $(NN_INFERENCE_ENGINE))
COMPONENTS+=ML_TFLM
endif
ifeq (tflm_less, $(NN_INFERENCE_ENGINE))
COMPONENTS+=ML_TFLM_LESS
DEFINES+=TF_LITE_MICRO_USE_OFFLINE_OP_USER_DATA
SOURCES+=$(wildcard $(NN_MODEL_FOLDER)/$(MODEL_PREFIX)_tflm_less_model_$(NN_TYPE).cpp*)
endif
```

#### Build and program onto the board

1. - Connect the board to your PC using the provided USB cable through the KitProg3 USB connector and program the board.
2. - Select the application project in the Project Explorer
3. - In the **Quick Panel**, scroll down, and click **<Application Name> Program (KitProg3\_MiniProg4)**

You can build and program the application using other methods, refer to *using\_the\_code\_example.md* file in the docs folder for detailed instructions.

We are working on the code example for PSOC™ 6 board.
