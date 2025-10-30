import spidev
import RPi.GPIO as GPIO
import time
import atexit

# ========= Config =========
# BCM pin used for manual Chip-Select (change to the pin you wired)
CS_BCM = 22

SPI_BUS = 0   # /dev/spidev0.0
SPI_DEV = 0

SPI_MAX_HZ = 10_000_000
SPI_MODE = 0

# ========= Setup =========
# GPIO (RPi.GPIO uses a single controller on Pi 4)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CS_BCM, GPIO.OUT, initial=GPIO.HIGH)

# SPI
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEV)        # /dev/spidev0.0
spi.max_speed_hz = SPI_MAX_HZ
spi.mode = SPI_MODE

def cleanup():
    # Ensure CS idles high and resources are released
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

# ========= CS helpers =========
def set_cs_low():  GPIO.output(CS_BCM, GPIO.LOW)
def set_cs_high(): GPIO.output(CS_BCM, GPIO.HIGH)

# ========= SPI transfer with manual CS =========
def spi_transfer(tx):
    # tx must be a list/bytes-like of ints [0..255]
    set_cs_low()
    time.sleep(0.00001)           # ~10 µs guard time (adjust if needed)
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

# ========= Your command =========
def identification():
    tx = [0x00, 0x00, 0x00, 0x00] + [0x00] * 156   # total length = 160
    rx = spi_transfer(tx)
    sgtin = ''.join(f"{b:02x}" for b in rx[5:30])  # bytes 5–30
    print("SGTIN:", sgtin)

if __name__ == "__main__":
    try:
        identification()
    except KeyboardInterrupt:
        pass
