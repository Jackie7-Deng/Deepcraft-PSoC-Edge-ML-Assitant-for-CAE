---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/machine-learning-algorithms"
fetched_at: "2026-03-10T15:51:13Z"
title: "Machine Learning Algorithms"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "machine-learning-algorithms"]
---

# Machine Learning Algorithms

### Machine learning Algorithms in DEEPCRAFT™ Studio

This section introduces the machine learning algorithms supported in DEEPCRAFT™ Studiofor building ML models to solve various business problems.

#### Semi-supervised machine learning algorithms: Computer Vision

DEEPCRAFT™ Studio supports the end-to-end development workflow for building computer vision models optimized for edge devices. Due to the built-in Ultralytics YOLO model training pipeline, there is no need to be a domain expert in order to build vision-based Edge AI models. The inherent size needed to process images has long prevented models
running on the edge. With the advent of powerful new microcontrollers (MCUs) containing neural processing units (NPUs) this is changing, and DEEPCRAFT™ Studio now streamlines the process of making vision models. Refer to the following topics for end-to-end guidance on building and deploying a computer vision model:

- - [Real-Time Image data collection and labeling using camera](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-without-kit/collect-image-data-using-graph-ux)
- - [Bring your own data for object detection projects](https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data/bring-your-own-data-object-detection)
- - [Adding data to object detection projects](https://developer.imagimob.com/deepcraft-studio/data-preparation/add-project-object-detection)
- - [Labeling Images](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-labeling/label-image-data)
- - [Training Object Detection Model](https://developer.imagimob.com/deepcraft-studio/model-training/training-object-detection)
- - [Evaluating Object Detection model](https://developer.imagimob.com/deepcraft-studio/model-evaluation/evaluating-object-detection-model)
- - [Code Generation for Vision Model](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-vision-models)
- - [Deploy Vision Model on PSOC™ Edge boards](https://developer.imagimob.com/deepcraft-studio/deployment/deploy-models-supported-boards/deploy-vision-model-PSOC-Edge)

#### Supervised machine learning algorithms: Regression and Classification

**Regression Algorithms**

Regression algorithms are designed to understand the correlations between dependent and independent variables. The dependent variables are those we aim to predict, while the independent variables are those we use for prediction. These algorithms are used to predict continuous numerical outputs. You can evaluate the regression models using metrics like Mean Squared Error (MSE), R2-Score, and Mean Absolute Percentage Error (MAPE), along with graphical plots such as Quantile - Quantile and Histogram of residuals. Studio supports linear regression analysis. Power Generation Prediction is one of the regression starter project supported in Studio.

![](https://developer.imagimob.com/Images/pic-4.png)

**Classification Algorithms**

Classification algorithms are used to predict categorical or discrete values. Classification involves predicting a label or category. These algorithms classify the dataset into one or more labels. A binary classifier deals with two classes or categories, while a multi-class classification algorithm handles more than two classes. You can evaluate the classification models using metrics, like confusion matrix, recall, F1-Score, accuracy. Human activity recognition, keyword spotter, baby cry detection, siren detection are some of the classification starter projects supported in Studio. To know more about the different classification starter projects supported in studio, refer to [Starter Projects](https://developer.imagimob.com/getting-started/workspace-project/starter-project).

![](https://developer.imagimob.com/Images/pic-3.png)

#### Determining Project Type: Classification or Regression

In a classification project, there are two types of files, .data and .label. The .data file contains the actual data, while the .label file contains the labels that annotate the data in the .data file.

In a regression project, we use a .data file that contains the actual data, and instead of a .label file, the .data file itself is used to label the data. Additionally, regression projects do not require separate labeling, which saves time and makes the project more efficient.

So, when you import data into the project, studio will determine the project type based on the active label track of the sessions:

- - If all sessions have the active label track set to .data, Studio will classify the project as regression.
- - If all sessions have the active label track set to .label, Studio will classify the project as classification

In a project, all sessions must use either .data file or .label file as an active label track. It is not permissible to have some sessions with .data file and others with .label file as the active label track.
