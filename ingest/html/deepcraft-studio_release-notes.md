---
source_url: "https://developer.imagimob.com/deepcraft-studio/release-notes"
fetched_at: "2026-03-10T15:51:10Z"
title: "Release Notes"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "release-notes"]
---

# Release Notes

### Release Notes 5.9

This section lists the new functionality, improvements and some of the major changes related to DEEPCRAFT™ Studio.

#### New Features and Enhancements

#### Improving timeline performance when recording many features or using high sample rate

When streaming data from sensors or development kits into DEEPCRAFT™ Studio, the timeline may become slow or laggy if one or more tracks contain many features and/or use a high sample rate. To improve timeline performance during recording, hide the affected track by clicking the **eye** icon next to the track name. Hiding a track disables timeline plotting for that track but continues streaming and recording data in the background. Click the **eye** icon again to unhide the track and view the plotted data after you stop recording. This workaround is especially useful when streaming high-rate data, such as radar data.

[iframe](https://player.vimeo.com/video/1165983071?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

#### Search and add nodes onto the canvas from Node Explorer

You can now search the nodes directly in the **Node Explorer**. In addition to searching nodes on the canvas, use the Node Explorer search box to find a node, then drag and drop the node from the search results onto the canvas.

![](https://developer.imagimob.com/Images/release-notes/pic-1.png)

#### Train your object detection models using YOLOv8n architecture

Train object detection models on custom data in the DEEPCRAFT™ Studio using the lightweight and efficient Ultralytics YOLOv8n architecture. YOLOv8n uses architectural improvements such as an anchor-free detection head and provides a strong balance between speed and accuracy, making it suitable for a wide range of deployment scenarios. For step-by-step instructions on training an object detection model with YOLOv8, refer to [Training Object Detection Model](https://developer.imagimob.com/deepcraft-studio/model-training/training-object-detection).

![](https://developer.imagimob.com/Images/release-notes/pic-2.png)

#### Fixes

Overall bug fixes and increased stability.
