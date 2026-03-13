---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data"
fetched_at: "2026-03-10T15:51:36Z"
title: "Bring your own data into DEEPCRAFT™ Studio"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "bring-your-data"]
---

### Bring your own data into DEEPCRAFT™ Studio

You can easily import your existing data into DEEPCRAFT™ Studio, which offers the flexibility to integrate datasets from your local hard drive. By importing your own datasets into Studio, you can bypass the often time-consuming task of data collection and immediately focus on training and refining your model. This approach not only saves time but also ensures that the model is trained on data that is highly relevant to your specific needs. However, it is important to note that the tool supports specific data types and file formats for import.

#### What type of data can you bring into Studio?

The type of data you can import into the DEEPCRAFT™ Studio depends on the machine learning model you are aiming to build:

##### Classification and Regression Algorithm

To solve a machine learning problem using a classification algorithm, you need:

- - **Data File**: This file contains the actual data, which could be audio data, IMU data, or any other sensor data relevant to the problem. The file extension should be `.data` or `.csv`.
- - **Label File**: This file contains the labels that annotate the data in the data file. The file extension should be `.label`.

To solve a machine learning problem using a regression algorithm, you need:

- - **Data File**: This file contains the actual data required to solve the regression machine learning problem. In regression projects, the data file itself is used as the label file. The file extension should be `.data` or `.csv`.

For detailed specifications of the data and label files and instructions on structuring your data directory, refer [Bring your own data for classification and regression projects](https://developer.imagimob.com/data-preparation/data-collection/bring-your-data/bring-your-own-data).

If you have data without labels, you can still import data into DEEPCRAFT™ Studio. Studio offers various techniques for labeling the data. To learn how to import your data into the tool, refer to [Adding data to classification and regression projects](https://developer.imagimob.com/data-preparation/add-data-to-project). For information on the different labeling techniques, refer to [Data Labeling](https://developer.imagimob.com/data-preparation/data-labeling).

##### Object Detection Algorithm

To solve a machine learning problem using an object detection algorithm, you need one of the following:

- - **Images**: If you have an image dataset without labels, you can import the data into Studio and label the data later in Studio. The file extensions should be `.png` or `.jpg`. To learn how to label image data, refer to [Labeling Images](https://developer.imagimob.com/data-preparation/data-labeling/label-image-data#labeling-images).
- - **Images dataset with labels**: You can import datasets with different label formats, such as `PASCAL VOC`, `COCO`, `YOLO` and `LabelXml` into Studio. To know about the label formats, refer to [Bring your own data for object detection projects](https://developer.imagimob.com/data-preparation/data-collection/bring-your-data/bring-your-own-data-object-detection).
  To learn how to import your data into the Studio, refer to [Adding data to object detection projects](https://developer.imagimob.com/data-preparation/add-project-object-detection).
