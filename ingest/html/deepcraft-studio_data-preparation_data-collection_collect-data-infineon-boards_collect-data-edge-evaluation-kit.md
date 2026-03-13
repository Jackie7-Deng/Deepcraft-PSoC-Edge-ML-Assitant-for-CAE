---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit"
fetched_at: "2026-03-10T15:51:28Z"
title: "Real-Time Data Streaming with PSOC™ Edge E84"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Real-Time Data Streaming with PSOC™ Edge E84

### Real-Time Data Streaming with PSOC™ Edge E84 Evaluation Kit

This topic provides information on how to stream real-data from various sensors present in the PSOC™ Edge E84 Evaluation Kit into DEEPCRAFT™ Studio. You can add additional data to your existing projects or build your own dataset from scratch. You can collect both labeled and unlabeled data, depending on your project requirements.

|  |
| --- |

Before you start collecting data using the PSOC™ Edge E84 Evaluation Kit, make sure to flash the kit with the Streaming Firmware. For step-by-step instructions, refer to [Streaming Firmware for PSOC™ Edge E84 Evaluation Kit](https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/psoc-edge-e84-eval-kit#streaming-firmware-for-psoc-edge-e84-evaluation-kit).

#### What type of data can be collected using the PSOC™ Edge E84 Evaluation Kit?

After you have flashed the streaming firmware, you can collect various types of data from multiple sensors, including:

- - **Audio Data**: Pulse Density Modulation (PDM) and Pulse Code Modulation (PCM) audio data can be collected from the microphone at sample rates of 8 kHz, 16 kHz, 22.05 kHz, 44.1 kHz, 48 kHz.
- - **Inertial Measurement Unit (IMU) Data**: Data from the 6-axis IMU (accelerometer and gyroscope) can be sampled at frequencies of 50 Hz, 100 Hz, 200 Hz or 400 Hz. This allows for acceleration and gyroscopic angular rate sensing in each spatial direction. The IMU sensor can be configured to collect data from only the accelerometer, only the gyroscope, or both.
- - **Magnetometer Data**: The 3-axis magnetometer provides data at a sample rate of 50 Hz, 100 Hz, 200 Hz or 400 Hz, enabling geomagnetic field direction and strength sensing.

#### How to collect and label real-time data from the sensors?

Collecting and labeling data in real-time is straightforward using Graph UX in DEEPCRAFT™ Studio. Follow these steps to efficiently collect and label your data:

#### Step 1: Create Graph UX Project

To create a Graph UX project for data collection, follow the steps:

![](https://developer.imagimob.com/Images/getting-started/boards/pic-3.png)

1. - In DEEPCRAFT™ Studio, navigate to **File> New Project**. The New Project window appears.
2. - Expand **Templates> Graph UX> Generic** and to select **Empty project**.
3. - In **New Project Name**, modify the name of the project, if required.
4. - In **Location**, specify the location where you want to save the project directory.
5. - Click **Ok** to create the project.

#### Step 2: Connect PSOC™ Edge E84 Evaluation Kit to PC/laptop

Connect the PSOC™ Edge E84 Evaluation Kit to the laptop or PC through USB connector (J30) using a Type-C USB cable. After connecting the kit, navigate to **Node Explorer Window> Boards** to check if the board is connected properly. The PSOC™ Edge E84 Evaluation Kit, along with all the sensors is displayed under Boards.

- - If the **Node Explorer Window** is not open, navigate to **View> Node Explorer** to access the window.
- - If the PSOC™ Edge E84 Evaluation Kit and sensors are not displayed under Board in Node Explorer, navigate to **Tools> Options> Graph UX> Capture Nodes** and select **Use Node Explorer with Protocol Version 2**.

#### Step 3: Create Data Collection and Data Labeling Graph

To create a simple data-collection and labeling graph, add a sensor to stream data, a data track to visualize and label the stream, and a predefine labels node to define the labels.

##### 1. Select the Sensor node to stream data

The PSOC™ Edge E84 Evaluation Kit consists of various sensors, such as microphone, IMU (accelerometer or gyroscope) and magnetometer. Depending on the type of data you want to collect, select the desired sensor and drag and drop onto the canvas. You can also collect data using multiple sensors simultaneously.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-5.png)

- - **Microphone node**: for streaming audio data
- - **IMU node**: for streaming accelerometer and gyroscope data
- - **Magnetometer node**: for streaming magnetometer data

If you want to stream video data alongside sensor data, you can use the **Library> Capture Devices> Local Camera** node to stream video using the built-in PC camera. This is particularly useful for labeling data, especially when collecting data from the IMU or other sensors. To know how to set up the Local Camera node, refer to [Setting up the Local Camera](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-multiple-sensors#setting-up-the-local-camera).

##### 2: Setup the Visualization Tracks

The Visualization Nodes help in visualizing the data collected from the sensor nodes as tracks in the session file.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-9.png)

- - **Data Track**: for visualizing and labeling the sensor data collected from Microphone, IMU and Magnetometer.
- - **Video Track**: for visualizing video data collected from the Local Camera node. (Applicable only if you set the Local Camera node to collect video data.)

##### 3: Setup the Predefined Labels

Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

![](https://developer.imagimob.com/Images/getting-started/boards/pic-10.png)

Depending on the type of data you want to collect and how you plan to collect it, you can create different data collection graphs.

#### Step 4: Real-time data collection and data labeling

[iframe](https://player.vimeo.com/video/1127091016?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

Refer to the topics below for detailed instructions on setting up the sensors and collecting and labeling real-time data:

- - To collect data using the **Microphone**, connect the Microphone node to the data track. For setting up the microphone node and collecting data using microphone, refer to [Collecting and labeling data using Microphone sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-microphone).
- - To collect data using the **IMU sensor**, connect the IMU node to the data track. For setting up IMU node and collecting data using IMU sensor, refer to [Collecting and labeling data using IMU sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-imu).
- - To collect data using the **Magnetometer sensor**, connect the Magnetometer node to the data track. For setting up Magnetometer node and collecting data using Magnetometer sensor, refer to [Collecting and labeling data using Magnetometer sensor](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-magnetometer).

You can collect data concurrently from microphone, IMU and magnetometer. Refer to [Collecting and Labeling data using multiple sensors](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-multiple-sensors) to know more.

However, if you want to collect video data along with sensor data, connect the **Local Camera** to the Video Track in the existing graph. For collecting data using the Local Camera, refer to [Setting up the Local Camera](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-evaluation-kit/data-collection-multiple-sensors#setting-up-the-local-camera).
