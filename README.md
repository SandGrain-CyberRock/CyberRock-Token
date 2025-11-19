<picture>
  <source media="(prefers-color-scheme: dark)" srcset="image-dark.png" width="300">
  <source media="(prefers-color-scheme: light)" srcset="image-light.png" width="300">
  <img alt="SandGrain Logo" src="image-light.png" width="300">
</picture>

# SandGrain / CyberRock Suite – Raspberry Pi 4 Integration and Implementation Guide

This document provides a complete overview of the **SandGrain CyberRock Security Suite** running on a **Raspberry Pi 4**.  
It covers hardware setup, software environment, and practical use of all included Python scripts for token communication, authentication, secure boot, file integrity, and sensor data verification.

---

## 🔌 Hardware Setup – Connecting the CyberRock Token (SGT1001)

The CyberRock Token communicates with the Raspberry Pi 4 via the SPI interface.  

### Connection Summary

- Raspberry Pi 4 SPI0 bus operates at **10 MHz**, **mode 0** (`/dev/spidev0.0`)
- Manual **chip‑select (CS)** on **GPIO 22**
- Power is supplied via 3.3 V from the Pi

### Wiring

Raspberry Pi 4 GPIO to Token pin connections:

- **Pin 17 (3.3 V)** → Token VDD (Pin 8)  
- **Pin 25 (GND)** → Token VSS (Pin 4)  
- **Pin 19 (BCM 10)** → Token MOSI (Pin 5)  
- **Pin 21 (BCM 9)** → Token MISO (Pin 2)  
- **Pin 23 (BCM 11)** → Token CLK (Pin 6)  
- **Pin 15 (BCM 22)** → Token CSN (Pin 1)**  

Only one SPI device should be connected at a time, or ensure independent CS lines are managed.

---

## ⚙️ Software Environment Setup

### Raspberry Pi 4 Configuration

Enable SPI on your Raspberry Pi 4:
```bash
sudo raspi-config
# Navigate to: Interface Options → SPI → Enable
```

Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-rpi.gpio python3-spidev
pip3 install python-periphery requests
```

---

## 🔐 Credentials Configuration

All scripts depend on valid cloud credentials stored in **SandGrain_Credentials.py**:
These credentails are only available when your Tentant user account has been created by SandGrain.
Please contact support@sandgrain.eu to get a tenant user account.

```python
cloudflaretokens = {'CF-Access-Client-Id': 'your_id', 'CF-Access-Client-Secret': 'your_secret'}
iotusername = 'your_device_username'
iotpassword = 'your_device_password'
```

Keep this file secure and private.

---

## 🧠 Core Device API Modules

These modules provide the foundation for all example scripts:

- **CyberRock_Cloud.py** – Handles all REST API communication with the CyberRock Cloud (login, challenge/response, HRW/EK transactions, verification).  
- **CyberRock_Token.py** – Interfaces with the hardware token via SPI and GPIO to execute cryptographic operations (TID, RW, HRW, EK).  
- **SandGrain_Credentials.py** – Stores your access tokens and IoT credentials for device‑to‑cloud authentication.

These files must reside in `/home/pi/SandGrain/SandGrainSuite_DeviceAPI/`.

---

## 🧩 Overview of Functional Groups

### 1. Device Identification and Authentication

- **identification.py** – Reads and prints the token’s unique TID.  
- **authentication.py** – Performs a full token authentication cycle (CW → RW → verification).  
- **ephemeralkey.py** – Generates and verifies ephemeral session keys between the token and CyberRock Cloud.

### 2. Daisy Chain Authentication

- **CreateDaisyChainData.py** – Produces a multi‑step authentication chain (HCW1, HRW1, HRW2, HRW3) and stores it as JSON.  
- **LocalVerifyDaisyChainData.py** – Validates the chain by checking the final HRW value with the CyberRock Cloud.

### 3. Secure Boot and Firmware Attestation

Implements multi‑stage firmware verification (FW1 → FW2 → FW3) and attestation recording.

- **CreateManifest.py** – Hashes FW2 and FW3 to create `manifest.json`.  
- **FirmwareLevel1.py** – Starts the secure boot sequence and verifies FW2.  
- **FirmwareLevel2.py** – Verifies FW3 and passes attestation data.  
- **FirmwareLevel3.py** – Creates `attestationvalue.json` and regenerates `initialcw.json`.  
- **VerifyAttestationValue.py** – Validates all hashes and attestation values with the CyberRock Cloud.  
Supporting data files: `manifest.json`, `initialcw.json`, `attestationvalue.json`.

### 4. File Integrity Verification

- **CreateFileHRWtag.py** – Generates a hardware‑authenticated hash (HRW) for a file and saves metadata in JSON (filename, SHA‑256, TID, date, HRW).  
- **VerifyFileHRWtag.py** – Rehashes the file and validates it against the saved metadata and HRW.  
Example test files: `kernel.img`, `kernel.json`, `test.json`.

### 5. Sensor Data Authentication

- **CreateSensorData.py** – Creates a signed sensor data JSON record containing TID, timestamp, and HRW.  
- **LocalVerifySensorData.py** – Verifies the sensor data authenticity locally using the CyberRock HRW API.  
- **VerifySensorData.py** – Performs full priority host authentication on the sensor data.

---

## 💻 Typical Implementation Flow (on Raspberry Pi 4)

### Identify your Token
```bash
python3 identification.py
```

### Perform Ephemeral Key Authentication
```bash
python3 ephemeralkey.py
```

### Run Daisy Chain Example
```bash
python3 CreateDaisyChainData.py chain
python3 LocalVerifyDaisyChainData.py chain
```

### Execute Secure Boot Workflow
```bash
python3 CreateManifest.py
python3 FirmwareLevel1.py
python3 VerifyAttestationValue.py
```

### File Tagging and Verification
```bash
python3 CreateFileHRWtag.py kernel.img kernel
python3 VerifyFileHRWtag.py kernel
```

### Sensor Data Workflow
```bash
python3 CreateSensorData.py temperature_log
python3 LocalVerifySensorData.py temperature_log
python3 VerifySensorData.py temperature_log
```

---

## 🧠 Summary

This suite demonstrates the **full SandGrain hardware‑anchored trust chain** on a Raspberry Pi 4:
- Device identification and token‑based authentication  
- Ephemeral session key establishment  
- Multi‑stage firmware secure boot and attestation  
- File integrity proof with HRW tags  
- Sensor data authenticity verification

Each process integrates hardware‑based cryptography (via SandGrain CyberRock Token) with **CyberRock Cloud verification**, achieving an end‑to‑end, tamper‑resistant security model for IoT devices.

---

## 🛠️ Author

**Support**  
SandGrain / IoT Integration Team  
📧 support@sandgrain.eu  

---

## 📝 License

This project is proprietary and intended for internal use within the SandGrain suite ecosystem.  
Do not distribute or modify without authorization.

---
