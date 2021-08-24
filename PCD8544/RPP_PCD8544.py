import machine
import utime
from PCD8544_Font import PCD8544_Fonts

GLCD_WIDTH	= 84
GLCD_HEIGHT	= 48

spi_sck      = machine.Pin(2)
spi_tx       = machine.Pin(3)
reset        = machine.Pin(13, machine.Pin.OUT)
chip_enable  = machine.Pin(14, machine.Pin.OUT)
data_command = machine.Pin(15, machine.Pin.OUT)

spi = machine.SPI(0, baudrate = 100000, sck = spi_sck, mosi = spi_tx)

def GLCD_command_write(data):    
    # Select command register (D/C = 0)
    data_command.value(0)
    chip_enable.value(0)
    spi.write(data)
    chip_enable.value(1)

def GLCD_data_write(data):
    # Select data register (D/C = 1)
    data_command.value(1)
    chip_enable.value(0)
    for i in data:
        spi.write(str(i))
    chip_enable.value(1)

def GLCD_init():
    reset.value(0)
    reset.value(1)
    GLCD_command_write('\x21')    
    GLCD_command_write('\x90')
    GLCD_command_write('\x20')
    GLCD_command_write('\x0C')
    GLCD_command_write('\x80')
    GLCD_command_write('\x40')
    for i in range(GLCD_WIDTH * GLCD_HEIGHT):
        GLCD_data_write('\x00')

def GLCD_send_string(str):
    str2 = list(str)
    for i in str2:
        GLCD_data_write(PCD8544_Fonts[ord(i)-32])
        
GLCD_init()
GLCD_send_string("Raspberry Pi")
utime.sleep(4)

GLCD_command_write('\x80')
GLCD_command_write('\x40')
for i in range(GLCD_WIDTH * GLCD_HEIGHT):
    GLCD_data_write('\x00')

GLCD_send_string("RP2040 Microcontroller") 
