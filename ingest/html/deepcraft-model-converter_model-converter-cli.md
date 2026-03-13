---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/model-converter-cli"
fetched_at: "2026-03-10T15:52:06Z"
title: "Model Converter CLI"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "model-converter-cli"]
---

# Model Converter CLI

### Command Line Interface

This section provides step-by-step information on generating, optimizing and validating the code for Infineon targets PSOC™ 6, PSOC™ Edge M55+U55, PSOC™ Edge M33+NNLite using the Command Line Interface.

#### Code Generation Workflow

This is the workflow for generating code using DEEPCRAFT™ Model Converter:

1. - **Generate Code**: Convert your model (.h5, .tflite, or .pt2) into (.c) and (.h) files which you can deploy onto the Infineon board.
2. - **Optimize the Model**: Use calibration data to apply quantization
3. - **Validate the Model**: Test the quantized or non-quantized model using validation data to ensure accuracy

#### Launch Command Line Interface (CLI)

After you download and install the DEEPCRAFT™ Model Converter executable file, open a command prompt, type **dcmc — help** and press Enter. A command prompt window appears listing all the available commands.

![](https://developer.imagimob.com/Images/model-converter/pic-12.png)

#### Ways to Generate Model Code via Command Line Interface

You can generate code for a model from the CLI in two ways:

##### Using Bring Your Own Model project file (.byom) exported from the GUI

While the Model Converter provides full functionality directly through the Command Line Interface and does not require a project file (.byom), we recommend creating one from the GUI based on your model. This reduces typing and helps to prevent errors. Refer to [Configure the Project File](https://developer.imagimob.com/deepcraft-model-converter/model-converter-gui#configure-the-project-file) to know more.

After you create the project file in the GUI, load the project file in the CLI. The CLI will consume the parameters from the file and generate the code accordingly. Run the following command to generate code using the BYOM project file:

```
dcmc convert-project -p <project file path>
```

##### Issuing the required commands manually on the command line

If you prefer not to use a project file, you can invoke code generation by providing all necessary parameters directly. The complete command syntax is documented in the sections below.

#### Pre-requisites for the PyTorch Models

When generating the code for PyTorch models, you must select one of the following options: **Cloud-Based Code Generation** or **Container-Based Code Generation**.

The selection of the Cloud-Based Code Generation and Container-Based Code Generation is required only for the PyTorch Models.

**This video provides a concise, visual introduction to the topics and workflows described in this documentation.**

[iframe](https://player.vimeo.com/video/1118504403?badge=0&autopause=0&player_id=0&app_id=58479)

#### Command Line Syntax

Below are the commands that you can run to attain the following functionality:

#### Generate Code for model

You can generate code for Keras(.h5), TensorFlow Lite (.tflite) or PyTorch (.pt2) models for Infineon targets PSOC 6, PSOC Edge M55+U55, PSOC Edge M33+NNLite.

- - For Keras(.h5) and TensorFlow Lite (.tflite) models, the input shape of the model is detected automatically, so you do not need to provide a shape parameter. However, when generating code for PyTorch (.pt2) models, you must specify the model shape.
- - Before you generate the code for PyTorch models, you must run the required commands to use either the Cloud-Based Code Generation or Container-Based Code Generation, refer to [Pre-requisites for the PyTorch Models](https://developer.imagimob.com/deepcraft-model-converter/model-converter-cli#pre-requisites-for-the-pytorch-models)
  to know the commands.

To generate the code for Keras(.h5) and TensorFlow Lite (.tflite) models, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]
```

To generate the code for PyTorch (.pt2) models, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --input-shape <Input shape as comma-separated dimensions, example ("224,224,3">
```

By default, the model files (.c and.h) are generated with predefined names and are placed in *Codegen* directory. Additionally, the function names in the optimized C API are predefined with a default prefix. To customize the names of the output files, the directory where the files are stored, or the prefix for the function names, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] -n <name of the output file> -o <name of the output directory> --prefix <name of prefix>
```

By default, the **Override Arena Size** is set to 0 to enable automatic calculation of the arena size. However, if the model fails to initialize on the embedded device and crashes during initialization (IMAI\_int()), modify the arena size value. Increase in increments of 4096 bytes from the default calculated size. When you find a working value, decrease in steps of 1024 bytes or less to determine the minimum stable size that does not crash. The calculated arena size can be found in the *code\_generation\_report.md* under the *Scratch memory* column in the *Memory Usage* section. Refer to [Insufficient model arena memory during deployment](https://developer.imagimob.com/deepcraft-model-converter/troubleshooting/arena-memory) for detailed information.To set the Override Arena Size, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] --arena-size <arena size in bytes>
```

By default, the **Interpreterless** mode is disabled. The interpreterless mode pre-interprets the model to generate the static C++ code that executes the neural network directly, removing the need for the TensorFlow Lite Micro interpreter at runtime. When this option is enabled, the runtime, memory planner and unused operator code, memory planner are not compiled into the final application, reducing the ROM footprint. This can provide memory savings for very small models (under 400 KB) that use a limited set of operator types. The exact amount of memory saved may vary from model to model but in some cases can be close to ~200KB. To enable Interpreterless mode, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite] --interpreterless
```

Interpreterless mode is supported on PSOC™ 6, PSOC™ Edge M33+NNLite targets only.

#### File specifications for calibration and validation

Before starting model optimization and validation, prepare the calibration and validation data. Calibration data is used to quantize the model, while validation data is used to evaluate the model. You can select the data source as Compressed NumPy file (.npz)\*\*, **CSV file**, or a **Recursive Directory**. Specifications for Compressed NumPy file, CSV file or Recursive Directory are listed in **[Supported Data Formats](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-data-formats)**.

The calibration dataset should be diverse and representative of expected inputs, including edge cases and extremes. It is recommended not to use the validation dataset for calibration to avoid bias and maintain an unbiased evaluation.

#### Model Optimization

Model optimization involves refining the code to enhance performance, efficiency, and accuracy of the model on the Infineon targets. It reduces computational cost, shortens inference time, and reduces memory footprint to deliver reliable performance across environments.

##### Quantize the model

Generate a 8-bit quantized model by providing the calibration data. Specify the maximum number of samples to use for calibration. If the number of samples in the provided dataset exceeds this value, the dataset will be truncated to the first N samples. To quantize the model, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --c-max-samples <max samples>
```

You can enable sparsity to further optimize the model by packing sparse weights, thereby saving memory when deploying the model on the target device. By default, this option is disabled. To enable sparsity, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> -s <enable sparsity>
```

Quantization Type parameter is applicable for Keras (.h5) models only.

You can select the Quantization Type as **Int8x8** or **Int16x8**. In Int8x8 quantization, both weights and activations are quantized to 8-bit integers (Int8). Int8x8 quantization reduces the time consumption and minimizes memory and bandwidth usage but at the cost of some accuracy. In Int16x8 quantization, weights are quantized to 8-bit integers (Int8), but activations are quantized to 16-bit integers (Int16). Int16x8 quantization can provide higher accuracy with only a marginal increase in compute time, model binary size, and work-buffer memory by storing intermediate values in 16-bit integers rather than 8-bit. However, the benefit is model-dependent, so you must evaluate Int8x8 and Int16x8 side by side to determine which configuration suits your needs.

You can generate the code twice — first with Int8x8 quantization, then with Int16x8 quantization and compare the results side by side in the **Output window**. For complex models, review quantitative metrics (for instance, see the validation results) in the `code_generation_report.md` file to assess differences. To select the quantization type, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] --c-data <path to calibration data> --quantize-type [int8x8/int16x8]
```

- - If you prefer automation or deeper analysis, you can also perform the comparison using Python scripts on the following files: **output\_folder/eval\_data/expected\_output.npy** and **output\_folder/eval\_data/actual\_output.npy**.
- - NPUs accelerating neural network inference usually only accelerate int8x8 or int16x8 layers, float32 layers will fall back to the MCU.

Refer to **[Supported Data Formats](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-data-formats)** to know the specifications for Compressed NumPy file, CSV file or Recursive Directory.

#### Advanced optimization for PSOC™ Edge M55+U55

The Vela compiler includes different optimizations settings for Ethos-U55 NPU targets that lower scratch memory usage with minimal to no effect on model accuracy. These optimizations are enabled by default, and you can modify the settings as required using the relevant commands.

1. - **System Configuration**: Select **Pse8xSOCMEM300MHzQUADXIP** or **Pse8xSOCMEM200MHzQUADXIP** as the system configuration of the Ethos-U NPU. By default, Pse8xSOCMEM300MHzQUADXIP is selected. For information about these configurations, refer to the Silicon documentation. By default, Pse8xSOCMEM300MHzQUADXIP is set as the system configuration. To select Pse8xSOCMEM200MHzQUADXIP as the system configuration, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-system-config Pse8xSOCMEM200MHzQUADXIP
  ```
2. - **Memory Mode**: Select **Shared SRAM** or **SRAM Only** as the memory mode. Shared SRAM is shared between Ethos-U and Cortex-M software, whereas SRAM Only is dedicated to Ethos-U. The non-SRAM memory is considered read-only. By default, Shared SRAM is selected. To set SRAM Only as the memory mode, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-mem-mode SRAMonly
  ```
3. - **NPU optimization strategy**: Select the optimization strategy based on **Size** or **Performance**. The Size strategy ensures minimal RAM usage by avoiding the use of the arena cache memory area size whereas the Performance strategy prioritizes maximal performance by utilizing the specified arena cache memory area size. By default, Performance strategy is selected. To set the optimization strategy as size, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-opt-strategy <size>
  ```
4. - **Tensor Allocator**: Select **Linear Alloc**, **Greedy** or **HillClimb** to specify the algorithm for allocating non‑constant tensors on the NPU and CPU. By default, HillClimb is selected. To modify the allocator algorithm, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-tensor-alloc [Greedy/LinnearAlloc/HillClimb]
  ```
5. - **Arena Cache Size**: Set the size of the arena cache memory area, in bytes. The size of the arena cache memory area must be any integer greater than or equal to 0. By default, the value of arena cache memory is set as 2936012. To modify, the value of arena cache size, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-arena-cache <value>
  ```
6. - **Recursion Limit**: Set the Python internal limit to depth of recursion. For very large networks, increasing the recursive limit may be necessary due to the recursive graph traversal algorithm. If generation fails with a RecursionError, increase the limit using this option. By default, the recursion limit is set as 1000. To modify the recursion limit, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-rec-limit <999>
  ```
7. - **Max Block Dependency**: Set the maximum value that can be used for the block dependency delay between NPU kernel operations. A lower value may result in longer execution time. You may set: 0, 1, 2 or 3 as the value for Npu block dependency. By default, the value of block dependency is set as 3. To modify the block dependency, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55]  --c-data <path to calibration data> --npu-block-depend <3>
  ```

#### Model Validation

Model validation evaluates the optimized model to the original baseline and generates a report. The report summarizes how closely the converted model’s predictions match your reference outputs along with other validation metrics. You can validate both quantized and non-quantized models without connecting to a actual device.

Specify the maximum number of samples to use for validation. If the number of samples in the provided dataset exceeds this value, the dataset will be truncated to the first N samples. For on-device profiling, select a smaller value to ensure the data fits on the target device. To validate the model, run the following command:

```
dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] --v-data <path to validation data> --v-max-samples <max samples>
```

Refer to **[Supported Data Formats](https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-data-formats)** to know the specifications for Compressed NumPy file, CSV file or Recursive Directory.

#### Other commands

- - **No Verbose**: Set the no verbose option, if you want to display information related to warnings and errors only. By default, this option is disabled. To enable no verbose, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] --no-verbose
  ```
- - **No cleanup**: By default, the application automatically removes temporary files created during code generation.To retain these files, run the following command:

  CLI Command

  ```
  dcmc -m <path to model> -o <path to output directory> -t [Psoc6/PsocEdgeM33NNLite/PsocEdgeM55U55] --no-cleanup
  ```
- - **Version**: Displays the version information. Run the following command:

  CLI Command

  ```
  dcmc --version
  ```
- - **Help**: Displays the primary commands and provides detailed help for a specific command.Run the following command:

  CLI Command

  ```
  dcmc --help
  ```

The code (model.c/.h files) is generated in the Output Directory defined earlier along with the **code generation report**. You can also view the validation and optimization results in the The Output window at the bottom of the model converter.

### Whats Next?

After you have generated, optimized and validated the code for your model, the next step is to deploy the code onto the Infineon boards using ModusToolbox™. To learn how to deploy the code, refer to [Deploy model on PSOC™ Edge using the Code Examples](https://developer.imagimob.com/deepcraft-model-converter/deploy-model-using-code-example).
