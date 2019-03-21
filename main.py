import serial
import time
# import pdb
# pdb.set_trace()

# Listar dispositivos en terminal:
# ls /dev/ttyAC*
# arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
# arduino.close()

"""
El script debe:
Conectarse con el micro.
Enviar data hasta que responda "ok"

Una vez que está en espera el micro, preguntar:
  Margenes de escaneo: [{x_inf_izq,y_inf_izq},{x2,y2},{x3,y3},{xf,yf}]
  Cantidad de puntos de escaneo: [{x_cant},{y_cant}]
Con los datos procesar:
  Dividir la distancia máxima de cada eje entre la cantidad de puntos a sensar
  El valor obtenido es el avance que hay que darle al código G (¿Coord relat?)
"""

# Instancia de objeto serial
ard_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)


def input_datos():
    print("Margenes de escaneo:")
    # x_inf_izq = float(input("X inferior izq: "))
    x_inf_izq = 0
    # y_inf_izq = float(input("Y inferior izq: "))
    y_inf_izq = 0
    # x_sup_der = float(input("X superior der: "))
    x_sup_der = 10
    # y_sup_der = float(input("Y superior der: "))
    y_sup_der = 10

    # Imprimir posiciones para verificar la entrada de datos
    tupla_posiciones = (x_inf_izq, y_inf_izq, x_sup_der, y_sup_der)
    print("TuplaPosiciones: " + str(tupla_posiciones))
    # n_puntos_x = float(input("Cantidad de puntos en X: "))
    n_puntos_x = 2
    # n_puntos_y = float(input("Cantidad de puntos en Y: "))
    n_puntos_y = 2

    avance_x = (x_sup_der - x_inf_izq) / n_puntos_x
    avance_y = (y_sup_der - y_inf_izq) / n_puntos_y

    print("Avance X: " + str(avance_x))
    print("Avance Y: " + str(avance_y))


def wake_up_grbl():
    # Wake up grbl
    bytes_to_send = b'\r\n\r\n'
    ard_serial.write(bytes_to_send)
    time.sleep(2)   # Wait for grbl to initialize
    print(ard_serial.readline())
    print(ard_serial.readline())
    print(ard_serial.readline())
    ard_serial.flushInput()  # Flush startup text in serial input


def mapear():
    gcode_to_send = ["G91 G38.2 Z-1 F50",
                     "G91 G38.5 Z1 F50",
                     "G91 G38.2 Z-1 F10",
                     "G91 G38.5 Z1 F10",
                     "M2"]
    # Coordenadas relativas, velocidad 10
    # Zondear bajando Z
    # Zondear subiendo Z
    # Stream g-code to grbl
    """
    for i in range(len(gcode_to_send)):
        print('Sending: ' + str(gcode_to_send[i]))   # Preview comando
        command_to_send = "gcode_to_send[i]" + '\r\n'  # Asignar linea a enviar
        ard_serial.write(bytes(command_to_send,
                               encoding="ascii"))    # Enviar gcode
        grbl_out = ard_serial.readline()			 # Esperar por \n de grbl
        # print(' : ' + grbl_out.strip(str(grbl_out)))
        print("Grbl says: " + str(grbl_out))
    """
    print("Grbl says: " + str(ard_serial.readline()))
    print("Grbl says: " + str(ard_serial.readline()))
    print("Grbl says: " + str(ard_serial.readline()))

    command_to_send = "G91 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "G38.2 Z-10 F50 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "G38.5 Z1 F50 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "G38.2 Z-1 F10 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "G38.5 Z1 F10 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "G92 Z0 \r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break

    command_to_send = "$X \r\n\r\n"
    print("\r\n\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        print("Grbl says: " + str(ard_serial.readline()))
        if ard_serial.readline() == b'ok\r\n':
            break
            
    return 1


def close_serial():
    ard_serial.close()
    return 1


def main():
    # Open grbl serial port
    input_datos()
    wake_up_grbl()
    mapear()
    close_serial()


main()
