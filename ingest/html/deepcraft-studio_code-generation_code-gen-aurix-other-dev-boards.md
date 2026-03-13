---
source_url: "https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-aurix-other-dev-boards"
fetched_at: "2026-03-10T15:51:51Z"
title: "Code Gen Aurix Other Dev Boards"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "code-generation", "code-gen-aurix-other-dev-boards"]
---

# Code Gen Aurix Other Dev Boards

### Code Generation for Infineon AURIX, Traveo, XMC7200 and Other Development Boards

After you have trained and evaluated the performance of the h5 model Keras or Tensorflow model, you can convert the best model into optimized C- code that can be deployed on an Edge device such as small printed circuit board with microcontroller and accelerometer sensor. For supported layers for C code conversion, refer to [Supported layers and functions](https://developer.imagimob.com/deployment/supported-layers).

To generate the code, follow the steps:

1. - Double click the HDF5 (\*.h5) model and click the **Code Gen** tab on the left pane.

  ![](https://developer.imagimob.com/Images/code-gen.png)
2. - Configure the following parameters:

  * In **Architecture** select the target architecture for optimization. Select **Any(ANSI C99)** to compile for any platform, **Infineon Aurix** to compile for Aurix board, **Infineon TRAVEO** to compile for Traveo board and **Infineon XMC** to compile for XMC7200 Evaluation Kit.
  * In **Target Device**, select the required Infineon Traveo board or core type from the following options - TRAVEO T2G (KIT\_T2G-B-H-LITE) or TRAVEO T2G (KIT\_T2G-B-E\_LITE). This parameter is applicable when you select Infineon Traveo as the architecture type.
  * In **Output name** enter the name for the generated .c/.h files.
  * In **Output directory** browse the directory where you want to save the optimized output. By, default **Gen** is selected as the default folder.
  * In **Timestamps API** enable the checkbox to track corresponding input time for each output prediction. To know about the edge API, refer to [Edge API](https://developer.imagimob.com/edge-optimization/edge-api).
  * In **C Prefix** enter the prefix for the function names in the optimized C API.
  * In **Build** select the build type as Preprocessor and Network, Preprocessor, or Network.
  * In **Generate Python Bindings** enable the checkbox to generate data python bindings for the C library. This will add a Makefile to build native (.dll) library and python wrapper to output directory. Distribution requires only (.dll) and (.py) files.
  * In **Generate Data Compare Test** enable the checkbox to generate tests together with the Edge model. This test verifies that the output from the Edge model matches the output from the HDF5 (.h5) model for the same input. You need to provide the input and output data to test the optimized output.

  You can perform the compare test in two ways, by using:

  * the input and output data files (.data) generated after training the model
    You can download these files from Imagimob Cloud. To know more, refer to [Downloading model files](https://developer.imagimob.com/model-training/download-import-model-files).

    ![](https://developer.imagimob.com/Images/compare-test.png)
  * any dataset from the **Data** folder as input and the corresponding data predictions in the **Predictions** folder as output
  * In **Input file to use for compare test**

    + In **File type**, select the file type of the input file that you want to compare.
    + In **File path**, browse to the location to select the input file.
  * In **Expected output data file to use for compare test**

    + In **File type**, select the file type of the output file that you want to compare.
    + In **File path**, browse to the location to select the output file.

Make sure you select the input and output files from the same session with the correct file type otherwise the test will fail because of data mismatch.

1. - Click **Generate Code**. The code is generated and the **Code generation Report** window appears.

  ![](https://developer.imagimob.com/Images/report.png)

  The optimized C-code along with ‘Makefile’ and ‘runner.c’ is automatically saved in the **Gen** folder. This is the folder that you select in the **Output Directory** parameter.
2. - Click **Ok** to close the report. A pop up window appears.
3. - You can run the compare test right away or later, as needed.

  * To run the test later,

    + Navigate to the **Gen** directory created when generating the code.
    + Right-click the **Makefile** and select **Make All**. The Cygwin window appears and test run the model using the provided input and output files.
  * To run the test right away, click **Build Now**.
4. - A console window appears.

  ![](https://developer.imagimob.com/Images/console-build.png)

  From the output above, we can now confirm that the generated code is equal to the HDF5 (.h5) model to within the sixth decimal. You can safely deploy this code and be confident that the edge model will perform as good as the .h5 model. The only difference between the two models is that the Edge model consumes a fraction of the memory and processing power during runtime and can run on any embedded platform.
