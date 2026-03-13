---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/infineon-PSoC6-wi-fi-pioneer-kit"
fetched_at: "2026-03-10T15:51:17Z"
title: "Infineon Psoc6 Wi Fi Pioneer Kit"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "infineon-boards"]
---

# Infineon Psoc6 Wi Fi Pioneer Kit

### Infineon PSOC™ 6 Wi-Fi BT Pioneer Kit and IoT sense expansion kit

[PSOC™ 62S2 Wi-Fi BT Pioneer Kit](https://www.infineon.com/cms/en/product/evaluation-boards/cy8ckit-062s2-43012/?tab=~%27all#!designsupport) (CY8CKIT-062S2-43012) is a feature rich hardware evaluation platform that enables development of applications based on the PSOC™ 62 series MCU. The kit also includes a wireless module based on the AIROC™ CYW43012 combo device to develop cloud connected IoT applications including Matter over Wi-Fi applications.

[IoT sense expansion kit](https://www.infineon.com/cms/en/product/evaluation-boards/cy8ckit-028-sense/) (CY8CKIT-028-SENSE) is a low-cost Arduino™ UNO compatible shield board that can be used to easily interface a variety of sensors with the PSoC™ 6 MCU platform, specifically targeted for audio and machine learning applications.

|  |
| --- |

#### Streaming Firmware for PSOC™ 6 Wi-Fi BT Pioneer Kit

The Streaming firmware (HEX files) for PSOC™ 6 Wi-Fi BT Pioneer Kit is implemented using Protocol version 1. Protocol version 1 is deprecated and we recommend using Protocol version 2 for improved performance and easy implementation. If you want to collect data using Protocol Version 2, you need to implement your custom streaming firmware. Refer to [Registering sensors and boards for data streaming using Protocol version 2](https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2) for detailed instructions on how to implement the firmware.

Streaming Firmware implemented using Protocol version 1 for PSOC™ 62S2 Wi-Fi BT Pioneer Kit supports data collection using a mono microphone at 16 kHz and an accelerometer at 50 Hz. However, the Streaming Protocol supports data collection from all types of sensors at different rates. If you want to use the Streaming Firmware without any modifications, flash the development kit with ModusToolbox™ Programmer. For collecting data at different rates or adding support for additional sensors, you can customize the firmware, refer to [Implement your own firmware](https://developer.imagimob.com/getting-started/tensor-streaming-protocol#implement-your-own-firmware) to know more.

The Streaming firmware for the PSOC™ 62S2 Wi-Fi BT Pioneer Kit is implemented using Protocol version 1. For customization, we recommend using Protocol version 2 for improved performance and easier implementation. Refer [Streaming Protocol for Real-Time Data Collection](https://developer.imagimob.com/getting-started/tensor-streaming-protocol) to know more.

#### Flashing Streaming Firmware

Following are the steps to flash the Streaming Firmware onto Infineon PSOC™ 6 Wi-Fi BT Pioneer Kit and IoT sense expansion kit to facilitate real-time data collection.

##### Pre-requisites:

- - [Streaming Firmware - PSOC™ 62S2 Wi-Fi BT Pioneer Kit](https://developer.imagimob.com/Resources/imagimob-streaming-firmware.zip) (HEX Files)
- - [Cypress Programmer](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.cypressprogrammer) (Flash Utility)
- - [PSOC 6 Wi-Fi BT Pioneer Kit](https://www.infineon.com/cms/en/product/evaluation-boards/cy8ckit-062s2-43012/?tab=~%27all#!designsupport) (CY8CKIT-062S2-43012)
- - [IoT sense expansion kit](https://www.infineon.com/cms/en/product/evaluation-boards/cy8ckit-028-sense/) (CY8CKIT-028-SENSE)

Before attaching the expansion kit on the Pioneer Kit, check the revision printed on the back of the expansion kit (nine‑axis or six‑axis inertial measurement unit) to select the corresponding hex file when flashing.

##### Steps to flash the Streaming Firmware onto the PSOC™6 Wi-Fi BT Pioneer Kit

After the pre-requisites are met, follow the steps to flash the firmware:

1. - Download and unzip the hex file to flash the Streaming Firmware onto the board.
2. - Connect the **KitProg3** USB port on the board with the PC using the USB cable.
3. - Open ModusToolbox™ Programmer from the Windows **Start menu**. The ModusToolbox™ Programmer window appears.

  ![](https://developer.imagimob.com/Images/psoc6/pic-1.png)
4. - In the **Programmer** drop-down box, select the device type as *CY8CKIT-062S2-43012-XXXXXXXXXXXXXXXX*.
5. - In **Board** drop-down box, select the board type as **CY8CKIT-062S2-43012**.

Make sure you select the hex file compatible with the revision of the expansion kit:

- - For Rev\*\* (nine-axis inertial measurement unit), select *mtb-example-imagimob-streamer-shield-nine-axis.hex* file.
- - For Rev\* A, Rev\*B or later (six-axis inertial measurement unit), select *mtb-example-imagimob-streamer-shield-six-axis.hex* file.

1. - Click **Open** and navigate to select the Streaming Firmware (hex file) downloaded earlier.

  ![](https://developer.imagimob.com/Images/psoc6/pic-2.png)
2. - Click **Connect** to establish a connection between the board and the ModusToolbox™ Programmer.
3. - Click **Program** to flash the Streaming Firmware on the board. The firmware is flashed on the development kit.

  ![](https://developer.imagimob.com/Images/psoc6/pic-3.png)

After flashing, follow the instructions in [Real-Time Data Collection from Sensors using old streaming firmware/protocol](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-using-graph-ux) section to stream data from the kit. However, if you implement your firmware using Protocol version 2, follow the steps outlined in this [section](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-ai-kit) to stream data from the kit.
