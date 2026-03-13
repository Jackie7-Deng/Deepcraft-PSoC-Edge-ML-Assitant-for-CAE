---
source_url: "https://developer.imagimob.com/deepcraft-studio/getting-started/infineon-boards/other-infineon-boards"
fetched_at: "2026-03-10T15:51:18Z"
title: "Other Infineon Boards"
content_format: "markdown"
tags: ["deepcraft", "checked-url", "web-mirror", "deepcraft-studio", "getting-started", "infineon-boards"]
---

# Other Infineon Boards

### Other Infineon Development Kits

Listed below are the Infineon boards on which you can deploy the model after building the model using the DEEPCRAFT™ Studio.

#### AURIX™ TC375 Lite Kit

Infineon’s low-cost development board on the AURIX TC375 MCU is ideal for automotive motor control applications. AURIX™ TC375 lite kit is equipped with a 32-Bit Single-Chip AURIX™ TriCoreTM based-Microcontroller AURIX™ TC375. It can be used with a range of development tools including AURIX™ Development Studio, Infineon’s free of charge Eclipse based IDE, or the Eclipse based “FreeEntryToolchain” from Hightec/PLS/Infineon. You can purchase the AURIX™ TC375 Lite Kit, [here](https://www.infineon.com/cms/en/product/promopages/AURIX-microcontroller-boards/low-cost-arduino-kits/aurix-tc375-lite-kit//).

The AURIX™ Audio Shield Board is a flexible extension shield to evaluate different audio applications in conjunction with the AURIX™ TC375 lite kit. You can purchase the KIT\_A2G Audio Shield Board, [here](https://www.infineon.com/cms/en/product/evaluation-boards/kit_a2g_audio_shield/).

|  |
| --- |

#### TRAVEO™ T2G

Infineon offers an extensive range of hardware development kits designed to facilitate the rapid prototyping and evaluation of applications based on the TRAVEO™ T2G MCU. Among these are the **TRAVEO™ T2G Body Entry Lite** and **TRAVEO™ T2G Body High Lite** kits, both of which are fully supported by ModusToolbox™. A code example is provided for each evaluation board.

##### 1. TRAVEO™ T2G Body Entry Lite Kit (KIT_T2G-B-E_LITE)

|  |
| --- |

The TRAVEO™ T2G Body Entry Lite evaluation kit allows you to evaluate and develop applications using the TRAVEO™ T2G Body Entry MCU. ModusToolbox™ software can be used for developing and debugging TRAVEO™ T2G-B-E MCU projects. This kit features the CYT2BL MCU, which includes an ARM® Cortex®-M4 core. Although it lacks a native audio interface, the example project analyzes preloaded audio data stored in the 4 MB code flash memory.

You can purchase the KIT\_T2G-B-E\_LITE [here](https://www.infineon.com/cms/en/product/evaluation-boards/kit_t2g-b-e_lite/).

##### 2. TRAVEO™ T2G Body High Lite Kit (KIT_T2G-B-H-LITE)

|  |
| --- |

The TRAVEO™ T2G Body High Lite evaluation kit allows you to evaluate and develop applications using the TRAVEO™ T2G Body High MCU. ModusToolbox™ software can be used for developing and debugging TRAVEO™ T2G-B-H MCU projects. This kit features the CYT4BF MCU, which includes two ARM® Cortex®-M7 cores and 8 MB of code flash memory. It also has hardware capabilities for audio, supporting I2S and TDM interfaces. For the example project, live data from a microphone is utilized, specifically using the S2GO MEMSMIC IM69D.

You can purchase the KIT\_T2G-B-H-LITE [here](https://www.infineon.com/cms/de/product/evaluation-boards/kit_t2g-b-h_lite/). The S2GO MEMSMIC IM69D is available for purchase [here](https://www.infineon.com/cms/en/product/evaluation-boards/s2go-memsmic-im69d/).

The S2GO MEMSMIC IM69D cannot be directly connected to the S2GO interface of the KIT\_T2G-B-H-LITE due to mismatched I2S pins. An adapter board is required for proper connection. Detailed instructions for creating this adapter board are provided in the relevant section.

#### XMC7200 Evaluation Kit (KIT_XMC72_EVK)

|  |
| --- |

The XMC7200 evaluation kit (KIT\_XMC72\_EVK) enables you to evaluate and develop your applications using the XMC7200D microcontroller. The XMC7200D is designed for industrial applications and is a true programmable embedded system-on-chip, integrating up to two 350-MHz Arm® Cortex®-M7 as the primary application processor, a 100-MHz Arm® Cortex®-M0+ that supports, low-power operations, up to 8 MB flash and 1 MB SRAM, Gigabit Ethernet, CAN FD, Secure Digital Host Controller (SDHC) supporting SD/SDIO/eMMC interfaces and programmable analog and digital peripherals that allow faster time-to-market.

You can purchase the XMC7200 Evaluation Kit [here](https://www.infineon.com/cms/en/product/evaluation-boards/kit_xmc72_evk/).

To learn how to deploy the siren detection machine learning model on Infineon board, using ModusToolbox™ or AURIX™ Development Studio, refer to the respective sections based on the type of board you are using.

- - [Deploy siren detection model on AURIX™ TC375 Lite Kit](https://developer.imagimob.com/deployment/deploy-models-supported-boards/deploy-siren-detection-model-aurix-TC375-lite)
- - [Deploy siren detection model on PSOC™ 6 and PSOC™ Edge boards](https://developer.imagimob.com/deployment/deploy-models-supported-boards/deploy-siren-detection-model-PSoC-boards)
- - [Deploy siren detection model on TRAVEO™ T2G (KIT\_T2G-B-E\_LITE)](https://developer.imagimob.com/deployment/deploy-models-supported-boards/deploy-siren-detection-model-T2G-B-E-lite)
- - [Deploy siren detection model on TRAVEO™ T2G (KIT\_T2G-B-H\_LITE)](https://developer.imagimob.com/deployment/deploy-models-supported-boards/deploy-siren-detection-model-T2G-B-H-lite)
- - [Deploy siren detection model on XMC7200 Evaluation Kit (KIT\_XMC72\_EVK)](https://developer.imagimob.com/deployment/deploy-models-supported-boards/deploy-siren-detection-model-on-XMC7200)
