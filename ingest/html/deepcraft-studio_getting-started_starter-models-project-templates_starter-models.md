---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/starter-models-project-templates/starter-models"
fetched_at: "2026-03-10T15:51:14Z"
title: "Starter Models"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "starter-models-project-templates"]
---

# Starter Models

### DEEPCRAFT™ Studio Accelerators

The DEEPCRAFT™ Studio Accelerators are designed to kickstart your Edge AI journey. The DEEPCRAFT™ Studio Accelerators are deep learning-based projects that cover various use cases and serve as starting points for building custom applications. The DEEPCRAFT™ Studio Accelerators are open-source and include all the necessary datasets, preprocessing steps, model architectures, and instructions to help you develop production-ready Edge AI models.

You can download the DEEPCRAFT™ Studio Accelerators from the DEEPCRAFT™ Studio and start fine-tuning them to suit your specific needs. The DEEPCRAFT™ Studio offers 3000 minutes of compute time per month, free for development, evaluation, and testing purposes. This provides a valuable opportunity to gain hands-on experience in creating and deploying machine learning models from start to finish.

You can use the DEEPCRAFT™ Studio Accelerators as:

- - a starting point and fine-tune the model as per your requirement
- - an inspiration and collect your own data to build a similar project

Formerly known as DEEPCRAFT™ Starter Models, these are now referred to as DEEPCRAFT™ Studio Accelerators. We have expanded our DEEPCRAFT™ Studio Accelerators portfolio by adding a number of new models. Refer to our official website [DEEPCRAFT™ Studio Accelerators](https://www.imagimob.com/starter-models) to know more.

### How do I get started with Studio Accelerators?

1. - Open DEEPCRAFT™ Studio.
2. - Click **New Project** in the welcome screen. The welcome screen appears, when you open the Studio for the first time.
  OR
  Go to **File** and select **New Project**. The New Project window appears.
3. - Expand **Studio Accelerators** and depending on the machine learning problem you want to solve expand either **Classification** or **Object Detection**. Select the relevant sensor type, browse the available projects, and choose one of the Studio Accelerator as your starting point.

  ![](https://developer.imagimob.com/Images/getting-started/starter-models/pic-2.png)
4. - In **New Project Name**, edit the project name, if needed. By default, the default project name is displayed.
5. - In **Location**, specify the location where you want to create the workspace and the project directory.

We do not recommend creating workspace in the directories that are synced with OneDrive due to this [known issue](https://answers.microsoft.com/en-us/msoffice/forum/all/onedrive-bug-the-tag-present-in-the-reparse-point/214c1387-adf9-4d7c-abd7-110eea4121ec) in OneDrive.

1. - Select **Download project data** checkbox to download the project data to the workspace selected earlier.
2. - This is an optional step and applicable only if you plan to deploy your model to the PSOC Edge boards and do not have a ModusToolbox™ project. Select the **Create ModusToolbox™ Project** checkbox to launch ModusToolbox™ Project Creator and create the required ModusToolbox™ project. To know how to create the ModusToolbox project from Studio, refer to [Creating ModusToolbox™ project from Studio](https://developer.imagimob.com/deepcraft-studio/getting-started/starter-models-project-templates/starter-models#creating-modustoolbox-project-from-studio).
  After the project is created, Studio automatically saves the project path. During code generation for PSOC Edge boards, the saved ModusToolbox™ project path is available as a selectable output location. Select the desired ModusToolbox™ project and Studio will place the generated code directly into that project. To know more, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).
3. - Click **OK** to download the data and create the studio accelerator project. After you download the Studio Accelerator, you can start collecting data to fine-tune the model as per your needs.Refer to [Data Collection](https://developer.imagimob.com/data-preparation/data-collection) to know how to collect data in DEEPCRAFT™ Studio and [Data Preparation](https://developer.imagimob.com/data-preparation#data-preparation) to understand the different steps involved after collecting the data in Studio.

If you have an existing ModusToolbox™ project for PSOC Edge board and plan to use the same for deployment, launch DEEPCRAFT™ Studio from within ModusToolbox™: open ModusToolbox™, select your project, go to Quick Panel > Library Configurator, and click DEEPCRAFT™ Studio. Studio will launch and automatically save the project path. During code generation for PSOC boards, this saved path is available as a selectable output location. Select the desired ModusToolbox™ project and Studio will place the generated code directly into that project. To know more, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).

#### Creating ModusToolbox™ project from Studio

To simplify and streamline the deployment workflow for PSOC™ Edge boards, we offer the capability to launch ModusToolbox™ Project Creator directly from DEEPCRAFT™ Studio. This functionality enables you to create the ModusToolbox™ project corresponding to the Studio project. This integration ensures consistency, minimizes manual intervention, and streamlines the overall development-to-deployment workflow. For detailed explanation, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).

**To Launch and create the project in ModusToolbox™, follow the steps**:

1. - After you select the **Create ModusToolbox Project** checkbox and click ok to launch the project creator. The Choose Board window appears.

  ![](https://developer.imagimob.com/Images/getting-started/starter-models/pic-3.png)
2. - Expand the Kit Name from the list and select the required MCU as BSP for your board and click **Next**. The Select Application window appears.

  ![](https://developer.imagimob.com/Images/getting-started/starter-models/pic-4.png)
3. - In **Template Application**, expand **Machine Learning** and select the required deploy code example and click **Create**. After the project is created successful, the code example appears in ModusToolbox™.

During code generation in Studio, select the ModusToolbox™ project as the output location to automatically place the generated code into that project. Refer to [ModusToolbox™ Project](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-project) to know more.

### Choose your Studio Accelerator

Based on the sensor type utilized in the project, we offer the following Studio Accelerators: **IMU and Vibration**, **Microphone**, **Capacitive and Inductive Sensing** and **Camera**.

#### IMU and Vibration

1. - **Human activity detection**: This Studio Accelerator allows you to build a human activity detector that can be used on any supported Infineon MCU (or other MCUs) with a BMI160 IMU or another IMU. You can use this project as a starting point to develop a production-ready model intended for deployment in wrist-worn wearables.
2. - **Fall detection (Belt-mounted)**: This Studio Accelerator allows you to build models to detect a fall using an IMU (accelerometer and gyroscope) mounted on the buckle of a belt. For that, this Accelerator Model uses data collected from two different IMUs: a Bosh IMU and an STMicroelectronics IMU. Both sensors are set up to collect data at 50 Hz using a +- 8g for the accelerometer scale and +- 500 dps for the gyro scale.
3. - **Anomalous vibration detection**: This Studio Accelerator aims to provide general guidance on how to develop an anomaly detection system for detecting anomalous behavior in machinery based on vibration measurements. This project will monitor a simple desktop fan, but the same concept and workflow can be easily ported to any other machinery, whether industrial or consumer.
4. - **Drill material detection IMU**: This Studio Accelerator is capable of classifying the material a power drill is drilling into based on the IMU (6 axis accelerometer and gyroscope) signature. It is designed to be incorporated into smart power tools. It differentiates between wood, plastic and air.

#### Microphone

1. - **Siren Detection**: This machine learning project contains everything you need to develop and deploy your very own siren detection model. Bundled with the project is an already trained model, and instructions for how to deploy it to the Infineon AURIX™ TC375 Lite Kit Board and KITA2G Audio Shield Board, which is ideally suitable for automotive and industrial applications.
2. - **Baby Cry detection**: This machine learning project contains everything you need to develop and deploy your very own baby cry detection model. Bundled with the project is an already trained model, and instructions for how to deploy it on the Infineon PSOC™ 6, which is ideally suitable for consumer applications.
3. - **Drill Material Detection**: This Studio Accelerator is capable of classifying the material a power drill is drilling into based on the audio signature. It is designed to be incorporated into smart power tools. It is developed as a proof of concept and is not fully optimized, achieving around a 85% plastic/wood accuracy. It differentiates between wood, plastic and air.
4. - **Gunshot Detection**: This Studio Accelerator detects gunshots in a noisy environment. The model includes strong invariance to many different background noises, and has around one hour of microphone data. A limitation with this model is difficulty in testing.
5. - **Keyword Detection**: This machine learning project contains everything to get started with keyword detection. Bundled with the project is a trained model, the Google Speech commands dataset, and the guide for how to download and prepare the dataset. You also get some hints on how to take the model to production.
6. - **Chainsaw detection**: This Studio Accelerator classifies if there is a chainsaw actively cutting material in the vicinity. Chainsaws that are stalling are defined as not cutting. A fully developed model based on this Starter Model could be used to detect illegal logging or to create automatic warning systems.
7. - **Home Sounds Detection**: This Studio Accelerator is capable of detecting a number of audio signatures common to a home setting. It currently has three labels; ‘cough’, ‘baby cry’, and ‘water tap’. This Starter Model can easily be modified to add more labels. This contains 550 minutes of data, most of which is unlabeled background noise.

#### Capacitive and Inductive Sensing

1. - **Touch detection (CAPSENSE™)**: This Studio Accelerator allows you to build a touch detection model that can be used on any supported Infineon MCU with CAPSENSE™. This Studio Accelerator gives you the infrastructure you need to expand on the project or to mimic it and create your own project based on the available/included data and tools.

#### Camera

1. - **Rock Scissors Paper Detection**: This Studio Accelerator is a real-time gesture recognition model powered by YOLO-based backend for detecting and classifying hand gestures. The project aims to build a robust end-to-end system that identifies rock, scissors, and paper gestures from live video input.
2. - **Termite Detection**: This Studio Accelerator allows you to build a model that can detect termites. The model aims to build a robust end-to-end system that identifies termites from live video input. The YOLO-based termite object detection model can be applied in various fields, such as biology research for termite population and species counting, as well as in house and garden maintenance to manage termite infestations.
