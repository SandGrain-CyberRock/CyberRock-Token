# CyberRock Ephemeral Key Authentication Script

This script facilitates **ephemeral key (EK) authentication** for a SandGrain-based IoT device using the CyberRock Cloud API and Token API.  
It securely generates and verifies a short-lived key (ephemeral key) between the device token and the cloud, ensuring secure and transient authentication sessions.

---

## 🚀 Features

- Initializes GPIO communication with SandGrain Token hardware  
- Retrieves the device TID (Token ID)  
- Logs into the CyberRock Cloud using device credentials  
- Performs token challenge–response exchange for ephemeral key generation  
- Validates and prints both local and cloud-generated ephemeral keys for verification

---

## ⚙️ Workflow Overview

1. **Setup GPIO** communication with the hardware token.  
2. **Retrieve TID** (Token Identifier) from the hardware.  
3. **Authenticate with CyberRock Cloud** using stored credentials.  
4. **Request Challenge Word (CW)** for EK authentication.  
5. **Generate Response Word (RW)** and **Ephemeral Key (EK)** using the token.  
6. **Send RW to Cloud** for validation.  
7. **Verify Cloud-generated EK** against device-generated EK.  

If both keys match, the ephemeral authentication is successful.

---

## 📁 Project Structure

```
ephemeralkey.py
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

> ⚠️ The script depends on these local modules. Make sure the path is correctly set.

---

## 🧠 Requirements

### Hardware
- Raspberry Pi with GPIO support  
- SandGrain Token (hardware security element)

### Software
- Python 3.x  
- `RPi.GPIO`  
- `periphery`  
- `requests`  

Install dependencies:
```bash
sudo apt-get install python3-rpi.gpio
pip install python-periphery requests
```

---

## 💻 Usage

Run the script directly from the command line:

```bash
python3 ephemeralkey.py
```

**Example Output:**
```
EK token:     7f91a2d9e35e4b62a1b5d3f9e4c0...
EK CyberRock: 7f91a2d9e35e4b62a1b5d3f9e4c0...
```

If both values match → Ephemeral key authentication succeeded.

---

## 🧩 Functions Summary

| Function | Description |
|-----------|-------------|
| `gpio_setup()` | Configures Raspberry Pi GPIO pins for token operations. |
| `listToInt(lst)` | Converts a list of bytes to an integer. |
| `intToList(number)` | Converts an integer to a byte-list format for SPI transmission. |
| `main()` | Executes the full EK authentication workflow (cloud login, token challenge, and verification). |

---

## 🔐 Credentials

The following fields are expected in `SandGrain_Credentials.py`:

```python
cloudflaretokens = "<your_cloudflare_token>"
iotusername = "<your_iot_username>"
iotpassword = "<your_iot_password>"
```

Keep your credentials **confidential** and never publish them publicly.

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
