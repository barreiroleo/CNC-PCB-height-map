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
    ard_serial.flushInput()  # Flush startup text in serial input


def send_to_serial(gcode):
    command_to_send = gcode
    print("\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        grbl_says = str(ard_serial.readline())
        if grbl_says != '':                 # Imprimir los mensajes no vacíos
            print("Grbl says: " + grbl_says)
        if grbl_says.find("") > (-1):     # Cuando encuentre ok, salir.
            break


def mapear():
    # Verificar que la linea esté desocupada
    while True:
        grbl_says = str(ard_serial.readline())
        if grbl_says != '':                 # Imprimir los mensajes no vacíos
            print("Grbl says: " + grbl_says)
        if grbl_says.find("''") > (-1):     # Si hay mensaje vacío (timeout)
            break                           # Salir del while

    gcodes = ["G91",
              "G1 Z1 F50",
              "G38.2 Z-10 F50",
              "G38.5 Z1 F50",
              "G38.2 Z-1 F10",
              "G38.5 Z1 F10",
              "G92 Z0",
              "$X",
              "M2"
              ]

    for i in range(len(gcodes)):
        send_to_serial(gcodes[i] + "\r\n")

    """command_to_send = "G91 \r\n"
    command_to_send = gcodes[0]
    print("\r\n" + command_to_send)
    ard_serial.write(bytes(command_to_send, encoding="ascii"))
    while True:
        grbl_says = str(ard_serial.readline())
        if grbl_says != '':                 # Imprimir los mensajes no vacíos
            print("Grbl says: " + grbl_says)
        if grbl_says.find("ok") > (-1):     # Cuando encuentre ok, salir.
            break
    """
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
