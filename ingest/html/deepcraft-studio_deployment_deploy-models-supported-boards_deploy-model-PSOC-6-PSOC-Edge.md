---
source_url: "https://developer.imagimob.com/deepcraft-studio/deployment/deploy-models-supported-boards/deploy-model-PSOC-6-PSOC-Edge"
fetched_at: "2026-03-10T15:51:54Z"
title: "Deploy Model Psoc 6 Psoc Edge"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "deployment", "deploy-models-supported-boards"]
---

# Deploy Model Psoc 6 Psoc Edge

### Deploy model on PSOC™ 6 and PSOC™ Edge boards

For deploying the computer vision models, refer to [Deploy Vision Model on PSOC™ Edge boards](https://developer.imagimob.com/deepcraft-studio/deployment/deploy-models-supported-boards/deploy-vision-model-PSOC-Edge).

In this section, we cover information on how to deploy an Imagimob-generated machine learning model for PSOC™ 6 and PSoC™ Edge using ModusToolbox™. To demonstrate this, we will use a code example provided within ModusToolbox™. We offer a variety of code examples designed for different use cases for both PSOC™ 6 and PSoC™ Edge, simplifying the deployment process.
You need to create the required machine learning project for your board within ModusToolbox™ and then replace the model.c and model.h files in the project with the model.c and model.h files for your model following by building the project. Follow the step-by-step instructions to learn the deployment process.

#### Pre-requisites:

- - Download and Install [ModusToolbox™](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox) (recommended v3.4 or later)
- - Infineon PSOC™ 6 or PSOC™ Edge board on which you want to deploy the model

#### Code Examples for PSOC™ 6 and PSOC™ Edge

The following code examples are available for PSOC™ 6 AI Evaluation Kit in ModusToolbox™:

- - [DEEPCRAFT™ Studio Deploy Model: Audio](https://github.com/Infineon/mtb-example-ml-deepcraft-deploy-audio)
- - [DEEPCRAFT™ Studio Deploy Model: Motion](https://github.com/Infineon/mtb-example-ml-deepcraft-deploy-motion)
- - [DEEPCRAFT™ Studio Deploy Model: Radar](https://github.com/Infineon/mtb-example-ml-deepcraft-deploy-radar)

The following code examples are available for PSOC™ Edge in ModusToolbox™:

- - [DEEPCRAFT™ Studio Deploy Model: Audio](https://github.com/Infineon/mtb-example-psoc-edge-ml-deepcraft-deploy-audio?tab=readme-ov-file)
- - [DEEPCRAFT™ Studio Deploy Model: Motion](https://github.com/Infineon/mtb-example-psoc-edge-ml-deepcraft-deploy-motion)
- - [DEEPCRAFT™ Studio Deploy Model: Radar](https://github.com/Infineon/mtb-example-psoc-edge-ml-deepcraft-deploy-radar)

#### How to deploy the model onto the board?

Deploying the model using ModusToolbox™ consists of two parts:

- - Create and build the project
- - Flash and run the project

We will show how to deploy the model on PSoC™ 6 AI Evaluation Kit, similarly you can deploy the model on PSOC™ Edge.

#### Create and Build the project

1. - Open **ModusToolbox™ > Eclipse IDE for ModusToolbox™** from the Windows **Start menu**. The Eclipse IDE for ModusToolbox window appears.
2. - Browse and select the workspace directory for your project and click **Launch** to open the ModusToolbox™ workspace.
3. - Select **New Application** from the Quick Panel or navigate to **File> New> Modus Toolbox™ Application** to open the Project Creator Tool.

  ![](https://developer.imagimob.com/Images/project-tool.png)
4. - Expand the Kit Name PSoC™ 6 from the list and select the CY8CKIT-062S2-AI as BSP for your board and click **Next**. The Select Application window appears.

  ![](https://developer.imagimob.com/Images/img1.png)
5. - In **Template Application**, expand **Machine Learning** and select the required deploy code example and click **Create**.

  ![](https://developer.imagimob.com/Images/img2.png)
6. - After the project is created successful, navigate to the *models* directory and substitute the provided example *model.c* and *model.h* files with the actual *model.c* and *model.h* files that you have generated for your model.

  ![](https://developer.imagimob.com/Images/img3.png)
7. - Right-click the project and select **Build Project** or click **Build Application** in the Quick panel to build the project.

  ![](https://developer.imagimob.com/Images/img4.png)

#### Flash and Run the project

1. - Connect the USB port on the board with the PC using the USB cable.
2. - In **Quick Panel> Launches**, click the program. The code is deployed on the board.

  ![](https://developer.imagimob.com/Images/img5.png)
