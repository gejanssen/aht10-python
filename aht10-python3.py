# -*- coding: utf-8 -*-
#!/usr/bin/python3
# https://github.com/Thinary/AHT10/blob/master/src/Thinary_AHT10.cpp
# https://myhydropi.com/raspberry-pi-i2c-temperature-sensor
# cleaned up and documented smbus 1 and some errors
# GJ 03-2020
# i2cdetect -y 0
import smbus
import time

# Get I2C bus
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

config = [0x08, 0x00]
bus.write_i2c_block_data(0x38, 0xE1, config)
time.sleep(0.5)
byt = bus.read_byte(0x38)
#print(byt&0x68)
MeasureCmd = [0x33, 0x00]
bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
time.sleep(0.5)
data = bus.read_i2c_block_data(0x38,0x00)
#print(data)
temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
ctemp = ((temp*200) / 1048576) - 50
print(u'Temperature: {0:.1f}°C'.format(ctemp))
tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
#print(tmp)
ctmp = int(tmp * 100 / 1048576)
print(u'Humidity: {0}%'.format(ctmp))
