---
source_url: "https://developer.imagimob.com/deepcraft-studio/deployment/custom-layers-functions"
fetched_at: "2026-03-10T15:51:57Z"
title: "Custom Layers Functions"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "deployment", "custom-layers-functions"]
---

# Custom Layers Functions

### Creating custom layers or functions

During the compile time, Imaginet handles the memory management and no dynamic memory is allocated to the generated code. All arrays have a shape and an element type. However, the advanced arrays may have additional attributes for streaming and quantization, for example, zero and scale.

Imaginet supports Python as well as C language. As Python is great for rapid prototyping, you can start by just implementing Python support for your units and continue with model training. When you are satisfied with your model and preprocessor architecture, implement the units in C for your platform and Imaginet will generate a contained firmware code in C without any dynamic memory allocations. You can generate C and Python comparison and unit tests to validate that the two implementations yield the same result.

### Overview

- - All C and Python files (\*.[c,h,py]) in Imaginet include directories are scanned and split into *code-fragments*.
- - All .imunit XML files are parsed to construct *units* using the *code-fragments*.
- - Units are stacked as layers in the DEEPCRAFT™ Studio preprocessing UI.

### Code Fragments

All code files (\*.py \*.c \*.h) are scanned for `#pragma` directives, used for annotating sections of the code
into named *fragments*. Each fragment within a file must have a unique name. It is recommended to use matching fragment names and code function names.

| Token | Description |
| --- | --- |
| `#pragma IMAGINET_FRAGMENT_BEGIN "FRAGMENT_NAME"` | Start of code fragment |
| `#pragma IMAGINET_FRAGMENT_END` | End of code fragment |
| `#pragma IMAGINET_DEPENDENCY "FILE_PATH:FRAGMENT_NAME"` | Annotate a dependency to another fragment. FILE\_PATH is a relative path of the file containing FRAGMENT\_NAME. If used within an fragment, it applies to the current fragment only. If declared outside, it applies to all the fragments in the file. |
| `#pragma IMAGINET_INCLUDES_BEGIN` | Start of includes section. Include statements (e.g. C `#include "foo.h"` or import statements (e.g. Python `import numpy as np`) are parsed. |
| `#pragma IMAGINET_INCLUDES_END` | End of includes section. |
| `#pragma #pragma IMAGINET_FRAGMENT_TEST "FILE_PATH:TEST_FUNCTION"` | [TBA] |

**C Example**

```
#pragma IMAGINET_INCLUDES_BEGIN
#include <stdint.h.h>
#pragma IMAGINET_INCLUDES_END

// Since this code is not in any annotated region, it is ignored by Imaginet.
#include "subdir/example_helpers.h"

#pragma IMAGINET_FRAGMENT_BEGIN "subavgf32"
#pragma IMAGINET_DEPENDENCY "subdir/example_helpers.c:__subavgf32"

// Remove offset by subtracting the average from each element given an axis.
// input = float array (any shape >= 2D)
// output = float array (same shape as input array)
// d0 = input.shape.step(axis)
// d1 = input.shape.size(axis)
// d2 = input.shape.slot(axis)
static inline void subavgf32(const float* restrict input, int d0, int d1, int d2, float* restrict output)
{
    const int d3 = d0 * d1;

    for (int j = 0; j < d2; j++) {
        int j3 = j * d3;
        for (int i = 0; i < d0; i++) {
            // declared in subdir/example_helpers.c
            __subavgf32(input + i + j3, d0, d1, output + i + j3);
        }
    }
}
#pragma IMAGINET_FRAGMENT_END
```

File *subdir/example\_helpers.c* for completeness:

```
#pragma IMAGINET_FRAGMENT_BEGIN "__subavgf32"

static inline void __subavgf32(const float *restrict input, int step, int count, float *restrict output)
{
	double avg = 0;
	for (int i = 0; i < count; i++) {
		avg += input[i * step];
	}

	avg /= (double)count;

	for (int i = 0; i < count; i++) {
		output[i * step] = input[i * step] - avg;
	}
}
#pragma IMAGINET_FRAGMENT_END
```

### Imagimob Unit Format (.immunit)

- - XML file with header `<?xml version="1.0" encoding="utf-8" ?>`
- - Contains one or more units decelerations
- - Three types of units: queue-, composite- and function-units

```
<?xml version="1.0" encoding="utf-8" ?>
<Imaginet>
  <Queue unit="MyNameSpace.MyQueue">
    ...
  </Queue>
  <Function unit="MyNameSpace.MyFunction">
    ...
  </Function>
  <Composite unit="MyNameSpace.MyComposite">
    ...
  </Composite>
</Imaginet>
```

The following characters must be escaped in XML documents:

| Character | XML Escape Code |
| --- | --- |
| `"` | `&quot;` |
| `'` | `&apos;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |

#### Function Units <Function>

- - Multiple input and output array arguments
- - May optionally allocate static memory
  * Static (stateful) memory allocations should however be avoided since only [pure functions](https://en.wikipedia.org/wiki/Pure_function) are optimized with expression rewrites.

**XML Example**:

```
<?xml version="1.0" encoding="utf-8" ?>
<Imaginet>
  <Function unit="Core.Math.Max">
    <DisplayName>Max</DisplayName>
    <DisplayPath>/Math</DisplayPath>

    <Description>
      Computes the maximum value along an axis. Collapses the dimension of the selected axis.

      <Header>Python implementation</Header>
      <Inline fragment="max.py:max" language="Python" />
    </Description>

    <Parameters>
      <InputSocket name="input" pipe="data" />
      <Int32Option name="axis" min="0" max="9" ui="textbox" text="Axis" description="Axis along which the max operation is performed. Enumerated from right to left." />
      <OutputSocket name="output" shape="input.shape.remove(axis)" type="input.type" pipe="data" />

      <Hidden name="d0" value="input.shape.step(axis)" />
      <Hidden name="d1" value="input.shape.size(axis)" />
      <Hidden name="d2" value="input.shape.slot(axis)" />
    </Parameters>

    <Contracts>
      <Assert test="input.shape.count &gt;= 2" error="Max requires an input with two or more dimensions since it reduces one dimension." />
      <Assert test="axis &lt; input.shape.count" error="Axis must be less than the number of input dimensions." />
    </Contracts>

    <Implementations>
      <Implementation language="C" fragment="max.h:max_f32" call="max_f32(input, d0, d1, d2, output)" >
        <TensorType tensor="input" type="Float32" />
        <TensorType tensor="output" type="Float32" />
      </Implementation>

      <Implementation language="Python" fragment="max.py:max" call="max_py(input, axis, output)">
        <TensorType tensor="input" />
        <TensorType tensor="output" />
      </Implementation>
    </Implementations>

  </Function>
</Imaginet>
```

#### Queue Units <Queue>

- - Units operate on data streams
- - Have state memory (stateful)
- - Defined with enqueue() and dequeue() functions
- - Is an instance of a class

Implements three seperate implementations instead on one as in function

**Queue XML:**

```
 <Queue unit="MyNameSpace.MyQueue">

    ...

    <Init>
      <Implementation ... />
    </Init>

    <Enqueue>
      <Implementation ... />
    </Enqueue>

    <Dequeue>
      <Implementation ... />
    </Dequeue>

  </Queue>
```

#### Composite Units <Composite>

Consist of a list of other unit stacked on top of each other.

***Composite XML:***

```
<Composite unit="MyNamespace.ContextualWindow">
    <DisplayName>Contextual Window</DisplayName>
    <DisplayPath>/Packages</DisplayPath>

    <Description>
      This is a wrapper for a sliding window where the windows shape and stride are computed.
    </Description>

    <Parameters>
      <Int32Option
        name="sampling_rate" min="0" max="65536"
        default="50" ui="textbox"
        text="Sample rate"
        description="Input data sample rate (Hz)." />

      <DoubleOption
        name="contextual_length_sec" min="0" ui="textbox"
        default="2"
        text="Contextual length (sec)"
        description="The length (in seconds) of the contextual window. How many seconds should the network consider for each prediction."/>

      <DoubleOption
        name="prediction_freq" min="0" ui="textbox"
        default="10"
        text="Prediction frequency (Hz)"
        description="How often to produce a prediction."/>

      <InputSocket
        name="input"
        pipe="data"
        text="Data Input"
        description="Data to be enqueue to buffer." />

      <InputSocket
        name="time_input"
        pipe="time"
        text="Time Input"
        description="Array with time codes."
        optional="yes"  />

      <Hidden name="contextual_size" value="Math.round(contextual_length_sec * sampling_rate)"/>
      <Hidden name="context_stride" value="Math.round(sampling_rate/prediction_freq)" />
      <Hidden name="output_shape" value="System.Shape(contextual_size, input.shape.flat)" />

      <OutputSocket
        name="output"
        type="input.type"
        shape="output_shape"
        pipe="data"
        text="Output Window"
        description="Output data buffer to write window to." />

      <OutputSocket
        name="time_output"
        type="System.Float32"
        shape="System.Shape(2)"
        pipe="time"
        text="Time Output"
        conditional="time_input != null"
        description="Output time buffer to write timestamps to." />

    </Parameters>

    <Contracts>
      <Assert test="contextual_size &gt;= 1" error="Contextual length {contextual_length_sec} seconds is too low. Min is {1.0/sampling_rate} seconds when sample frequency is {sampling_rate} Hz." />

      <Assert test="context_stride &lt;= contextual_size" error="Prediction frequency {prediction_freq} Hz is too low. Min is {1/contextual_length_sec} Hz" />

      <Assert test="prediction_freq &lt;= sampling_rate" error="Prediction frequency {prediction_freq} Hz is too high. Max is {sampling_rate} Hz" />
    </Contracts>

    <Stacked>
      <Unit id="Core.Queues.SlidingWindow">
        <Argument param="input">input</Argument>
        <Argument param="time_input">time_input</Argument>
        <Argument param="window_shape">output_shape</Argument>

         <!-- Argument values can be any expression -->
        <Argument param="stride">input.shape.flat * context_stride</Argument>

        <Argument param="buffer_multiplier">1</Argument>
        <Argument param="output">output</Argument>
        <Argument param="time_output">time_output</Argument>
      </Unit>

      <!---
        More units can be stacked here
      --->

    </Stacked>

  </Composite>
```

#### Parameters <Parameters>

All unit parameters have the following three attributes:

```
name="name_of_parameter"
# Identifier name of parameter.
# No white space, may not start with a digit.
```

```
text="My FooBar name"
# If not specified, the value of name= is used.
# User-friendly display name to display in UI.
# May contain any characters (e.g white space)
```

```
description="Parameter description text."
# Description text for parameter.
# Can also be expressed as a child XML element <Description>Text</Description> (if newlines are wanted).
```

Some parameters accept dynamic expressions.

| Notation | Should Evaluate To |
| --- | --- |
| BOOLEAN\_EXPRESSION | `bool` |
| INTEGER\_EXPRESSION | `int` |
| VALUETYPE\_EXPRESSION | [System.ValueType](https://developer.imagimob.com/edge-optimization/imaginet#systemvaluetype) |
| SHAPE\_EXPRESSION | [System.Shape](https://developer.imagimob.com/edge-optimization/imaginet#systemshape) |

##### Input Array Parameter <InputSocket>

Declares a read-only input array parameter.

```
 <InputSocket
    name="my_input_array_param"
    text="User friendly name"
    description="User friendly description"

    # Optional name of pipe to read from. String value.
    # Note! If no pipe is specified the unit will not show up in unit stacking UI.
    pipe="data"

    # Optional boolean value, defaults to False.
    # If True, the parameter is optional and may be Null.
    optional="False" />
```

##### Output Array Parameter <OutputSocket>

Declares an output array parameter.

```
 <OutputSocket
    name="my_out_param"
    text="User friendly name"
    description="User friendly description"

    # Required output array type.
    # Should evaluate to System.ValueType
    type="VALUETYPE_EXPRESSION"

    # Required output array shape.
    # Should evaluate to System.Shape
    shape="SHAPE_EXPRESSION"

    # Optional name of pipe to write to. String value.
    # Note! If no pipe is specified the unit will not show up in unit stacking UI.
    pipe="data"

    # Optional. Defaults to "true"
    # If BOOLEAN_EXPRESSION evaluates to false the parameter is skipped and resolves to null.
    # This can for example be used to only compute create the data output if corresponding input is given,
    # as in the case to only compute time-stamps if the "time" data pipe is supplied.
    conditional="BOOLEAN_EXPRESSION" />
```

##### Int32 Parameter <Int32Option>

Declare an integer input parameter (int).

```
 <Int32Option
   name="my_int_param"
   text="User friendly name"
   description="User friendly description"

   # Optional default value, in not specified "0" is assumed.
   default="42"

   # Optional minimum value for UI control.
   # If not specified -2147483648 is assumed
   # See also "Unit Contracts"
   min="0"

   # Optional maximum value for UI control.
   # If not specified 2147483647 is assumed
   # See also "Unit Contracts"
   max="100"

   # Optional UI control to use
   # default is TextBox
   # Valid values is one of: "TextBox", "Slider"
   ui="TextBox" />
```

##### Double Parameter <DoubleOption>

Declare a floating point input parameter (double).

```
 <DoubleOption
   name="my_real_param"
   text="User friendly name"
   description="User friendly description"

   # Optional default value, in not specified "0" is assumed.
   default="42.1"

   # Optional minimum value for UI control.
   # If not specified -1.7976931348623157E+308 is assumed
   # See also "Unit Contracts"
   min="0.0"

   # Optional maximum value for UI control.
   # If not specified 1.7976931348623157E+308 is assumed
   # See also "Unit Contracts"
   max="100.123"

   # Optional UI control to use
   # default is TextBox
   # Valid values is one of: "TextBox", "Slider"
   ui="TextBox" />
```

##### Shape Parameter <ShapeOption>

Declare a shape input parameter (System.Shape).

```
 <ShapeOption
   name="my_shape_param"
   text="User friendly name"
   description="User friendly description"

   # Optional default value to use in UI.
   # Must be a string with or without brackets. e.g. (3,128) [3,128] 3,128
   default="(3,16,128)" />
```

##### String Parameter <StringOption>

Declare a string input parameter (string).

```
 <StringOption
   name="my_string_param"
   text="User friendly name"
   description="User friendly description"

   # Optional default value to use in UI.
   default="my string"  />
```

##### Handle Parameter <Handle>

Creates an object handle in static state memory with a given number of bytes.

```
 <Handle
   name="my_handle_param"
   text="User friendly name"
   description="User friendly description"

   # Required number of bytes to allocate for handle.
   size="INTEGER_EXPRESSION"  \>
```

##### Hidden Parameter <Hidden>

Create a parameter form an expression.
The parameter type is determined by the evaluated expression.

Hidden parameters are not show in the UI.

```
 <Hidden
   name="my_hidden_param"
   text="User friendly name"
   description="User friendly description"

   # Required expression to be evaluated
   value="ANY_EXPRESSION"
  />
```

#### Implementation <Implementation>

Register an implementation with [Fragments](https://developer.imagimob.com/edge-optimization/imaginet#code-fragments).

If more than one implementation is selected (conditional is true) an error is raised.

```
   <!-- C with 32-bit floating point implementation. -->
   <Implementation

        # Required C or Python
        language="C"

        # Optional, if present it must evaluate to true.
        conditional="input.type == System.Float32"

        # Fragment to use
        fragment="subavg.h:subavgf32"

        # Function call
        call="subavgf32(input, d0, d1, d2, output)">

         <!-- (Optional) Implementation only selected if foo is equal to 42 -->
         <Conditional value="foo == 42" />

         <!-- (Optional) argument named 'input' must be a tensor of type Float32 -->
         <TensorType tensor="input" type="Float32" />

         <!-- (Optional) argument named 'd0' must be a constant of type Int16 -->
         <ConstantType constant="d1" type="Int16" optimize="warning" />

     </Implementation>
```

#### Contracts <Contracts>

```
<Contracts>
    <Assert
        # Required attribute must evaluate to true.
        test="BOOL_EXPRESSION"

        # The test expression must evaluate to true, if not, given error is raised.
        # Expressions can be inlined using { }
        error="Stride ({stride}) can't be bigger than window size {window_shape} ({window_shape.flat})" />

</Contracts>
```

#### Expressions

All expressions can be evaluated to a value type (e.g 3.14) or an object reference (e.g ArrayBuffer).

Examples:

```
// Evaluates to (4*5)+(6*7) = 62
4*5+6*7

// Evaluates to 1
Math.sin(Math.PI / 2.0)
```

##### Globals

Globals can be directly accessed. The global scope contains

- - Boolean constants (`true/false`)
- - Null value (`null`)
- - System library (`System`) reference to standard system functions
- - Math library (`Math`) reference to standard math functions
- - All parameters with arguments (e.g `foobar`)

```
// Calls with no arguments, i.e empty parentheses, can be omitted.
input.shape()
// is the same as
input.shape
```

##### Operators

Standard operators are defined for bool, int, double and object.

The operators `* / + -` also work with arrays of different dimensions
with shape broadcasting. For example:

`array_4x5x6 / array_4x5x1`

The operators are also defined for an array and scalar .

`multidim_array * 3.3`

In an expression with multiple operators, the operators with higher precedence are evaluated before the operators with lower precedence.

| Operator precedence | Operators |
| --- | --- |
| Primary | Name of any global, argument or constant expression |
| Member access | `x.y()` |
| Unary | `- ~ !` |
| Multiplicative | `* / %` |
| Additive | `+ -` |
| Shift | `<< >>` |
| Relational | `< > <= >=` |
| Equality | `== !=` |
| Logical | ``` & ^ |
| Ternary | `?:` |

##### Operator functions

*In no particular order*

```
+ (Array,Array)
+ (Array,Double)
+ (Double,Double)
+ (Int32,Int32)

- (Array,Array)
- (Array,Double)
- (Double,Double)
- (Int32,Int32)

* (Array,Array)
* (Array,Double)
* (Double,Double)
* (Double,Array)
* (Int32,Int32)

/ (Array,Array)
/ (Array,Double)
/ (Double,Double)
/ (Int32,Int32)

- (Double)
- (Int32)

% (Double,Double)
% (Int32,Int32)

! (Boolean)
|| (Expression,Expression)
&& (Expression,Expression)

?: (Expression,Expression,Expression)

!= (Double,Double)
!= (Object,Object)
== (Double,Double)
== (Object,Object)
< (Double,Double)
< (Int32,Int32)
> (Double,Double)
> (Int32,Int32)
<= (Double,Double)
<= (Int32,Int32)
>= (Double,Double)
>= (Int32,Int32)

~ (Int32)
^ (Boolean,Boolean)
^ (Int32,Int32)
& (Boolean,Boolean)
& (Int32,Int32)
| (Boolean,Boolean)
| (Int32,Int32)
<< (Int32,Int32)
>> (Int32,Int32)
```

#### Library Functions

List of standard library classes.

##### Math

Standard math functions.

```
 // Static functions
 Math.real(int x) -> double                       - Convert integer to real number (double)
 Math.int(double x) -> int                        - Truncate real number
 Math.abs(int x) -> int                           - Returns the absolute value of a specified number.
 Math.abs(double x) -> double                     - Returns the absolute value of a specified number.
 Math.max(double a, double b) -> double           - Returns the larger of two specified numbers.
 Math.max(int a, int b) -> int                    - Returns the larger of two specified numbers.
 Math.min(double a, double b) -> double           - Returns the smaller of two numbers.
 Math.min(int a, int b) -> int                    - Returns the smaller of two numbers.
 Math.pow(double a, double b) -> double           - Returns a specified number raised to the specified power.
 Math.pow(int a, int b) -> int                    - Returns a specified number raised to the specified power.
 Math.exp(double x) -> double                     - Returns e raised to the specified power.
 Math.log(double x, double x) -> double           - Returns the logarithm of a specified number in a specified base.
 Math.hann(ValueType type, int size) -> Array     - Computes a Hann window
 Math.floor(double x) -> int                      - Returns the largest integral value less than or equal to the specified number.
 Math.ceil(double x) -> int                       - Returns the smallest integral value greater than or equal to the specified number.
 Math.round(double x) -> int                      - Rounds a double-precision floating-point value to the nearest integral value, and rounds midpoint values to the nearest even number.
 Math.sqrt(double x)  -> double                   - Returns the square root of a specified number.
 Math.sign(double x) -> int                       - Returns an integer that indicates the sign of a double-precision floating-point number.
 Math.sign(int x) -> int                          - Returns an integer that indicates the sign of a 32-bit signed integer.
 Math.sin(double x) -> double                     - Returns the sine of the specified angle.
 Math.sinh(double x) -> double                    - Returns the hyperbolic sine of the specified angle.
 Math.cos(double x) -> double                     - Returns the cosine of the specified angle.
 Math.cosh(double x) -> double                    - Returns the hyperbolic cosine of the specified angle.
 Math.tan(double x) -> double                     - Returns the tangent of the specified angle.
 Math.tanh(double x) -> double                    - Returns the hyperbolic tangent of the specified angle.
 Math.atan(double x) -> double                    - Returns the angle whose tangent is the specified number.
 Math.atan2(double y, double x) -> double         - Returns the angle whose tangent is the quotient of two specified numbers.
 Math.acos(double x) -> double                    - Returns the angle whose cosine is the specified number.
 Math.asin(double x) -> double                    - Returns the angle whose sine is the specified number.

 // Constants
 Math.E -> double                                 - Represents the natural logarithmic base, specified by the constant, e.
 Math.PI -> double                                - Represents the ratio of the circumference of a circle to its diameter, specified by the constant, π.
 Math.Epsilon -> double                           - Represents the smallest positive Double value that is greater than zero. This field is constant.
 Math.NaN -> double                               - Represents a value that is not a number (NaN). This field is constant.
 Math.MinValue -> double                          - Represents the smallest possible value of a Double. This field is constant.
 Math.MaxValue -> double                          - Represents the largest possible value of a Double. This field is constant.
```

##### System.Shape

Represents an array shape.

```
// Create a new Shape object with given dimensions
System.Shape(d0)
System.Shape(d1,d0)
System.Shape(d2,d1,d0)
System.Shape(d3,d2,d1,d0)

Shape methods:
 .count() -> int                                  - Get shape rank.
 .flat() -> int                                   - Get total number of elements.
 .size(int dim) -> int                            - Get size of given dimension.
 .step(int axis) -> int                           - Get the number of indexes between two adjacent elements in given dimension.
 .step(int start, int stop) -> int                - Get the number of indexes between two dimensions.
 .slot(int axis) -> int                           - Get the slot size for given axis.
 .replace(int axis, int newDim) -> Shape          - Get a new shape with the given dimension replaced.
 .insert(int axis, int newDim) -> Shape           - Get a new shape with an additional dimension.
 .remove(int axis) -> Shape                       - Get a new shape with given dimension removed.
 .broadcast(Shape other) -> ShapeBroadcast        - Broadcast shape into given one.
```

##### System.ValueType

Represents an array element type.

```
// Floating point element types
System.Float16 -> ValueType     - Get value type. Sign bit, 5-bit exponent, 10-bit significand.
System.Float32 -> ValueType     - Get value type. Sign bit, 8-bit exponent, 23-bit significand.
System.Float64 -> ValueType     - Get value type. Sign bit, 11-bit exponent, 52-bit significand.

// Integer element types
System.Int8 -> ValueType        - Get signed int 8 bit value type.
System.Int16 -> ValueType       - Get signed int 16 bit value type.
System.Int32 -> ValueType       - Get signed int 32 bit value type.

ValueType methods:
 .size() -> int                 - Get the byte size.
```

##### System.ArrayBuffer

Allocated memory. May be readonly (flash) or writable (RAM).

```
// Create a new ArrayBuffer in RAM
System.ArrayBuffer(ValueType elementType, Shape shape) -> ArrayBuffer   - Create a new array with given shape in writable memory.
System.ArrayBuffer(ValueType elementType, int count) -> ArrayBuffer     - Create a one-dimensional array in writable memory.
System.ArrayBuffer(ValueType elementType, Shape shape, bool static) -> ArrayBuffer   - Create a new array with given shape, if 'static' is true static menory will be used, else dynamic memory is used.
System.ArrayBuffer(ValueType elementType, int count, bool static) -> ArrayBuffer     - Create a one-dimensional array, if 'static' is true static menory will be used, else dynamic memory is used.

ArrayBuffer methods:
 .type() -> ValueType                             - Get array element type.
 .shape() -> Shape                                - Get array shape.
```

##### System.Array

Constant data array. Precomputed and stored in read-only memory (flash).

```
Array methods:
 .type() -> ValueType                             - Get array element type.
 .shape() -> Shape                                - Get array element shape.
 .exp() -> Array                                  - Element-wise, e raised to the specified power.
 .pow(double b) -> Array                          - Element-wise, values raised to the specified power.
 .log(double b) -> Array                          - Element-wise, returns the logarithm of a specified number in a specified base.
 .sqrt() -> Array                                 - Element-wise, returns the square root.
 .abs() -> Array                                  - Element-wise, absolute value.
 .transpose(int d0) -> Array                      - Create a new array with the given dimensions
 .transpose(int d1, d0) -> Array                  - Create a new array with the given dimensions
 .transpose(int d2, d1, d0) -> Array              - Create a new array with the given dimensions
 .transpose(int d3, d2, d1, d0) -> Array          - Create a new array with the given dimensions
 .reshape(Shape shape) -> Array                   - Reshape array to given shape.
 .buffer() -> ArrayBuffer                         - Convert to readonly ArrayBuffer object.
```

##### System.ShapeBroadcast

Result of an array broadcasting.

```
ShapeBroadcast methods:
  .left()    -> int                              - product of axis length of left parts in dimensions with no broadcast, default 1
  .group1()  -> int                              - product of axis length of left group which needs broadcasting, default 1
  .middle()  -> int                              - product of axis length of middle parts in dimensions with no broadcast, default 1
  .group2()  -> int                              - product of axis length of right group which needs broadcasting, default 1
  .right()   -> int                              - product of axis length of right parts in dimensions with no broadcast, default 1
```

Calculation starts from right to left (d0 to dn). If the shape sequences is not long enough to compute all parameters above, then remained parameters stay with default 1. Explainations are given along with detailed examples below:

```
Example 1:
 - Broadcast array A with shape [2,1,4,1,6] into B with [2,3,4,5,6], start from the rightmost dimension till the leftmost:
    A_d0 = 6 == B_d0 = 6, no need to boardcast, right = right * b_d0 = 1 * 6 = 6;
    A_d1 = 1 != B_d1 = 5, d1 needs broadcasting, group2 = group2 * B_d1 = 1 * 5 = 5;
    A_d2 = 4 == B_d2 = 4, no need to boardcast, middle = middle * B_d2 = 1 * 4 = 4;
    A_d3 = 1 != B_d3 = 3, d3 needs broadcasting, group1 = group1 * B_d3 = 1 * 3 = 3;
    A_d4 = 2 == B_d4 = 2, no need to boardcast, left = left * b_d4 = 1 * 2 = 2;

Example 2:
 - Broadcast array A with shape [2,1,1,5] into B with [2,3,4,5], start from the rightmost dimension till the leftmost:
    A_d0 = 5 == B_d0 = 5, no need to boardcast, right = right * b_d0 = 1 * 5 = 5;
    A_d1 = 1 != B_d1 = 4, d1 needs broadcasting, group2 = group2 * B_d1 = 1 * 4 = 4;
    A_d2 = 1 != B_d2 = 3, d2 needs broadcasting, group2 = group2 * B_d2 = 4 * 3 = 12;
    A_d3 = 2 == B_d3 = 2, no need to boardcast, middle = middle * b_d3 = 1 * 2 = 1;
    group1 & left are not updated, so group1 = left = 1;

Example 3:
 - Broadcast array A with shape [2,3,1] into B with [2,3,4], start from the rightmost dimension till the leftmost:
    A_d0 = 1 != B_d0 = 4, d0 needs to boardcast, group2 = group2 * B_d0 = 1 * 4 = 4;
    A_d1 = 3 == B_d1 = 3, no need to boardcast, middle = middle * B_d1 = 1 * 3 = 3;
    A_d2 = 2 == B_d2 = 2, no need to boardcast, middle = middle * B_d2 = 3 * 2 = 6;
    right & group1 & left are not updated, so right = group1 = left = 1;
```

#### Expression Grammar

Backus normal form (BNF) context-free grammar.

```
CONSTANT = '-'? [0-9]+ ('.' [0-9]+)? | '"' [^"]* '"'
IDENTIFIER = [a-zA-Z_] [a-zA-Z0-9_]*

EXPR = TERNARY
TERNARY = LOGICAL ('?' LOGICAL ':' LOGICAL)*
LOGICAL = EQUALITY (('&' | '^' | '|' | '&&' | '||') EQUALITY)*
EQUALITY = RELATIONAL (('==' | '!=') RELATIONAL)*
RELATIONAL = SHIFT (('<' | '>' | '>='| '<=') SHIFT)*
SHIFT = ADDITIVE (('<<' | '>>') ADDITIVE)*
ADDITIVE = MULTIPLICATIVE (('+' | '-') MULTIPLICATIVE)*
MULTIPLICATIVE = UNARY (('*' | '/' | '%') UNARY)*
UNARY = ('-'|'~'|'!')? CALL
CALL = PRIMARY ('.' IDENTIFIER ARGSLIST)*
PRIMARY = CONSTANT | GLOBAL | '(' EXPR ')'
ARGSLIST = ('(' EXPR (',' EXPR)+ ')')?
GLOBAL = IDENTIFIER
FUNCTION = IDENTIFIER
```
