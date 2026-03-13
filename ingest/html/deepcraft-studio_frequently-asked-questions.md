---
source_url: "https://developer.imagimob.com/deepcraft-studio/frequently-asked-questions"
fetched_at: "2026-03-10T15:52:03Z"
title: "Frequently Asked Questions"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "frequently-asked-questions"]
---

### Frequently Asked Questions

This section provides answers to some of the frequently asked questions about DEEPCRAFT™ Studio.

**Q: What happens if the data file contains a mix of analog and digital (bit field) data?**

**A:** The model will differentiate between the digital and analog signals. Refer to the sample data file that contains both the analog and digital data.

![](https://developer.imagimob.com/Images/faq.png)

**Q: Should the data be manually pre-formatted or is there a way to preprocess the data in DEEPCRAFT™ Studio?**

**A:** DEEPCRAFT™ Studio supports pre-processing of data, refer to [Preprocessing](https://developer.imagimob.com/model-building/preprocessing) for more information.

**Q: Is timestamp always expected in seconds?**

**A:** It is recommended to have timestamps in seconds. However, it does not have an impact on the model training. If the timestamps are provided in milliseconds (ms), the view will have the numbers off by a thousand.

**Q: Can we remove/ignore some columns from the data file?**

**A:** DEEPCRAFT™ Studio has a pre-processor that allows to drop columns.

**Q: If the data is periodic and not continuous, for instance heating regulation is only periodically active, how does that affect the overall machine learning process?**

**A:** This will not affect the machine learning process if the sliding window of the model is configured to skip the non-continuous parts. Refer to the sample images.

![](https://developer.imagimob.com/Images/example.png)

![](https://developer.imagimob.com/Images/example-pic.png)

**Q: Why is the generated Edge code (*.c/*.h) not build in my compiler?**

**A:** Configure your compiler for the C99 and ANSI C standard. Make sure that you do not treat warnings as errors.

**Q: How do I enable or disable the experimental features?**

**A:** Navigate to **Tools** in the menu bar and select **Options**. In **General** tab, select or deselect the **Enable Experimental Features** checkbox to enable or disable the experimental features respectively. Some features require that you restart Studio for the change to have effect.

These features are provided without support.

**Q: How do I enable or disable the development updates?**

**A:** Navigate to **Tools** in the menu bar and select **Options**. In **General** tab, select or deselect the **Enable Development Updates** checkbox to enable or disable the development updates respectively. When you enable the development updates, this will change the update server to development server, allowing you to fetch the internal updates.

**Q: My jobs seem to run at different speeds?**

**A:** The AI Training Service is free to assign jobs to different compute resources, which may cause this effect.

**Q: I cannot delete my “Gen” directory because a file is being used by another process.**

**A:** A common cause of this error is that the *Gen* directory is your current working directory in Cygwin. Close Cygwin and try again.

**Q: Does the time\_out variable in the C code give you the first or last timestamp in the window for the prediction?**

**A:** The time\_out variable is an array containing the first and the last timestamps that were input to the model to form the current predictions. In most cases, the first timestamp in the array is the first timestamp of the input for the prediction and the last array entry is the last timestamp of the input for the prediction.

**Q: Can I deploy the Python/.h5 models?**

**A:** Yes, it is possible to deploy the python models. This is especially useful for performing live testing and anlaysing pre-processor before putting the AI application on the edge device and we have a special tool for this purpose. Please contact us for more details.
