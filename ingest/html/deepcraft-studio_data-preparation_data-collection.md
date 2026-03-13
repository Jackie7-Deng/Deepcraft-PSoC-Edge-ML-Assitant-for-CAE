---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection"
fetched_at: "2026-03-10T15:51:23Z"
title: "Real-time Data Collection"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

### Real-time Data Collection

Data collection is one of the most important steps in building an efficient machine learning model. It is the process of creating new data from multiple sources for training the machine learning model. The performance of the machine learning model depends on the data on which it has been trained, so collecting qualitative data is crucial for developing a robust model. To simplify data collection for our users, Studio provides the functionality to stream data from any sensor or development kits directly into DEEPCRAFT™ Studio. The data fed into the Studio adheres to the required specifications, eliminating the need for data formatting and thus saving valuable time.

### How to collect and label real-time data in Studio?

You can collect and label real-time data using the following: **Infineon Boards**, **Without using a kit** or **Any development Board**.

Here are the main steps to stream real-time data using different boards or sensors:

#### Step 1: Choose the Board

Select the board you want to use to stream data into the Studio. You can choose from **PSOC™ Edge E84 AI Kit**, **PSOC Edge E84 Evaluation Kit**, **PSOC™ 6 AI Evaluation Kit**, **PSOC™ 6 Wi-Fi BT Pioneer Kit** or any other sensor or development board.

You can also collect and label audio and image data for various audio and computer-vision projects using built-in PC microphone or camera. To know more, refer to [Collect data without a kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-without-kit).

#### Step 2: Flash the Streaming Firmware onto the Board

Before collecting data, you need to flash the streaming firmware onto the board.

For the following Infineon kits, we provide the Streaming Firmware to collect real-time data. To know how to flash the streaming firmware onto the boards, refer to [PSOC™ Edge E84 AI Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-ai-kit), [PSOC Edge E84 Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-eval-kit), [PSOC™ 6 AI Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/infineon-ai-evaluation-kit), or [PSOC™ 6 Wi-Fi BT Pioneer Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/infineon-PSoC6-wi-fi-pioneer-kit) to know the detailed steps.

For other sensors or development boards, you will need to implement your own custom firmware using Streaming Protocol Version 2. Refer to [Streaming Protocol for Real-Time Data Collection](https://developer.imagimob.com/getting-started/tensor-streaming-protocol) to know about the protocol.
Refer to [Registering sensors and boards for data streaming using Protocol version 2](https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2) for detailed instructions on firmware implementation.

For flashing information on boards other than Infineon boards, refer to your specific board documentation.

#### Step 3: Select how to collect the real-time data: Serial or Wi-Fi

You can stream data from the board to Studio over **Serial connection** or **Wi-Fi network**.

- - **Stream data over serial connection**: Flash the kit with the streaming firmware and connect the board to the PC running Studio via USB, then start streaming data.
- - **Stream data over Wi-Fi network**: Flash the kit with the streaming firmware, enable the Wi‑Fi service on the board, select the board in the Studio to start streaming data. Refer to the section [How to stream data into Studio over Wi‑Fi network](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection#how-to-stream-data-into-studio-over-wifi-network) for step-by-step instructions.

Data streaming over Wi-Fi is supported only on PSOC™ 6 AI Evaluation Kit.

#### Step 4: Start collecting real-time data

Utilize the Graph UX functionality within Studio to stream data from any sensor or development board.

- - [Data Streaming with PSOC™ Edge E84 AI Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit)
- - [Data Streaming with PSOC™ Edge E84 Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit)
- - [Data Streaming with PSOC™ 6 AI Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-ai-kit)
- - [Real-Time Data Collection without a kit](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-without-kit)
- - [Real-Time Data Collection from PSOC™ 6 Wi-Fi BT Pioneer Kit Sensors using old streaming firmware/protocol version 1](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-using-graph-ux)
- - [Real-Time Data Collection using any development boards](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-other-boards)

#### Best practices

The following are some of the best practices for collecting data:

- - **Quality over Quantity**: Prioritize collecting high-quality data over large quantities. As the saying goes, “garbage in, garbage out.” While large datasets are valuable, the accuracy and relevance of the data are paramount for building better models.
- - **Imbalanced data**: In classification projects, ensure that you have balanced datasets. This means having an equal representation of each class to avoid bias and improve model performance.
- - **Diverse data**: Collect diverse data to build a robust model as diversity in data helps the model generalize better and perform well across different scenarios.
