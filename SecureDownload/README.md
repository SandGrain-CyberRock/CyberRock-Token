# SandGrain File Integrity Tagging and Verification System

This set of scripts provides a simple and secure way to **generate and verify hardware-based authentication tags (HRW)** for files using the SandGrain Token and CyberRock Cloud API.  
It ensures downloaded or transferred files have not been tampered with and that they originate from a trusted device.

---

## 🚀 Overview

The system uses **Host Read/Write (HRW) tags** derived from cryptographic hashes and verified by the SandGrain hardware token.  
It follows a two-step process:

1. **Generate HRW tag** for any file (e.g., firmware, kernel, or binary).  
2. **Verify HRW tag** to confirm file authenticity and integrity.

---

## 🧱 Components

| Script | Description |
|---------|-------------|
| `CreateFileHRWtag.py` | Generates an HRW tag and JSON record for a specified file. |
| `VerifyFileHRWtag.py` | Verifies a file’s integrity and HRW tag from the JSON record. |
| `kernel.img` | Example file used for testing. |
| `kernel.json` / `test.json` | Example JSON metadata files produced by `CreateFileHRWtag.py`. |

---

## ⚙️ Hardware & Software Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)  
- SandGrain Token (hardware secure element)

### Software Dependencies
Install required Python packages:

```bash
sudo apt-get install python3-rpi.gpio
pip install python-periphery requests
```

Ensure you have the following local modules installed under:
```
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

---

## 🔐 Credentials

Before running the scripts, configure `SandGrain_Credentials.py` with valid credentials:

```python
cloudflaretokens = "<your_cloudflare_token>"
iotusername = "<your_iot_username>"
iotpassword = "<your_iot_password>"
```

Keep this file private — it allows cloud authentication.

---

## 💻 Step-by-Step Implementation

### **1️⃣ Generate a Secure HRW Tag**

To create a file authentication tag and metadata JSON:

```bash
python3 CreateFileHRWtag.py <file_to_protect> <output_json_name_without_extension>
```

#### Example:
```bash
python3 CreateFileHRWtag.py kernel.img test
```

**Output:** A new file named `test.json` containing the secure HRW tag and metadata.

#### Example JSON output:
```json
{
    "downloadname": "kernel.img",
    "filehash": "a503898ef03e6433f3283e984a37e442081f6bff4ac729cf3a8bffc84c53a726",
    "JSONname": "test.json",
    "TID": "8000000000000000000000000000002498705fdfed23805e018e7e1e6e087b3c",
    "date": "Tue 28 Oct 2025 14 51 45",
    "HRW": "a3ddf2f4616fa7a81f5f75e88294417b"
}
```

This metadata ties the file to the device (via `TID`) and its exact binary contents (via SHA‑256 hash).

---

### **2️⃣ Verify the File’s HRW Tag**

To confirm that the file and metadata match and have not been altered:

```bash
python3 VerifyFileHRWtag.py <json_name_without_extension>
```

#### Example:
```bash
python3 VerifyFileHRWtag.py test
```

**Example Output:**
```
Downloaded Filename matches
JSON Filename matches
TID matches
File hash matches
Authentication tag matches
Secure download successful
```

If any element has changed (file content, name, TID, or tag), you’ll see:
```
Secure download failed!
```

---

## 🧩 File Verification Flow

| Step | Input | Output | Description |
|------|--------|---------|-------------|
| 1️⃣ CreateFileHRWtag | File (e.g., kernel.img) | `<filename>.json` | Computes SHA‑256 hash and HRW tag. |
| 2️⃣ VerifyFileHRWtag | File + JSON | Console Result | Validates file name, TID, hash, and HRW tag. |

---

## 🧠 Notes for Implementation

- The **HRW tag** is unique to both the device (TID) and file contents.  
- Even a one‑byte change in the file will cause verification to fail.  
- Always keep the `.json` file alongside its corresponding binary for future validation.  
- You can rename the JSON output, but keep the link between file and tag intact.

---

## 🧰 Example Test Workflow

1. Create a sample text file:
   ```bash
   echo "test data" > test.txt
   ```
2. Generate tag:
   ```bash
   python3 CreateFileHRWtag.py test.txt testdata
   ```
3. Verify tag:
   ```bash
   python3 VerifyFileHRWtag.py testdata
   ```
4. Modify the file and verify again — you should see a failure message.

---

## 🛠️ Author

**Your Name**  
SandGrain Cybersecurity / IoT File Integrity Team  
📧 your.email@example.com  

---

## 📝 License

This project is proprietary and intended for internal use within the SandGrain suite ecosystem.  
Do not distribute or modify without authorization.

---
