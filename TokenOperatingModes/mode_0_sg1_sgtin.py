import spidev
import gpiod
import time

# === SPI setup ===
spi = spidev.SpiDev()
spi.open(0, 0)              # Bus 0, Device 0
spi.max_speed_hz = 10_000_000
spi.mode = 0

# === GPIO setup for CS pin ===
chip = gpiod.Chip("gpiochip4")
CS_LINE_OFFSET = 22
cs_line = chip.get_line(CS_LINE_OFFSET)
cs_line.request(consumer="spi-cs", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[1])

def set_cs_low():  cs_line.set_value(0)
def set_cs_high(): cs_line.set_value(1)

def spi_transfer(tx):
    set_cs_low()
    time.sleep(0.00001)
    rx = spi.xfer2(tx)
    time.sleep(0.00001)
    set_cs_high()
    return rx

# === Identification ===
def identification():
    tx = [0x00, 0x00, 0x00, 0x00] + [0x00] * 156   # total length = 160
    rx = spi_transfer(tx)
    sgtin = ''.join(f"{b:02x}" for b in rx[5:30])    # bytes 5–30
    print("SGTIN:", sgtin)

if __name__ == "__main__":
    identification()
