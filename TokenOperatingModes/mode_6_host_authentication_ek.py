import spidev
import RPi.GPIO as GPIO
import time
import atexit

# === Configuration (BCM numbering) ===
SPI_BUS = 0          # /dev/spidev0.0
SPI_DEV = 0
SPI_MAX_HZ = 10_000_000
SPI_MODE = 0

# Use a free GPIO for manual CS (avoid BCM8/BCM7 unless hardware CS is disabled)
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
def spi_transfer(tx):
    set_cs_low()
    time.sleep(0.00001)        # ~10 µs guard time
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

def hex_char_to_byte_pair(hex_str):
    """Convert hex string (even length) into list of byte ints."""
    if len(hex_str) % 2 != 0:
        hex_str += "0"
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

# === Authentication + Ephemeral Key ===
def generate_ephemeral_key(cw_hex: str):
    # Normalize to exactly 64 hex chars (256 bits)
    hcw_hex = (cw_hex or "").lower()
    if len(hcw_hex) < 64:
        hcw_hex = hcw_hex.ljust(64, "0")
    elif len(hcw_hex) > 64:
        hcw_hex = hcw_hex[:64]
    hcw_bytes = hex_char_to_byte_pair(hcw_hex)[:32]

    # Build 160-byte frame (first byte 0x06 per your comment)
    tx = [0x06, 0x00, 0x08, 0x00, 0x00] + [0x00] * (160 - 5)
    tx[5:5+32] = hcw_bytes

    # Send & receive
    rx = spi_transfer(tx)

    # Extract fields
    tid = ''.join(f"{b:02x}" for b in rx[5:37])      # bytes 5–36
    hrw = ''.join(f"{b:02x}" for b in rx[71:87])     # bytes 71–86
    ek  = ''.join(f"{b:02x}" for b in rx[87:103])    # next 16 bytes

    # Print results
    print("TID :", tid)
    print("HCW :", hcw_hex)
    print("HRW :", hrw)
    print("EK  :", ek)

if __name__ == "__main__":
    # Example dummy CW (64 hex characters = 256 bits)
    dummy_hcw = "0123456789abcdef" * 4
    generate_ephemeral_key(dummy_hcw)
