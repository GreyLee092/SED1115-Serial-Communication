#Run Pico 2 Logic operator program before starting Pico 1 PWM module
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
led1 = PWM(Pin(20))
led2 = PWM(Pin(16))
led3 = PWM(Pin(18))
#LED frequency to see blinking
led1.freq(20)
led2.freq(20)
led3.freq(20)

#Bool to end loop
matches = False
#Buffer to store data communicated

#function to read incoming data and format into str
#str and not int for Bool or int return values
def reading():
    # Gemini sourced
    #buffer created to read off
    buffer = bytearray(8)
    while True:
        #only reads if there's data in buffer
        if uart.any():
            #reads into buffer
            bytes_read = uart.readinto(buffer)
            #if data read into buffer, it saves data points from buffer
            if bytes_read:
                #decodes bytes to string
                rate = buffer[:bytes_read].decode("utf-8")
                break

    # waiting to differentiate between desired and measured
    time.sleep(1)
    return rate

#while loop prompting an input frequency
while True:
    #issues of code skipping input prompt, this triggers the skip before important prompts
    input('')
    input('Set desired frequency with left dial and press enter:')
    desired_value = adcB.read_u16()
    freq_user_input = input(f'Is {desired_value} correct? y/n\n')
    #user picks 'n' to go back
    if freq_user_input == 'n':
        print('Adjust frequency and try again.')
    #user picks 'y' to send target frequency to pico 2
    elif freq_user_input == 'y':
        #Sends target frequency to Pico Board 2 as a string
        uart.write(str(desired_value))
        #lights up an LED for visual comparison
        led1.duty_u16(desired_value)
        #Sleep to ensure data isn't mixed
        time.sleep(1)
        break
    #reprompts user if invalid response
    else:
        print('enter valid input')

#Setting 'scrambled' frequency reprompting
while True:
    input('Set desired frequency with right dial and press enter:')
    Wave_value = adcA.read_u16()
    freq_user_input = input(f'Is {Wave_value} correct? y/n\n')
    #user picks 'n' to go back
    if freq_user_input == 'n':
        print('Adjust frequency and try again.')
    #user picks 'y' to send target frequency to pico 2
    elif freq_user_input == 'y':
        #Saves variable for comparison later on
        wave_value = Wave_value
        break
    #reprompts user if invalid response
    else:
        print('enter valid input')
#While loop running communication and adjustments, breaks when target == scrambled
while not matches:
    #lights up LED for user comparison
    led2.duty_u16(wave_value)
    #sends wave value as string to be compared on Pico Board 2
    uart.write(str(wave_value))
    #Waits for response
    time.sleep_ms(100)
    if uart.txdone():
        print('sent\n')
    #Reads input from Pico Board 2
    data_return = reading()
#convert bytes to string before type checking
    # if type returned is boolean, will end program
    if data_return == 'True':
        matches = True
        break
    #if type returned can be typecast int, it will keep looping until returned type is the string 'True'
    else:
        #tries converting string to int
        #if it works, will proceed with adjusting wave
        try:
            # gets int value from bytes
            difference = int(data_return)
            print('∆ =', difference, 'wV =', wave_value)
            #if scrambled value was above the target, it will subtract the absolute difference
            if desired_value < wave_value:
                wave_value = difference - wave_value
            # if scrambled value was below the target, it will add the absolute difference
            elif desired_value > wave_value:
                wave_value = difference + wave_value
        #if fails starts over
        except  ValueError:
            print('TypeError')
#if wave_value == desired_value, program ends
print('complete')
#LEDs 20 & 16 should be blinking at the same rate (red)
led3.duty_u16(wave_value)
