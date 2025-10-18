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

def hex_char_to_byte_pair(hex_str):
    """Convert hex string (64 chars → 32 bytes) into list of ints."""
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

# === Authentication + Ephemeral Key ===
def generate_ephemeral_key(cw_hex: str):
    # Ensure CW is 64 hex chars (256 bits), pad with zeros if shorter
    cw_hex = cw_hex.ljust(64, '0')
    cw_bytes = hex_char_to_byte_pair(cw_hex)

    # Build transmit buffer: NOTE first byte is 0x07
    tx = [0x06, 0x00, 0x08, 0x00, 0x00] + [0x00] * (160 - 5)
    tx[5:5+32] = cw_bytes[:32]

    # Send & receive
    rx = spi_transfer(tx)

    # Extract fields
    tid = ''.join(f"{b:02x}" for b in rx[5:37])
    rw  = ''.join(f"{b:02x}" for b in rx[71:87])
    ek  = ''.join(f"{b:02x}" for b in rx[87:103])  # EK is next 16 bytes

    # Print results
    print("TID     :", tid)
    print("FCW      :", cw_hex)
    print("FRW      :", rw)
    print("EK      :", ek)

if __name__ == "__main__":
    # Example dummy CW (64 hex characters = 256 bits)
    dummy_cw = "0123456789abcdef" * 4
    generate_ephemeral_key(dummy_cw)
