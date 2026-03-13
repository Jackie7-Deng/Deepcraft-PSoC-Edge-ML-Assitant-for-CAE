---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-labeling/manual-labeling"
fetched_at: "2026-03-10T15:51:39Z"
title: "Manual Labeling"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-labeling"]
---

### Manual Labeling

Labeling data can be a time-consuming task. To streamline this process, we offer a technique that allows you to label data with just a click of a button. By defining labels at the project level once, you can effortlessly apply these predefined labels to your data. Rather than creating labels individually, our solution enables you to set up labels at the project level, allowing for consistent and efficient labeling with a single click.

#### Labeling using the Predefined labels

1. - Identify the classes you want to train the model on
2. - Define the classes in the **Predefined Labels Pane** in the Data Tab
3. - Open the session files and use the predefined classes to label the data with the click of button

#### How to Predefine Labels for the project?

1. - Navigate to the project directory and open the project file. By default, the **Data** tab is selected.

  ![](https://developer.imagimob.com/Images/project-file.png)
2. - In the **Predefined Labels Pane**, click the ![](https://developer.imagimob.com/Images/icons/add.svg) **Add New label** icon to add a label. A label is created under the **Label Name** column.

  ![](https://developer.imagimob.com/Images/image1.png)
3. - Double-click the label to modify the label name and click outside the label box to save the change.

  Similarly, define all the labels for the project in the Predefined Labels Pane. If you want to remove a label from the Predefined Labels Pane, click the ![](https://developer.imagimob.com/Images/icons/delete.svg) **Remove** icon next to the label you want to remove.

  When you open a session file, you can view all the Predefined Labels in the **Labels Bar**.

To use this functionality, ensure you open the session files from the Session Table in the **Data Pane**. This feature is not available if you open the session files from the Workspace.

#### How to label data using the Predefine Labels?

1. - Double-click the session file from the session table in which you want to add the labels. The predefined labels are displayed in the **Labels** bar.

  ![](https://developer.imagimob.com/Images/image4.png)
2. - Select a label in the **Labels Bar** and click and drag the mouse to select the part of the event you want to label. The label is added to the event automatically.
  You can also select a label by using the keyboard shortcuts, displayed when hovering the mouse over a label in the **Labels** bar.

  ![](https://developer.imagimob.com/Images/label.gif)

  Similarly, select the other labels in the **Label bar** and label the event. If you do not want to add anymore labels, select the label in the **Labels** bar again to disable the label.
