# SandGrain Secure Boot and Firmware Attestation Suite

This set of scripts implements a **Secure Boot and Firmware Attestation process** using the SandGrain Token and CyberRock Cloud platform.  
It verifies the integrity of multiple firmware layers, ensuring that each level is authenticated before the next executes.

---

## 🚀 Overview

The Secure Boot sequence uses **cryptographic chaining** and **hardware-based authentication** to verify that firmware levels (FW1, FW2, FW3) have not been tampered with.  
Each firmware level computes and validates the next one before execution, building an **unbroken chain of trust**.

---

## 🧱 Components

| Script | Description |
|---------|-------------|
| `CreateManifest.py` | Generates a manifest JSON file containing SHA-256 hashes of Firmware Levels 2 and 3. |
| `FirmwareLevel1.py` | First firmware level. Starts the secure boot process and verifies Level 2 before execution. |
| `FirmwareLevel2.py` | Second firmware level. Verifies Level 3 firmware and forwards attestation data. |
| `FirmwareLevel3.py` | Final firmware level. Stores attestation data and regenerates a new initial challenge word. |
| `VerifyAttestationValue.py` | Validates the entire boot chain and attestation value against the CyberRock Cloud. |
| `manifest.json` | Stores precomputed hashes of verified firmware versions. |
| `initialcw.json` | Contains the initial challenge word used in the first boot iteration. |
| `attestationvalue.json` | Stores the output of the full secure boot chain and attestation data. |

---

## ⚙️ Hardware & Software Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)
- SandGrain Token (hardware secure element)

### Software
Install the following dependencies:

```bash
sudo apt-get install python3-rpi.gpio
pip install python-periphery requests
```

Ensure that the following local modules are installed under:
```
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

---

## 🔐 Credential Configuration

Edit `SandGrain_Credentials.py` and add your secure credentials:

```python
cloudflaretokens = "<your_cloudflare_token>"
iotusername = "<your_iot_username>"
iotpassword = "<your_iot_password>"
```

Keep these credentials **private**.

---

## 💻 Step-by-Step Implementation

### **1️⃣ Generate the Firmware Manifest**

Run the following to compute the SHA‑256 hashes of Firmware 2 and 3:

```bash
python3 CreateManifest.py
```

This will create `manifest.json` like:

```json
{
    "FW2hash": "a5a6dfab467a...",
    "FW3hash": "18e4229b5d80..."
}
```

---

### **2️⃣ Prepare the Initial Challenge Word (CW0)**

Before starting the secure boot, ensure `initialcw.json` exists:

```json
{
    "CW0": "c1bfdff7b3285158da5fa084fde05da2bd23221c0642e37d178ee7c1a967d6e3"
}
```

If it doesn’t exist, you can copy an existing one or allow `FirmwareLevel3.py` to generate it after the first run.

---

### **3️⃣ Execute the Secure Boot Chain**

Start with Firmware Level 1:

```bash
python3 FirmwareLevel1.py
```

- **FW1** verifies **FW2** and launches it.  
- **FW2** verifies **FW3** and launches it.  
- **FW3** saves the final attestation data into `attestationvalue.json` and generates a new `initialcw.json` for the next boot.

After successful execution, you should see output similar to:

```
------------------------FW3--------------------------------
Saving Attestation value

{
    "TID": "80000000000000000000000000000024...",
    "initialcw": "72933417c6350584...",
    "FW2hash": "a5a6dfab467ae7f25...",
    "FW3hash": "18e4229b5d8038ea...",
    "attestationvalue": "801974efce843e7f..."
}
```

---

### **4️⃣ Verify Firmware and Attestation with CyberRock Cloud**

After the full secure boot sequence completes, verify everything using:

```bash
python3 VerifyAttestationValue.py
```

This script will:

1. Compare firmware hashes with `manifest.json`
2. Retrieve cloud-based HRW values for verification
3. Confirm the attestation chain with the CyberRock Cloud

✅ **Successful Verification Example:**

```
Secure Boot: Firmware level 2 file hash correct
Secure Boot: Firmware level 3 file hash correct
Secure Boot attestation value authenticated
```

❌ **Failure Example:**

```
Secure Boot failed!
Firmware level 3 file hash incorrect!
```

---

## 🧩 File Generation Flow

| Step | Input | Output | Description |
|------|--------|---------|-------------|
| CreateManifest | Firmware 2 & 3 | `manifest.json` | Records official firmware hashes. |
| Firmware 1 | `initialcw.json` | Intermediate values | Verifies and launches Firmware 2. |
| Firmware 2 | Chaining value | Intermediate RW2 | Verifies and launches Firmware 3. |
| Firmware 3 | Attestation data | `attestationvalue.json`, new `initialcw.json` | Saves results and regenerates CW0. |
| VerifyAttestationValue | `attestationvalue.json`, `manifest.json` | Console output | Confirms entire chain integrity. |

---

## 🧠 Tips for Implementation

- Always run the scripts **in order**: CreateManifest → FirmwareLevel1 → VerifyAttestationValue.  
- If you modify any firmware file, regenerate both `manifest.json` and `initialcw.json`.  
- Keep `attestationvalue.json` safe—it represents the proof of firmware authenticity.  
- To test failure scenarios, manually alter one of the firmware files and rerun verification.

---

## 🛠️ Author

**Your Name**  
SandGrain Cybersecurity / IoT Authentication Team  
📧 your.email@example.com  

---

## 📝 License

This project is proprietary and intended for internal use within the SandGrain suite ecosystem.  
Do not distribute or modify without authorization.

---
