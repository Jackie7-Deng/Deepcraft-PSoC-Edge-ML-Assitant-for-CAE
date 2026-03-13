---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data/bring-your-own-data-object-detection"
fetched_at: "2026-03-10T15:51:37Z"
title: "Bring Your Own Data Object Detection"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "bring-your-data"]
---

# Bring Your Own Data Object Detection

### Bring your own data for object detection projects

DEEPCRAFT™ Studio provides you the flexibility to bring your own dataset in order to build a object detection project. To train an Object Detection model in the DEEPCRAFT™ Studio, you need images and labels. Now, there can be two scenarios:

- - **Images dataset with labels**: If you have a dataset with labels in formats such as PASCAL VOC, COCO, and YOLO, Studio provides functionality to convert these different label formats into the Studio-specific label format, which is LabelXml. When you add the dataset with PASCAL VOC, COCO, and YOLO label format into the Project, Studio automatically converts these label formats into LabelXml.
- - **Image dataset without labels**: If you have an image dataset without labels, you can still import data into Studio and label your images within the Studio. To learn how to label image data, refer to [Labeling Images](https://developer.imagimob.com/data-preparation/data-labeling/label-image-data#labeling-images).

For instructions on importing **Images dataset with labels** or **Image dataset without labels** into Studio, refer to [Adding data to object detection projects](https://developer.imagimob.com/data-preparation/add-project-object-detection).

### Supported Image formats

You can bring the images in the following format: **JPG**, **PNG**, **JPEG**

### Supported Labels formats

You can bring the labels in the following format: **PASCAL VOC**, **COCO**, **YOLO**, **LabelXml**

#### PASCAL VOC

The **[PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2005/index.html)** dataset is a widely recognized benchmark in the field of computer vision. It is used for various tasks such as object detection and image classification. The dataset provides standardized image sets and labels to facilitate the evaluation and comparison of different methods.

**PASCAL VOC Label Format**: The Pascal VOC label format stores annotations in XML files, where each file includes:

- - **Metadata**: The XML file includes metadata such as the filename, image size (width, height, depth), and the folder name.
- - **Object Annotations**: For each object in the image, the XML file specifies:
- - **Object Class**: The category or class of the object (e.g., person, car, dog).
- - **Bounding Box Coordinates**: The position of the object within the image, defined by four coordinates: xmin, ymin, xmax, and ymax. These coordinates represent the top-left and bottom-right corners of the bounding box in absolute pixel values.
- - **Pose**: The pose of the object (optional).
- - **Truncated**: Indicates if the object is partially visible (optional).
- - **Difficult**: Indicates if the object is difficult to recognize (optional).

**Example Pascal VOC XML label file:**

```
 <annotation>
     <folder>VOC2012</folder>
     <filename>image1.jpg</filename>
     <size>
         <width>500</width>
         <height>375</height>
         <depth>3</depth>
     </size>
     <object>
         <name>dog</name>
         <pose>Unspecified</pose>
         <truncated>0</truncated>
         <difficult>0</difficult>
         <bndbox>
             <xmin>48</xmin>
             <ymin>240</ymin>
             <xmax>195</xmax>
             <ymax>371</ymax>
         </bndbox>
      </object>
  </annotation>
```

#### COCO

The **[COCO](https://cocodataset.org/#home)** (Common Objects in Context) dataset is one of the most popular and comprehensive datasets used in computer vision. It contains images of complex everyday scenes with common objects in their natural context.

**The COCO Label Format**: COCO annotations are stored in a single JSON file, which includes:

- - **Images**: Metadata for each image, such as ID, filename, width, and height.
- - **Categories**: Definitions of object classes, each with a unique ID and name.
- - **Annotations**: Details of object instances, including:

  * **image\_id**: Reference to the image.
  * **category\_id**: Reference to the category.
  * **bbox**: Bounding box coordinates in the format [x, y, width, height].
  * **segmentation**: Segmentation mask (optional).
  * **area**: Area of the bounding box.
  * **iscrowd**: Indicates if the object is part of a crowd.

  **Example COCO JSON label file:**

  ```
  {
    "images": [
      {
        "id": 0,
        "file_name": "image1.jpg",
        "width": 640,
        "height": 416
      }
   ],
   "categories": [
     {
       "id": 0,
       "name": "cat"
     }
   ],
   "annotations": [
     {
       "image_id": 0,
       "category_id": 0,
       "bbox": [540.0, 295.0, 23.0, 18.0]
     }
   ]
  }
  ```

#### YOLO

The **[YOLO](https://labelformat.com/formats/object-detection/yolov11/)** (You Only Look Once) dataset is a real-time object detection system known for its speed and accuracy. It processes images in a single pass through a neural network, making it highly efficient for applications requiring quick detection.

**The YOLO Label Format**: YOLO annotations are stored in text files, with each image having a corresponding .txt file. Each line in the file represents an object and follows this format:

- - **class\_id**: Integer representing the object’s class.
- - **x\_center, y\_center**: Normalized coordinates of the object’s center (relative to the image’s width and height).
- - **width, height**: Normalized width and height of the bounding box.

**Example of a YOLO annotation line:**

```
   0 0.5 0.5 0.2 0.2
```

This line indicates an object of class 0, centered at (0.5, 0.5) with a width and height of 0.2 (normalized values).

After you have formatted the data as per the specifications listed above, you can now add data into your project in Studio. Refer to [Adding data to object detection projects](https://developer.imagimob.com/data-preparation/add-project-object-detection).
