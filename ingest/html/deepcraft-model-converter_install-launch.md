---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/install-launch"
fetched_at: "2026-03-10T15:52:05Z"
title: "Install and Launch"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "install-launch"]
---

### Install and Launch

This section covers steps on how to install the DEEPCRAFT™ Model Converter and launch the DEEPCRAFT™ Model Converter **Graphical User Interface** and **Command Line Interface**.

#### Install DEEPCRAFT™ Model Converter

![](https://developer.imagimob.com/Images/model-converter/pic-9.png)

1. - Navigate to the [Infineon Developer Center](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.deepcraftmodelconverter).
2. - Download the executable file corresponding to your operating system (Windows, Mac, or Linux).
3. - Locate and run the executable file to launch the setup wizard.
4. - Select the installation mode - **Quick Installation** or **Custom Installation** and follow the prompts to complete the installation.
5. - Read the terms of license agreement. If you agree, select **I accept the agreement** and click **Next**.
6. - Upon successful installation, the DEEPCRAFT™ Model Converter will be available for use in both **Graphical User Interface (GUI)** and **Command-Line Interface (CLI)** modes.

#### Launch DEEPCRAFT™ Model Converter

##### Graphical User Interface (GUI)

Upon successful installation, the DEEPCRAFT™ Model Converter GUI mode will launch automatically. Refer to [Graphical User Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-gui) to know how to generate code for models.

![](https://developer.imagimob.com/Images/model-converter/pic-2.png)

##### Command-Line Interface (CLI)

Upon successful installation, open a command prompt, type **dcmc —help** and press Enter. A command prompt window appears listing all the available commands. Refer to [Command Line Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-cli) to know how to generate code for models.

![](https://developer.imagimob.com/Images/model-converter/pic-4.png)

#### Pre-requisites for PyTorch models

When generating the code for PyTorch models, two primary options are available:

- - **Cloud-Based Code Generation**: When you select this option, the PyTorch model is uploaded to the Imagimob Cloud for code generation, requiring you to sign in with your Imagimob company email and password. If you do not have an Imagimob account, create one [here](https://account.imagimob.com/signup).
- - **Container-Based Code Generation**: When you select this option, the PyTorch model is not uploaded to the Imagimob Cloud and code generation runs locally using a downloaded PyTorch Converter Container. You can either setup Docker or Podman Container as per your requirement. Refer to [Setup Docker or Podman Container](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/container-setup) for the detailed steps.

Before generating code for PyTorch models, you must configure one of the following options. Step-by-step instructions are available in the GUI and CLI sections.

- - Before generating code for PyTorch models, you must configure one of the following options. Step-by-step instructions are available in the GUI and CLI sections.
- - The Local PyTorch Converter container allows you to generate code locally from your models, using the same tested code as the cloud API, however, we do not provide the technical support for the container.

#### Whats Next?

Lets learn how to generate, optimize and validate the code for the model, refer to [Graphical User Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-gui) and [Command Line Interface](https://developer.imagimob.com/deepcraft-model-converter/model-converter-cli).
