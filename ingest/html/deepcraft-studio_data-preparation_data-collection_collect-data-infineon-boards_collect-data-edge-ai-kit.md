---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit"
fetched_at: "2026-03-10T15:51:24Z"
title: "Real-Time Data Streaming with PSOC™ Edge E84"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Real-Time Data Streaming with PSOC™ Edge E84

### Real-Time Data Streaming with PSOC™ Edge E84 Artificial Intelligence Kit

This topic provides information on how to stream real-data from various sensors present in the PSOC™ Edge E84 AI Kit into DEEPCRAFT™ Studio. You can add additional data to your existing projects or build your own dataset from scratch. You can collect both labeled and unlabeled data, depending on your project requirements.

|  |
| --- |

Before you start collecting data using the PSOC™ Edge E84 AI Kit, make sure to flash the kit with the Streaming Firmware. For step-by-step instructions, refer to [Streaming Firmware for PSOC™ Edge E84 AI Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-ai-kit#streaming-firmware-for-psoc-edge-e84-ai-kit).

#### What type of data can be collected using the PSOC™ Edge E84 AI Kit?

After you have flashed the streaming firmware, you can collect various types of data from multiple sensors, including:

- - **Audio Data**: Pulse Density Modulation (PDM) and Pulse Code Modulation (PCM) audio data can be collected from the microphone at sample rates of 8 kHz, 16 kHz, 22.05 kHz, 44.1 kHz, 48 kHz.
- - **Inertial Measurement Unit (IMU) Data**: Data from the 6-axis IMU (accelerometer and gyroscope) can be sampled at frequencies of 50 Hz, 100 Hz, 200 Hz or 400 Hz. This allows for acceleration and gyroscopic angular rate sensing in each spatial direction. The IMU sensor can be configured to collect data from only the accelerometer, only the gyroscope, or both.
- - **Magnetometer Data**: The 3-axis magnetometer provides data at a sample rate of 50 Hz, 100 Hz, 200 Hz or 400 Hz, enabling geomagnetic field direction and strength sensing.
- - **Pressure and Temperature Data**: Data from the pressure sensor can be sampled at a frequency of 8 Hz, 16 Hz, 32 Hz, 64 Hz or 128 Hz capturing changes in atmospheric pressure and temperature .
- - **Humidity and Temperature Data**: Data from the humidity and temperature sensor can be collected at low, medium or high precision capturing changes in humidity and temperature.
- - **Radar Data**: Radar data can be utilized for various applications, including macro presence detection, micro presence detection, gesture recognition and other use cases.

#### How to collect and label real-time data from the sensors?

Collecting and labeling data in real-time is straightforward using Graph UX in DEEPCRAFT™ Studio. Follow these steps to efficiently collect and label your data:

#### Step 1: Create Graph UX Project

![](https://developer.imagimob.com/Images/getting-started/boards/pic-3.png)

To create a Graph UX project for data collecting, follow the steps:

1. - In DEEPCRAFT™ Studio, navigate to **File> New Project**. The New Project window appears.
2. - Expand **Templates> Graph UX> Generic** and to select **Empty project**.
3. - In **New Project Name**, modify the name of the project, if required.
4. - In **Location**, specify the location where you want to save the project directory.
5. - Click **Ok** to create the project.

#### Step 2: Connect PSOC™ Edge E84 AI Kit to PC/laptop

Connect the PSOC™ Edge E84 AI Kit to the laptop or PC through USB connector (J2) using a Type-C USB cable. After connecting the kit, navigate to **Node Explorer Window> Boards** to check if the board is connected properly. The PSOC™ Edge E84 AI Kit, along with all the sensors is displayed under Boards.

- - If the **Node Explorer Window** is not open, navigate to **View> Node Explorer** to access the window.
- - If the PSOC™ Edge E84 AI Kit and sensors are not displayed under Board in Node Explorer, navigate to **Tools> Options> Graph UX> Capture Nodes** and select **Use Node Explorer with Protocol Version 2**.

#### Step 3: Create Data Collection and Data Labeling Graph

To create a simple data-collection and labeling graph, add a sensor to stream data, a data track to visualize and label the stream, and a predefine labels node to define the labels.

##### 1. Select the Sensor node to stream data

The PSOC™ Edge E84 AI Kit consists of various sensors, such as microphone, IMU (accelerometer or gyroscope), magnetometer, pressure- temperature sensor, humidity-temperature sensor and radar. Depending on the type of data you want to collect, select the desired sensor and drag and drop onto the canvas. You can also collect data using multiple sensors simultaneously.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-13.png)

- - **Microphone node**: for streaming audio data
- - **IMU node**: for streaming accelerometer and gyroscope data
- - **Magnetometer node**: for streaming magnetometer data
- - **DPS Node**: for streaming pressure and temperature data
- - **SHT4x Node**: for streaming humidity and temperature data
- - **Radar node**: for streaming radar data

If you want to stream video data alongside sensor data, you can use the **Library> Capture Devices> Local Camera** node to stream video using the built-in PC camera. This is particularly useful for labeling data, especially when collecting data from the IMU or other sensors. To know how to set up the Local Camera node, refer to [Setting up the Local Camera](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-multiple-sensors#setting-up-the-local-camera).

##### 2: Setup the Visualization Tracks

The Visualization Nodes help in visualizing the data collected from the sensor nodes as tracks in the session file.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-14.png)

- - **Data Track**: for visualizing and labeling the sensor data collected from Microphone, IMU, DPS, Magnetometer and Radar node.
- - **Video Track**: for visualizing video data collected from the Local Camera node. (Applicable only if you set the Local Camera node to collect video data.)

##### 3: Setup the Predefined Labels

Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-12.png)

Depending on the type of data you want to collect and how you plan to collect it, you can create different data collection graphs.

#### Step 4: Real-time data collection and data labeling

[iframe](https://player.vimeo.com/video/1127152963?badge=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

Refer to the topics below for detailed instructions on setting up the sensors and collecting and labeling real-time data:

- - To collect data using the **Microphone**, connect the Microphone node to the data track. For setting up the microphone node and collecting data using microphone, refer to [Collecting and labeling data using Microphone sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-microphone).
- - To collect data using the **IMU sensor**, connect the IMU node to the data track. For setting up IMU node and collecting data using IMU sensor, refer to [Collecting and labeling data using IMU sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-imu).
- - To collect data using the **Magnetometer sensor**, connect the Magnetometer node to the data track. For setting up Magnetometer node and collecting data using Magnetometer sensor, refer to [Collecting and labeling data using Magnetometer sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-magnetometer).
- - To collect data using the **Pressure and temperature sensor**, connect the DPS node to the data track. For setting up DPS node and collecting data using pressure and temperature sensor, refer to [Collecting and labeling data using Pressure and Temperature sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-pressure-sensor).
- - To collect data using the **Humidity and temperature sensor**, connect the SHT4X node to the data track. For setting up SHT4X node and collecting data using humidity and temperature sensor, refer to [Collecting and labeling data using Humidity and Temperature sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-humidity-sensor).
- - To collect data using the **Radar sensor**, connect the Radar node to the data track. For setting up Radar node and collecting data using Radar sensor, refer to [Collecting and labeling data using Radar sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-radar).

You can collect data from microphone, IMU, magnetometer, pressure-temperature sensor and humidity-temperature sensor concurrently. However, you must collect data from Radar sensor independently, without concurrent data collection from any other sensors. When you enable all sensors simultaneously, it is recommended to initialize the sensors at the default or minimum frequency. To know how to collect data using multiple sensors, refer to [Collecting and Labeling data using multiple sensors](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-multiple-sensors).

However, if you want to collect video data along with sensor data, connect the **Local Camera** to the Video Track in the existing graph. For collecting data using the Local Camera, refer to [Setting up the Local Camera](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-multiple-sensors#setting-up-the-local-camera).
