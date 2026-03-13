---
source_url: "https://developer.imagimob.com/deepcraft-model-converter/additional-resources/supported-data-formats"
fetched_at: "2026-03-10T15:52:08Z"
title: "Supported Data Formats"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-model-converter", "additional-resources", "supported-data-formats"]
---

### Supported Data Formats

This section outlines the supported input data formats, structural requirements, and the expectations for data shapes and values.

#### General Expectations

- - **Numeric dtype**: Features and outputs are read as `float32`.
- - **Batching/Shape**: Features must match the expected input and output shapes, including the batch dimension.
- - **Headers**: CSV files may include an optional header row. If the first line contains letters (excluding the letter ‘e’ in scientific notation), the header is detected and skipped automatically.

#### Supported input types

- - NPZ file with arrays
- - CSV file(s)
- - Recursive folder and dictionary file (mix CSV samples and JPEG images)

#### NPZ (NumPy compressed)

A single `.npz` file can contain one or two arrays:

**Inputs**:

- - Preferred keys:`input`, `x`, `X`, `features`, or `arr_0`.
- - If none of the preferred keys are present, the first array is used as inputs.

**Outputs** (paired):

- - Preferred keys: `output`, `y`, `Y`, `labels`, or `arr_1`.
- - If none of the preferred keys are present, the second array is used if available.

Requirements:

- - Inputs are converted to `float32`
- - For paired data, outputs must be present and reshapeable to the specified output shape

#### CSV Inputs

CSV data can be provided in multiple layouts. All numeric values are read as `float32`. Each row represents a sample with flattened input data (optionally including flattened output data). All data are read as flattened arrays and reshaped to the target dimensions.

- - Optional header row is supported
- - Input columns: 0 to (input\_shape\_product - 1)
- - Output columns (if paired): from input\_shape\_product onwards.
- - Shape after load and reshape: `[num_samples, ...input_shape_dimensions]`.

**Example:**

**Two samples, three features:**

```
f0,f1,f2
0.1,0.2,0.3
0.4,0.5,0.6
```

**With embedded labels (two samples, three features, one prediction):**

```
f0,f1,f2,label
0.1,0.2,0.3,1.0
0.4,0.5,0.6,0.0
```

#### Recursive folder with dictionary

Use this option to combine CSV samples and JPEG images from a base folder, with per-sample outputs specified next to the paths. The dictionary must be a CSV-formatted file saved with the “.txt” extension, all paths to the sample files are relative to the dictionary file.

#### Base folder and allowed file types

- - Base: Root of the dataset folder tree
- - Allowed file types:
  * **CSV files**: Must represent a single sample per file (exactly one row)
  * **JPEG images**: Only `.jpeg` files are supported
- - Not supported: NPY and other image types (e.g., `.jpg`, `.png`)

#### Dictionary file format:

- - CSV-formatted text file use to enumerate samples and outputs.
- - Ignore empty lines and lines starting with `#`
- - Each non-empty and non-commented line:
  * First field: path relative to the base folder (no absolute paths; must not escape the base).
  * Remaining fields: numeric output values (if outputs are used).
- - The file is always parsed as comma-delimited with optional spaces after commas.

Examples:
**Input-only (no outputs):**

```
data/sample_01.csv
images/img_0001.jpeg
```

**Paired (outputs after the path):**

```
data/sample_02.csv, 0.0
images/img_0002.jpeg, 1.0, 0.2, 0.3
```

#### Sample constraints

- - **CSV entries**: Each referenced CSV file must contain exactly one row.
- - **JPEG entries**:
  * Images are resized to the target resolution and channel count:
    + If channels = 1, converted to grayscale; otherwise converted to RGB (3 channels)
  * Pixel values are normalized to [0, 1]
  * Shape of each image sample before batching: `[height, width, channels]`

#### Outputs in dictionary rows

- - If outputs are used, the values following the path must be numeric (floats).
- - For multi-dimensional outputs, provide flattened values in row-major order
- - Total count must match the product of the expected output shape

#### Shapes and Validation

- - **Feature shapes**:
  * Flattened CSV: `[N, flattened_input_size]` reshaped to `[N] + input_shape_dims`.
  * JPEG (folder with dictionary): `[N, H, W, C]`.
- - **Output shapes (paired)**: reference outputs must be reshapeable to `[N] + output_shape`.
- - **Dtypes**: All inputs and outputs are processed as `float32`.

#### Quick checklist

Quick checklist

- - **Headers in CSVs**: If a header is present, it is detected and skipped automatically.
- - **Single-row CSVs in dictionary mode**: CSV files referenced by the dictionary must contain exactly one row (one sample).
- - **JPEG-only for images**: Only `.jpeg` files are supported for images in recursive folder mode.
- - **Relative paths in dictionary**: Paths must be relative to the base folder and must not escape it (no `..` traversal and no absolute paths).
