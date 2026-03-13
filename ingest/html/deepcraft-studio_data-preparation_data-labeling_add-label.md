---
source_url: "https://developer.imagimob.com/deepcraft-studio/data-preparation/data-labeling/add-label"
fetched_at: "2026-03-10T15:51:40Z"
title: "Add Label"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "data-preparation", "data-labeling"]
---

# Add Label

### Sequential Labeling

DEEPCRAFT™ Studio also offers a feature to add labels to the data sequentially. After you add data to the project, a session file and an empty label file are automatically created for each data file in the data directory. The session file then displays the data file and label file as the data track and label track, respectively.

To add labels sequential, follow the steps:

1. - Double-click the session file (.imsession) in which you want to add labels from the session table in the project file.

  ![session-file](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsession-terminal.b8c8c656.png&w=3840&q=75)

  The session file opens in a new tab.
2. - Locate the label track in the session file.

  ![session-file](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Flabel-track.12516d72.png&w=1920&q=75)

You can use video as visual reference for labeling the time series data.

1. - Zoom-in or zoom-out until you see the entire event and navigate to the part you want to label.

  ![select-region](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fregion-select.f6628535.png&w=1920&q=75)
2. - Move the cursor to the label track region, right-click and select **New Label** from the list of options.

  ![label-region](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fregion-label.f20b3d15.png&w=1920&q=75)

  The Add New Label window appears.

  ![add-label](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fadd-new-label.63367d80.png&w=828&q=75)
3. - Configure the following parameters:

  * In **Track**, select the label track in which you want to add the labels.
  * In **Label**, enter the name of the label you want to add for that specific data part in the track.
  * In **Begin**, set the timestamp from where you want to start the label.
  * In **Duration**, set the timestamp at which you want to end the label.
  * In **Confident**, enter the confidence percentage for your label.
  * In **Comment**, enter the comment, if required.
  * Click **OK**. A label is added in the track.

  ![up-label](https://developer.imagimob.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Frun-label.7693d03a.png&w=1200&q=75)
