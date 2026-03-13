---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-model-formats"
fetched_at: "2026-03-10T15:52:07Z"
title: "Supported Model Formats"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "additional-resources", "supported-model-formats"]
---

# Supported Model Formats

### Supported Models and Quantization

This section outlines the supported model types for code generation and the quantization configurations available in the DEEPCRAFT™ Model Converter.

#### Supported Models

You can generate code for TensorFlow, Keras or PyTorch models with the following specifications:

**TensorFlow Lite or TensorFlow Keras**

You can use TensorFlow models built with Keras 2 saved in (.h5) format. The models exported with Keras 3 are not supported. If you use **TensorFlow 2.16+** to build a model: install the `tf-keras` python package,
force Keras 2 with `os.environ["TF_USE_LEGACY_KERAS"] = "1"` before the statement importing Tensorflow or Keras into your script.

```
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf
from tensorflow import keras
```

Support for **Keras 3** and the `.keras` file format will be available soon.

**PyTorch**

You must use **torch==2.6.0+**, when exporting models to the .pt2 format. Models exported with other PyTorch versions are not supported. For information on exporting pytorch models to .pt2, refer to [torch.export](https://docs.pytorch.org/docs/stable/export.html#overview) and [serialization](https://docs.pytorch.org/docs/stable/export.html#serialization) section in the PyTorch documentation.

#### Supported Quantization

The table below lists the supported quantization configurations in Model Converter:

| Supported Quantization | TensorFlow Keras | TensorFlow Lite | PyTorch |
| --- | --- | --- | --- |
| Float32 activations + Float32 weights | **✓** | **✓** | **✓** |
| Int8 activations + Int8 weights | **✓** | **✓** | **✓** |
| Int16 activations + Int8 weights | **✓** | **✓** | **x** |

You can quantize Keras (.h5) models to Int8×8 or Int16×8 by providing representative input samples for calibration. For PyTorch models exported as (.pt2), you can quantize the model to Int8x8 quantization only.

Models must have a single input and output. The input and output must use the same data type:

- - Float32 in → Float32 out
- - Int8 in→ Int8 out
- - Int16 in → Int16 out
