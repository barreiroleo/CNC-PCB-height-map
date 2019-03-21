import serial
import time
ard_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
bytes_to_send = b'\r\n\r\n'
ard_serial.write(bytes_to_send)
time.sleep(2)   # Wait for grbl to initialize
print(ard_serial.readline())
print(ard_serial.readline())
print(ard_serial.readline())
ard_serial.flushInput()  # Flush startup text in serial input


command_to_send = "G91 G38.2 Z-1 F50 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
print("Grbl says: " + str(ard_serial.readline()))
command_to_send = "G91 G38.5 Z1 F50 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
print("Grbl says: " + str(ard_serial.readline()))
command_to_send = "G91 G38.2 Z-1 F10 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
print("Grbl says: " + str(ard_serial.readline()))
command_to_send = "G91 G38.5 Z1 F10 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
print("Grbl says: " + str(ard_serial.readline()))
command_to_send = "$X \r\n\r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
print("Grbl says: " + str(ard_serial.readline()))

ard_serial.write(bytes('G91 G1 y1 f100', encoding="ascii"))    # Enviar gcode
$X

"""ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
command_to_send = "G90 G1 Z1 F50 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
command_to_send = "G90 G1 Z-1 F50 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
command_to_send = "G90 G1 Z1 F50 \r\n"
ard_serial.write(bytes(command_to_send, encoding="ascii"))    # Enviar gcode
"""

grbl_out = ard_serial.readline()
print("Grbl says: " + str(grbl_out))
