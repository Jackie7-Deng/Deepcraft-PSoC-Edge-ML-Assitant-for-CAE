---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/other-boards"
fetched_at: "2026-03-10T15:51:18Z"
title: "Other Boards"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "other-boards"]
---

# Other Boards

### Other Development Boards

You can use any sensor or development board as a rapid prototyping platform for machine learning applications. DEEPCRAFT™ Studio delivers an end-to-end workflow from real-time data collection and code generation to on-device deployment—across a wide range of hardware, enabling rapid iteration and a streamlined path from concept to embedded inference.

- - **Data collection**: Stream real‑time data from any sensor or board using the [Streaming Protocol for Real‑Time Data Collection](https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol). Using the Protocol, implement the firmware for your development board that stream data adhering to the required specifications, eliminating the need for data formatting. Refer to
  [Registering sensors and boards for data streaming using Protocol version 2](https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2) for detailed instructions on firmware implementation.

  Refer to [Data collection using other development Boards](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-other-boards) for collecting real-time data and your specific board documentation, for flashing boards with the implemented firmware.

**Protocol version 1** is deprecated and we recommend using **Protocol version 2** for implementing your firmware for improved performance and easy implementation.

- - **Code generation**: After training and evaluating your model, generate the code using the ANSI C99 suitable for any platform. To know how to generate the code, refer to [Code Generation for Other Development Boards](https://developer.imagimob.com/deepcraft-studio/code-generation/code-gen-aurix-other-dev-boards) and [Code Generation using Graph UX](https://developer.imagimob.com/deepcraft-studio/code-generation/code-generation-using-graph-ux).
- - **Deployment**: Deploy the model to your development board using the APIs. To know how to deploy the model onto any development board, refer to [Model Deployment on Other Development Boards](https://developer.imagimob.com/deepcraft-studio/deployment/deploy-models-other-boards) and [Edge API](https://developer.imagimob.com/deepcraft-studio/deployment/edge-api).
