# SandGrain Sensor Data Authentication Suite

This suite of scripts enables **secure creation and verification of sensor data** using the SandGrain Token and CyberRock Cloud APIs.  
It ensures each data record is cryptographically bound to a specific hardware token, providing integrity and authenticity validation for IoT sensor data.

---

## 🚀 Overview

The Sensor Data Authentication workflow involves three main steps:

1. **Create Sensor Data:** Generate a sensor data JSON file and compute a hardware-based authentication tag (HRW).  
2. **Local Verification:** Verify the generated data locally using the CyberRock Cloud API (HRW validation).  
3. **Cloud Verification:** Perform full priority authentication via the CyberRock Cloud to confirm end-to-end authenticity.

---

## 🧱 Components

| Script | Description |
|---------|-------------|
| `CreateSensorData.py` | Generates sensor data and signs it with the SandGrain Token using HRW. |
| `LocalVerifySensorData.py` | Verifies the HRW tag locally against the CyberRock Cloud. |
| `VerifySensorData.py` | Performs complete authentication using a high-level host verification endpoint. |
| `test.json` | Example JSON file containing a signed sensor data record. |

---

## ⚙️ Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)  
- SandGrain Token (hardware secure element)

### Software
Install required dependencies:

```bash
sudo apt-get install python3-rpi.gpio
pip install python-periphery requests
```

Ensure these files exist in your environment:
```
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

---

## 🔐 Credential Configuration

Edit the `SandGrain_Credentials.py` file to include your CyberRock Cloud credentials:

```python
cloudflaretokens = "<your_cloudflare_token>"
iotusername = "<your_iot_username>"
iotpassword = "<your_iot_password>"
```

Keep this file **confidential**.

---

## 💻 Step-by-Step Implementation

### **1️⃣ Create Sensor Data**

This script generates a new JSON data record tied to the token’s TID (Token ID) and includes a hardware-based authentication tag (HRW).

Run:
```bash
python3 CreateSensorData.py <filename_without_extension>
```

Example:
```bash
python3 CreateSensorData.py test
```

**Example Output:**
```json
{
    "name": "test.json",
    "TID": "8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c",
    "date": "Tue 28 Oct 2025 14 50 48",
    "HRW": "00244a764956ca2b3f5037a1f9a7ee14"
}
```

This file (`test.json`) now represents **authenticated sensor data**.

---

### **2️⃣ Local Verification**

Locally verify the authenticity of the generated JSON data against the CyberRock Cloud HRW records.

Run:
```bash
python3 LocalVerifySensorData.py <filename_without_extension>
```

Example:
```bash
python3 LocalVerifySensorData.py test
```

**Expected Output:**
```
Sensor Data authenticated
```

If any field or tag has been tampered with, you’ll see:
```
Sensor Data not authentic!
```

---

### **3️⃣ Cloud Verification (Priority Host Authentication)**

For full remote verification (e.g., during server-side processing), use the **VerifySensorData** script.

Run:
```bash
python3 VerifySensorData.py <filename_without_extension>
```

Example:
```bash
python3 VerifySensorData.py test
```

**Expected Output:**
```
Sensor Data authenticated
```

If verification fails:
```
Sensor Data not authentic!
```

---

## 🧩 File Flow Summary

| Step | Script | Input | Output | Purpose |
|------|---------|--------|---------|----------|
| 1️⃣ | CreateSensorData.py | — | `test.json` | Generates signed sensor data. |
| 2️⃣ | LocalVerifySensorData.py | `test.json` | Console Output | Verifies data integrity and HRW tag. |
| 3️⃣ | VerifySensorData.py | `test.json` | Console Output | Confirms authenticity via full cloud check. |

---

## 🧠 Implementation Notes

- The **HRW tag** is unique to each data record and linked to the device’s TID.  
- Even minor modifications to the JSON file will invalidate the HRW.  
- Cloud verification requires valid credentials and an active connection.  
- These scripts can easily integrate into sensor data logging systems to ensure **end-to-end authenticity**.

---

## 🧰 Example Workflow

1. Generate authenticated sensor data:
   ```bash
   python3 CreateSensorData.py temperature_log
   ```
2. Verify locally:
   ```bash
   python3 LocalVerifySensorData.py temperature_log
   ```
3. Perform full cloud verification:
   ```bash
   python3 VerifySensorData.py temperature_log
   ```

---

## 🛠️ Author

**Your Name**  
SandGrain Cybersecurity / IoT Data Integrity Team  
📧 your.email@example.com  

---

## 📝 License

This project is proprietary and intended for internal use within the SandGrain suite ecosystem.  
Do not distribute or modify without authorization.

---
