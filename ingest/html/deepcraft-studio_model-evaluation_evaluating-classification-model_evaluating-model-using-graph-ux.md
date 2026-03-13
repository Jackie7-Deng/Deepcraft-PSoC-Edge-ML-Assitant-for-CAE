---
source_url: "https://developer.imagimob.com/deepcraft-studio/model-evaluation/evaluating-classification-model/evaluating-model-using-graph-ux"
fetched_at: "2026-03-10T15:51:48Z"
title: "Evaluating Model Using Graph UX"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "model-evaluation", "evaluating-classification-model"]
---

### Evaluating model using Graph UX

Model evaluation is a crucial step in building a machine learning model. It helps in analyzing the model performance by using multiple statistics and metrics. However, a model performing ideally in the evaluation phase may not perform as expected in real world. To address this, the model should be thoroughly evaluated before deploying. Graph UX supports real-time model evaluation functionality which helps in analyzing and monitoring the model predictions before deploying a model to production. It also ensures that the model generates accurate predictions on real-time data.

#### Creating an Evaluation Graph

To create an evaluation graph for evaluating a model, follow the steps:

#### Step 1: Bring the trained model onto the canvas

To bring the trained model onto the canvas, follow the steps:

[iframe](https://player.vimeo.com/video/893640982?title=0&byline=0&portrait=0&badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Double-click the **Main.imunit** to open the canvas.
2. - Expand **Project** and drag and drop the **Keras Model** unit onto the canvas.
3. - Click on the node to open the **Properties** window and define the path of the model (\*.h5) file.
4. - Under **Inputs** in **Model File**, click the three horizontal dots to select the model file that is trained in Imagimob Cloud.
5. - The path of the selected model file is reflected in the **Model File** node and in the **Properties** window.

You can also navigate to the project directory and drag and drop the trained model file (.h5) onto the canvas.

#### Step 2: Select Input node to stream data

Graph UX provides the flexibility to stream data using the following units as Input Node:

- - Serial Capture
- - Local microphone
- - CSV file
- - Wave file

You can set the properties as per your requirement but it is recommended to use the default settings for the input nodes.

##### Setting up Serial Capture

Before using the development board to evaluate the model, make sure to flash your board with Imagimob Streaming Firmware. If using Infineon PSoC™ 6 development board, refer to [Getting started with Infineon PSoC™6 Wi-Fi BT Pioneer Kit and IoT sense expansion kit](https://developer.imagimob.com/supported-development-kits/infineon-PSoC6-wi-fi-pioneer-kit#getting-started-with-infineon-psoc6-wi-fi-bt-pioneer-kit-and-iot-sense-expansion-kit) and for using generic development board, refer to [Imagimob Streaming Protocol Specification](https://bitbucket.org/imagimob/imagimob-streaming-protocol-psoc6/src/main/PROTOCOL.md) for detailed instructions.

To set up Serial Capture, follow the steps:

![](https://developer.imagimob.com/Images/sc-eva.png)

1. - Connect the development board to laptop or PC using the serial port.
2. - Expand **Devices** and drag and drop the **Serial Capture** unit onto the canvas.
3. - Click on the node to edit the properties in the **Properties** window.
4. - Under **Inputs** set the following parameters:
  * In **Port**, select the serial port on which you connect the board.
  * In **Sample Rate**, select the required value
  * In **Sensor**, displays the sensor type

##### Setting up local microphone

To set up local microphone, follow the steps:

![](https://developer.imagimob.com/Images/microphone.png)

1. - Connect the microphone or use the speaker of the laptop or PC.
2. - Expand **Devices** and drag and drop the **Local Microphone** unit onto the canvas.
3. - Click on the node to edit the properties in the **Properties** window.
4. - Under **Inputs** set the following parameters:
  * In **Channels**, select the number of channels - Mono or Stereo
  * In **Device**, select the device that will be used for data streaming
  * In **Sample Rate**, select the required value

##### Setting up Wave File

To set up Wave File, follow the steps:

[iframe](https://player.vimeo.com/video/893687322?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Expand **File Formats** and drag and drop the **Wave File** unit onto the canvas.
2. - Click on the node to open the **Properties** window and define the path of the wave file.
3. - Under **Inputs** in **File Path**, click the three horizontal dots to select the desired wave file.
4. - The path of the selected wave file is reflected in the **Wave File** node and in the **Properties** window.

You can also drag and drop a wave file from the Solution Explorer onto the canvas.

Graph UX supports PCM encoded wave file with a sample rate of 16 bits.

##### Setting the CSV File

To set up CSV File, follow the steps:

[iframe](https://player.vimeo.com/video/893715371?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Expand **File Formats** and drag and drop the **CSV File** unit onto the canvas.
2. - Click on the node to open the **Properties** window and define the path of the csv file.
3. - Under **Inputs** in **File Path**, click the three horizontal dots to select the desired csv file.
4. - The path of the selected wave file is reflected in the **CSV File** node and in the **Properties** window.

You can also drag and drop a csv file from the Solution Explorer onto the canvas.

Graph UX supports csv file with timestamps.

#### Step 3: Setting up Visualization nodes and connecting different nodes

To set up the visualization nodes and connecting different nodes , follow the steps:

[iframe](https://player.vimeo.com/video/893738044?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Expand **Visualization** and drag and drop one **Label Track** and two **Data Tracks** unit onto the canvas. The visualization nodes helps in viewing and analysing the model predictions.
2. - Click on the visualization nodes to open the **Properties** window and set the properties, if required.
3. - Click on the red output icon present in the **Input Node** and drag over to the red input icon in the **Data Track** node. The output from the input node can be visualized in the **Data Track** node.
4. - Click on the red output icon present in the **Input Node** and drag over to the red input icon in the **Model Node**. The output from the input node is fed into the model creating a connection between the two nodes.
5. - Click on the red network output icon present in the **Model Node** and drag over to the gray icon in the **Data Track**. The output from the model is fed into the data track helping in visualization the model predictions.
6. - Click on the red network output icon present in the **Model Node** and drag over to the gray icon in the **Label Track**. The output from the model is fed into the label track helping in better visualization the model predictions as generated labels.

#### Generate predictions to evaluate the model

To generate predictions to evaluate the model, follow the steps:

[iframe](https://player.vimeo.com/video/893753444?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

1. - Navigate to the toolbar and click the **Start** button to open the session file (.imsession). An empty session file opens displaying the different tracks in timeline.
2. - Click the **Record** button and speak into the local microphone or sensors on the board to start the data streaming, when using Serial Capture or Local microphone as an Input node. Click the **Play** button to start data streaming, when using Wave or CSV file as an Input node.
3. - Based on the real-time data streaming, the model starts to make predictions.
4. - Capture the model predictions data for few seconds.
5. - Click the **Record** button to stop data streaming and model predictions. If you are streaming data using Wave or Csv file, click the **Stop** button.
  After evaluating the model performance on the real-time data, you can make a decision to deploy or further train the model. You can save the generated predictions as dataset for improving the model.
6. - Select **File>Save Main.session As**, if you only want to the save the session file. However, select **File>Save** to save all the files in the timeline. The **Save New Session** window appears.
7. - In **location**, click the three dot and select the desired location to save the file.
8. - In **Session Name**, enter the name of the session file.
9. - In **Track options**, select the save checkbox corresponding to the tracks you want to save. You can also edit the track name and file name by double clicking the respective columns.
10. - Click **OK** to save the files.
