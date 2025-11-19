# CyberRock Token Operating Modes – Raspberry Pi 4 (Python)

This guide shows how to run the **CyberRock Token (SGT1001) operating modes** on a **Raspberry Pi 4** using Python.  
It includes the full wiring information, setup steps, and explanations for each operating mode.

---

## 🔌 Hardware Setup – Wiring the CyberRock Token to Raspberry Pi 4

The CyberRock Token communicates with the Raspberry Pi 4 through the SPI0 interface at **10 MHz**, **mode 0**, using a manual **chip‑select (CS)** on **GPIO 22**.

### Wiring Connections

| Raspberry Pi 4 Pin | GPIO | Token Pin | Description |
|--------------------|-------|------------|-------------|
| 17 | 3.3 V | 8 | Power Supply |
| 25 | GND | 4 | Ground |
| 19 | GPIO 10 | 5 | SPI MOSI |
| 21 | GPIO 9 | 2 | SPI MISO |
| 23 | GPIO 11 | 6 | SPI CLK |
| 15 | GPIO 22 | 1 | Manual CS (CSN) |

### Notes

- Only one SPI device should be connected to SPI0 at a time unless you manage multiple CS lines.  
- The **manual chip select** (GPIO 22) is toggled in software by the example scripts.  
- SPI must be enabled on the Pi (`sudo raspi-config` → Interface Options → SPI → Enable).

---

## ⚙️ Software Setup

Install dependencies:

```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-rpi.gpio python3-spidev
pip3 install python-periphery requests
```

Ensure you have the supporting modules either in the same folder or under `/home/pi/SandGrain/SandGrainSuite_DeviceAPI/`:

- `CyberRock_Cloud.py`
- `CyberRock_Token.py`
- `SandGrain_Credentials.py`

---

## 🧠 General Notes

- All scripts communicate over SPI0 at 10 MHz, Mode 0, with GPIO 22 as manual CS.  
- Each mode transmits a 160‑byte frame and reads a 160‑byte response.  
- Run only one mode script at a time.  
- Ensure the token is powered before executing any script.

---

## 🔢 Operating Modes Overview

### Mode 0 – GS1 SGTIN‑198

**Script:** `mode_0_sg1_sgtin.py`  
**Purpose:** Reads the GS1 SGTIN identifier stored in the token and prints it as hex.  
**Run:**
```bash
python3 mode_0_sg1_sgtin.py
```
**Output Example:**
```
SGTIN: 303436...abcd
```

---

### Mode 1 – Token Identification

**Script:** `mode_1_token_identification.py`  
**Purpose:** Requests identification and prints the **TID** (Token ID).  
**Run:**
```bash
python3 mode_1_token_identification.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
```

---

### Mode 3 – Token Authentication (CW → RW)

**Script:** `mode_3_token_authentication.py`  
**Purpose:** Performs a Challenge–Response authentication using a Challenge Word (CW) and Response Word (RW).  
**How it works:** Sends CW to the token → token returns RW → printed to console.  
**Run:**
```bash
python3 mode_3_token_authentication.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
CW:  00112233445566778899aabbccddeeff...
RW:  aabbccddeeff00112233445566778899...
```

---

### Mode 5 – Host Authentication (HCW → HRW)

**Script:** `mode_5_host_authentication.py`  
**Purpose:** Sends a Host Challenge Word (HCW) to the token and computes a Host Response Word (HRW).  
**Run:**
```bash
python3 mode_5_host_authentication.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
HCW: 00112233445566778899aabbccddeeff...
HRW: 112233445566778899aabbccddeeff00...
```

---

### Mode 6 – Host Authentication with Ephemeral Key (HCW → HRW, EK)

**Script:** `mode_6_host_authentication_ek.py`  
**Purpose:** Performs host authentication plus ephemeral key generation.  
**Run:**
```bash
python3 mode_6_host_authentication_ek.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
HCW: 00112233445566778899aabbccddeeff...
HRW: aabbccddeeff00112233445566778899...
EK:  7f91a2d9e35e4b62a1b5d3f9e4c0...
```

---

### Mode 7 – Token Authentication with Ephemeral Key (CW → RW, EK)

**Script:** `mode_7_token_authentication_ek.py`  
**Purpose:** Performs token authentication and ephemeral key generation in one operation.  
**Run:**
```bash
python3 mode_7_token_authentication_ek.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
CW:  00112233445566778899aabbccddeeff...
RW:  aabbccddeeff00112233445566778899...
EK:  7f91a2d9e35e4b62a1b5d3f9e4c0...
```

---

### Mode 255 (0xFF) – Built‑In Self Test (BIST)

**Script:** `mode_255_bist.py`  
**Purpose:** Executes the token’s built‑in self‑test and reports TID, BRW, BEK, and Result.  
**Run:**
```bash
python3 mode_255_bist.py
```
**Output Example:**
```
TID: 8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c
BRW: 4d7f2a6d9a85b...
BEK: 7a8f3d4c91ee...
Result: 00  (Pass)
```

---

## 🧩 Implementation Tips

- Always enable SPI before running these scripts.  
- Power the token through the Pi’s 3.3 V rail only (never 5 V).  
- Run one mode script at a time.  
- A stable 3.3 V supply is essential for accurate responses.  
- If communication fails, verify MOSI/MISO orientation and CS pin logic.

---

## 🧰 Summary

Each **mode script** demonstrates a specific token operation available through the CyberRock API and hardware command set.  
These scripts are ideal for validation, testing, and hardware bring‑up before integrating cloud‑based workflows.

---

## 🛠️ Author

**Your Name**  
SandGrain Cybersecurity / IoT Token Development Team  
📧 your.email@example.com

---

## 📝 License

This project is proprietary and intended for internal use within the SandGrain suite ecosystem.  
Do not distribute or modify without authorization.

---
