#based on adc-pwm lab code
from machine import Pin, PWM, ADC, UART
import time

#defined serial communication variables
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1, txbuf=64, rxbuf=64, timeout=2000)

#analog input pins
adcA = ADC(Pin(26))
adcB = ADC(Pin(27))
#LED pins
led1 = PWM(Pin(18))
led2 = PWM(Pin(16))
led3 = PWM(Pin(17))
#LED frequency to see blinking
led1.freq(20)
led2.freq(20)
led3.freq(20)

#Input variable
freq_user_input = ''
#Bool to end loop
matches = False
#Buffer to store data communicated
buffer = bytearray(16)

#while loop prompting an input frequency
while freq_user_input != 'y':
    input('Set desired frequency with left dial and press enter')
    desired_value = adcB.read_u16()
    freq_user_input = input(f'Is {desired_value} correct? y/n')
    if freq_user_input == 'n':
        print('Adjust frequency and try again.')
    #Sends target frequency to Pico Board 2
    elif freq_user_input == 'y':
        uart.write(desired_value)
        led1.duty_u16(desired_value)
        #Sleep to ensure data isn't mixed
        time.sleep_ms(100)
        break
    else:
        print('enter valid input')

#Setting frequency to be adjusted
input('Set frequency with right dial and press enter')
wave_value = adcA.read_u16()
print(wave_value)
while not matches:
    #lights up LED for user comparison
    led2.duty_u16(wave_value)
    #sends wave value to be compared on Pico Board 2
    uart.write(wave_value)
    #Waits for response
    time.sleep_ms(100)
    if uart.txdone():
        print('sent\n')
    #Reads input from Pico Board 2
    return_value = uart.read(8)
    print(return_value)
    #if type returned is boolean, will end program
    if return_value == type(bool):
        matches = True
        break
    #if type returned is int, it will keep looping until returned type is a boolean
    elif return_value == type(int):
        #gets int value from bytes
        difference = int.from_bytes(buffer, byteorder='big')
        wave_value = difference - wave_value
        #clears buffer for next loop
        buffer.clear()
print('complete')
#LEDs 16 & 17 should be blinking at the same rate
led3.duty_u16(wave_value)
