/*
* ImagiNet Compiler 5.8.4292+50129d917517243fc033cba30ce355705c84a08c
* Copyright © 2023- Imagimob AB, All Rights Reserved.
* 
* Generated at 03/09/2026 06:09:09 UTC. Any changes will be lost.
* 
* Model ID  696b81b5-1679-4604-ae47-013a820ff189
* 
* Memory    Size                      Efficiency
* Buffers   300 bytes (RAM)           100 %
* State     16912 bytes (RAM)         100 %
* Readonly  38592 bytes (Flash)       100 %
* 
* Exported functions:
* 
*  @description: Try read data from model.
*  @param data_out Output features. Output float[2].
*  @return IPWIN_RET_SUCCESS (0) or IPWIN_RET_NODATA (-1), IPWIN_RET_ERROR (-2), IPWIN_RET_STREAMEND (-3)
*  int IMAI_IMU_dequeue(float *data_out);
* 
*  @description: Try write data to model.
*  @param data_in Input features. Input float[3].
*  @return IPWIN_RET_SUCCESS (0) or IPWIN_RET_NODATA (-1), IPWIN_RET_ERROR (-2), IPWIN_RET_STREAMEND (-3)
*  int IMAI_IMU_enqueue(const float *data_in);
* 
*  @description: Closes and flushes streams, free any heap allocated memory.
*  void IMAI_IMU_finalize(void);
* 
*  @description: Initializes buffers to initial state.
*  @return IPWIN_RET_SUCCESS (0) or IPWIN_RET_NODATA (-1), IPWIN_RET_ERROR (-2), IPWIN_RET_STREAMEND (-3)
*  int IMAI_IMU_init(void);
* 
* 
* Disclaimer:
*   The generated code relies on the optimizations done by the C compiler.
*   For example many for-loops of length 1 must be removed by the optimizer.
*   This can only be done if the functions are inlined and simplified.
*   Check disassembly if unsure.
*   tl;dr Compile using gcc with -O3 or -Ofast
* 
* Notes:
* 	-> This code was generated with DEEPCRAFT Studio using:
* 		ml-coretools 3.0.1.9035.
* 		tensorflow 2.19.0.
* 	-> This code requires the following Modus Toolbox libraries (add them to your
* 	project using the Library Manager):
* 		ml-middleware 3.0.1.
* 		ml-tflite-micro 3.0.1.
*/

#include <stdbool.h>
#include <stdint.h>
#include "mtb_ml_model.h"
#define IMAI_IMU_API_QUEUE

typedef int8_t q7_t;         // 8-bit fractional data type in Q1.7 format.
typedef int16_t q15_t;       // 16-bit fractional data type in Q1.15 format.
typedef int32_t q31_t;       // 32-bit fractional data type in Q1.31 format.
typedef int64_t q63_t;       // 64-bit fractional data type in Q1.63 format.

// Model GUID (16 bytes)
#define IMAI_IMU_MODEL_ID {0xb5, 0x81, 0x6b, 0x69, 0x79, 0x16, 0x04, 0x46, 0xae, 0x47, 0x01, 0x3a, 0x82, 0x0f, 0xf1, 0x89}


// First nibble is bit encoding, second nibble is number of bytes
#define IMAGINET_TYPES_NONE	(0x0)
#define IMAGINET_TYPES_FLOAT32	(0x14)
#define IMAGINET_TYPES_FLOAT64	(0x18)
#define IMAGINET_TYPES_INT8	(0x21)
#define IMAGINET_TYPES_INT16	(0x22)
#define IMAGINET_TYPES_INT32	(0x24)
#define IMAGINET_TYPES_INT64	(0x28)
#define IMAGINET_TYPES_Q7	(0x31)
#define IMAGINET_TYPES_Q15	(0x32)
#define IMAGINET_TYPES_Q31	(0x34)
#define IMAGINET_TYPES_BOOL	(0x41)
#define IMAGINET_TYPES_STRING	(0x54)
#define IMAGINET_TYPES_D8	(0x61)
#define IMAGINET_TYPES_D16	(0x62)
#define IMAGINET_TYPES_D32	(0x64)
#define IMAGINET_TYPES_UINT8	(0x71)
#define IMAGINET_TYPES_UINT16	(0x72)
#define IMAGINET_TYPES_UINT32	(0x74)
#define IMAGINET_TYPES_UINT64	(0x78)

// data_out [2] (8 bytes)
#define IMAI_IMU_DATA_OUT_RANK (1)
#define IMAI_IMU_DATA_OUT_SHAPE (((int[]){2})
#define IMAI_IMU_DATA_OUT_COUNT (2)
#define IMAI_IMU_DATA_OUT_TYPE float
#define IMAI_IMU_DATA_OUT_TYPE_ID IMAGINET_TYPES_FLOAT32
#define IMAI_IMU_DATA_OUT_SHIFT 0
#define IMAI_IMU_DATA_OUT_OFFSET 0
#define IMAI_IMU_DATA_OUT_SCALE 0
#define IMAI_IMU_DATA_OUT_SYMBOLS {"unlabelled", "anomaly"}

// data_in [3] (12 bytes)
#define IMAI_IMU_DATA_IN_RANK (1)
#define IMAI_IMU_DATA_IN_SHAPE (((int[]){3})
#define IMAI_IMU_DATA_IN_COUNT (3)
#define IMAI_IMU_DATA_IN_TYPE float
#define IMAI_IMU_DATA_IN_TYPE_ID IMAGINET_TYPES_FLOAT32
#define IMAI_IMU_DATA_IN_SHIFT 0
#define IMAI_IMU_DATA_IN_OFFSET 0
#define IMAI_IMU_DATA_IN_SCALE 1
#define IMAI_IMU_DATA_IN_SYMBOLS { }

#define IMAI_IMU_KEY_MAX (7)

// Return codes
#define IMAI_IMU_RET_SUCCESS 0
#define IMAI_IMU_RET_NODATA -1
#define IMAI_IMU_RET_ERROR -2
#define IMAI_IMU_RET_STREAMEND -3

#define IPWIN_RET_SUCCESS 0
#define IPWIN_RET_NODATA -1
#define IPWIN_RET_ERROR -2
#define IPWIN_RET_STREAMEND -3

// Exported methods
int IMAI_IMU_dequeue(float *restrict data_out);
int IMAI_IMU_enqueue(const float *restrict data_in);
void IMAI_IMU_finalize(void);
int IMAI_IMU_init(void);

// Implement this method to perform profiling	
void IMAI_IMU_hook_region(bool entered, int32_t region_id);

// Symbol IMAI_IMU_PROFILING must be defined to enable profiling of models
void IMAI_IMU_mtb_models_profile_log();
void IMAI_IMU_mtb_models_print_info();
#define IMAI_IMU_MAX_MTB_MODELS 4
extern int32_t IMAI_IMU_mtb_models_count;
extern mtb_ml_model_t* IMAI_IMU_mtb_models[IMAI_IMU_MAX_MTB_MODELS];

// Profiling regions
#ifdef IMAI_IMU_PROFILING
    #define IMAI_IMU_REGIONS_COUNT 2
    #define IMAI_IMU_REGIONS_NAMES {\
    	"PREPROCESSOR",\
    	"NETWORK",\
    }
    typedef enum {
    	IMAI_IMU_PREPROCESSOR = 0,
    	IMAI_IMU_NETWORK = 1,
    } IMAI_IMU_Region_t;
#else
    #define IMAI_IMU_REGIONS_COUNT 0
    #define IMAI_IMU_REGIONS_NAMES {}
    typedef enum {IMAI_IMU_REGIONS_EMPTY} IMAI_IMU_Region_t;
#endif

typedef enum {
    IMAI_IMU_PARAM_UNDEFINED = 0,
    IMAI_IMU_PARAM_INPUT = 1,
    IMAI_IMU_PARAM_OUTPUT = 2,
    IMAI_IMU_PARAM_REFERENCE = 3,
    IMAI_IMU_PARAM_HANDLE = 7,
} IMAI_IMU_param_attrib;

typedef char *label_text_t;

typedef struct {
    char* name;
    int size;
    label_text_t *labels;
} IMAI_IMU_shape_dim;

typedef struct {
    char* name;
    IMAI_IMU_param_attrib attrib;
    int32_t rank;
    IMAI_IMU_shape_dim *shape;
    int32_t count;
    int32_t type_id;
    float frequency;
    int shift;
    float scale;
    long offset;
} IMAI_IMU_param_def;

typedef enum {
    IMAI_IMU_FUNC_ATTRIB_NONE = 0,
    IMAI_IMU_FUNC_ATTRIB_CAN_FAIL = 1,
    IMAI_IMU_FUNC_ATTRIB_PUBLIC = 2,
    IMAI_IMU_FUNC_ATTRIB_INIT = 4,
    IMAI_IMU_FUNC_ATTRIB_DESTRUCTOR = 8,
} IMAI_IMU_func_attrib;

typedef struct {
    char* name;
    char* description;
    void* fn_ptr;
    IMAI_IMU_func_attrib attrib;
    int32_t param_count;
    IMAI_IMU_param_def *param_list;
} IMAI_IMU_func_def;

typedef struct {
    uint32_t size;
    uint32_t peak_usage;
} IMAI_IMU_mem_usage;

typedef enum {
    IMAI_IMU_API_TYPE_UNDEFINED = 0,
    IMAI_IMU_API_TYPE_FUNCTION = 1,
    IMAI_IMU_API_TYPE_QUEUE = 2,
    IMAI_IMU_API_TYPE_QUEUE_TIME = 3,
    IMAI_IMU_API_TYPE_USER_DEFINED = 4,
} IMAI_IMU_api_type;

typedef struct {
    uint32_t api_ver;
    uint8_t id[16];
    IMAI_IMU_api_type api_type;
    char* prefix;
    IMAI_IMU_mem_usage buffer_mem;
    IMAI_IMU_mem_usage static_mem;
    IMAI_IMU_mem_usage readonly_mem;
    int32_t func_count;
    IMAI_IMU_func_def *func_list;
} IMAI_IMU_api_def;

IMAI_IMU_api_def *IMAI_IMU_api(void);

