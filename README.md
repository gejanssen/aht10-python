# AHT10 python library for Raspberry Pi

Originally found on the internet, somewhere, and it had some errors

[![badge](https://raw.githubusercontent.com/gejanssen/aht10-python/master/images/aht10-raspberrypi-zero.jpg)](https://raw.githubusercontent.com/gejanssen/aht10-python/master/images/aht10-raspberrypi-zero.jpg)


## detect i2c bus for devices

```
gej@rpi-z:~/aht10-python $ i2cdetect -y 1
Error: Could not open file `/dev/i2c-1': Permission denied
Run as root?
gej@rpi-z:~/aht10-python $ 
```

whoops, no rights...

user rights (Adding the current user gej to the i2c group)
Don't forget to logout and login again after this.

## adding user rights

```
gej@rpi-z:~/aht10-python $ cat /etc/group | grep i2c
i2c:x:998:pi
gej@rpi-z:~/aht10-python $ sudo usermod -aG i2c gej
gej@rpi-z:~/aht10-python $ cat /etc/group | grep i2c
i2c:x:998:pi,gej
gej@rpi-z:~/aht10-python $ logout
```


## detect i2c bus for devices


```
gej@rpi-z:~/aht10-python $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- 38 -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --                         
gej@rpi-z:~/aht10-python $ 
```

yess, we found a device on address 38

## Testrun

```
rpi-z:~/aht10-python $ python aht10-python3.py 
Traceback (most recent call last):
  File "aht10-python3.py", line 9, in <module>
    bus = smbus.SMBus(0)
IOError: [Errno 2] No such file or directory
gej@rpi-z:~/aht10-python $


SMBus(0) is not used on a modern raspberry pi (for example a 0)
gej@rpi-z:~/aht10-python $
```

Huh.. Searched a long time for this one. The original code was SMBus(0).
This was for the raspberry pi 1....
Recent versions use SMBus(1) - i2c bus 1

This is allready changed is this version. Error in this document for future debugging.

## Testrun

```
gej@rpi-z:~/aht10-python $ python aht10-python3.py
    bus.write_i2c_block_data(0x38, 0xE1, config)
IOError: [Errno 121] Remote I/O error
gej@rpi-z:~/aht10-python $ 
```

This error happends when the device is not connected or false connected.
Error: Device not connected (false address)

## Testrun

```
gej@rpib42g:~/aht10-python $ sudo python aht10-python3.py 
Traceback (most recent call last):
  File "aht10-python3.py", line 23, in <module>
    data = bus.read_i2c_block_data(0x38,0x00)
IOError: [Errno 121] Remote I/O error
gej@rpib42g:~/aht10-python $ 
```

Hmm, after investigating, it could be a timing issue, 
uncomment the folowing rule:

```
time.sleep(1) #wait here to avoid 121 IO Error
```

Or, for me it was a false connected ground....
As allways, check your wiring.

## Testrun 

```
gej@rpi-z:~/aht10-python $ sudo python aht10-python3.py
Temperature: 22.0C
Humidity: 32%
gej@rpi-z:~/aht10-python $ 
```


Tadaaaaaaa


You're the master.....
