---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-distribution"
fetched_at: "2026-03-10T15:51:41Z"
title: "Data Distribution"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-distribution"]
---

### Data Distribution

After you add data to the project, you need to distribute the data into different datasets. You can split the data into the following three sets:

- - **Train Set :** Data in the train set is used to train the model
- - **Validation Set :** Data in the validation set is used to test and evaluate the performance of the model during training
- - **Test Set :** Data in the test set is used at the end of training to evaluate the performance of the model on unseen data

It is recommended to keep the training set significantly bigger than the validation and test sets. Some standard splits are (train/validation/test) 60/20/20 or 80/10/10. The more data you have collected, the smaller you can make your validation and test set target size.

To distribute the data into the three sets, follow the steps:

1. - Open the project file and select **Redistribute Sets**. The redistribute data tool window appears.
2. - Set **Scope** as either **Redistribute data from All Sets** or **Redistribute data from Unassigned sets**.

  ![](https://developer.imagimob.com/Images/siren-tutorial/pic-10.png)
3. - Use the graphical tool to distribute the data into different datasets. The target size can either be based on Label Count or Annotated Time.
4. - Select **Redistribute** and the data in the selected scope will be distributed among the three data sets.
