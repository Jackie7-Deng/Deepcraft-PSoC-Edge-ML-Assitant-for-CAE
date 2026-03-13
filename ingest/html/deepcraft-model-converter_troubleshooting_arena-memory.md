---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/troubleshooting/arena-memory"
fetched_at: "2026-03-10T15:52:10Z"
title: "Arena Memory"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "troubleshooting", "arena-memory"]
---

# Arena Memory

### Insufficient model arena memory during deployment

The table lists the issue, the root cause, and the corresponding solution.

| **Issue** | **Description** |
| --- | --- |
| **Observation** | The model fails to initialize on the embedded device and crashes during initialization phase, typically with:   - Crash at `IMAI_init()` or similar initialization function  - The device resetting or hanging while loading the model |
| **Root Cause** | The default tensor arena size allocated for TFLite Micro may be insufficient for your model. The tensor arena is the working memory used by TFLite Micro for storing intermediate results of operations during inference.   If the arena size is too small, model initialization will fail. While the default size is usually sufficient, you can override the arena size with a higher value when needed. |
| **Solution** | Override the Arena Size in your DEEPCRAFT™ Model Converter project by modifying the **Override Arena Size** field. Increase in increments of 4096 bytes from the default calculated size. When you find a working value, decrease in steps of 1024 bytes or less to determine the minimum stable size that does not crash.   The calculated arena size can be found in the `code_generation_report.md` under the `Scratch memory` column in the `Memory Usage` section. |
