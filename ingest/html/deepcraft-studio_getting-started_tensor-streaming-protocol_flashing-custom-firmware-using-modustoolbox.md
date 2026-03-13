---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/flashing-custom-firmware-using-modustoolbox"
fetched_at: "2026-03-10T15:51:21Z"
title: "Flashing Custom Firmware Using Modustoolbox"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "tensor-streaming-protocol"]
---

# Flashing Custom Firmware Using Modustoolbox

### Flashing your custom firmware using ModusToolbox™

This topic provides instructions for flashing custom firmware onto Infineon boards using ModusToolbox™ to facilitate real-time data collection and model evaluation.

To facilitate understanding, we will demonstrate the process of flashing custom firmware on Infineon PSoC™ 6 AI Evaluation Kit. You can follow the same steps to flash the firmware on other Infineon boards that support flashing through ModusToolbox™.

For flashing information on boards other than Infineon boards, refer to your specific board documentation.

#### Pre-requisites:

- - Download and Install [ModusToolbox™](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox)(version 3.3 or later)
- - Custom Firmware Repository
- - Infineon PSOC™ 6 board

#### Flashing the firmware using ModusToolbox™

Flashing the firmware using ModusToolbox consists of two parts:

- - Create and build the project
- - Flash and run the project

##### Create and Build the project

1. - Open **ModusToolbox™ > Eclipse IDE for ModusToolbox™** from the Windows **Start menu**. The Eclipse IDE for ModusToolbox window appears.
2. - Browse and select the workspace directory for your project.
3. - Click **Launch** to open the ModusToolbox™ workspace.
4. - Select **New Application** from the Quick Panel or navigate to **File> New> Modus Toolbox™ Application** to open the Project Creator Tool.
5. - Expand **PSOC™6 BSPs**, select **CY8CKIT-062S2-AI** as the BSP for your board and click Next. The Select Application window appears.
6. - Click **Browse for Application** and select the folder containing your Custom Firmware.
7. - Select the checkbox against the firmware and click to change the firmware name to something concise, for instance custom\_firmware.
8. - Click **Create** to create the project. After the project is created successful, the following window appears.
9. - Right-click the *custom\_firmware* project and select **Build Project** or click **Build Application** in the Quick panel to build the project.

##### Flash and Run the project

1. - Connect the **KitProg3 USB connector (J1)** port on the board with the PC using the USB cable.
2. - In **Quick Panel> Launches**, click **custom\_firmware\_Program**. The firmware is flashed on the development kit.
3. - Disconnect the USB cable from KitProg3 USB connector (J1) and connect to KitProg3 USB connector (J2) port on the board.

You can start collecting the real-live data using the PSoC™ 6 AI Evaluation Kit, refer to [Collect real-time data using Graph UX](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-new-streaming-firmware) to know more.
