---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-eval-kit"
fetched_at: "2026-03-10T15:51:16Z"
title: "Psoc Edge E84 Eval Kit"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "infineon-boards"]
---

# Psoc Edge E84 Eval Kit

### PSOC™ Edge E84 Evaluation Kit

The PSOC™ Edge E84 Evaluation Kit is a general purpose evaluation kit for PSOC™ Edge with full functional integration of all interfaces. The kit enables applications to use the PSOC™ Edge E84 Series Microcontroller (MCU) together with multiple on-board multimedia, Machine Learning (ML), and connectivity features including custom MIPI-DSI displays, audio interfaces, and AIROC™ Wi-Fi and Bluetooth combo-based connectivity modules. The kit carries a PSOC™ Edge E84 MCU on a SODIMM-based detachable SOM board connected to the baseboard. The MCU SOM also has 128 MB of QSPI Flash, 1GB of Octal Flash, 128MB of Octal RAM, PSOC™ 4000T as CAPSENSE™ co-processor, and on-board AIROC™ Wi-Fi and Bluetooth combo. The baseboard has M.2 interface connectors for external radio modules based on AIROC™ Wi-Fi and Bluetooth combos and external memory. It also features an on-board programmer/debugger (KitProg3), ETM/JTAG/SWD debug headers, a custom display capacitive touch-panel connector, RPi compatible MIPI-DSI and a MIPI-DSI custom display connectors, analog and PDM microphones, a headphone connector, a speaker, USB host Type-A and USB device Type-C connectors, an RJ45 Ethernet connector, M.2 (B-key) memory and M.2 (E-key) radio interfaces, Infineon’s Shield2Go interface, MIKROE’s mikroBUST”-compatible headers, a 6-Axis IMU sensor, a 3-axis magnetometer, a microSD card holder, CAPSENSE™ buttons and slider, user LEDs, and user buttons. For more information, refer to [KIT\_PSE84\_EVAL\_EPC2/KIT\_PSE84\_EVAL\_EPC4](https://www.infineon.com/evaluation-board/kit-pse84-eval#documents).

#### Kit contents

The KIT\_PSE84\_EVAL PSOC™ Edge E84 Evaluation Kit box includes the following:

- - PSOC™ Edge E84 Evaluation Kit
  * PSOC™ Edge E8 base board
  * PSOC™ Edge E84 SOM (MOD\_PSE84\_SOMS2)
- - USB Type-C to Type-C cable
- - 4.3 Inch Capacitive Touch Display
- - 0.3 MP USB Camera Module with USB Type-A Cable

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

#### Streaming Firmware for PSOC™ Edge E84 Evaluation Kit

You can flash the PSOC™ Edge E84 Evaluation kit with streaming firmware that streams sensor data from the USB port into DEEPCRAFT™ Studio, enabling rapid data collection and model creation. The streaming firmware is designed to collect data from all the sensors integrated into the kit, including the microphone, accelerometer, gyroscope and magnetometer.

There are two ways to flash the Streaming Firmware onto the kit:

- - Using Web-based OOB webpage
- - Using ModusToolbox™ Programmer

#### Flashing the Streaming Firmware using OOB Web Page

To flash the streaming firmware onto the kit, follow the pre-requisites and steps outlined below:

1. - Connect the **KitProg3 USB connector (J8)** port on the board to the PC using the Type-C to Type-C USB cable. Ensure that the power LED (D1, yellow) on the base board and the power LED (D3, yellow) on the SOM are ON.

  |  |
  | --- |
2. - Navigate to [Web-based OOB webpage](https://osts.infineon.com/devkit). The landing page displays a list of available kits.
3. - Locate the **PSOC™ Edge Evaluation Kit** and click **Select**.

  |  |
  | --- |
4. - In **Select application** and **Select Module**, select the required application and the use-case respectively

  |  |
  | --- |
5. - In **Select Port for Device**, click the **Add** icon to to initiate the connection. In the dialog, select the device type **KitProg3 CMSIS-DAP** and click **Connect**. The device is ready for flashing.

  |  |
  | --- |
6. - In **Select application**, navigate to **Experience Application with DEEPCRAFT™ Studio** and click **Continue** to program the streaming firmware onto the board.

  |  |
  | --- |
7. - The flashing process is initiated. The following screen appears.

  |  |
  | --- |

After the kit is programmed successfully. Refer to [Real-Time Data Streaming with PSOC™ Edge E84 Artificial Intelligence Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit) to collect and label real-time data into Studio.

#### Flashing the Streaming Firmware using ModusToolbox™ Programmer

To flash the streaming firmware onto the kit, follow the pre-requisites and steps outlined below:

##### Pre-requisites:

- - [Streaming Firmware - PSOC™ Edge E84 Evaluation Kit](https://developer.imagimob.com/Resources/KIT_PSE84_EVAL.zip) (HEX File)
- - Download and Install [ModusToolbox™ Programmer](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolboxprogtools) v3.8 and above (Flash Utility)
- - [PSOC™ Edge E84 Evaluation Kit (KIT\_PSE84\_EVAL)](https://www.infineon.com/evaluation-board/kit-pse84-eval)

##### Steps to flash the Streaming Firmware

1. - Download and unzip the hex file to flash the Streaming Firmware onto the board.
2. - Connect the **KitProg3 USB connector (J8)** port on the board to the PC using the Type-C to Type-C USB cable. Ensure that the power LED (D1, yellow) on the base board and the power LED (D3, yellow) on the SOM are ON.
3. - Open ModusToolbox™ Programmer from the Windows Start menu. The ModusToolbox™ Programmer window appears.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-21.png)
4. - In **Programmer** drop-down, select the device type as **KitProg3 CMSIS-DAP BULK-XXXXXXXXXXXXXXXX**.
5. - In **Board** drop-down box, select the board type as **KIT\_PSE84\_EVAL** for BSP KIT\_PSE84\_EVAL\_EPC2; for BSP KIT\_PSE84\_EVAL\_EPC4, select the board type as **custom** and device as **PSE846GPS4DBZC4A**.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-22.png)
6. - Select the **External Memory** checkbox.
7. - Click **Open**, browse to the Streaming Firmware (hex file) downloaded earlier, and select the hex file that matches your board: select **KIT\_PSE84\_EVAL\_EPC2\_data\_collection** for KIT\_PSE84\_EVAL\_EPC2 and **KIT\_PSE84\_EVAL\_EPC4\_data\_collection** for KIT\_PSE84\_EVAL\_EPC4.
8. - Click **Connect** to establish a connection between the board and the ModusToolbox™ Programmer.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-23.png)
9. - Click **Program** to flash the Streaming Firmware on the board. The kit is programmed successfully.

#### What’s Next?

After flashing the kit with the streaming firmware, disconnect the KitProg3 USB connector (J8) port and connect the USB connector (J30) port with the PC using the Type-C USB cable. Refer to [Real-Time Data Streaming with PSOC™ Edge E84 Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit) to collect and label real-time data into Studio.
