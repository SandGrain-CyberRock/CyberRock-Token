import spidev
import RPi.GPIO as GPIO
import time
import atexit

# === Configuration (BCM numbering) ===
SPI_BUS = 0          # /dev/spidev0.0
SPI_DEV = 0
SPI_MAX_HZ = 10_000_000
SPI_MODE = 0

# Manual Chip-Select pin (BCM numbering)
# Use a free GPIO pin (avoid BCM8/BCM7 unless hardware CS is disabled)
CS_BCM = 22

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_BCM, GPIO.OUT, initial=GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEV)
spi.max_speed_hz = SPI_MAX_HZ
spi.mode = SPI_MODE

def cleanup():
    """Release SPI and GPIO on exit."""
    try:
        GPIO.output(CS_BCM, GPIO.HIGH)
    except Exception:
        pass
    try:
        spi.close()
    except Exception:
        pass
    try:
        GPIO.cleanup(CS_BCM)
    except Exception:
        pass

atexit.register(cleanup)

# === CS control ===
def set_cs_low():
    GPIO.output(CS_BCM, GPIO.LOW)

def set_cs_high():
    GPIO.output(CS_BCM, GPIO.HIGH)

# === SPI transfer ===
def spi_transfer(tx):
    set_cs_low()
    time.sleep(0.00001)  # ~10 µs guard time
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

# === Built-In Self Test (BIST) ===
def run_bist():
    # Command 0xFF (BIST), pad to 160 bytes
    tx = [0xFF] + [0x00] * (160 - 1)
    rx = spi_transfer(tx)

    # Extract fields
    tid    = ''.join(f"{b:02x}" for b in rx[5:37])    # bytes 5–36
    brw    = ''.join(f"{b:02x}" for b in rx[38:54])   # 16 bytes
    bek    = ''.join(f"{b:02x}" for b in rx[54:70])   # 16 bytes
    result = ''.join(f"{b:02x}" for b in rx[70:72])   # 2 bytes

    # Print results
    print("TID   :", tid)
    print("BRW   :", brw)
    print("BEK   :", bek)
    print("Result:", result)

if __name__ == "__main__":
    run_bist()
