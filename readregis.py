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
            
    resp = spi.xfer2([0x01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    #resp = spi.xfer2([0x9E,0x08])
    print(BytesToHex(resp))
    time.sleep(1)
    spi.close()
