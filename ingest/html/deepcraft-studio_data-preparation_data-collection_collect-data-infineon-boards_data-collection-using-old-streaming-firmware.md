---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-using-old-streaming-firmware"
fetched_at: "2026-03-10T15:51:42Z"
title: "Data Collection Using Old Streaming Firmware"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Data Collection Using Old Streaming Firmware

### Real-Time Data Collection with PSOC™ 6 AI Evaluation Kit using old streaming firmware

If you have not yet flashed the PSOC™ 6 AI Evaluation Kit with the new streaming firmware, follow the instructions in this topic to stream data into DEEPCRAFT™ Studio. However, we recommend using the new streaming firmware for improved functionality. For detailed instructions on how to flash the firmware, please refer to this [section](https://developer.imagimob.com/getting-started/infineon-ai-evaluation-kit#streaming-firmware-for-psoc-6-ai-evaluation-kit).

If you are collecting data using the PSOC™ 6 AI Evaluation Kit or any other board flashed with old streaming firmware/ Protocol version 1, make sure you select **Serial Capture Nodes with Protocol Version 1** option in **Tools> Options> General**, before collecting data.

You can stream real-time data using the PSOC™ 6 AI Evaluation Kit into DEEPCRAFT™ Studio. You can add additional data to your existing projects or build your own dataset from scratch. You can collect labeled as well as unlabeled data as per your project requirement.

#### How to collect and label real-time data?

Collecting and labeling data is straightforward using [Graph UX](https://developer.imagimob.com/getting-started/graph-ux) in DEEPCRAFT™ Studio. Follow these steps to efficiently collect and label your data:

1. - [Connecting PSOC™ 6 AI Evaluation Kit to the laptop](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-old-streaming-firmware#step-1-connecting-psoc-6-ai-evaluation-kit-with-laptop)
2. - [Creating a Graph UX Project](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-old-streaming-firmware#step-2-creating-project-in-deepcraft-studio)
3. - [Creating Data Collection and Data Labeling Graph](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-old-streaming-firmware#step-3-creating-data-collection-and-data-labeling-graph)
4. - [Real-time data collection and data labeling](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-old-streaming-firmware#step-4-real-time-data-collection-and-data-labeling)

#### Step 1: Connecting PSOC™ 6 AI Evaluation Kit with laptop

Connect the PSOC™ 6 AI Evaluation Kit to the laptop or PC through PSOC™ 6 USB connector (J2) using a Type-C USB cable.

#### Step 2: Creating project in DEEPCRAFT™ Studio

You can create an **Empty Graph UX Project** or **Live Data Collection Starter Graph UX Project** containing an example graph. Refer to [How to get started with Graph UX?](https://developer.imagimob.com/getting-started/graph-ux#how-do-i-get-started-with-graph-ux) for instructions on creating the Graph UX project.

![](https://developer.imagimob.com/Images/ai-kit/img-28.png)

The Live Data Collection Starter Graph UX project contains an example graph for collecting and labeling data using a Local Microphone. So, if you use the Live data Collection starter graph ux project to collect data using other sensons, just replace the Local Microphone node with the desired sensor node. But, if you select the Empty Graph UX project to collect and label data, you need to create the data collection and labeling graph. Follow the steps below to create the data collection graph.

#### Step 3: Creating Data Collection and Data Labeling Graph

DEEPCRAFT™ Studio provides the functionality to collect and label the real-time data simultaneously. Let’s set up the **Serial Capture** unit for collecting data and **Predefined** unit for labeling data on the canvas.

##### Setting up the Serial Capture

1. - Connect the board to the laptop or PC through PSOC™ 6 USB connector (J2) using a Type-C USB cable.
2. - Expand **EmptyProject** directory and double-click the **Main.imunit** to open the canvas.
3. - Navigate to the **Node Explorer** window, expand **Library> Capture Devices** and drag and drop the **Serial Capture** unit onto the canvas.
4. - Navigate to the **Node Explorer** window, expand **Library> Tracks** and drag and drop the **Data Track** onto the canvas.
5. - Goto **Serial Capture > Properties** and select **USB Serial Device** port. To check the COM port at which the board is connected, open **Device Manager > Ports** and look for **USB Serial Device**.
6. - Click on the red icon in the **Serial Capture** node and drag over to the gray icon in the **Data Track** node. This creates a connection between the two nodes.

  ![](https://developer.imagimob.com/Images/ai-kit/img-33.png)

- - The microphone collects data at a sampling rate of 16000 and an accelerometer collects data at a sampling rate of 50.
- - The connection might not establish if the COM port is already in use in DEEPCRAFT™ Studio or another tool.

After setting up the Serial Capture, you can utilize the same graph to label the real-time data, by adding a Predefined Labels unit onto the canvas. Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

##### Setting up the Predefined Labels

1. - Navigate to the **Node Explorer** window, expand **Library> Annotation** and drag and drop the **Predefined Labels** unit onto the canvas. The **Predefined Labels** unit displays the default classes.
2. - Define the classes in **Predefined Labels** node by entering every class in a new line.

  ![](https://developer.imagimob.com/Images/ai-kit/img-34.png)

  After defining the classes, start collecting and labeling data simultaneously.

#### Step 4: Real-time data collection and data labeling

1. - Navigate to the toolbar and click the **Start** button to open the session file (main.imsession). An empty session file opens displaying the pre-defined classes in the Labels bar.
2. - Click the **Record** button to start capturing the real-time data.

  ![](https://developer.imagimob.com/Images/ai-kit/img-35.png)
3. - In the **Labels bar**, select a class to start adding labels to the streaming data.
4. - Deselect the same class to stop adding the labels. Similarly, you can enable or disable the other classes and label the data.
5. - Click the **Record** button to stop collecting the data.
6. - Select **File > Save** to save the session file, data track and label track. The Save New Session window appears.

  ![](https://developer.imagimob.com/Images/evaluation-kit/pic-10.png)
7. - In **Location**, click the three dot and select the desired location to save the files.
8. - In **Session Name**, enter the name of the session file.
9. - Under **Track Options**, set the following:

  * In **Wave Format Encoding**, select the encoding format for the audio tracks
  * In **Track Name**, double-click the column to edit the track name, if required
  * In **File Name**, double-click the columns to edit the track name, if required
10. - Select the save checkbox corresponding to the tracks you want to save.
11. - Click **OK** to save the files.
12. - Repeat the instructions from step 2 to collect and save data in multiple session files.

After collecting the data, add data to the required project and start with the machine learning workflow in Studio. Refer to [Create project](https://developer.imagimob.com/getting-started/workspace-project/create-a-project) and [Add data to project](https://developer.imagimob.com/data-preparation/add-data-to-project) to know more.

#### Testing OOB application with serial terminal

1. - Connect the board to the PC through PSOC™ 6 USB connector (J2) using a Type-C USB cable. This enables a serial port for sensor data collection.
2. - Ensure that the power LED (D1) turns ON, indicating the board is powered.
3. - In the terminal application, open the serial connection to the device. It should present itself as USB serial device. Connect to this port with the following settings:

  * Baud rate: 115200
  * Data: 8 bit
  * Parity: None
  * Stop bit: 1 bit
  * Flow control: None
  ![](https://developer.imagimob.com/Images/evaluation-kit/pic-2.png)
4. - Set the terminal settings as follows:

  * Newlines should be transmitted as CR+LF
  * Enable local echo
  ![](https://developer.imagimob.com/Images/evaluation-kit/pic-3.png)
5. - Type **config?** and press Enter key (to send CR+LF) and verify that the device responds with a JSON structure describing the protocol configuration.

  ![](https://developer.imagimob.com/Images/evaluation-kit/pic-4.png)
6. - Type **subscribe,1,16000** and verify that the device streams audio data. Notice that sample collection stops after 5 seconds. The garbled text on the terminal is the audio data.
7. - Type **subscribe,2,50** and verify that the device streams IMU data. Notice that sample collection stops after 5 seconds. The garbled text on the terminal is the IMU data.

Currently backspace is not supported in terminal commands. If you encounter issues such as being unable to see commands on the terminal or receiving unknown command errors, follow the steps below:

- - Reset the terminal and clear the buffer.
- - Reset board to ensure a fresh execution.
