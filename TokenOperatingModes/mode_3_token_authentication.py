import spidev
import RPi.GPIO as GPIO
import time
import atexit
from typing import List

# === Configuration (BCM numbering) ===
SPI_BUS = 0          # /dev/spidev0.0
SPI_DEV = 0
SPI_MAX_HZ = 10_000_000
SPI_MODE = 0

# Use a free GPIO for manual CS (avoid BCM8/BCM7 unless you disable hardware CS)
CS_BCM = 22

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_BCM, GPIO.OUT, initial=GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEV)
spi.max_speed_hz = SPI_MAX_HZ
spi.mode = SPI_MODE

def cleanup():
    try: GPIO.output(CS_BCM, GPIO.HIGH)
    except Exception: pass
    try: spi.close()
    except Exception: pass
    try: GPIO.cleanup(CS_BCM)
    except Exception: pass

atexit.register(cleanup)

# === CS helpers ===
def set_cs_low():  GPIO.output(CS_BCM, GPIO.LOW)
def set_cs_high(): GPIO.output(CS_BCM, GPIO.HIGH)

# === SPI transfer (manual CS) ===
def spi_transfer(tx: List[int]) -> List[int]:
    set_cs_low()
    time.sleep(0.00001)        # ~10 µs guard time
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

def hex_char_to_byte_pair(hex_str: str):
    """Convert hex string (even length) into list of byte ints."""
    if len(hex_str) % 2 != 0:
        # pad a trailing nibble if needed
        hex_str += "0"
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

# === Authentication ===
def authentication(cw_hex: str):
    # Normalize CW to 64 hex chars (256 bits), right-pad with zeros if shorter, truncate if longer
    cw_hex = (cw_hex or "").lower()
    if len(cw_hex) < 64:
        cw_hex = cw_hex.ljust(64, "0")
    elif len(cw_hex) > 64:
        cw_hex = cw_hex[:64]
    cw_bytes = hex_char_to_byte_pair(cw_hex)[:32]  # 32 bytes

    # Build 160-byte frame
    tx = [0x03, 0x00, 0x08, 0x00, 0x00] + [0x00] * (160 - 5)
    tx[5:5+32] = cw_bytes  # insert challenge word

    rx = spi_transfer(tx)

    # Extract fields from response
    # (same byte ranges as your Pi 5 code)
    tid = ''.join(f"{b:02x}" for b in rx[5:37])    # bytes 5–36 inclusive
    cw  = ''.join(f"{b:02x}" for b in rx[38:70])   # bytes 38–69
    rw  = ''.join(f"{b:02x}" for b in rx[71:87])   # bytes 71–86

    print("TID:", tid)
    print("CW :", cw)
    print("RW :", rw)

if __name__ == "__main__":
    # Example CW (64 hex characters = 256 bits)
    example_cw = "0123456789abcdef" * 4
    authentication(example_cw)
