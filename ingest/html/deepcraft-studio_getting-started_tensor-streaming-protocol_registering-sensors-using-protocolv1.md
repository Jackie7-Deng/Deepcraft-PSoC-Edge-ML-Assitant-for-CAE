---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv1"
fetched_at: "2026-03-10T15:51:20Z"
title: "Registering Sensors Using Protocolv1"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "tensor-streaming-protocol"]
---

# Registering Sensors Using Protocolv1

### Registering sensors and boards for data streaming using Protocol version 1

**Protocol version 1** is deprecated and we recommend using **Protocol version 2** for implementing your firmware for improved performance and easy implementation. However, we continue to support the backward compatibility. This means that if your firmware is currently implemented using Protocol version 1, you will still be able to stream data into Studio without any issues. Refer to the [Protocol version 2](https://developer.imagimob.com/deepcraft-studio/getting-started/tensor-streaming-protocol/registering-sensors-using-protocolv2) to know more about the protocol.

This topic provides a brief overview of how to register sensors and development boards using the [Protocol version 1](https://github.com/Infineon/mtb-example-imagimob-streaming-protocol/blob/master/PROTOCOL.md). The following sample files outline the necessary functions for registering new sensors:

- - [simple\_protocol.c](https://developer.imagimob.com/Resources/simple_protocol.c): This file includes the steps for defining the sensor configuration, initializing the protocol, and implementing the streaming protocol.
- - [simple\_main.c](https://developer.imagimob.com/Resources/simple_main.c): This file contains the main function.

Refer to the [Protocol version 1](https://github.com/Infineon/mtb-example-imagimob-streaming-protocol/tree/master) Bitbucket repository to know more about the protocol.

#### Step 1: Include the header files

Include all the header files as declared in simple\_protocol.c.

**Example including header files**

```
#include <stdio.h>
#include "clock.h"
#include "config.h"
#include "protocol.h"
```

#### Step 2: Define sensor configuration

**Example for defining microphone and accelerometer**

```
static const char* CONFIG_MESSAGE =
        "{\r\n"
		"    \"device_name\": \"PSoC6\",\r\n"
		"    \"protocol_version\": 1,\r\n"
		"    \"heartbeat_timeout\": 5,\r\n"
		"    \"sensors\": [\r\n"
		"        {\r\n"
		"            \"channel\": 1,\r\n"
		"            \"type\": \"microphone\",\r\n"
		"            \"datatype\": \"s16\",\r\n"
		"            \"shape\": \[ 1024, 1 ],\r\n"
		"            \"rates\": [ 16000 ]\r\n"
		"        },\r\n"
		"        {\r\n"
		"            \"channel\": 2,\r\n"
		"            \"type\": \"accelerometer\",\r\n"
		"            \"datatype\": \"f32\",\r\n"
		"            \"shape\": \[ 1, 3 ],\r\n"
		"            \"rates\": [ 50,500 ]\r\n"
		"        }\r\n"
		"    ]\r\n"
		"}\r\n\0";"
```

The second step is to define the sensor configuration in the protocol. Begin by defining the following parameters:

- - **device name**: Write the name of the device name for easy identification. For instance, PSoC6.
- - **heartbeat timeout**: Set the duration in seconds after which the sensor stops data transmission data if no heartbeat is received.
- - **channel**: Set one or more channels for handling the incoming sensor data. Each sensor must be assigned a unique channel. You can set channel number from 1 to 9 for each sensor type. For instance, the device will receive audio data at channnel 1 and accelerometer data at channel 2.
- - **sensor type**: Write the name of the sensors in lowercase letters.
- - **data type**: Set the data type as “u8” “s8”, “u16”, “s16”, “u32”, “s32”, “f32”, “f64”. All multi byte types are sent little endian.
- - **shape**: Set the format in which sensor data is transmitted to the device. For instance, the shape for microphone is set as [1024, 1], where 1024 indicates the amount of data sent in one packet, and 2 represents the stereo channel. Similarly, the shape for accelerometer is set to [1, 3], where 1 means one packet is sent at a time, and 3 corresponds to the X, Y, and Z axis.
- - **rate**: Set the range of valid sampling rates for data collection in Hz. For instance, the rate for microphone is set to [16000], indicating a sampling frequency of 16000 Hz for microphone data. For the accelerometer, the rate is set to [50, 500], meaning data can be collected at either 50 Hz or 500 Hz.

#### Step 3: Initializing the protocol

This function initializes the protocol and should be called once before using any other functions in this file. In the code snippet, the `clock_init()` function is called to initialize a clock used for sampling, this function is defined in clock.h.

**Example Initializing the protocol function**

```
void protocol_init()
{
	clock_init()
}
```

#### Step 4: Define protocol_repl Function

This function processes incoming characters, executes commands, and sends response messages within a read-eval-print loop. The function may block execution until the response transmission is complete.

**Example protocol\_repl**

```
 void protocol_repl()
{
	/* Update clock */
	clock_update();

	/* Test clock */
	/* Uncomment if desired!
	static uint32_t last_t = 0;
	if (clock_get_ms() > last_t + 1000)
	{
		static char buffer[20];
		sprintf(buffer, "%lu\r\n", clock_get_ms());
		streaming_send(buffer, strlen(buffer));
		last_t += 1000;
	}
	*/

	/* Read and handle data if any bytes are available */
	size_t bytes_read = streaming_receive(receive_p, RECEIVE_BUFFER_SIZE - (receive_p - receive_buffer));
    if (bytes_read)
    {
    	/* Register receive time */
    	last_receive_time = clock_get_ms();

    	/* Echo incoming characters when not streaming data */
    	/* Uncomment if desired!
    	if (!subscribe_audio && !subscribe_imu)
    		streaming_send(receive_p, bytes_read);
    	*/

    	/* Advance receive pointer */
    	receive_p += bytes_read;

    	/* Check for \r\n at end */
    	if (receive_p >= receive_buffer + 2 && *(receive_p - 2) == '\r' && *(receive_p - 1) == '\n')
    	{
    		/* Remove \r\n */
            *(receive_p - 2) = 0;

            /* config? */
            if (strcmp(receive_buffer, "config?") == 0)
            {
            	subscribe_audio = subscribe_imu = false;
            	streaming_send(CONFIG_MESSAGE, strlen(CONFIG_MESSAGE));
            }
            /* subscribe,1,16000 */
            else if (strcmp(receive_buffer, "subscribe,1,16000") == 0)
            {
            	subscribe_audio = true;
            }
            /* unsubscribe,1 */
            else if (strcmp(receive_buffer, "unsubscribe,1") == 0)
            {
            	subscribe_audio = false;
            	streaming_send(OK_MESSAGE, strlen(OK_MESSAGE));
            }
            /* subscribe,2,50 */
            else if (strcmp(receive_buffer, "subscribe,2,50") == 0)
            {
            	subscribe_imu = true;
            }
            /* unsubscribe,2 */
            else if (strcmp(receive_buffer, "unsubscribe,2") == 0)
            {
            	subscribe_imu = false;
            	streaming_send(OK_MESSAGE, strlen(OK_MESSAGE));
            }
            /* unsubscribe */
            else if (strcmp(receive_buffer, "unsubscribe") == 0)
            {
            	subscribe_audio = subscribe_imu = false;
            	streaming_send(OK_MESSAGE, strlen(OK_MESSAGE));
            }
            /* empty command or heartbeat */
            else if (*receive_buffer == 0 || strcmp(receive_buffer, "heartbeat") == 0)
            {
            	/* Nothing to do except register receive time, which was done above */
            }
            else
            {
            	streaming_send(UNRECOGNIZED_COMMAND_MESSAGE, strlen(UNRECOGNIZED_COMMAND_MESSAGE));
            }

            /* Reset receive pointer; ready for new command */
    		receive_p = receive_buffer;
    	}

    	/* Check end of buffer */
    	if (receive_p == receive_buffer + RECEIVE_BUFFER_SIZE)
    	{
    		streaming_send(TOO_LONG_COMMAND_MESSAGE, strlen(TOO_LONG_COMMAND_MESSAGE));
    		receive_p = receive_buffer;
    	}
    }

    /* Check receive timeout: If no message for 5 seconds, stop streaming */
    if ((subscribe_audio || subscribe_imu) && clock_get_ms() - last_receive_time > HEARTBEAT_TIMEOUT_MS)
    {
    	subscribe_audio = subscribe_imu = false;
    }
}
```

#### Step 5: Define protocol_send Function

This function transmits a packet of data from the sensor to Studio. The function may block execution until the transmission is complete.

**Parameters used in this function:**

- - **channel**: Specifies the channel through which the packet will be sent
- - **data**: Pointer to the data to be transmitted
- - **size**: Number of bytes to be transmitted

**Example Define protocol\_send Function**

```
void protocol_send(uint8_t channel, const uint8_t* data, size_t size)
{
	uint8_t header[2] = { 'B', '0' + channel };
    switch (channel)
    {
    case PROTOCOL_AUDIO_CHANNEL:
    	if (subscribe_audio)
    	{
    		streaming_send(header, 2);
    	    streaming_send(data, size);
    	    streaming_send(CRLF, 2);
    	}
    	break;
    case PROTOCOL_IMU_CHANNEL:
    	if (subscribe_imu)
    	{
    		streaming_send(header, 2);
    	    streaming_send(data, size);
    	    streaming_send(CRLF, 2);
    	}
    }
}
```

Refer to [Flashing your custom firmware using ModusToolbox](https://developer.imagimob.com/getting-started/tensor-streaming-protocol/flashing-custom-firmware-using-modustoolbox) to know how to flash the custom firmware on your Infineon board using ModusToolbox™.

- - For flashing information on boards other than Infineon boards, refer to your specific board documentation.

After you have flashed your custom firmware onto the board, refer to [Real-Time Data Collection with PSoC™ 6 AI Evaluation Kit using old streaming firmware](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/data-collection-using-old-streaming-firmware) or [Real-Time Data Collection from Sensors using old streaming firmware/protocol](https://developer.imagimob.com/deepcraft-studio/data-preparation/data-collection/collect-data-infineon-boards/collect-data-using-graph-ux) to know how to stream real-time data into Studio.

When collecting data using a board flashed with **Old Streaming Firmware/ Protocol version 1**, make sure you select **Serial Capture Nodes with Protocol Version 1** option in **Tools> Options> General**.
