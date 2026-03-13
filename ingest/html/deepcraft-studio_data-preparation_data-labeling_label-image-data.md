---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-labeling/label-image-data"
fetched_at: "2026-03-10T15:51:40Z"
title: "Label Image Data"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-labeling"]
---

# Label Image Data

### Labeling Images

This section provides information on how to label the image data after you import the data into Studio.

#### Labeling using the Predefined labels

1. - Identify the classes you want the model to identify in the Images
2. - Define the classes in the **Predefined Labels Pane** in the Data Tab
3. - Open the session files and use the predefined classes to draw bounding boxes on the images

#### How to Predefine Labels for the project?

1. - Navigate to the project directory and open the project file. By default, the **Data** tab is selected.

  ![](https://developer.imagimob.com/Images/object-detection/pic-19.png)
2. - In the **Predefined Labels Pane**, click the ![](https://developer.imagimob.com/Images/icons/add.svg) **Add New label** icon to add a label. A label is created under the **Label Name** column.

  ![](https://developer.imagimob.com/Images/object-detection/pic-20.png)
3. - Double-click the label to modify the label name and click outside the label box to save the change.

  Similarly, define all the classes for the project in the Predefined Labels Pane. If you want to remove a class from the Predefined Labels Pane, click the ![](https://developer.imagimob.com/Images/icons/delete.svg) **Remove** icon next to the label you want to remove.

  When you open a session file, you can view all the Predefined Labels listed below in the panel.

To use this functionality, ensure you open the session files from the Session Table in the **Data Pane**. This feature is not available if you open the session files from the Workspace.

#### How to label image data using the Predefined Labels?

1. - Double-click the session file from the session table in which you want to add the labels. The session file window opens in a new tab. The predefined labels are displayed in in the panel.

  ![](https://developer.imagimob.com/Images/object-detection/pic-21.png)
2. - Select the image from the Image list that you want to label. The selected image appears in the Labeling window.
3. - Select the desired class from the Predefined Classes list and select the ![](https://developer.imagimob.com/Images/icons/pen.svg) **Pen Tool** to draw a bounding box around the relevant object in the image. The name of the selected class will appear in the top-left corner of the bounding box. Similarly, draw the required bounding boxes in the image. To label multiple classes, repeat the process with different class selections. You can use the available tools to draw the bounding boxes correctly. To know more, see [Tools for labeling the Images](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-without-kit/collect-image-data-using-graph-ux#tools-for-labeling-the-images).
4. - After you have labeled the image, press Ctrl+ S to save the image. Similarly, you can select the other image from the list and drawing the bounding boxes as explained above.
