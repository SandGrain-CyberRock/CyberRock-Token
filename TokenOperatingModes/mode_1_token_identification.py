import spidev
import RPi.GPIO as GPIO
import time
import atexit

# === Configuration ===
SPI_BUS = 0        # /dev/spidev0.0
SPI_DEV = 0
SPI_MAX_HZ = 10_000_000
SPI_MODE = 0

# Manual Chip-Select pin (BCM numbering)
CS_BCM = 22        # <-- change if you wired CS to another pin

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_BCM, GPIO.OUT, initial=GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEV)
spi.max_speed_hz = SPI_MAX_HZ
spi.mode = SPI_MODE

def cleanup():
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

# === Chip Select Control ===
def set_cs_low():  GPIO.output(CS_BCM, GPIO.LOW)
def set_cs_high(): GPIO.output(CS_BCM, GPIO.HIGH)

# === SPI Transfer ===
def spi_transfer(tx):
    set_cs_low()
    time.sleep(0.00001)           # small guard delay (~10 µs)
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

# === Identification ===
def identification():
    tx = [0x01, 0x00, 0x00, 0x00] + [0x00] * 156   # total length = 160
    rx = spi_transfer(tx)
    tid = ''.join(f"{b:02x}" for b in rx[5:37])    # bytes 5–36
    print("TID:", tid)

if __name__ == "__main__":
    identification()
