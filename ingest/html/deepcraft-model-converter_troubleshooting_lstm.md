---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/troubleshooting/lstm"
fetched_at: "2026-03-10T15:52:10Z"
title: "Lstm"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "troubleshooting", "lstm"]
---

# Lstm

### Degraded LSTM Model Performance

The table lists the issue, the root cause, and the corresponding workaround.

| **Issue** | **Description** |
| --- | --- |
| **Observation** | The .h5 model contains LSTM layers and shows significant performance degradation in both FLOAT32 and INT8x8 formats after conversion. In the Code Generation Report, for a pure classification model this typically appears as:  **Classification Metrics** (All results are relative to the original model) Argmax Errors: 2418/10000 samples  Argmax Similarity: 75.82%   **Key Indicators**:  - Argmax Similarity < 85% for classification models   - Performance degradation in both FLOAT32 and INT8x8, an issue beyond quantization  - Model contains LSTM or bidirectional LSTM layers  - For regression models, look for degradation in relevant metrics other than Argmax Similarity |
| **Root Cause** | LSTM layers in Keras models have `unroll=True` set for optimal TFLite Micro deployment. Without this setting, the recurrent operations may not convert correctly to TFLite Micro’s expected format, resulting in poor inference performance. We are investigating a proper fix for `unroll=False`, in the meantime we offer a workaround. |
| **Solution** | Use the provided python script to rebuild the model while allowing unrolling of the LSTM layers and transferring the weights. A README.md with instructions is provided with the script. Download the script **[here](https://developer.imagimob.com/Resources/lstm_unroller.zip)**. |

If code generated for a modified LSTM model crashes during device initialization, see [Insufficient model arena memory during deployment](https://developer.imagimob.com/deepcraft-model-converter/troubleshooting/arena-memory).
