# SandGrain Device Identification Script

This script retrieves and displays the **Token ID (TID)** of a SandGrain hardware token.  
It is used as a basic identification and verification step in the CyberRock / SandGrain IoT security suite.

---

## 🚀 Features

- Initializes GPIO interface for token communication  
- Connects to the SandGrain Token hardware  
- Retrieves the device’s unique Token ID (TID)  
- Prints the TID to the console for verification

---

## ⚙️ Workflow Overview

1. **Initialize GPIO:** Configures Raspberry Pi GPIO pins for token communication.  
2. **Retrieve TID:** Uses the SandGrain Token API to read the hardware token’s identifier.  
3. **Display Result:** Prints the TID to the console for logging or registration purposes.

---

## 📁 Project Structure

```
identification.py
/home/pi/SandGrain/SandGrainSuite_DeviceAPI/
├── CyberRock_Cloud.py
├── CyberRock_Token.py
└── SandGrain_Credentials.py
```

> ⚠️ The script depends on the SandGrain Suite Device API modules. Make sure the import path is correctly set.

---

## 🧠 Requirements

### Hardware
- Raspberry Pi (any model with GPIO support)  
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
python3 identification.py
```

**Example Output:**
```
TID: 123456789ABCDEF
```

This confirms that the SandGrain Token was successfully detected and its unique ID retrieved.

---

## 🧩 Functions Summary

| Function | Description |
|-----------|-------------|
| `gpio_setup()` | Configures Raspberry Pi GPIO pins for communication with the token. |
| `listToInt(lst)` | Converts a list of bytes to an integer. |
| `intToList(number)` | Converts an integer to a list of bytes for SPI communication. |
| `main()` | Executes GPIO setup, retrieves TID, and prints it to the console. |

---

## 🔐 Credentials

The following credentials file must exist but is **not directly used** in this script:  
`SandGrain_Credentials.py` — it ensures compatibility with other SandGrain scripts in the same suite.

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
