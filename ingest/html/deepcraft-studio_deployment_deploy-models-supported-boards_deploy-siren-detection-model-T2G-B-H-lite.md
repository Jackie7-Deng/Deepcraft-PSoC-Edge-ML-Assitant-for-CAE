---
source_url: "https://developer.imagimob.com/deepcraft-studio/deployment/deploy-models-supported-boards/deploy-siren-detection-model-T2G-B-H-lite"
fetched_at: "2026-03-10T15:51:55Z"
title: "Deploy Siren Detection Model T2g B H Lite"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "deployment", "deploy-models-supported-boards"]
---

# Deploy Siren Detection Model T2g B H Lite

### Deploy siren detection model on TRAVEO™ T2G (KIT_T2G-B-H_LITE)

This section explains how to deploy the siren detection model on TRAVEO™ T2G Body High Lite evaluation kit (KIT\_T2G-B-H\_LITE) using ModusToolbox™. We provide a code example with a pre-generated model, ready for deployment.

#### Objective

This tutorial aims to demonstrate the following features:

- - how to use the I2S interface
- - Capture live PCM samples from the microphone and feed the samples into Imagimob model to recognize siren sounds
- - print the detection results via serial interface (UART) to a terminal

If a microphone is not available, you can flash PCM data directly onto the MCU to evaluate the AI model. Instructions for this process are provided in [Generating PCM Data](https://developer.imagimob.com/getting-started/infineon-boards-imagimob-studio/deploy-siren-detection-model-T2G-B-E-lite#generating-pcm-data).

#### Prerequisites

- - Download the [Code Example](https://developer.imagimob.com/Resources/SirenDetection_T2GBodyHigh.zip)
- - Download and Install [ModusToolbox](https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox)
- - Hardware boards
  * 1x [TRAVEO™ T2G (KIT\_T2G-B-H\_LITE)](https://www.infineon.com/cms/de/product/evaluation-boards/kit_t2g-b-h_lite/)
  * 1x [S2GO MEMSMIC IM69D](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-memsmic-im69d/)
  * 1x custom-built adapter board

While jumper cables can be used as an alternative to adapter boards, our internal testing has shown that jumper cables were not reliable. Therefore, we recommend creating an adapter board.

#### Hardware Boards

- - **KIT\_T2G-B-H-LITE**

  |  |
  | --- |
- - **S2GO MEMSMIC IM69D**: The S2GO MEMSMIC IM69D integrates two IM69D130 Digital MEMS microphones that generate PDM signals. The S2GO MEMSMIC IM69D includes a PDM to I2S converter, allowing to connect the microphones to the I2S interface of the TRAVEO™ T2G device directly.

  |  |
  | --- |
- - **Adapter Board**: The S2GO MEMSMIC IM69D cannot be connected to the S2GO interfaces on the board because the I2S-pins do not match. Instead, we will use the following pins on the X1 40-pin header of the KIT\_T2G-B-H\_LITE.

  * X1\_1/GND -> GND
  * X1\_2/3V3 -> 3V3
  * X1\_32/ADC1\_19 -> AUDIOSS1\_RX\_SDI
  * X1\_33/SPI\_CS3 -> AUDIOSS1\_RX\_WS
  * X1\_34/SPI\_CS2 -> AUDIOSS1\_RX\_SCK
  * X1\_40/GND -> GND

    | KIT_T2G-B-H_LITE Pins |
    | --- |

Don’t be confused by pins labeled as ADC or SPI. On the MCU, there are more peripherals than pins, so most pins have various functions multiplexed. While the schematic intends to use the pins as ADC or SPI, they can also be used as I2S\_RX pins without any issues when configured properly. For detailed functionality of each pin, refer to the datasheet of the device.

On the S2GO MEMSMIC IM69D, we use the following pins:

- - 6 -> GND
- - 7 -> 3V3
- - 14 -> I2S: CLK
- - 15 -> I2S: BCLK
- - 17 -> I2S: DATA

| S2GO_MEMSMIC Pins |
| --- |

After identifying all relevant pins, we need to make the following connections (left: pin number of S2GO MEMSMIC IM69D, right: pin number of KIT\_T2G-B-H\_LITE):

- - 6 -> X1\_1 and X1\_40 (connecting only one is also fine)
- - 7 -> X1\_2
- - 14 -> X1\_34
- - 15 -> X1\_32
- - 17 -> X1\_34

We highly recommend building an adapter board for these connections. When using jumper cables, we found signal integrity issues in our internal testing. For the adapter board, you have two options, either design and manufacture a PCB or manually solder one using pin headers, cables, and a perforated board with copper traces.

For this project, we created a manually soldered board, which looks like this:

**Top:**

![Adapterboard top](https://developer.imagimob.com/Images/traveo/adapterboard_top.jpg)

**Bottom:**

![Adapterboard bottom](https://developer.imagimob.com/Images/traveo/adapterboard_bot.jpg)

The cable colors represent the following signals:

- - Black: GND
- - Red: 3V3
- - Green: AUDIOSS1\_RX\_WS/WCLK
- - Yellow: AUDIOSS1\_RX\_SCK/BCLK
- - Blue: AUDIOSS1\_RX\_SDI/DATA

The adapter board is then attached on the bottom side of the board on the X1 header:

![Adapterboard on T2G](https://developer.imagimob.com/Images/traveo/adapterboard_on_t2g.jpg)

#### Hardware Setup

For the hardware setup, connect the microphone to the board, and then connect the board to the PC via USB.

### Implementation

The application does the following:

- - Initialize the board, Imagimob model, UART via retarget-io, and I2S interface
- - Using an interrupt, retrieve PCM data from I2S peripheral and store the data in a buffer continuously.
- - In a loop:
  * converts the sample from I2S buffer to float and scale it to model input range
  * inputs sample into the model
  * if sufficient samples are available, obtain the classification result
  * print the timestamp and classification result via UART to the serial monitor

To configure the I2S peripheral, the device configurator was used and set to the appropriate settings for the S2GO MEMSMIC IM69D. The generated configuration was then copied to main.c for convenience. If you intend to use a different I2S source, you can change the settings accordingly.

#### Compiling and Running

1. - Open **ModusToolbox™ > Eclipse IDE for ModusToolbox™** from the Windows **Start menu**. The Eclipse IDE for ModusToolbox window appears.
2. - Browse and select the workspace directory for your project.
3. - Click **Launch** to open the ModusToolbox™ workspace.
4. - Select **Import Existing Application In-Place** from the Quick Panel. The Import ModusToolbox™ Project window appears.
5. - Browse and select the code example folder downloaded earlier and click **Finish**. The code example is imported into the ModusToolbox™.
6. - Navigate to the Terminal and run the command *make getlibs* to ensure all necessary libraries are downloaded.
7. - In **Launches**, click on **Generate Launches for SirenDetection\_T2GBodyHigh** after the libraries are imported.
8. - Click on Siren Detection\_T2gBodyHigh Program(KitProg3\_MiniProg4) to build and flash the application onto the board. You can view the current status in the console.

  ![](https://developer.imagimob.com/Images/traveo/mtb_serial_monitor.png)

Once the flashing process is complete, you need to open a serial monitor. You have two options: you can either use an external tool like [PuTTY](https://putty.org/), or the integrated serial monitor in ModusToolbox™. For latter, click on the terminal window, then on the terminal icon, and select Serial Terminal and configure the following settings:

- - Serial port: Choose port of device, depends on local machine
- - Baud rate: 115200
- - Data size: 8
- - Parity: None
- - Stop bits: 1
- - Encoding: Default (ISO-8859-1)

After completing these steps, you should observe the following output:

![](https://developer.imagimob.com/Images/traveo/body-high-output.png)

The application continuously analyzes the incoming PCM stream and prints the current timestamp in seconds. If a siren sound is detected with a probability exceeding 70%, the classification results will be printed. If no siren sound is detected, only the timestamps will be printed. For example, an output of None: 0.13 Sound: 0.87 indicates that the model is 87% confident that a siren sound is detected, while the 0.13 represents the confidence level for no siren sound. For testing purposes, this [video](https://www.youtube.com/watch?v=3TiQB7_YfZw) was played back through mobile phone speakers.
