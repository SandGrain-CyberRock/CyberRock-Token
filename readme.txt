# CyberRock Token - modes

This script demonstrates how to communicate with the CyberRock Token
over SPI on a Raspberry Pi 5. It implements the 
 - Mode 0 GS1 SGTIN-198
 - Mode 1 Token Identification
 - Mode 3 Token Authentication
 - Mode 5 Host Authentication
 - Mode 6 Host Authentication with Ephemeral Key
 - Mode 7 Token Authentication with Ephemeral Key
 - Mode 255 Built-in Self-Test (BIST)

Initializes SPI0 at 10 MHz, mode 0.

Uses GPIO22 for manual chip-select via gpiod.

Sends a 160-byte command starting with 0x01.

Reads back the response and extracts bytes [5:37] as the TID.

Prints the results as a lowercase hex string.

## Wiring Diagram

Connect the Raspberry Pi GPIO header to the CyberRock Token as follows:

 

Raspberry Pi 5 GPIO (40-pin)              SGT1001 (8-pin, top view)

   (3.3V)  Pin 1  ----------------------->  Pin 8  VDD
   (GND)   Pin 6  ----------------------->  Pin 4  VSS
   (MOSI)  Pin 19 ----------------------->  Pin 5  MOSI
   (MISO)  Pin 21 ----------------------->  Pin 2  MISO
   (SCLK)  Pin 23 ----------------------->  Pin 6  CLK
   (GPIO22, CS) Pin 22 ------------------>  Pin 1  CSN

   Pin 3 (NC)  --- Not Connected
   Pin 7 (NC)  --- Not Connected---

## Requirements

- Raspberry Pi 5 (or compatible with `spidev` and `gpiod`)
- CyberRock Token connected to SPI bus 0, chip-select on **GPIO22**
- Python 3 with the following modules:
  - `spidev`
  - `gpiod`

Install dependencies:

```bash
sudo apt-get install python3-spidev python3-libgpiod