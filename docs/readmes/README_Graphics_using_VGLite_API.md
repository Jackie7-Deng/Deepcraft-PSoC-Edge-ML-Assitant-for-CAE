---
title: PSoC Edge MCU - Graphics using VGLite API
category: graphics
subcategory: 2d-rendering
target_hardware:
  - KIT_PSE84_EVAL_EPC2 (Default)
  - KIT_PSE84_EVAL_EPC4
display: Waveshare 4.3-inch DSI LCD
interface: MIPI DSI
gpu: VGLite (Vivante)
rtos: FreeRTOS
features:
  - Hardware-accelerated 2D vector drawing
  - Platform-independent VGLite API
github_repo: mtb-example-psoc-edge-gfx-vglite
code_example_id: CE238628
modustoolbox_version: 3.6+
toolchains: [GCC_ARM, ARM, IAR, LLVM_ARM]
tags: [graphics, vglite, 2d, vector, dsi-display, gpu, freertos]
summary: |
  VGLite 2D 图形 API 示例。使用 Vivante VGLite 硬件加速 API 进行 2D 矢量绘图。
  通过 MIPI DSI 接口连接 Waveshare 4.3 英寸显示屏。
  展示硬件加速的矢量图形操作，运行在 FreeRTOS 环境中。
---

# PSOC&trade; Edge MCU: Graphics using VGLite API

This code example demonstrates how to utilize Vivante's platform-independent VGLite Graphics APIs to carry out hardware-accelerated 2D vector drawing operations and render the generated image on a [Waveshare 4.3 inch Raspberry Pi DSI display](https://www.waveshare.com/4.3inch-dsi-lcd.htm). The display is connected via a MIPI display serial interface (DSI). The code is designed to run in a FreeRTOS environment.

This code example has a three project structure: CM33 secure, CM33 non-secure, and CM55 projects. All three projects are programmed to the external QSPI flash and executed in Execute in Place (XIP) mode. Extended boot launches the CM33 secure project from a fixed location in the external flash, which then configures the protection settings and launches the CM33 non-secure application. Additionally, CM33 non-secure application enables CM55 CPU and launches the CM55 application.

[View this README on GitHub.](https://github.com/Infineon/mtb-example-psoc-edge-gfx-vglite)

[Provide feedback on this code example.](https://cypress.co1.qualtrics.com/jfe/form/SV_1NTns53sK2yiljn?Q_EED=eyJVbmlxdWUgRG9jIElkIjoiQ0UyMzg2MjgiLCJTcGVjIE51bWJlciI6IjAwMi0zODYyOCIsIkRvYyBUaXRsZSI6IlBTT0MmdHJhZGU7IEVkZ2UgTUNVOiBHcmFwaGljcyB1c2luZyBWR0xpdGUgQVBJIiwicmlkIjoibWFqdW1kYXIiLCJEb2MgdmVyc2lvbiI6IjIuMC4xIiwiRG9jIExhbmd1YWdlIjoiRW5nbGlzaCIsIkRvYyBEaXZpc2lvbiI6Ik1DRCIsIkRvYyBCVSI6IklDVyIsIkRvYyBGYW1pbHkiOiJQU09DIn0=)

See the [Design and implementation](docs/design_and_implementation.md) for the functional description of this code example.


## Requirements

- [ModusToolbox&trade;](https://www.infineon.com/modustoolbox) v3.6 or later (tested with v3.6)
- Board support package (BSP) minimum required version: 1.0.0
- Programming language: C
- Associated parts: All [PSOC&trade; Edge MCU](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm) parts


## Supported toolchains (make variable 'TOOLCHAIN')

- GNU Arm&reg; Embedded Compiler v14.2.1 (`GCC_ARM`) – Default value of `TOOLCHAIN`
- Arm&reg; Compiler v6.22 (`ARM`)
- IAR C/C++ Compiler v9.50.2 (`IAR`)
- LLVM Embedded Toolchain for Arm&reg; v19.1.5 (`LLVM_ARM`)


## Supported kits (make variable 'TARGET')

- [PSOC&trade; Edge E84 Evaluation Kit](https://www.infineon.com/KIT_PSE84_EVAL) (`KIT_PSE84_EVAL_EPC2`) – Default value of `TARGET`
- [PSOC&trade; Edge E84 Evaluation Kit](https://www.infineon.com/KIT_PSE84_EVAL) (`KIT_PSE84_EVAL_EPC4`)


## Hardware setup

This example uses the board's default configuration. See the kit user guide to ensure that the board is configured correctly.

Ensure the following jumper and pin configuration on board.
- BOOT SW must be in the HIGH/ON position
- J20 and J21 must be in the tristate/not connected (NC) position

### Supported display and electrical connection with KIT_PSE84_EVAL 

- **Waveshare 4.3 inch Raspberry Pi DSI 800*480 display:** <br>
  Connect the FPC 15-pin cable between the display connector and the PSOC&trade; Edge E84's RPI MIPI DSI connector as outlined in the table below and shown in Figure 1.

  Display's Connector | PSOC&trade; Edge E84 Evaluation Kit's connector
  ------------------- | ----------------------------------------------------
  DSI connector       | J39

  **Figure 1. Display connection with PSOC&trade; Edge E84 evaluation kit**

  ![](images/display-kit-connection.png)

## Software setup

See the [ModusToolbox&trade; tools package installation guide](https://www.infineon.com/ModusToolboxInstallguide) for information about installing and configuring the tools package.

Install a terminal emulator if you do not have one. Instructions in this document use [Tera Term](https://teratermproject.github.io/index-en.html).

This example requires no additional software or tools.


## Operation

See [Using the code example](docs/using_the_code_example.md) for instructions on creating a project, opening it in various supported IDEs, and performing tasks, such as building, programming, and debugging the application within the respective IDEs.

1. Connect the Waveshare 4.3 display to the board according to the instructions given in [Display setup](#supported-display-and-electrical-connection-with-kit_pse84_eval) section

2. Connect the board to your PC using the provided USB cable through the KitProg3 USB connector

3. Open a terminal program and select the KitProg3 COM port. Set the serial port parameters to 8N1 and 115200 baud

4. Build and program the application

5. After programming, the application starts automatically. Please confirm that "PSOC Edge MCU: Graphics using VGLite API" is displayed on the UART terminal, followed by a list of operations for the user to try and regularly updated Frame Per Second (FPS) statistics data [Figure 2](images/terminal-default-demo-select-option.png)

   **Figure 2. Terminal output**

   ![](images/terminal-default-demo-select-option.png)

6. Observe the Infineon logo periodically animated on the LCD [Figure 3](images/display-default-animated-infineon-logo.gif)

   **Figure 3. Animated image output on LCD**

   ![](images/display-default-animated-infineon-logo.gif)

7. To run demonstration case 1 (**Fill Rules**), open the terminal and press 1. The terminal displays the "Fill rules: two vector path shapes using different fill rules." header [Figure 4](images/terminal-demo-1.png). The display shows two shapes on the left side with the VG_LITE_FILL_EVEN_ODD filling rule and two shapes on the right side with the VG_LITE_FILL_NON_ZERO filling rule [Figure 5](images/display-demo-1.png)

   **Figure 4. Demonstration case 1 (Fill Rules) terminal**

   ![](images/terminal-demo-1.png)

   **Figure 5. Demonstration case 1 (Fill Rules) display**

   ![](images/display-demo-1.png)

8. To return to the main menu, press Ctrl+C. You can then select other demonstration options from here

9. To run demonstration case 2 (**Alpha Blending**), press 2 on the main menu of the terminal. The terminal displays the "Alpha behavior: Alpha blending between two vector path shapes using different blend modes." header [Figure 6](images/terminal-demo-2.png). The display shows two shapes on the left side with the VG_LITE_BLEND_SRC_OVER blending mode and two shapes on the right side with the VG_LITE_BLEND_MULTIPLY blending mode [Figure 7](images/display-demo-2.png)

   **Figure 6. Demonstration case 2 (Alpha Blending) terminal**

   ![](images/terminal-demo-2.png)

   **Figure 7. Demonstration case 2 (Alpha Blending) display**

   ![](images/display-demo-2.png)

10. To run demonstration case 3 (**Blit Color Rendering**), press 3 on the main menu of the terminal. The terminal displays the "Blit color: Blit in rectangle Infineon logo." header [Figure 8](images/terminal-demo-9.png). The display shows two Infineon logos rectangularly blitted onto a TEAL_COLOR frame [Figure 9](images/display-demo-3.png)

    **Figure 8. Demonstration case 3 (Blit Color Rendering) terminal**

    ![](images/terminal-demo-3.png)

    **Figure 9. Demonstration case 3 (Blit Color Rendering) display**

    ![](images/display-demo-3.png)

11. To run demonstration case 4 (**Pattern Fill**), press 4 on the main menu of the terminal [Figure 10](images/terminal-demo-4.png). The terminal displays the "Pattern fill: Pattern fill demonstration" header. The display shows the Infineon logo on four different shapes using the `vg_lite_draw_pattern` API [Figure 11](images/display-demo-4.png)

    **Figure 10. Demonstration case 4 (Pattern Fill) terminal**

    ![](images/terminal-demo-4.png)

    **Figure 11. Demonstration case 4 (Pattern Fill) display**

    ![](images/display-demo-4.png)

12. To run demonstration case 5 (**UI/Filter Demo**), press 5 on the main menu of the terminal. The terminal displays the "UI/filter: Demonstrate VG_LITE_FILTER_LINEAR." header [Figure 12](images/terminal-demo-5.png). The display shows four different icons and a highlighted rectangle moving over all four icons with VG_LITE_FILTER_LINEAR [Figure 13](images/display-demo-5.gif)

    **Figure 12. Demonstration case 5 (UI/Filter Demo) terminal**

    ![](images/terminal-demo-5.png)

    **Figure 13. Demonstration case 5 (UI/Filter Demo) display**

    ![](images/display-demo-5.gif)


## Performance KPIs of demonstrated operations

 Sr No. | Demonstration description      | FPS | CPU usage (%)
--------|--------------------------------|-----|--------------
 0      | Default animated Infineon logo | 56  | 2             
 1      | Fill Rules (vector paths)      | 56  | 2
 2      | Alpha Blending (vector paths)  | 42  | 4
 3      | Blit Color Rendering           | 53  | 3
 4      | Pattern Fill                   | 53  | 2
 5      | UI / Filter Demo               | 53  | 3


## Related resources

Resources  | Links
-----------|----------------------------------
Application notes  | [AN235935](https://www.infineon.com/AN235935) – Getting started with PSOC&trade; Edge E8 MCU on ModusToolbox&trade; software <br> [AN239191](https://www.infineon.com/AN239191) – Getting started with graphics on PSOC&trade; Edge MCU
Code examples  | [Using ModusToolbox&trade;](https://github.com/Infineon/Code-Examples-for-ModusToolbox-Software) on GitHub
Device documentation | [PSOC&trade; Edge MCU datasheets](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm#documents) <br> [PSOC&trade; Edge MCU reference manuals](https://www.infineon.com/products/microcontroller/32-bit-psoc-arm-cortex/32-bit-psoc-edge-arm#documents)
Development kits | Select your kits from the [Evaluation board finder](https://www.infineon.com/cms/en/design-support/finder-selection-tools/product-finder/evaluation-board)
Libraries  | [mtb-dsl-pse8xxgp](https://github.com/Infineon/mtb-dsl-pse8xxgp) – Device support library for PSE8XXGP <br> [retarget-io](https://github.com/Infineon/retarget-io) – Utility library to retarget STDIO messages to a UART port
Tools  | [ModusToolbox&trade;](https://www.infineon.com/modustoolbox) – ModusToolbox&trade; software is a collection of easy-to-use libraries and tools enabling rapid development with Infineon MCUs for applications ranging from wireless and cloud-connected systems, edge AI/ML, embedded sense and control, to wired USB connectivity using PSOC&trade; Industrial/IoT MCUs, AIROC&trade; Wi-Fi and Bluetooth&reg; connectivity devices, XMC&trade; Industrial MCUs, and EZ-USB&trade;/EZ-PD&trade; wired connectivity controllers. ModusToolbox&trade; incorporates a comprehensive set of BSPs, HAL, libraries, configuration tools, and provides support for industry-standard IDEs to fast-track your embedded application development

<br>


## Other resources

Infineon provides a wealth of data at [www.infineon.com](https://www.infineon.com) to help you select the right device, and quickly and effectively integrate it into your design.


## Document history

Document title: *CE238628* – *PSOC&trade; Edge MCU: Graphics using VGLite API*

 Version | Description of change
 ------- | ---------------------
 1.x.0   | New code example <br> Early access release
 2.0.0   | GitHub release
 2.0.1   | Updated terminal messages to be more user-friendly
<br>


All referenced product or service names and trademarks are the property of their respective owners.

The Bluetooth&reg; word mark and logos are registered trademarks owned by Bluetooth SIG, Inc., and any use of such marks by Infineon is under license.

PSOC&trade;, formerly known as PSoC&trade;, is a trademark of Infineon Technologies. Any references to PSoC&trade; in this document or others shall be deemed to refer to PSOC&trade;.

---------------------------------------------------------

© Cypress Semiconductor Corporation, 2023-2025. This document is the property of Cypress Semiconductor Corporation, an Infineon Technologies company, and its affiliates ("Cypress").  This document, including any software or firmware included or referenced in this document ("Software"), is owned by Cypress under the intellectual property laws and treaties of the United States and other countries worldwide.  Cypress reserves all rights under such laws and treaties and does not, except as specifically stated in this paragraph, grant any license under its patents, copyrights, trademarks, or other intellectual property rights.  If the Software is not accompanied by a license agreement and you do not otherwise have a written agreement with Cypress governing the use of the Software, then Cypress hereby grants you a personal, non-exclusive, nontransferable license (without the right to sublicense) (1) under its copyright rights in the Software (a) for Software provided in source code form, to modify and reproduce the Software solely for use with Cypress hardware products, only internally within your organization, and (b) to distribute the Software in binary code form externally to end users (either directly or indirectly through resellers and distributors), solely for use on Cypress hardware product units, and (2) under those claims of Cypress's patents that are infringed by the Software (as provided by Cypress, unmodified) to make, use, distribute, and import the Software solely for use with Cypress hardware products.  Any other use, reproduction, modification, translation, or compilation of the Software is prohibited.
<br>
TO THE EXTENT PERMITTED BY APPLICABLE LAW, CYPRESS MAKES NO WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, WITH REGARD TO THIS DOCUMENT OR ANY SOFTWARE OR ACCOMPANYING HARDWARE, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  No computing device can be absolutely secure.  Therefore, despite security measures implemented in Cypress hardware or software products, Cypress shall have no liability arising out of any security breach, such as unauthorized access to or use of a Cypress product. CYPRESS DOES NOT REPRESENT, WARRANT, OR GUARANTEE THAT CYPRESS PRODUCTS, OR SYSTEMS CREATED USING CYPRESS PRODUCTS, WILL BE FREE FROM CORRUPTION, ATTACK, VIRUSES, INTERFERENCE, HACKING, DATA LOSS OR THEFT, OR OTHER SECURITY INTRUSION (collectively, "Security Breach").  Cypress disclaims any liability relating to any Security Breach, and you shall and hereby do release Cypress from any claim, damage, or other liability arising from any Security Breach.  In addition, the products described in these materials may contain design defects or errors known as errata which may cause the product to deviate from published specifications. To the extent permitted by applicable law, Cypress reserves the right to make changes to this document without further notice. Cypress does not assume any liability arising out of the application or use of any product or circuit described in this document. Any information provided in this document, including any sample design information or programming code, is provided only for reference purposes.  It is the responsibility of the user of this document to properly design, program, and test the functionality and safety of any application made of this information and any resulting product.  "High-Risk Device" means any device or system whose failure could cause personal injury, death, or property damage.  Examples of High-Risk Devices are weapons, nuclear installations, surgical implants, and other medical devices.  "Critical Component" means any component of a High-Risk Device whose failure to perform can be reasonably expected to cause, directly or indirectly, the failure of the High-Risk Device, or to affect its safety or effectiveness.  Cypress is not liable, in whole or in part, and you shall and hereby do release Cypress from any claim, damage, or other liability arising from any use of a Cypress product as a Critical Component in a High-Risk Device. You shall indemnify and hold Cypress, including its affiliates, and its directors, officers, employees, agents, distributors, and assigns harmless from and against all claims, costs, damages, and expenses, arising out of any claim, including claims for product liability, personal injury or death, or property damage arising from any use of a Cypress product as a Critical Component in a High-Risk Device. Cypress products are not intended or authorized for use as a Critical Component in any High-Risk Device except to the limited extent that (i) Cypress's published data sheet for the product explicitly states Cypress has qualified the product for use in a specific High-Risk Device, or (ii) Cypress has given you advance written authorization to use the product as a Critical Component in the specific High-Risk Device and you have signed a separate indemnification agreement.
<br>
Cypress, the Cypress logo, and combinations thereof, ModusToolbox, PSoC, CAPSENSE, EZ-USB, F-RAM, and TRAVEO are trademarks or registered trademarks of Cypress or a subsidiary of Cypress in the United States or in other countries. For a more complete list of Cypress trademarks, visit www.infineon.com. Other names and brands may be claimed as property of their respective owners.
