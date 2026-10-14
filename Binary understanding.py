

#how to determine this is desired value?

#simulated rates
data1 = b'\xAA\x00\x00\x00'
data2 = b'\xAD\x00\x00\x00'
print(len(data1))

Matches = False

#while loop should terminate when average wave value is within 1% of desired
while True:
    #convert this into type int
    desired_rate = int.from_bytes(data1, byteorder='little')
    print(desired_rate)
    ##time.sleep(1)
    while not Matches:
        #stores X# of bits, enough to define the digits in a PCM wave, shorter=better
        given_rate = int.from_bytes(data2, byteorder='little')
        print(given_rate)
        if given_rate is not None:
            if given_rate == desired_rate:
                Matches = True
            else:
                #math for difference
                correction =  given_rate - desired_rate
                #sends correction value?
                ##uart.write(bytes([correction]))
        #error because not reading from the bus
        else:
            ##time.sleep(1)
            continue





