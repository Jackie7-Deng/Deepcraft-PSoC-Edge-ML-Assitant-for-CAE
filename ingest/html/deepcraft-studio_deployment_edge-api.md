---
source_url: "https://developer.imagimob.com/deepcraft-studio/deployment/edge-api"
fetched_at: "2026-03-10T15:51:52Z"
title: "Edge API"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "deployment", "edge-api"]
---

### Edge API

When you click the **Generate Code** button to generate the code in Studio, your AI model is converted into a self contained C (model.c) file and Header (model.h) file. This section specifies the API for interacting with the Edge model.

The following code snippets are sourced from the header (model.h) file, which is created during the code generation process.

#### Adding Defines

Add the compatibility parameters so that the code works regardless of the selected deployment target in DEEPCRAFT™ Studio.

```
// Imagimob compatibility defines to support all versions of code generation APIs

#ifndef IPWIN_RET_SUCCESS
#define IPWIN_RET_SUCCESS (0)
#endif

#ifndef IPWIN_RET_NODATA
#define IPWIN_RET_NODATA (-1)
#endif

#ifndef IPWIN_RET_ERROR
#define IPWIN_RET_ERROR (-2)
#endif

#ifndef IMAI_DATA_OUT_SYMBOLS
#define IMAI_DATA_OUT_SYMBOLS IMAI_SYMBOL_MAP
#endif
```

#### Initialize the model

Before calling any other functions, initialize the model using IMAI\_Init(). This function returns 0 upon successful initialization and a non-zero value if an error occurs.

```
// Initialize the model before calling any other functions.
int IMAI_Init();
```

#### Input data into the model

See IMAI\_Compute() and IMAI\_Enqueue() definitions below.

#### Get output from the model

See IMAI\_Compute() and IMAI\_Dequeue() definitions below.

If the Queue API is used, IMAI\_Dequeue() should be called right after every call to IMAI\_Enqueue()

#### Additional information

The API generated depends on the preprocessing functions and the timestamp API.

|  | Requested API *with* Timestamps | Requested API *without* Timestamps |
| --- | --- | --- |
| **Zero Queue layers exist** | Function API | Function API |
| **One or more queue layers exist** | Queue API | Queue No Time API |

##### Queue API

```
/**
* @brief Queue API for enqueuing and dequeuing data to and from the model.
*/
#ifdef IMAI_API_QUEUE

/**
* @brief Enqueues input data and timestamp into the model.
*
* @param data_in Pointer to an input sample array with IMAI_DATA_IN_COUNT elements.
* @param time_in Pointer to a timestamp of length 1, expressed in seconds.
* @return
* - IMAI_RET_SUCCESS (0) : Success.
* - IMAI_RET_ERROR (-2)  : Error enqueuing data. Dequeue first.
*/
int IMAI_enqueue(const float* data_in, const float* time_in);

/**
* @brief Dequeues output predictions from the model.
*
* @param data_out Pointer to an array to store model output, with IMAI_DATA_OUT_COUNT elements.
* @param time_out Pointer to an array with two timestamps (start and end) of the input that generated the output.
* @return
* - IMAI_RET_SUCCESS (0) : Success.
* - IMAI_RET_NODATA (-1) : No data available.
* - IMAI_RET_ERROR (-2)  : Error retrieving data.
*/
int IMAI_dequeue(float* data_out, float* time_out);

#endif /* IMAI_API_QUEUE */
```

##### Queue No Time API

```
/**
* @brief Queue No Time API for enqueuing and dequeuing data to/from the model without timestamps.
*/
#ifdef IMAI_API_QUEUE_NO_TIMESTAMPS

/**
* @brief Enqueues input data into the model.
*
* @param data_in Pointer to an input sample array with IMAI_DATA_IN_COUNT elements.
* @return
* - IMAI_RET_SUCCESS (0) : Success.
* - IMAI_RET_ERROR (-2)  : Error enqueuing data. Dequeue first.
*/
int IMAI_enqueue(const float* data_in);

/**
* @brief Dequeues output predictions from the model.
*
* @param data_out Pointer to an array to store model output, with IMAI_DATA_OUT_COUNT elements.
* @return
* - IMAI_RET_SUCCESS (0) : Success.
* - IMAI_RET_NODATA (-1) : No data available.
* - IMAI_RET_ERROR (-2)  : Error retrieving data.
*/
int IMAI_dequeue(float* data_out);

#endif /* IMAI_API_QUEUE_NO_TIMESTAMPS */
```

##### Queue API Return Codes

When utilizing the Queue API, either with or without the time feature, it is crucial to always consider the return codes. The possible return codes are outlined below:

```
#define IMAI_RET_SUCCESS 0    // Operation was successful.
#define IMAI_RET_NODATA -1    // No data is available.
#define IMAI_RET_ERROR -2     // Error.
```

`int IMAI_enqueue(...)`
This function is responsible for pushing data into the model.
**Return Values:**

- - `IMAI_RET_SUCCESS` (0): Data was successfully pushed to the model.
- - `IMAI_RET_ERROR` (-2): There was an error and data could not be enqueued.

`int IMAI_dequeue(...)`
This function retrieves data from the model. On successful retrieval, data will be written to the provided pointers.
**Return Values:**

- - `IMAI_RET_SUCCESS` (0): Data was successfully retrieved from the model.
- - `IMAI_RET_NODATA` (-1): No data is currently available. Ensure you have pushed input data using `IMAI_enqueue()` before trying to dequeue.
- - `IMAI_RET_ERROR` (-2): An error occurred.

##### Function API

```
/**
* @brief Function API for computing model predictions directly from input data.
*/

#ifdef IMAI_API_FUNCTION

/**
* @brief Computes model predictions directly from input data.
*
* This function processes the input data and produces the corresponding model output.
*
* @param data_in Pointer to an input sample array with IMAI_DATA_IN_COUNT elements.
* @param data_out Pointer to an array to store the model output, with IMAI_DATA_OUT_COUNT elements.
*/
void IMAI_compute(const float* data_in, float* data_out);

#endif /* IMAI_API_FUNCTION */
```

#### Deallocating resources

In instances, where IMAI\_init() has allocated dynamic resources, these resources can be released using the IMAI\_finalize() function.

```
// Deallocate resources
void IMAI_finalize();
```

This function is only defined when generating code for PSoC targets or through Graph UX code generation.
