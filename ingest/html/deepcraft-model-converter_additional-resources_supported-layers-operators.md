---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-layers-operators"
fetched_at: "2026-03-10T15:52:09Z"
title: "Supported Layers Operators"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "additional-resources", "supported-layers-operators"]
---

# Supported Layers Operators

### Supported Operators and Layers

When generating code for the models in Model Converter, the following operators and layers are supported on Infineon hardware.

| Operators/Layers | Float32 | Int8x8 | Int16x8 |
| --- | --- | --- | --- |
| ABS | ✓ | Χ | ✓ |
| ADD | ✓ | ✓ | ✓ |
| ADD\_N | ✓ | ✓ | Χ |
| ARG\_MAX | ✓ | ✓ | Χ |
| ARG\_MIN | ✓ | ✓ | Χ |
| ASSIGN\_VARIABLE | ✓ | ✓ | ✓ |
| AVERAGE\_POOL\_2D | ✓ | ✓ | ✓ |
| BATCH\_MATMUL | ✓ | ✓ | ✓ |
| BATCH\_TO\_SPACE\_ND | ✓ | ✓ | Χ |
| BROADCAST\_ARGS | ✓ | ✓ | ✓ |
| BROADCAST\_TO | ✓ | ✓ | ✓ |
| CALL\_ONCE | ✓ | ✓ | ✓ |
| CAST | ✓ | ✓ | ✓ |
| CEIL | ✓ | Χ | Χ |
| CONCATENATION | ✓ | ✓ | ✓ |
| CONV\_2D | ✓ | ✓ | ✓ |
| CUMSUM | ✓ | ✓ | Χ |
| DEQUANTIZE | ✓ | ✓ | ✓ |
| DEPTH\_TO\_SPACE | ✓ | ✓ | Χ |
| DEPTHWISE\_CONV\_2D | ✓ | ✓ | ✓ |
| DIV | ✓ | ✓ | Χ |
| ELU | ✓ | ✓ | ✓ |
| EMBEDDING\_LOOKUP | ✓ | ✓ | Χ |
| EQUAL | ✓ | ✓ | Χ |
| EXP | ✓ | Χ | Χ |
| EXPAND\_DIMS | ✓ | ✓ | ✓ |
| FILL | ✓ | ✓ | ✓ |
| FLOOR | ✓ | Χ | Χ |
| FLOOR\_DIV | ✓ | Χ | Χ |
| FLOOR\_MOD | ✓ | Χ | Χ |
| FULLY\_CONNECTED | ✓ | ✓ | ✓ |
| GATHER | ✓ | ✓ | ✓ |
| GATHER\_ND | ✓ | ✓ | Χ |
| GREATER | ✓ | ✓ | Χ |
| GREATER\_EQUAL | ✓ | ✓ | Χ |
| HARD\_SWISH | ✓ | ✓ | Χ |
| IF | ✓ | ✓ | ✓ |
| L2\_NORMALIZATION | ✓ | ✓ | Χ |
| L2\_POOL\_2D | ✓ | Χ | Χ |
| LEAKY\_RELU | ✓ | ✓ | ✓ |
| LESS | ✓ | ✓ | Χ |
| LESS\_EQUAL | ✓ | ✓ | Χ |
| LOGISTIC (Sigmoid) | ✓ | ✓ | ✓ |
| LOG\_SOFTMAX | ✓ | ✓ | Χ |
| LSTM\_EVAL | ✓ | ✓ | ✓ |
| MAX\_POOL\_2D | ✓ | ✓ | ✓ |
| MAXIMUM | ✓ | ✓ | ✓ |
| MEAN | ✓ | ✓ | ✓ |
| MINIMUM | ✓ | ✓ | ✓ |
| MIRROR\_PAD | ✓ | ✓ | Χ |
| MUL | ✓ | ✓ | ✓ |
| NEG | ✓ | Χ | Χ |
| NOT\_EQUAL | ✓ | ✓ | Χ |
| PACK | ✓ | ✓ | Χ |
| PAD | ✓ | ✓ | ✓ |
| PRELU | ✓ | ✓ | Χ |
| QUANTIZE | ✓ | ✓ | ✓ |
| READ\_VARIABLE | ✓ | ✓ | ✓ |
| REDUCE\_MAX | ✓ | ✓ | ✓ |
| RELU | ✓ | ✓ | Χ |
| RELU6 | ✓ | ✓ | ✓ |
| RESHAPE | ✓ | ✓ | ✓ |
| RESIZE\_BILINEAR | ✓ | ✓ | Χ |
| RESIZE\_NEAREST\_NEIGHBOR | ✓ | ✓ | ✓ |
| ROUND | ✓ | Χ | Χ |
| RSQRT | ✓ | Χ | ✓ |
| SELECT | ✓ | ✓ | ✓ |
| SHAPE | ✓ | ✓ | ✓ |
| SLICE | ✓ | ✓ | ✓ |
| SOFTMAX | ✓ | ✓ | ✓ |
| SPACE\_TO\_BATCH\_ND | ✓ | ✓ | Χ |
| SPACE\_TO\_DEPTH | ✓ | ✓ | ✓ |
| SPLIT | ✓ | ✓ | ✓ |
| SPLIT\_V | ✓ | ✓ | ✓ |
| SQUARED\_DIFFERENCE | ✓ | ✓ | ✓ |
| SQUEEZE | ✓ | ✓ | ✓ |
| STRIDED\_SLICE | ✓ | ✓ | ✓ |
| SUB | ✓ | ✓ | ✓ |
| SUM | ✓ | ✓ | Χ |
| SVDF | ✓ | ✓ | Χ |
| TANH | ✓ | ✓ | ✓ |
| TRANSPOSE | ✓ | ✓ | ✓ |
| TRANSPOSE\_CONV | ✓ | ✓ | ✓ |
| UNIDIRECTIONAL\_SEQUENCE\_LSTM | ✓ | ✓ | ✓ |
| UNPACK | ✓ | ✓ | ✓ |
| VAR\_HANDLE | ✓ | ✓ | ✓ |
| WHILE | ✓ | ✓ | ✓ |
| ZEROS\_LIKE | ✓ | ✓ | Χ |
