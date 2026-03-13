---
source_url: "https://developer.imagimob.com/deepcraft-studio/model-training/download-import-model-files"
fetched_at: "2026-03-10T15:51:46Z"
title: "Download Import Model Files"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "model-training", "download-import-model-files"]
---

# Download Import Model Files

#### Downloading Model Files and Import predictions into your Project

After you have trained the model in Imagimob Cloud, the next step is to download the model files.

To download the model files, follow the steps:

1. - Click **Open Cloud** icon to browse the training jobs on the Imagimob Cloud.
  The account portal window opens and the **Jobs** tab is selected, by default.
2. - Double-click the training job of the project you want to track from the list of jobs. The project training job window appears in a new tab and provides the detailed view of the model.
3. - Scroll right to the **Download** column and click the **download icon** to download the model files.

  ![](https://developer.imagimob.com/Images/download-ml.png)
4. - The Download model files window appears with the option to download:

  * trained model (.h5 file)
  * model predictions for evaluating the trained model
  * test input and output datasets to be used in the ‘Generate Data Compare Test’

  Select the required files and click **Download**.

  ![](https://developer.imagimob.com/Images/download-model.png)
5. - Save the model files to an appropriate folder in your workspace.

  After you have downloaded the model files, the next step is to import the predictions.

#### Importing predictions into your project

DEEPCRAFT™ Studio allows a much more detailed view of the performance of a model by merging the model predictions as tracks into the sessions containing the original data.

To import predictions, follow the steps:

1. - Navigate to the project directory and open the project (.improj) file.
2. - In the **Data** tab, click **Merge** button and browse to select the **Predictions** folder.

  ![](https://developer.imagimob.com/Images/merge-button.png)
3. - Select the **Nested structure** or **Flat structure** radio button and click **Next**. Predictions from the selected folder will be merged as tracks into the corresponding local sessions.

  ![](https://developer.imagimob.com/Images/predict-folder.png)
4. - Select or deselect what you want to import and click **OK** to complete the merge.

After merging the predictions, you can evaluate the model, refer to [evaluation section](https://developer.imagimob.com/model-evaluation).
