# CyberRock Device Authentication Script

This script handles authentication for a SandGrain-based IoT device using the **CyberRock Cloud API** and **Token API**.  
It performs secure device login, token authentication, and status verification using hardware-based cryptography and cloud communication.

---

## 🚀 Features

- Initializes GPIO interfaces for token communication  
- Retrieves the device TID (Token ID)  
- Authenticates the device with the CyberRock Cloud  
- Performs token challenge–response authentication  
- Checks authentication transaction status  
- Handles communication between hardware token and cloud services

---

## 📁 Project Structure

```
authentication.py
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

> ⚠️ These modules must be present for the script to function.

---

## 🧠 Requirements

- **Hardware:** Raspberry Pi with GPIO support  
- **Software:**  
  - Python 3.x  
  - `RPi.GPIO`  
  - `periphery`  
  - `requests`  
  - SandGrain Suite Device API (CyberRock modules)

Install dependencies:

```bash
sudo apt-get install python3-rpi.gpio
pip install python-periphery requests
```

---

## ⚙️ Usage

Run the authentication process directly from the command line:

```bash
python3 authentication.py
```

### Example Output

```
123456789ABCDEF
<authentication transaction details>
```

The script will:
1. Initialize GPIO and token interface  
2. Retrieve device TID  
3. Log into the CyberRock Cloud  
4. Execute a token authentication challenge–response  
5. Verify and print the authentication result

---

## 🧩 Functions Overview

| Function | Description |
|-----------|-------------|
| `gpio_setup()` | Initializes GPIO pins for token communication. |
| `listToInt(lst)` | Converts a list of bytes to an integer. |
| `intToList(number)` | Converts an integer into a list of byte values. |
| `main()` | Orchestrates the authentication flow: device login, token challenge, response, and verification. |

---

## 🔐 Credentials

The following fields are expected in `SandGrain_Credentials.py`:

```python
cloudflaretokens = "<your_cloudflare_token>"
iotusername = "<your_iot_username>"
iotpassword = "<your_iot_password>"
```

Keep these credentials **secure** — never commit them to a public repository.

---

## 🧾 Logging & Debugging

You can enable additional logging in the CyberRock modules if needed for debugging network or token communication.

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
