---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-without-kit/collect-data-microphone"
fetched_at: "2026-03-10T15:51:35Z"
title: "Collect Data Microphone"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Collect Data Microphone

### Real-Time Audio data collection and labeling using PC/laptop Microphone

You can collect acoustic data from the microphone sensor present on your PC or laptop to develop various audio-based models. Using the Graph UX functionality, you can collect and label real-time acoustic data simultaneously.

#### How to collect and label real-time data from the microphone?

Collecting and labeling data in real-time is straightforward using Graph UX in DEEPCRAFT™ Studio. Follow these steps to efficiently collect and label your data using your PC/laptop Microphone:

#### Step 1: Create Graph UX Project

![](https://developer.imagimob.com/Images/getting-started/boards/pic-3.png)

To create a Graph UX project, follow the steps:

1. - In DEEPCRAFT™ Studio, navigate to **File> New Project**. The New Project window appears.
2. - Expand **Templates> Graph UX> Generic** and to select **Empty project**.
3. - In **New Project Name**, modify the name of the project, if required.
4. - In **Location**, specify the location where you want to save the project directory.
5. - Click **Ok** to create the project.
6. - Expand **EmptyProject** directory and double-click the **Main.imunit** to open the canvas.

#### Step 2: Create Data Collection and Data Labeling Graph

To create a simple data-collection and labeling graph, add a sensor to stream real-time data, a data track to visualize and label the data stream, and Predefine labels node to define the labels. Optionally, you can also add a Local Camera node and a video track to record a video alongside sensor data collection, providing a visual reference for labeling the sensor data. After connecting the board to the PC and creating a Graph UX project, let’s set up the Sensor unit for data collection and Predefined unit for data labeling on the canvas.

#### Setting up the Microphone

1. - Navigate to the **Node Explorer** window, expand **Library> Capture Devices** and drag and drop the **Local Microphone** sensor onto the canvas.
2. - Navigate to the **Node Explorer** window, expand **Library> Tracks** and drag and drop the **Data Track** onto the canvas.
3. - Click on the red icon in the **Local Microphone** node and drag over to the red icon in the **Data Track** node. This creates a connection between the two nodes.
4. - Click on the **Local Microphone** sensor node to edit the settings in the Properties window, if required.

  ![](https://developer.imagimob.com/Images/ai-kit/img-1.png)

  **Setting the Properties of Microphone Sensor Node**

  | Local Camera Node | Properties |
  | --- | --- |
  | **Unit** | **Unit Name:** Displays the name for the unit. This parameter is not editable.   **Unit Description:** Displays the description of the unit. |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Device :** Select the device to be used for recording the audio.   **Sample rate :** Select the sampling frequency at which you want to collect data in Studio - 8 kHz, 16 kHz, 44.1 kHz, 48 kHz..   **Channel:** Select Stereo or Mono as the channel. By default, streaming audio data is set to Mono. Stereo uses two channels, typically left and right while mono uses a single channel to send the sensor data. |
  | **Outputs** | **Output Samples :** Displays the output sample. |

After setting up the **Local Microphone** node, you can utilize the same graph to label the real-time data, by adding a Predefined Labels unit onto the canvas. Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

#### Setting up the Predefined Labels

1. - Navigate to the **Node Explorer** window, expand **Library> Annotation** and drag and drop the **Predefined Labels** unit onto the canvas. The **Predefined Labels** unit displays the default classes.
2. - Define the classes in **Predefined Labels** node by entering every class in a new line.

  ![](https://developer.imagimob.com/Images/evaluation-kit/pic-14.png)

  After defining the classes, you can start collecting and labeling data simultaneously. You can also set the Local Camera to collect the video data along with the sensor data. You can use the video to label the sensor data.

Setting up Local Camera for collecting video data is an optional step, you can skip and start with real-time data collection.

#### Setting up the Local Camera (Optional)

To set up the Local Camera, follow the steps:

![](https://developer.imagimob.com/Images/graph-ux-new/pic-6.png)

1. - Connect a camera or use the built-in camera of the laptop or PC.
2. - Navigate to **Node Explorer window** and expand **Library> Capture Devices** and drag and drop the **Local Camera** unit onto the canvas.
3. - Click on the **Local Camera** node to edit the settings in the Properties window, if required.

  ![](https://developer.imagimob.com/Images/graph-ux-new/pic-12.png)

  **The table represents the default properties of the local camera:**

  | Local Camera Node | Properties |
  | --- | --- |
  | **Unit** | **Unit Name:** Displays the name for the unit. This parameter is not editable.   **Unit Description:** Displays the description of the unit. |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Device :** Select the device to be used for recording the video.   **Resolution :** Select the resolution for recording the video from the list.   **Output Format :** Select the output shape from the list.   **Output Type :** Select the output type from the node: UInt8 or Float32. |
  | **Outputs** | **Output Samples :** Displays the output sample. |
4. - Navigate to **Node Explorer window** and expand **Library> Tracks** and drag and drop the Video Track unit onto the canvas.
5. - Click on the **Video Track** node to edit the settings in the Properties window, if required.

  ![](https://developer.imagimob.com/Images/graph-ux-new/pic-7.png)

  **The table represents the default properties of the Video track:**

  | Video Track Node | Properties |
  | --- | --- |
  | **Unit** | **Unit Name:** Displays the name for the unit. This parameter is not editable.   **Unit Description:** Displays the description of the unit. |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Input :** Displays the connection status of the video track node.   **Quality :** Select the quality (bits per pixel) at which you want to record the video.   **Persist :** Enable or disable the persist option. |
  | **Outputs** | **Output Samples :** Displays the output sample. |

Disabling the **Persist** option enables real-time video streaming without saving the footage. As a result, replaying or rewinding the video will not be possible. This configuration is optimal for real-time model evaluation when video storage is not required.

1. - Connect the Output of the Local Camera Node to the Input of the Video Track by clicking on the red icon in the Local Camera node and dragging over to the red icon in the Video Track. This creates a connection between the two nodes.

  ![](https://developer.imagimob.com/Images/getting-started/boards/pic-46.png)

#### Real-time data collection and data labeling

[iframe](https://player.vimeo.com/video/1056575547?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Navigate to the toolbar and click the **Start** button to open the session file (live.imsession). An empty session file opens displaying the pre-defined classes in the Labels bar.
2. - Click the **Record** button to start capturing the real-time data.
3. - In the **Labels bar**, select a class to start adding labels to the streaming data.
4. - Deselect the same class to stop adding the labels. Similarly, you can enable or disable the other classes and label the data.
5. - Click the **Record** button to stop collecting the data.
6. - Select **File > Save** to save the session file, data track and label track. The Save New Session window appears.
7. - In **Location**, click the three dot and select the desired location to save the files.
8. - In **Session Name**, enter the name of the session file.
9. - Under **Track Options**, set the following:

  ![](https://developer.imagimob.com/Images/ai-kit/img-13.png)

  * In **Wave Format Encoding**, select the encoding format for the audio tracks
  * In **Track Name**, double-click the column to edit the track names, if required
  * In **File Name**, double-click the columns to edit the track names, if required
10. - Select the save checkbox corresponding to the tracks you want to save.
11. - Click **OK** to save the files.
12. - Repeat the instructions from step 2 to collect and save data in multiple session files.

  After collecting the data, add data to the required project and start with the machine learning workflow in Studio. Refer to [Create project](https://developer.imagimob.com/getting-started/workspace-project/create-a-project) and [Add data to project](https://developer.imagimob.com/data-importing/import-data-studio) to know more.

If you prefer not to collect and label data simultaneously, you can first collect the data. Once the data collection is complete, simply press the play button in the session and begin labeling by selecting the appropriate labels in the Labels bar.
