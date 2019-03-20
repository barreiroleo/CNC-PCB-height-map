import serial, time
# Listar dispositivos en terminal:
# ls /dev/ttyAC*
arduino = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(2)
rawString = arduino.readline()
print(rawString)
arduino.write(b'9') #Envíar en binario
arduino.close()