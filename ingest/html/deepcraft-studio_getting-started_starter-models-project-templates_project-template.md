---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/starter-models-project-templates/project-template"
fetched_at: "2026-03-10T15:51:15Z"
title: "Project Template"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "starter-models-project-templates"]
---

# Project Template

### Project Templates

We provide project templates to facilitate your Edge AI journey with DEEPCRAFT™ Studio. Project templates include an empty classification, regression or object detection projects that allow you to create a machine learning model from scratch. You can either use your own dataset or collect data using DEEPCRAFT™ Studio to build, train and deploy a machine learning model as per your business scenarios.

The templates include a project file (.improj) that contains the essential tools and resources to streamline the development workflow of a machine learning model. To know about the the project file, refer to [Studio Project File](https://developer.imagimob.com/getting-started/advanced-functionality/studio-project-file).

### How do I use a Project Template?

1. - Open DEEPCRAFT™ Studio.
2. - Click **New Project** in the welcome screen. The welcome screen appears, when you open the Studio for the first time.
  OR
  Go to **File** and select **New Project**. The New Project window appears.
3. - Navigate to **Templates** and select the project template - **Classification**, **Regression** or **Vision**, depending on the type of model you want to build.

  ![](https://developer.imagimob.com/Images/ai-kit/img-37.png)
4. - In **New Project Name**, enter the name of the project.
5. - In **Location**, specify the location where you want to create the workspace and the project directory.

We do not recommend creating workspace in the directories that are synced with OneDrive due to this [known issue](https://answers.microsoft.com/en-us/msoffice/forum/all/onedrive-bug-the-tag-present-in-the-reparse-point/214c1387-adf9-4d7c-abd7-110eea4121ec) in OneDrive.

1. - Select **Download project data** checkbox to download the project data to the workspace selected earlier.
2. - This is an optional step and applicable only if you plan to deploy your model to the PSOC Edge boards and do not have a ModusToolbox™ project. Select the **Create ModusToolbox™ Project** checkbox to launch ModusToolbox™ Project Creator and create the required ModusToolbox™ project. To know how to create the ModusToolbox project from Studio, refer to [Creating ModusToolbox™ project from Studio](https://developer.imagimob.com/deepcraft-studio/getting-started/starter-models-project-templates/project-template#creating-modustoolbox-project-from-studio).
  After the project is created, Studio automatically saves the project path. During code generation for PSOC Edge boards, the saved ModusToolbox™ project path is available as a selectable output location. Select the desired ModusToolbox™ project and Studio will place the generated code directly into that project. To know more, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).
3. - Click **OK** to download the data and create the project in studio. After you download the project template, you can start collecting data to build your model as per your needs.Refer to [Data Collection](https://developer.imagimob.com/data-preparation/data-collection) to know how to collect data in DEEPCRAFT™ Studio and [Data Preparation](https://developer.imagimob.com/data-preparation#data-preparation) to understand the different steps involved after collecting the data in Studio.

- - If you select Empty project as the project type, only the project directory structure is downloaded to the workspace.
- - If you have an existing ModusToolbox™ project for PSOC Edge board and plan to use the same for deployment, launch DEEPCRAFT™ Studio from within ModusToolbox™: open ModusToolbox™, select your project, go to Quick Panel > Library Configurator, and click DEEPCRAFT™ Studio. Studio will launch and automatically save the project path. During code generation for PSOC boards, this saved path is available as a selectable output location. Select the desired ModusToolbox™ project and Studio will place the generated code directly into that project. To know more, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).

#### Creating ModusToolbox™ project from Studio

To simplify and streamline the deployment workflow for PSOC™ Edge boards, we offer the capability to launch ModusToolbox™ Project Creator directly from DEEPCRAFT™ Studio. This functionality enables you to create the ModusToolbox™ project corresponding to the Studio project. This integration ensures consistency, minimizes manual intervention, and streamlines the overall development-to-deployment workflow. For detailed explanation, refer to [ModusToolbox™ Integration](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-integration).

**To Launch and create the project in ModusToolbox™, follow the steps**:

1. - After you select the **Create ModusToolbox Project** checkbox and click ok to launch the project creator. The Choose Board window appears.

  ![](https://developer.imagimob.com/Images/getting-started/starter-models/pic-3.png)
2. - Expand the Kit Name from the list and select the required MCU as BSP for your board and click **Next**. The Select Application window appears.

  ![](https://developer.imagimob.com/Images/getting-started/starter-models/pic-4.png)
3. - In **Template Application**, expand **Machine Learning** and select the required deploy code example and click **Create**. After the project is created successful, the code example appears in the ModusToolbox™.

During code generation in Studio, select the ModusToolbox™ project as the output location to automatically place the generated code into that project. Refer to [ModusToolbox™ Project](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-infineon-boards#modustoolbox-project) to know more.
