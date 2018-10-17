import spidev
import time 
import numpy as np

def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()

if __name__ == "__main__":
    spi = spidev.SpiDev()
    spi.open(0,0)

#settings
    spi.max_speed_hz = 7800000
    spi.mode = 0b00
    #spi.bits_per_word = 8
    resp4 = spi.xfer2([0x81,0x08])
    resp5 = spi.xfer2([0x88,0x20])
    resp6 = spi.xfer([0x89,0x80])
    resp = spi.xfer2([0x8B,0x03])
    resp7 = spi.xfer2([0x90,0xFF])
    resp1 = spi.xfer2([0x9C,0x02])
    resp2 = spi.xfer2([0x9e,0x0A])
    print(BytesToHex(resp))
    print(BytesToHex(resp1))
    print(BytesToHex(resp2))
    time.sleep(1)
    spi.close()
