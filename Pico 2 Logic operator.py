#Code for second pico to interpret data structure before sending correcting or code terminating signals

from machine import UART, Pin
import time

#defined serial communication variables
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1, txbuf=64, rxbuf=64, timeout=2000)

#bool for engaging loop
Matches = False

#while loop should terminate when average wave value is within 1% of desired
while True:
    #how to determine this is desired value?
    #simulated binary input
    data1 = b'\x15'
    #convert this into type int
    desired_rate = int.from_bytes(data1, byteorder='big')
    print(desired_rate)
    #waiting to differentiate between desired and measured
    time.sleep(1)
    while not Matches:
        #stores X# of bits, enough to define the digits in a PCM wave, shorter=better
        #storage buffer for input, method from stack overflow
        buffer = bytearray(8)
        given_rate = int.from_bytes(buffer, byteorder='big')
        print(given_rate)
        if given_rate != 0:
            if given_rate == desired_rate:
                Matches = True
                #sends confirmation to other Pico
                uart.write(Matches)
            else:
                #math for difference
                correction =  given_rate - desired_rate
                #sends correction to other Pico
                uart.write(bytes([correction]))
        else:
            #delays to not overload buffer
            time.sleep(1)
            continue


