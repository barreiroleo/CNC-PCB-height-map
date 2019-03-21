# import serial

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


def input_datos():
    print("Margenes de escaneo:")
    x_inf_izq = float(input("X inferior izq: "))
    y_inf_izq = float(input("Y inferior izq: "))
    x_sup_der = float(input("X superior der: "))
    y_sup_der = float(input("Y superior der: "))

    # Imprimir posiciones para verificar la entrada de datos
    tupla_posiciones = (x_inf_izq, y_inf_izq, x_sup_der, y_sup_der)
    print("TuplaPosiciones: " + str(tupla_posiciones))
    n_puntos_x = float(input("Cantidad de puntos en X: "))
    n_puntos_y = float(input("Cantidad de puntos en Y: "))

    avance_x = (x_sup_der - x_inf_izq) / n_puntos_x
    avance_y = (y_sup_der - y_inf_izq) / n_puntos_y

    print("Avance X: " + str(avance_x))
    print("Avance Y: " + str(avance_y))
