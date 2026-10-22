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

#function reading incoming data into integers
def reading():
    # Gemini sourced
    #buffer created to read off
    buffer = bytearray(8)
    while True:
        # only reads if there's data in buffer and loops here until data is read
        if uart.any():
            # reads into buffer
            bytes_read = uart.readinto(buffer)
            # if data read into buffer, it saves data points from buffer
            if bytes_read:
                #decodes bytes to int
                rate = int(buffer[:bytes_read].decode("utf-8"))
                break
    # waiting to differentiate between desired and measured
    time.sleep(1)
    return rate


while True:
    #waits until data is able to read
    desired_rate = reading()
    while not Matches:
        #waits until scrambled data is read off buffer
        given_rate = reading()
        #if rates are same, bool is switched to kill loop and sent to pico 1 to do the same
        if given_rate == desired_rate:
            Matches = True
            #sends confirmation to other Pico as string
            uart.write(str(Matches))
            break
        #otherwise will measure the difference
        else:
            #math for difference
            print('Given Rate =', given_rate, 'Desired Rate =', desired_rate)
            #calculates absolute difference of values
            correction = abs(desired_rate - given_rate)
            print('correction =', correction)
            #Returns correction value to pico 1 as a string
            uart.write(str(correction))
    #if bool is True, will terminate program
    if Matches:
        print('complete')
        break