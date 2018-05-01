import serial

ser = serial.Serial('COM5')  # open serial port
print(ser.name)              # check which port was really used

while True:
    print(ser.readline())          # write a string

ser.close()                  # close port