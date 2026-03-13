---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2"
fetched_at: "2026-03-10T15:51:19Z"
title: "Registering Sensors Using Protocolv2"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "tensor-streaming-protocol"]
---

# Registering Sensors Using Protocolv2

### Registering sensors and boards for data streaming using Protocol version 2

This topic provides a step-by-step instructions on how to register sensors and development boards using the Protocol version 2 (commonly referred to as **Tensor Streaming Protocol**).

Before we begin, let’s get familiar with the protocol repository and some commonly used terms to explain Protocol version 2. We will also look into a session example that describes how the client and a board communicate using this protocol. Refer to the [Tensor Streaming Protocol](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/) Bitbucket repository to know more about the underlying protocol and to access utilities to test and debug your implementation.

#### Protocol Repository Overview

Navigate to the Source folder, where you will find the following:

- - **DotNetCli**: CLI tool written in DotNet for testing the implementation
- - **example-firmware**: basic firmware example for streaming and configuring a dummy device
- - **protocol**: Protocol definition files and API helper
- - **python-example-client**: Example client written in python
- - **tcp-demo-server**: TCP demo implementation of the protocol

For more details, see [here](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/source/).

You do not need to understand the protocol implementation in order to register and stream data to/from boards or devices in DEEPCRAFT™ Studio. You will interact with the protocol through the protocol functions and callbacks as shown below. It is important to note that you should not modify the protocol or any files within the protocol folder. Modifications to the protocol folder should only be made by advanced users who wish to understand the implementation details of the protocol.

#### Understanding Terminology and Protocol Session

The following terms are commonly used:

- - **Board**: hardware platform/board containing one or more devices. The board acts like the server in the protocol.
- - **Device**: component on a board that can produce or consume data. For instance: sensors, playback devices, ML models.
- - **Client**: application that connects to a board via TCP, UDP, serial port, or Bluetooth to interact with devices, in this case DEEPCRAFT™ Studio is the client.
- - **Stream**: data channel that can either send data (Output) or receive data (Input). Streams are associated with devices.
- - **Frame**: unit of data sent periodically over a stream, in the form of a tensor.
- - **Tensor**: multidimensional array used to represent data. The number of dimensions are referred to as the tensors rank.
- - **Shape**: size of each dimension in a tensor. For example, [640, 480, 3] represents the shape of a 640x480 video frame with 3 colors (rgb).

##### Protocol Session Example

The following steps outline a typical session between a client (such as DEEPCRAFT™ Studio) and a board using Protocol version 2:

1. - **BoardCapabilitiesRequest**: client sends a `BoardCapabilitiesRequest` message to inquire about the device capabilities on the board.
2. - **BoardCapabilitiesResponse**: board responds with a `BoardCapabilitiesResponse` message detailing the available devices and their capabilities. If the response includes a `watchdog_timeout`, the client must periodically send `WatchdogResetRequest` messages to prevent the board from resetting.
3. - **WatchdogResetRequest**: resets the watchdog timer on the board. This request should be sent at intervals specified by `watchdog_timeout`.
4. - **DeviceConfigurationRequest**: configures the specified device with the desired options. This request prompts a `DeviceConfigurationResponse` from the board.
5. - **DeviceConfigurationResponse**: board responds with a `DeviceConfigurationResponse` message describing the configured data streams and their properties.
6. - **StartRequest**: client sends a `StartRequest` to initiate data streaming for the specified device.
7. - **DataChunk**: board streams data in `DataChunk` messages for each active subscription.

Before you follow this tutorial, make sure you select **Use Node Explorer with Protocol Version 2** option in **Tools> Options> Graph UX> Capture Nodes** in DEEPCRAFT™ Studio.

#### Using the protocol in your firmware to enable streaming with DEEPCRAFT Studio™

Below is an example of how to register a sensor on a development board using the protocol’s API, configure the streams and handle data using essential callback functions: **configure\_streams**, **start**, **stop**, and **poll**. We are demonstrating this using a dummy sensor driver that generates data on the fly. However, the same logic can be applied to add any sensor to the protocol.

Here is the [example-firmware](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/source/example-firmware/source/) you can refer for this tutorial. After going through this tutorial you will be able to discover, configure, and stream data from your board in DEEPCRAFT™ Studio as seen in the video below.

[iframe](https://player.vimeo.com/video/1103826742?badge=0&autopause=0&player_id=0&app_id=58479&loop=1&autoplay=1&autopause=0&muted=1)

#### Step 1: Creating a protocol instance

Here we create the protocol instance and pass in some information that can be shown by the client.

**Example Protocol Initialization and processing loop in main.c**

```
/* ...omitted some device specific includes... */
#include "protocol/protocol.h"
#include "usbd.h"
#include "build.h"
#include "clock.h"
#include "board.h"

#include "devices/protocol_example.h"

int main(void)
{
    /* ...omitted some device specific code... */
    /* start timer, later used by device driver. */
    clock_init()

    /* Specify a firmware version that will show up in Studio when connecting to this board (optional) */
    protocol_Version firmware_version = {
        .major = 1,
        .minor = 2,
        .build = BUILD_DATE,
        .revision = BUILD_TIME
    };

    /* Serial UUID to identify the board (optional) */
    uint8_t* serial = board_get_serial_uuid();

    /* Create a protocol instance */
    protocol_t* protocol = protocol_create("PSOC 6 AI (CY8CKIT-06S2-AI)", serial, firmware_version);

    /* Add reset function, which will allow Studio to reset the board through its UI */
    protocol->board_reset = board_reset;

    if (!dev_register(protocol))
    {
        printf("Sample registration failed.\n");
        while( true );
    }

    /* Initialize the streaming interface, could be serial over USB, a TCP socket, Bluetooth or any other interface, in our example this is serial over USB */
    usbd_t* usb = usbd_create(protocol);
    printf("Ready accepting commands.\r\n");

/*******************************************************************************
*   protocol_process_request() reads and processes a complete package.
*   While waiting for packages this function calls protocol_call_device_poll() that
*   in turn reads/writes to/from devices and writes packages.
*   This call happens in _usbd_read() in usbd.c.
*
*   In short, this for-loop iterates one step for each incoming package, and while
*   waiting for new packages, packages are continuously sent.
*******************************************************************************/
    for (;;)
    {
        protocol_process_request(protocol, &usb->istream, &usb->ostream);
    }

}
```

#### Step 2: Implement the Device Registration Function

This function initializes the device-specific data structure, sets up the device manager, registers the device with the protocol, adds integer option for scaling of the sensor output, a bool option for enabling/disabling the scaling and a oneof option for selecting different wave functions for the dummy sensor to generate. To make it easy, combine all steps into a single function that registers your device.

![](https://developer.imagimob.com/Images/temp-images/scrn2.png)

**Example Device Registration Function in protocol\_example.c**

```
#include "clock.h"
#include "protocol/protocol.h"
#include "protocol/pb_encode.h"
#include "protocol_example.h"
#include "data_generator.h"

#define OPTION_SCALE_VALUE          1 // ID for our scale int value
#define OPTION_SCALE                2 // ID for our bool scale flag
#define OPTION_WAVEFORM             3 // ID for our one-of option to set waveforms

// Typically you are using some struct to keep track of the device's internal state if needed.
typedef struct {
    bool running;
    int16_t buffer[80]; // Keep space for 80 samples in the local buffer.
    int stream_id;

    // Keep track of our options.
    int waveform;
    int scale;
    bool apply_scale;
} device_t;

device_t dev;

/* Protocol callbacks: These are mandatory functions. Since they are callback's their
names can be changed if desired. */
static bool _write_payload( protocol_t* protocol, int device_id, int stream_id, int frame_count,
                            int total_bytes, pb_ostream_t* ostream, void* arg);

static bool _configure_streams(protocol_t* protocol, int device_id, void* arg);
static void _start_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg);
static void _stop_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg);
static void _poll_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg);

/******************************************************************************
* Function Name: _init_hw
*******************************************************************************
* Summary:
*   Local helper function to initialize the hardware
*
* Parameters:
*   dev: Pointer to device handle.
*
* Return:
*   True if operation is successful, otherwise false.
*
* Note: This is only a placeholder for possible initialization of hardware.
*       It is up to the needs and requirements of the driver.
*******************************************************************************/
static bool _init_hw(device_t* dev)
{

    UNUSED(dev);
    bool fail = false;

    if (fail)
    {
        return false;
    }

    printf("Dummy device initialized.\n");
    return true;
}
```

#### Step 3: Define the configure_streams Callback Function

The configure\_streams callback is invoked every time a DeviceConfigurationRequest is received. This callback is responsible for configuring the data streams for the device, including setting the frequency, direction, data type, and tensor shape of the streaming data. After the callback is executed, a DeviceConfigurationResponse is sent.

**Example configure\_streams callback in protocol\_example.c**

```
/*******************************************************************************
* Function Name: _configure_streams
********************************************************************************
* Summary:
*   Called when the device is configured or re-configured by DEEPCRAFT Studio.
*
* Parameters:
*   protocol: Pointer the protocol handle
*   device: The device index
*   arg: Pointer the device struct.
*
* Return:
*   True to keep the connection open, otherwise false.
*
* Note:
*   This is called automatically when Studio first finds the device and
*   when the configuration is changed from within Studio. The protocol supports
*   several channels in the same stream as well as multidimensional data.
*
*******************************************************************************/
static bool _configure_streams(protocol_t* protocol, int device_id, void* arg)
{

    /*******************************************************************************
    **  A device can have multiple streams of data and each stream can have a
    **  multidimensional array of data. A typical example of having multiple
    **  streams is when you have multiple sensors in the same physical device -
    **  for example an IMU containing an accelerometer and a gyro.
    **
    **  This example only configures one stream with one dimensional data.
    *******************************************************************************/
    device_t* dev = (device_t*)arg;

    if (protocol_clear_streams(protocol, device_id) != PROTOCOL_STATUS_SUCCESS) {
        protocol_set_device_status(
                protocol,
                device_id,
                protocol_DeviceStatus_DEVICE_STATUS_ERROR,
                "Failed to clear streams.");
        return true;
    }

    /*******************************************************************************
    **  A stream is transmitting frames (samples) over the protocol grouped in chunks.
    **  Sending multiple frames together is a good way of reducing protocol overhead.
    **  In this example we decided to put 80 frames in each chunk.
    **  We also decided that our dummy driver will generate 8000 frames (samples) per second.
    **  For audio this would be equal of one audio channel (mono) sampled at 8000Hz.
    *******************************************************************************/
    int max_numer_of_frames_in_chunk = 80;

    int stream = protocol_add_stream(
        protocol,
        device_id,
        "Wave", // The name of the stream.
        protocol_StreamDirection_STREAM_DIRECTION_OUTPUT, // This device stream is outputting data (typical for a sensor)
        protocol_DataType_DATA_TYPE_S16,
        8000, // Number of frames per second (frequency).
        max_number_of_frames_in_chunk,
        "Samples"); // This is typically the physical unit or type of value being sent.

    if (stream < 0) {
        protocol_set_device_status(
                protocol,
                device_id,
                protocol_DeviceStatus_DEVICE_STATUS_ERROR,
                "Failed to add streams.");
        return true;
    }

    dev->stream_id = stream;

    /*******************************************************************************
    **  A stream can be thought of as a tensor or array with one or multiple dimensions.
    **  With each dimension we need to associate a name and a length. We can also pass in
    **  an optional array of string pointers to name each element index of the dimension.
    **
    **  A simple wave, as in our example, have a single dimension of length 1 (a scalar).
    **  Since it only has one dimension we call protocol_add_stream_rank once.
    **  We chose to name this dimension "Primary axis". Since it only has one index,
    **  we don't care to name it.
    *******************************************************************************/
    protocol_add_stream_rank(
        protocol,
        device_id,
        stream,
        "Primary axis",
        1,   // A length of 1 means that each data point is a scalar.
        NULL // Array of string pointers. Gives names to the different indexes. Or NULL if the indexes shouldn't be named.
    );

    protocol_set_device_status(
            protocol,
            device_id,
            protocol_DeviceStatus_DEVICE_STATUS_READY,
            "Device is ready.");

    printf("Stream is configured!\n");

    return true;
}
```

#### Step 4: Define start and stop callback functions

The start callback is invoked when a StartRequest is received, and this initializes and starts the device. The stop callback is invoked when a StopRequest is received, and this stops and de-initializes the device. These functions manage the device’s active state.

**Example start callback in protocol\_example.c**

```
/*******************************************************************************
* Function Name: _start_streams
********************************************************************************
* Summary:
*   Called by the protocol engine when streaming is started by Studio.
*   This might be a good place to also initialize the device.
*
* Parameters:
*   protocol: Pointer the protocol handle
*   device: The device index
*   ostream: Pointer to the output stream to write to
*   arg: Pointer the device struct.
*
*******************************************************************************/
static void _start_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg)
{
    int waveform;
    int scale;
    bool apply_scale;

    device_t* dev = (device_t*)arg;

    UNUSED(ostream);
    UNUSED(arg);

    /*******************************************************************************
    ** Here when starting the device, we read out the user options for the device.
    ** These options can be modified from the Studio UI. We store the latest options in
    ** our struct that holds our device related information.
    *******************************************************************************/
    protocol_get_option_oneof(protocol, device_id, OPTION_WAVEFORM, &waveform);
    protocol_get_option_bool(protocol, device_id, OPTION_SCALE, &apply_scale);
    protocol_get_option_int(protocol, device_id, OPTION_SCALE_VALUE, &scale);

    dev->waveform = waveform;
    dev->scale = scale;
    dev->apply_scale = apply_scale;

    /** Optionally have a device specific start function. **/
    bool result = _device_start(dev);

    if (!result)
    {
        protocol_set_device_status( protocol, device_id, protocol_DeviceStatus_DEVICE_STATUS_ERROR,
                                                         "Failed to start device.");
        printf("Starting the stream failed somehow!\n");
        return;
    }

    protocol_set_device_status(
            protocol,
            device_id,
            protocol_DeviceStatus_DEVICE_STATUS_ACTIVE,
            "Device is streaming");
}
```

**Example stop callback in protocol\_example.c**

```
/*******************************************************************************
* Function Name: _stop_streams
********************************************************************************
* Summary:
*  Called by the protocol engine when streaming is stopped by Studio.
*  This might be a good place to also stop/free up the device.
*
* Parameters:
*  protocol: Pointer the protocol handle
*  device_id: The device index
*  ostream: Pointer to the output stream to write to
*  arg: Pointer the device struct.
*
*******************************************************************************/
static void _stop_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg)
{

    device_t* dev = (device_t*)arg;
    UNUSED(ostream);

    /** Optionally have a device specific stop function. **/
    bool result = _device_stop(dev);

    if (!result)
    {
        protocol_set_device_status( protocol, device_id, protocol_DeviceStatus_DEVICE_STATUS_ERROR,
                                                         "Failed to stop the device.");
        printf("Stopping the stream failed somehow!\n");
        return;
    }

    protocol_set_device_status(
            protocol,
            device_id,
            protocol_DeviceStatus_DEVICE_STATUS_READY,
            "Device stopped");
}
```

#### Step 5: Define poll callback function

When the device is in the Active state, the poll callback is called periodically to check if there is data available and send it using the protocol\_send\_data\_chunk function. The protocol\_send\_data\_chunk function will send a DataChunk message.

**Example poll callback in protocol\_example.c**

```
/*******************************************************************************
* Function Name: _poll_streams
********************************************************************************
* Summary:
*  Called periodically to send data messages.
*
* Parameters:
*  protocol: Pointer the protocol handle
*  device: The device index
*  ostream: Pointer to the output stream to write to
*  arg: Pointer the device struct.
*
*******************************************************************************/
static void _poll_streams(protocol_t* protocol, int device_id, pb_ostream_t* ostream, void* arg)
{

/*******************************************************************************
**  This callback is called by the protocol engine for each registered and started device.
**  protocol_call_device_poll() in usbd.c triggers this call.
**
**  This will be the place where data is collected and passed on using the protocol.
**  How it is collected is not part of this example since it can vary a lot
**  between different devices. Some timer or flags may be needed to keep track
**  of data and data rate.
**
**  For simplicity we have moved out the actual gathering of data to an external
**  function. This returns a simple flag if data is available.
**  We pass on the settings we got from the options earlier as separate values.
*******************************************************************************/

    // Check if there is data available.
    device_t* dev = (device_t*)arg;
    bool have_data = fetch_dummy_driver_data( dev->waveform, dev->scale, dev->apply_scale, dev->buffer ); // see dummy_driver.c

    // If data is available, write the protocol header to the outstream.
    if (have_data) {
        protocol_send_data_chunk(
            protocol,
            device_id,
            dev->stream_id,  // Stream ID. See configure streams.
            80, // This chunk we are sending here will have 80 frames.
            0,  // Skipped frames, not used.
            ostream,
            _write_payload);    // How to write the actual payload.
    }
}
```

#### Step 6: Define the write payload callback

The mic\_write\_payload function is used by protocol\_send\_data\_chunk to write the actual data to the output stream.

**Example \_write\_payload function in protocol\_example.c**

```
/*******************************************************************************
* Function Name: _write_payload
********************************************************************************
* Summary:
*  Used by protocol_send_data_chunk to write the actual data.
*
* Parameters:
*  protocol: Pointer the protocol handle
*  device_id: The device index
*  stream_id: The stream index
*  frame_count: Number of frames to write
*  total_bytes: Total number of bytes to write (= frame_count * sizeof(type) * frame_shape.flat)
*  ostream: Pointer to the output stream to write to
*  arg: Pointer the device struct.
*
* Return:
*   True if data writing is successful, otherwise false.
*
* Note:
*   This is a callback called after the protocol header previous sent away from
*   above. It sends the raw data collected into our buffer.
*******************************************************************************/
static bool _write_payload(
    protocol_t* protocol,
    int device_id,
    int stream_id,
    int frame_count,
    int total_bytes,
    pb_ostream_t* ostream,
    void* arg)
{
    UNUSED(protocol);
    UNUSED(stream_id);
    UNUSED(frame_count);
    UNUSED(device_id);

    // Just send away the raw data with the actual number of bytes precalculated for us.
    device_t* dev = (device_t*)arg;
    if (!pb_write(ostream, (const pb_byte_t *)dev->buffer, total_bytes))
    {
        return false;
    }

    return true;
}
```

#### Step 7: Connect the protocol to your transport layer

In this example we use serial over USB as the transport layer. The protocol is agnostic to the transport layer, so you can communicate using other protocols such as TCP/IP (wired or WiFi) as well. DEEPCRAFT™ Studio supports communication over both serial and TCP/IP.

**Example usbd\_create function in usbd.c**

```
/* omitted device specific includes... */
#include "protocol/protocol.h"
#include "protocol/pb_encode.h"
#include "protocol/pb_decode.h"
#include "usbd.h"
/* omitted device specific structs... */

/*******************************************************************************
* Function Name: usbd_create
********************************************************************************
* Summary:
*   Creates and initializes a new streaming instance.
*   Note: This is called from main.c to connect the protocol with the transport layer.
*
* Parameters:
*   protocol: Pointer to the protocol handle.
*
* Return:
*   Pointer to the newly created streaming instance.
*
*******************************************************************************/
usbd_t* usbd_create(protocol_t *protocol)
{
    /* Board specific functions to setup serial over USB */
    usbd_t* usb = malloc(sizeof(usbd_t)); // See usbd.h

    if(usb == NULL)
    {
        return NULL;
    }

    usb->protocol = protocol; // attach the protocol instance to our usb handle so that we can access it in the read function below

    /* ...omitted device specific code... */

    /* Initializes the USB stack */
    USBD_Init();

    /* Endpoint Initialization for CDC class (specific to the PSOC&trade; USB stack) */
    usb->usb_cdcHandle = _usbd_add_cdc();

    /* Set device info used in enumeration (specific to the PSOC&trade; USB stack) */
    USBD_SetDeviceInfo(&usb->usb_deviceInfo);

    /* Start the USB stack */
    USBD_Start();

    /* Setup USB in/out streams */
    /* Important: This exports the streams for later use by the protocol! */
    /* A stream is just a read or write function. */
    usb->istream = (pb_istream_t){ &_usbd_read, (void*)usb, SIZE_MAX, 0 };
    usb->ostream = (pb_ostream_t){ &_usbd_write, (void*)usb, SIZE_MAX, 0, NULL };
    /* These are used in protocol_process_request(protocol, &usb->istream, &usb->ostream) in main.c */

    return usb;
}
```

#### Step 8: Poll devices through the protocol and transmit data over your transport layer

In this function we poll the sensor devices and transmit the output over the usb output stream.
We also show the usbd\_write function for completeness, although there is no protocol interaction in that function.

**Example \_usbd\_read function in usbd.c**

```
/*******************************************************************************
* Function Name: _usbd_read
********************************************************************************
* Summary:
*   Reads data from the serial interface into the provided buffer.
*   This is called by the protocol engine to receive commands.
*   It returns once 'count' number of bytes are read.
*   While it is waiting for data it calls protocol_call_device_poll().
*
* Parameters:
*   stream: Pointer to the input stream.
*   buf: Pointer to the buffer where the read data will be stored.
*   count: Number of bytes to read.
*
* Return:
*   True if reading is successful, otherwise false.
*
*******************************************************************************/
static bool _usbd_read(pb_istream_t* stream, pb_byte_t* buf, size_t count)
{
    if (count == 0)
    {
        return true;
    }

    usbd_t *usb = (usbd_t*)stream->state;

    /* Ask USB driver to write 'count' number of bytes in the background (this is non-blocking). */
    USBD_CDC_ReadOverlapped(usb->usb_cdcHandle, buf, count);

    /* While retrieving all the requested data, call protocol_call_device_poll(). */
    /* This is needed as we might be waiting here for a long time waiting for new packages from the client. */
    /* If we don't poll the devices here, we don't allow them to perform tasks and stream data.. */
    do {
        protocol_call_device_poll(usb->protocol, &usb->ostream);
    } while(USBD_CDC_GetNumBytesRemToRead(usb->usb_cdcHandle) > 0);

    return true;

}
```

**Example \_usbd\_write function in usbd.c**

```
/*******************************************************************************
* Function Name: _usbd_write
********************************************************************************
* Summary:
*   Writes data from the provided buffer to the serial interface.
*   This is called by the protocol engine as devices are generating data.
*   We don't have to do anything else than writing the buf over our
*   communication channel (USB in this case).
*
* Parameters:
*   stream: Pointer to the output stream.
*   buf: Pointer to the buffer containing the data to be written.
*   count: Number of bytes to write.
*
* Return:
*   True if writing is successful, otherwise false.
*
*******************************************************************************/
static bool _usbd_write(pb_ostream_t* stream, const pb_byte_t* buf, size_t count)
{
    usbd_t *usb = (usbd_t*)stream->state;

    USBD_CDC_Write(usb->usb_cdcHandle, buf, count, 0);

    /* Block until write is complete */
    USBD_CDC_WaitForTX(usb->usb_cdcHandle, 0);

    return true;
}
```

After implementing your own firmware, you can use the DotNetCli test client to evaluate your implementation. For instructions on how to use the test client, refer to [tensor-streaming-protocol](https://bitbucket.org/imagimob/tensor-streaming-protocol/src/master/).

Refer to [Flashing your custom firmware using ModusToolbox](https://developer.imagimob.com/getting-started/tensor-streaming-protocol/flashing-custom-firmware-using-modustoolbox) to know how to flash the custom firmware on your board using ModusToolbox™.

For flashing information on boards other than Infineon boards, refer to your specific board documentation.

After you have flashed your custom firmware onto the board, refer to [Real-time Data Collection](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards) to know how to stream real-time data into Studio.

When collecting data using a board flashed with **New Streaming Firmware/ Protocol version 2**, make sure you select **Use Node Explorer with Protocol Version 2** option in **Tools> Options> General**.
