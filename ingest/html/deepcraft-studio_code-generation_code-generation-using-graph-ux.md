---
source_url: "https://developer.imagimob.com/deepcraft-studio/code-generation/code-generation-using-graph-ux"
fetched_at: "2026-03-10T15:51:52Z"
title: "Code Generation Using Graph UX"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "code-generation", "code-generation-using-graph-ux"]
---

### Code Generation using Graph UX

After you have evaluated the performance of the model, you can convert the best model into optimized C-code that can be deployed on an Edge device. Graph UX facilitates code generation between any two nodes in a graph with a simple click of a button. You can select the starting and ending nodes in the graph to generate the corresponding C code for model deployment.

![](https://developer.imagimob.com/Images/code-gen/img-1.png)

To generate the code, follow the steps:

1. - Navigate to the toolbar and click the **Generate Source Code** button. The Generate Source Code window appears.
2. - Configure the following parameters:

  * In **Input Node**, select the input node for code generation from the drop-down list. The output tensor from this node will be substituted with the data provided to the enqueue(data) function. This node is not included when generating in the code generation process.
  * In **Output Node**, select the output node for code generation from the drop-down list. The output tensor from this node will be the data provided to the dequeue(data) function.
    The available output node options depend on the selected input node. Nodes that precede the selected input node in the graph will not be available for selection as output nodes.
  * In **Output Name**, enter the name of the output files.
  * In **Output Directory**, browse and select the directory where you want to save the generated code. By, default **CodeGen** is selected as the default folder.
  * In **C Prefix** enter the prefix to be added to the generated API functions.
  * In **Timestamps API**, enable the checkbox to track corresponding input time for each output prediction. To know about the edge API, refer to [Edge API](https://developer.imagimob.com/edge-optimization/edge-api).
  * In **CMSIS-DSP**, enable the checkbox to optimize the code using the ARM CMSIS-DSP Library. The code will be hardware accelerated using the CMSIS-DSP library for compatible nodes.
  * Click **Ok** to generate the code.
