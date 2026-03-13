---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-ai-kit/data-collection-microphone"
fetched_at: "2026-03-10T15:51:30Z"
title: "Data Collection Microphone"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-collection"]
---

# Data Collection Microphone

### Collecting and labeling data using Microphone sensor

You can collect acoustic data from the microphone sensor on the PSOC™ 6 AI Evaluation Kit to develop audio-based models such as baby-cry detection, cough detection, alarm detection, siren detection, and snoring detection. Using the Graph UX functionality, you can collect and label real-time acoustic data simultaneously.

After connecting the kit to the PC and creating a Graph UX project, let’s set up the Microphone Sensor unit for data collection and Predefined unit for data labeling on the canvas. Refer to [Connecting PSOC™ 6 AI Evaluation Kit to PC/laptop](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-new-streaming-firmware#step-1-connecting-psoc-6-ai-evaluation-kit-to-pclaptop) and [Creating a Graph UX Project](https://developer.imagimob.com/data-preparation/data-collection/data-collection-using-new-streaming-firmware#step-2-creating-a-graph-ux-project) to know the detailed steps.

#### Setting up the Microphone Sensor

[iframe](https://player.vimeo.com/video/1056556267?title=0&byline=0&portrait=0&badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Expand **EmptyProject** directory and double-click the **Main.imunit** to open the canvas.
2. - Navigate to the **Node Explorer** window, expand **Boards> PSoC 6 AI (CY8CKIT-062S2-AI)** and drag and drop the **Microphone** sensor onto the canvas.
3. - Navigate to the **Node Explorer** window, expand **Library> Tracks** and drag and drop the **Data Track** onto the canvas.
4. - Click on the red icon in the **Microphone** sensor node and drag over to the red icon in the **Data Track** node. This creates a connection between the two nodes.
5. - Click on the **Microphone** sensor node to edit the settings in the Properties window.

  ![](https://developer.imagimob.com/Images/ai-kit/img-1.png)

  **Setting the Properties of Microphone Sensor Node**

  | Sensor Node | Properties |
  | --- | --- |
  | **Node** | **Enabled:** Turn the radio button ON or OFF to enable or disable the node respectively.   **Node Name:** Enter the name you want to assign to the node. |
  | **Inputs** | **Gain:** Gain refers to the amplification level of the audio signal transmitted from the AI Kit to the Studio. Modify the gain value allows you to increase or decrease the amplitude of the audio data being streamed. The gain parameter ranges from 0 to 10. A higher gain value amplifies the signal, resulting in a louder output, while a lower gain value reduces the amplitude of the signal.   **Stereo:** Enable or disable the radio button to select or deselect the Stereo option respectively. By default, streaming audio data is set to Mono. Stereo uses two channels, typically left and right while mono uses a single channel to send the sensor data.   **Frequency:** Select the sampling frequency at which you want to collect data in Studio - 8 KHz or 16 KHz. |
  | **Stream Inputs** | **Covert:** Turn the radio button Yes or No to enable or disable the conversion of the output stream into float 32 respectively. |
  | **Stream Outputs** | **Audio:** Displays the name of the output stream from the sensor node. |
  | **Device** | **Device Name:** Displays the name of the sensor.   **Device Description:** Displays the description of the sensor. |

After setting up the **Microphone** sensor node, you can utilize the same graph to label the real-time data, by adding a Predefined Labels unit onto the canvas. Define the classes in the Predefined Labels node for one time and utilize the defined classes to label the data on a click of button.

#### Setting up the Predefined Labels

1. - Navigate to the **Node Explorer** window, expand **Library> Annotation** and drag and drop the **Predefined Labels** unit onto the canvas. The **Predefined Labels** unit displays the default classes.
2. - Define the classes in **Predefined Labels** node by entering every class in a new line.

  ![](https://developer.imagimob.com/Images/ai-kit/img-2.png)

  After defining the classes, start collecting and labeling data simultaneously.

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
