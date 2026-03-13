---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-ai-kit/data-collection-imu"
fetched_at: "2026-03-10T15:51:31Z"
title: "Data Collection Imu"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Data Collection Imu

### Collecting and labeling data using IMU Sensor

You can collect data from accelerometer and gyroscope on the PSOC™ 6 AI Evaluation Kit to develop models for wearable devices. These models can be used for activity recognition, such as tracking human activities (walking, running, standing, sitting), fall detection, and other similar use cases. Using the Graph UX functionality, you can collect and label real-time data simultaneously.

After connecting the kit to the PC and creating a Graph UX project, let’s set up the IMU Sensor unit for data collection and Predefined unit for data labeling on the canvas. Refer to [Connecting PSOC™ 6 AI Evaluation Kit to PC/laptop](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-new-streaming-firmware#step-1-connecting-psoc-6-ai-evaluation-kit-to-pclaptop) and [Creating a Graph UX Project](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-new-streaming-firmware#step-2-creating-a-graph-ux-project) to know the detailed steps.

#### IMU Data Collection Options

You can collect data from the IMU in the following ways:

- - Data from accelerometer and gyroscope in a single data track
- - Data from accelerometer only
- - Data from gyroscope only
- - Data data from both accelerometer and gyroscope in two different data tracks

Select the desired mode for data collection in the IMU sensor node and follow the detailed instructions in *“Setting up the IMU Sensor”* section.

#### Setting up the IMU Sensor

[iframe](https://player.vimeo.com/video/1056584701?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Expand **EmptyProject** directory and double-click the **Main.imunit** to open the canvas.
2. - Navigate to the **Node Explorer** window, expand **Boards> PSoC 6 AI (CY8CKIT-062S2-AI)** and drag and drop the **IMU** sensor onto the canvas.
3. - Navigate to the **Node Explorer** window, expand **Library> Tracks** and drag and drop the **Data Track** Visualization unit onto the canvas.
4. - Click on the red icon in the **IMU** sensor node and drag over to the red icon in the **Data Track** node. This creates a connection between the two nodes.
5. - Click on the **IMU** sensor node to edit the settings in the Properties window.

  ![](https://developer.imagimob.com/Images/ai-kit/img-17.png)

  **Setting the Properties of IMU Sensor Node**

  | Sensor node | Properties |
  | --- | --- |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Frequency :** Select the sampling frequency at which you want to collect data in Studio - 50 Hz, 100 Hz, 200 Hz, 400 Hz.   **Accel Range:** Select the min/max gravity range from the list - 2G, 4G, 8G, 16G.   **Gyro Range:** Select the Angular rate measurement range from the list - 125 dps, 250 dps, 500 dps, 1000 dps, 2000 dps.   **Mode:** Select the mode of data collection from the following: 1. **combined**: collect both accelerometer and gyroscope in one data track 2. **Accel only**: collect data from accelerometer only 3. **Gyro only**: collect data from gyroscope only 4. **Split**: collect data from both accel and gyro in different data tracks |
  | **Stream Outputs** | **IMU:** Displays the name of the output stream from the sensor node. |
  | **Device** | **Device Name:** Displays the name of the sensor.   **Device Description:** Displays the description of the sensor. |

After setting up the **IMU** sensor node, you can utilize the same graph to label the real-time data, by adding a Predefined Labels unit onto the canvas. Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

##### Setting up the Predefined Labels

1. - Navigate to the **Node Explorer** window, expand **Library> Annotation** and drag and drop the **Predefined Labels** unit onto the canvas. The **Predefined Labels** unit displays the default classes.
2. - Define the classes in **Predefined Labels** node by entering every class in a new line.

  ![](https://developer.imagimob.com/Images/ai-kit/img-18.png)

  After defining the classes, start collecting and labeling data simultaneously.

#### Real-time data collection and data labeling

[iframe](https://player.vimeo.com/video/1056587401?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Navigate to the toolbar and click the **Start** button to open the session file (live.imsession). An empty session file opens displaying the pre-defined classes in the Labels bar.
2. - Click the **Record** button to start capturing the real-time data.
3. - In the **Labels bar**, select a class to start adding labels to the streaming data.
4. - Deselect the same class to stop adding the labels. Similarly, you can enable or disable the other classes and label the data.
5. - Click the **Record** button to stop collecting the data.
6. - Select **File > Save** to save the session file, data track and label track. The Save New Session window appears.
7. - In **Location**, click the three dot and select the desired location to save the files.
8. - In **Session Name**, enter the name of the session file.
9. - Under **Track Options**, set the following:

  ![](https://developer.imagimob.com/Images/ai-kit/img-19.png)
  * In **Track Name**, double-click the column to edit the track name, if required
  * In **File Name**, double-click the columns to edit the track name, if required
10. - Select the save checkbox corresponding to the tracks you want to save.
11. - Click **OK** to save the files.
12. - Repeat the instructions from step 2 to collect and save data in multiple session files.

  After collecting the data, add data to the required project and start with the machine learning workflow in Studio. Refer to [Create project](https://developer.imagimob.com/getting-started/workspace-project/create-a-project) and [Add data to project](https://developer.imagimob.com/data-importing/import-data-studio) to know more.

If you prefer not to collect and label data simultaneously, you can first collect the data. Once the data collection is complete, simply press the play button in the session and begin labeling by selecting the appropriate labels in the Labels bar.
