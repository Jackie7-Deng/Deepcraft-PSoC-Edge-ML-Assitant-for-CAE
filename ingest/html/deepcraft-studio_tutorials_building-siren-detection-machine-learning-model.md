---
source_url: "https://developer.imagimob.com/deepcraft-studio/tutorials/building-siren-detection-machine-learning-model"
fetched_at: "2026-03-10T15:51:59Z"
title: "Building Siren Detection machine learning model"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "tutorials", "building-siren-detection-machine-learning-model"]
---

### Building Siren Detection machine learning model

This tutorial covers end-to-end information on how to build, train, and evaluate a siren detection machine learning model using DEEPCRAFT™ Studio and Infineon board.

#### Objective

We will build a siren detection machine learning model that recognize the siren sounds from the emergency vehicles. This can be used to alert pedestrians to emergency vehicles in their vicinity, or to trigger other safety features in wearables.

#### Prerequisites

Before starting this tutorial, ensure you meet the following requirements:

- - **Select the Infineon Board**

  Choose the board on which you want to run the siren detection machine learning model. You can select from the following options:

  * **AURIX™ TC375 Lite Kit**
  * **PSOC™ 6 and PSOC™ Edge boards**
  * **XMC7200 EVK (KIT\_XMC72\_EVK)**
  * **TRAVEO™ T2G**
    + TRAVEO™ T2G Body Entry Lite Kit (KIT\_T2G-B-E\_LITE)
    + TRAVEO™ T2G Body High Lite Kit (KIT\_T2G-B-H-LITE)
- - **Flash Imagimob Streaming Firmware**

  If you want to collect the data using the PSOC™ 6 board, you must flash the the board with Imagimob Streaming Firmware. Refer to [Getting started with Infineon PSOC™ Wi-Fi BT Pioneer Kit and IoT sense expansion kit](https://developer.imagimob.com/getting-started/infineon-PSoC6-wi-fi-pioneer-kit) for detailed instructions.

  If you want to collect data using other development boards, refer to [Imagimob Streaming Protocol Specification](https://bitbucket.org/imagimob/imagimob-streaming-protocol-psoc6/src/main/PROTOCOL.md) for detailed instructions.

  However, if you do not want to collect data using the board and prefer to use your own data, refer to [Bring your own data](https://developer.imagimob.com/data-importing) for detailed instructions.

We offer [Imagimob Streaming Firmware](https://developer.imagimob.com/getting-started/infineon-PSoC6-wi-fi-pioneer-kit#streaming-firmware-for-psoc-62s2-wi-fi-bt-pioneer-kit) for PSOC™ 6 boards, simplifying data collection. For other boards, we provide [Imagimob Streaming Protocol](https://bitbucket.org/imagimob/imagimob-streaming-protocol-psoc6/src/main/PROTOCOL.md), allowing you to integrate the necessary sensors and develop custom firmware for data collection.

- - **Register an account and Install DEEPCRAFT™ Studio**

  DEEPCRAFT™ Studio is a development platform that streamlines the different stages of a machine learning project, such as, collecting, labeling and importing data, preprocessing data, designing and training models, and model evaluation. Create an Imagimob account to download and install Studio. For detailed instructions, refer to [Download and Install DEEPCRAFT™ Studio](https://developer.imagimob.com/install-download-studio).
- - **Siren Detection Stater Project**

  We will use the siren detection starter project as a starting point to understand the machine learning flow in detail. Begin with creating a project in Studio and select **Classification> Infineon> Siren Detection** as the project type. To know how to create a project, refer to [Creating a project](https://developer.imagimob.com/getting-started/workspace-project#creating-a-project).

It is recommended that an empty project is started after going through the starter projects and the ML flow is understood.

- - **ModusToolbox™ or Aurix™ Development Studio**

  Finally, we deploy the model on the development kit using the [ModusToolbox™](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox) or [AURIX™ Development Studio](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.aurixide).

After setting up everything, you can start building the siren detection machine learning model following the step-by-step instructions from the tutorial. The tutorial covers end-to-end machine learning stages from the data collection to deploying the generated model.

#### Let’s start building the model

We will cover the following machine learning development flow:

- - **[Data Preparation](https://developer.imagimob.com/tutorials/building-siren-detection-machine-learning-model/data-preparation-siren-tutorial)**: The first step is to collect and label data from sensors using Serial Capture in Graph UX and Infineon board. After collecting and labeling data, we will import data into the Siren Starter project followed by distributing the data into the different datasets.
- - **[Preprocessing](https://developer.imagimob.com/tutorials/building-siren-detection-machine-learning-model/preprocessing-siren-tutorial)**: The second main step is preprocessing where the data signal processing techniques are applied to the sensor data, such as windowing and filtering techniques to reduce the noise and extract the features of the sensors data.
- - **[Model Training](https://developer.imagimob.com/tutorials/building-siren-detection-machine-learning-model/model-training-siren-tutorial)**: After preprocessing, the data is passed to the model for training. In this step, we will generate, train and evaluate the model to find the best fitting siren detection model.
- - **[Code Generation and Model Deployment](https://developer.imagimob.com/tutorials/building-siren-detection-machine-learning-model/model-deployment-siren-tutorial)**: The last step is to generate the code and deploy the model on the board. After evaluating the model, we will generate the C code for the selected model in DEEPCRAFT™ Studio and then deploy the model on the Infineon board using ModusToolbox™ or Aurix™ Development Studio.
