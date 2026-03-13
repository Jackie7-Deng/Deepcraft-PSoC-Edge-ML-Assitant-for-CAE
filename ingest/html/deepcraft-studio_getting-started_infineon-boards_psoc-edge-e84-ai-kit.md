---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-ai-kit"
fetched_at: "2026-03-10T15:51:16Z"
title: "Psoc Edge E84 Ai Kit"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "infineon-boards"]
---

# Psoc Edge E84 Ai Kit

### PSOC™ Edge E84 Artificial Intelligence Kit

The PSOC™ Edge E84 Al Kit is a low-cost kit with multiple sensors designed for rapid prototyping of ML/AI-powered applications. It features the PSOC™ Edge E84 series microcontroller (MCU) and a multitude of on-board multimedia, machine learning and connectivity features. The evaluation kit carries a PSOC™ Edge E84 MCU, with 512-Mbit QSPI flash, 128-Mbit Octal RAM, and a AIROC™ CYW55513IUBGT based Wi-Fi & Bluetooth® combo Murata Type 2FY (LBEE5HY2FY) connectivity module. This kit features an on-board programmer/debugger (KitProg3) SWD debug header, a MIPI-DSI connector, speaker interface, USB host and device interfaces, IO expansion headers, IMU sensor, magnetometer, barometric pressure sensor, radar and, analog and digital microphones for audio interfaces, and an image sensor. For more information, refer to [KIT\_PSE84\_AI](https://www.infineon.com/evaluation-board/kit-pse84-ai).

#### Kit contents

The kit includes the following:

- - PSOC™ Edge E84 AI board
- - OV7675 DVP Camera module

|  |
| --- |

#### Key applications

Following are some of the applications that you can build using the kit:

| **Category** | **Applications** |
| --- | --- |
| Smart Home | Smart thermostats, smart locks, smart home appliances |
| HMI | Appliances, Industrial HMI, factory automation |
| Wearables | Fitness watches, AR/MR/VR glasses & accessories, audio accessories |
| Robotics | Vacuum cleaners, vacuum robots, service robots, industrial robotics |

#### Streaming Firmware for PSOC™ Edge E84 AI Kit

You can flash the PSOC™ Edge E84 AI kit with streaming firmware that streams sensor data from the USB port into DEEPCRAFT™ Studio, enabling rapid data collection and model creation. The streaming firmware is designed to collect data from all the sensors integrated into the kit, including the microphone, accelerometer, gyroscope, magnetometer, pressure-temperature, humidity-temperature and radar.

There are two ways to flash the Streaming Firmware onto the kit:

- - Using Web-based OOB webpage
- - Using ModusToolbox™ Programmer

#### Flashing the Streaming Firmware using OOB Web Page

To flash the streaming firmware onto the kit, follow the pre-requisites and steps outlined below:

1. - Connect the **KitProg3 USB connector (J1)** port on the board to the PC using the USB cable. The green LED (LED1) starts blinking.
2. - Navigate to [Web-based OOB webpage](https://osts.infineon.com/devkit). The landing page displays a list of available kits.

  |  |
  | --- |
3. - Locate the PSOC™ Edge E84 AI Kit and click **Select**. The PSOC™ Edge E84 AI Kit screen appears.
4. - In **Select application** and **Select Module**, select the required application and the use-case respectively.

  |  |
  | --- |
5. - In **Select Port for Device**, click the Add icon to to initiate the connection. In the dialog, select the device type **KitProg3 CMSIS-DAP** and click **Connect**. The device is ready for flashing.

  |  |
  | --- |
6. - In **Select application**, navigate to **Experience Application with DEEPCRAFT™ Studio** and click **Continue** to program the streaming firmware onto the board.

  |  |
  | --- |
7. - The flashing process is initiated. The following screen appears.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-26.png)

After the kit is programmed successfully. Refer to [Real-Time Data Streaming with PSOC™ Edge E84 Artificial Intelligence Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit) to collect and label real-time data into Studio.

#### Flashing the Streaming Firmware using ModusToolbox™ Programmer

To flash the streaming firmware onto the kit, follow the pre-requisites and steps outlined below:

##### Pre-requisites:

- - [Streaming Firmware - PSOC™ Edge E84 AI Kit](https://developer.imagimob.com/Resources/KIT_PSE84_AI_data_collection.zip) (HEX File)
- - Download and Install [ModusToolbox™ Programmer](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolboxprogtools) v3.8 and above (Flash Utility)
- - PSOC™ 6 Edge E84 AI Kit (KIT\_PSE84\_AI)

##### Steps to flash the Streaming Firmware

1. - Download and unzip the hex file to flash the Streaming Firmware onto the board.
2. - Connect the KitProg3 USB connector (J1) port on the board to the PC using the USB cable.
3. - Open ModusToolbox™ Programmer from the Windows Start menu. The ModusToolbox™ Programmer window appears.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-27.png)
4. - In **Programmer** drop-down box, select the device type as **KitProg3 CMSIS-DAP BULK-XXXXXXXXXXXXXXXX**.
5. - In **Board** drop-down box, select the board type as **KIT\_PSE84\_AI**.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-27.png)
6. - Click **Open** and navigate to select the Streaming Firmware (hex file) downloaded earlier.
7. - Click **Connect** to establish a connection between the board and the ModusToolbox™ Programmer.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-27.png)
8. - Click **Program** to flash the Streaming Firmware on the board. The kit is programmed successfully.

#### What’s Next?

After flashing the kit with the streaming firmware, disconnect the KitProg3 USB connector (J1) port and connect the KitProg3 USB connector (J2) port with the PC using the USB cable. Refer to [Real-Time Data Streaming with PSOC™ Edge E84 Artificial Intelligence Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit) to collect and label real-time data into Studio.
