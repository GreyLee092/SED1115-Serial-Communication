#Code for second pico to interpret data structure before sending correcting or code terminating signals

from machine import UART, Pin
import time

#defined serial communication variables
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1, txbuf=64, rxbuf=64, timeout=2500)

#bool for engaging loop
Matches = False

#=============================================================================
#to_write = '12345'
#uart.write(str(to_write))
#time.sleep_ms(100)
#=============================================================================

def reading():
    # Gemini sourced
    buffer = bytearray(8)
    while True:
        if uart.any():
            print('p')
            bytes_read = uart.readinto(buffer)
            if bytes_read:
                print('e')
                # convert this into type int
                rate = int(buffer[:bytes_read].decode("utf-8"))
                break
    # waiting to differentiate between desired and measured
    time.sleep(1)
    return rate


while True:
    desired_rate = reading()
    print(desired_rate, type(desired_rate))
    while not Matches:
        #stores X# of bits, enough to define the digits in a PCM wave, shorter=better
        #storage buffer for input, method from stack overflow
        #given_rate = int.from_bytes(buffer, 'big')
        #buffer = b'\x00' * len(buffer)
        given_rate = reading()
        print(given_rate, type(given_rate))
        if given_rate == desired_rate:
            Matches = True
            #sends confirmation to other Pico
            uart.write(str(Matches))
            break
        else:
            #math for difference
            print('gR =', given_rate, 'dR =', desired_rate)
            correction = abs(desired_rate - given_rate)
            print('correction =', correction)
            uart.write(str(correction))
            #sends correction to other Pico
    if Matches:
        print('complete')
        break
