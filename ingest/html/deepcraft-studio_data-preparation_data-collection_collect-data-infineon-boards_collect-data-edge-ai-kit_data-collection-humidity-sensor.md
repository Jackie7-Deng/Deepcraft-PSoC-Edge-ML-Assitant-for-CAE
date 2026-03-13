---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit/data-collection-humidity-sensor"
fetched_at: "2026-03-10T15:51:26Z"
title: "Data Collection Humidity Sensor"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Data Collection Humidity Sensor

### Collecting and labeling data using Humidity and Temperature sensor

You can collect data using a humidity and temperature sensor present on PSOC™ Edge E84 AI Kit and develop a model according to your business needs. Using the Graph UX functionality, you can collect and label real-time data simultaneously.

After connecting the kit to the PC and creating a Graph UX project, let’s set up the Microphone Sensor unit for data collection and Predefined unit for data labeling on the canvas. Refer to [Creating a Graph UX Project](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit#step-1-create-graph-ux-project) and [Connect PSOC Edge E84 Evaluation Kit to PC/laptop](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-edge-ai-kit#step-2-connect-psoc-edge-e84-ai-kit-to-pclaptop) to know the detailed steps.

#### Data Collection Options

You can collect data from the Humidity-Temperature data in the following ways:

- - Data from humidity and temperature sensors in a single data track
- - Data from humidity sensor only
- - Data from temperature only
- - Data data from both humidity and temperature sensors in two different data tracks

Select the desired mode for data collection in the sensor node and follow the detailed instructions in *“Setting up the Humidity-Temperature Sensor”* section.

#### Setting up the Humidity-Temperature Sensor

1. - Expand **EmptyProject** directory and double-click the **Main.imunit** to open the canvas.
2. - Navigate to the **Node Explorer** window, expand **Boards> PSOC Edge E84 AI Kit** and drag and drop the **SHT4X** sensor onto the canvas.
3. - Navigate to the **Node Explorer** window, expand **Library> Tracks** and drag and drop the **Data Track** onto the canvas.
4. - Click on the red icon in the **SHT4X** sensor node and drag over to the red icon in the **Data Track** node. This creates a connection between the two nodes.
5. - Click on the **SHT4X** sensor node to edit the settings in the Properties window.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-39.png)

  **Setting the Properties of Humidity-Temperature Sensor Node**

  | Sensor node | Properties |
  | --- | --- |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Precision :** Select the precision at which you want to collect data in Studio - Low, Medium, High    **Mode:** Select the mode of data collection from the following: 1. **combined**: collect both humidity and temperature in one data track 2. **Humidity only**: collect data from humidity sensor only 3. **Temperature only**: collect data from temperature sensor only  4. **Split**: collect data from both humidity and temperature sensors in different data tracks |
  | **Stream Outputs** | Displays the name of the output stream from the sensor node. |
  | **Device** | **Device Name:** Displays the name of the sensor.   **Device Description:** Displays the description of the sensor. |

After setting up the **SHT4X** sensor node, you can utilize the same graph to label the real-time data, by adding a Predefined Labels unit onto the canvas. Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

#### Setting up the Predefined Labels

1. - Navigate to the **Node Explorer** window, expand **Library> Annotation** and drag and drop the **Predefined Labels** unit onto the canvas. The **Predefined Labels** unit displays the default classes.
2. - Define the classes in **Predefined Labels** node by entering every class in a new line.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-38.png)

  After defining the classes, start collecting and labeling data simultaneously.

#### Real-time data collection and data labeling

[iframe](https://player.vimeo.com/video/1127137337?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Navigate to the toolbar and click the **Start** button to open the session file (live.imsession). An empty session file opens displaying the pre-defined classes in the Labels bar.
2. - Click the **Record** button to start capturing the real-time data.
3. - In the **Labels bar**, select a class to start adding labels to the streaming data.
4. - Deselect the same class to stop adding the labels. Similarly, you can enable or disable the other classes and label the data.
5. - Click the **Record** button to stop collecting the data.
6. - Select **File > Save** to save the session file, data track and label track. The Save New Session window appears.
7. - In **Location**, click the three dot and select the desired location to save the files.
8. - In **Session Name**, enter the name of the session file.
9. - Under **Track Options**, set the following:

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-40.png)

  * In **Track Name**, double-click the column to edit the track name, if required
  * In **File Name**, double-click the columns to edit the track name, if required
10. - Select the save checkbox corresponding to the tracks you want to save.
11. - Click **OK** to save the files.
12. - Repeat the instructions from step 2 to collect and save data in multiple session files.

  After collecting the data, add data to the required project and start with the machine learning workflow in Studio. Refer to [Create project](https://developer.imagimob.com/getting-started/workspace-project/create-a-project) and [Add data to project](https://developer.imagimob.com/data-importing/import-data-studio) to know more.

If you prefer not to collect and label data simultaneously, you can first collect the data. Once the data collection is complete, simply press the play button in the session and begin labeling by selecting the appropriate labels in the Labels bar.
