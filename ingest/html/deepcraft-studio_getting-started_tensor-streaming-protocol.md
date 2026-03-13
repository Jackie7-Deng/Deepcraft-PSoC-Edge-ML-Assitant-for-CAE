---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol"
fetched_at: "2026-03-10T15:51:19Z"
title: "Streaming Protocol for Real-Time Data Collection"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "tensor-streaming-protocol"]
---

### Streaming Protocol for Real-Time Data Collection

Data collection is widely recognized as a significant bottleneck in machine learning. Collecting data from various sources, including data companies, open-source datasets, and surveys can be expensive and often involves additional tasks like data cleaning, which is time-consuming. To simplify data collection for our users, we offer the Streaming Protocol. Using this protocol, you can build the firmware to stream data from any sensor or development kit directly into DEEPCRAFT™ Studio. The data fed into the Studio adheres to the required specifications, eliminating the need for data formatting and thus saving valuable time. This topic will cover what the Streaming Protocol is, when to use, how to customize, and how to flash on your development kit.

#### What is Streaming Protocol?

Streaming Protocol is a comprehensive set of rules designed to facilitate the streaming of data from any sensor or development board or kit into DEEPCRAFT™ Studio. Using the Streaming Protocol, you can build your own firmware to stream and collect data for building a machine learning model and evaluating a model in real-time. We offer two versions of the Streaming Protocol:

- - **Protocol version 1**
- - **Protocol version 2**

##### Protocol version 1

Refer to the [Protocol version 1](https://github.com/Infineon/mtb-example-imagimob-streaming-protocol/tree/master) Bitbucket repository to know more about the protocol.

**Protocol version 1** is deprecated and we recommend using **Protocol version 2** for implementing your firmware for improved performance and easy implementation. However, we continue to support the backward compatibility. This means that if your firmware is currently implemented using Protocol version 1, you will still be able to stream data into Studio without any issues.

##### Protocol version 2

Protocol version 2, also referred to as Tensor Streaming Protocol, defines a streaming mechanism used for communication between a client and a board. The protocol is intended to work over TCP, UDP, serial port, and Bluetooth communication. This protocol is designed to handle multiple data streams from sensors, models, and playback devices, enabling efficient data transfer and processing in embedded systems. This protocol is based on protobuf3 and provide the DotNetCli test client to evaluate the implementation. Refer to the [Protocol version 2](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/) Bitbucket repository to know more about the protocol.

#### Implement your own firmware

Using the Streaming Protocol, you can implement custom firmware to stream data from any sensor or development board into the DEEPCRAFT™ Studio. With the Protocol version 2, we implemented the streaming firmware for streaming data into Studio, see [example-firmware](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/source/example-firmware/). Drawing inspiration from our implementation, you can either implement your own firmware from scratch or extend the existing firmware to support additional sensors to collect data at different rates.

For step-by-step instructions on how to register a sensor or multiple sensors using Protocol Version 2 or Protocol version 1, refer to [Registering sensors and boards for data streaming using Protocol version 2](https://developer.imagimob.com/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2) and [Registering sensors and boards for data streaming using Protocol version 1](https://developer.imagimob.com/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv1) respectively.

We recommend implementing the custom firmware using [Protocol version 2](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/), as [Protocol version 1](https://github.com/Infineon/mtb-example-imagimob-streaming-protocol/tree/master) is deprecated. Note that support for Protocol version 1 will not be provided going forward.

By leveraging the Streaming Protocol, you can streamline your data collection process, making it more efficient and tailored to your specific needs.

- - If you are collecting data using a board flashed with **New Streaming Firmware/ Protocol version 2**, make sure you select **Use Node Explorer with Protocol Version 2** option in **Tools> Options> General**.
- - If you are collecting data using a board flashed with **Old Streaming Firmware/ Protocol version 1**, make sure you select **Serial Capture Nodes with Protocol Version 1** option in **Tools> Options> General**.
