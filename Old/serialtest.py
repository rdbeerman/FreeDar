import serial

ser = serial.Serial('COM6')  # open serial port
print(ser.name)              # check which port was really used

while True:
    string = ser.readline()          # write a string
    values = string.split()
    range = values[0]
    angle = values[1]
    print(float(range), float(angle))
ser.close()                  # close port