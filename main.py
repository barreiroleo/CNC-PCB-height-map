"""
El script debe:
Conectarse con el micro.
Una vez que está en espera el micro, preguntar:
  Margenes de escaneo: [{x_inf_izq,y_inf_izq},{x2,y2},{x3,y3},{xf,yf}]
  Cantidad de puntos de escaneo: [{x_cant},{y_cant}]
Con los datos procesar:
  Dividir la distancia máxima de cada eje entre la cantidad de puntos a sensar
  El valor obtenido es el avance que hay que darle al código G (¿Coord relat?)
Posicionarse en cero automáticamente y establecer sus coordenadas Z en cero
"""

import serial
import time
# import pdb
# pdb.set_trace()
# Listar dispositivos en terminal:
# ls /dev/ttyAC*
# Instancia de objeto serial
ard_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)


class milling_cnc():
    """ Definición de la clase milling:
        tupla puntos_extremos
          [x_inf_izq, y_inf_izq, x_sup_der, y_sup_der, x_cant, y cant]
    """
    x_pos, y_pos, z_pos = 0,0,0
    x_inf_izq, y_inf_izq = 0,0
    x_sup_der, y_sup_der = 0,0
    x_cant, y_cant = 0,0
    total_medidas = 0
    avance_x = 0
    avance_y = 0

    def __init__(self):
        # self.x_inf_izq = float(input("X inferior izq: "))
        # self.y_inf_izq = float(input("Y inferior izq: "))
        # self.x_sup_der = float(input("X superior izq: "))
        # self.y_sup_der = float(input("X superior izq: "))
        # self.x_cant    = float(input("X cantidad med: "))
        # self.y_cant    = float(input("X cantidad med: "))
        puntos_extremos = [0, 0, 10, 10, 2, 2]
        self.x_inf_izq, self.y_inf_izq = puntos_extremos[0], puntos_extremos[1]
        self.x_sup_der, self.y_sup_der = puntos_extremos[2], puntos_extremos[3]
        self.x_cant, self.y_cant = puntos_extremos[4], puntos_extremos[5]

        self.total_medidas = self.x_cant * self.y_cant
        self.avance_x = (self.x_sup_der - self.x_inf_izq) / self.x_cant
        self.avance_y = (self.y_sup_der - self.y_inf_izq) / self.y_cant

        # tupla_posiciones = (self.x_inf_izq, self.y_inf_izq,
        #                     self.x_sup_der, self.y_sup_der)
        # print("Posiciones: " + str(tupla_posiciones))
        # print("Avance X: "   + str(self.avance_x))
        # print("Avance Y: "   + str(self.avance_y))

    def consulta_posicion(self):
        self.wait_clean_buffer()
        gcode_to_send = "?" + "\r\n"
        ard_serial.write(bytes(gcode_to_send, encoding="ascii"))
        while True:
            grbl_says = str(ard_serial.readline())
            # Encuentra PRB, parsea y sale
            print("Grbl says: " + grbl_says)
            if grbl_says.find("MPos") > (-1):   # Para consulta
                # if grbl_says.find("PRB") > (-1):  # Para zonda
                print("Grbl says: " + grbl_says + "\n")
                var_aux_a = str(grbl_says)
                indice_first_PRB = var_aux_a.find(":") + 1
                indice_second_PRB = var_aux_a.find("|", indice_first_PRB)
                var_aux_a = var_aux_a[indice_first_PRB:indice_second_PRB]
                var_aux_a = var_aux_a.split(",")
                # En este punto hay una tupla con los elementos para:
                # x_pos, y_pos, z_pos
                self.x_pos, self.y_pos = var_aux_a[0], var_aux_a[1]
                self.z_pos = var_aux_a[2]
                for i in var_aux_a:
                    print(var_aux_a)
                break

    def probe_z(self):
        self.wait_clean_buffer()
        # 1er elemento: gcode. 2do elemento: Código que espera
        gcodes = [["G91", "ok"], ["G1 Z1 F50", "ok"],
                  ["G38.2 Z-10 F50", "PRB"], ["G38.5 Z01 F1", "PRB"],
                  ["G38.2 Z-1 F1", "PRB"], ["G38.5 Z01 F1", "PRB"],
                  ["G04 P5", "ok"],  # Pausa en seg
                  ["M2", "ok"], ["G90", "ok"]
                  ]
        for i in range(len(gcodes)):
            self.send_to_grbl(gcodes[i])

    def avanzar(self, X_avance, Y_avance):
        self.wait_clean_buffer()
        # 1er elemento: gcode. 2do elemento: Código que espera
        gcodes = [["G90", "ok"], ["G1 Z1 F10", "ok"], ["G91", "ok"],
                  ["G1 X" + str(X_avance) + "Y" + str(Y_avance), "ok"],
                  ["M2", "ok"], ["G90", "ok"]
                  ]
        for i in range(len(gcodes)):
            self.send_to_grbl(gcodes[i])

    def reset_coordinates(self):
        self.wait_clean_buffer()
        gcodes = ["G92 X0 Z0 Y0", "ok"]  # Establece coordenadas en Z = 0
        self.send_to_grbl(gcodes)

    def send_to_grbl(self, code_to_send):
        # Recibe un array con dos elementos:
        # Elem 0: Gcode, Elem 1: Tipo de mensaje de retorno
        print(code_to_send[0])
        code_to_send[0] = code_to_send[0] + "\r\n"
        ard_serial.write(bytes(code_to_send[0], encoding="ascii"))
        while True:
            grbl_says = str(ard_serial.readline())
            # Cuando encuentre el código esperado en el mensaje salir
            if grbl_says.find(code_to_send[1]) > (-1):
                break

    def wait_clean_buffer(self):
        # Verificar que la linea esté desocupada
        while True:
            grbl_says = str(ard_serial.readline())
            if grbl_says != '':                 # Mensajes no vacíos
                print("Grbl says: " + grbl_says)
            if grbl_says.find("''") > (-1):     # Hay mensaje vacío (timeout)
                break                           # Salir del while

    def wake_up_grbl(self):
        bytes_to_send = b'\r\n\r\n'
        ard_serial.write(bytes_to_send)
        time.sleep(2)            # Wait for grbl to initialize
        ard_serial.flushInput()  # Flush startup text in serial input

    def close_grbl(self):
        ard_serial.close()
        return 1


def main():
    fresa = milling_cnc()
    fresa.wake_up_grbl()
    fresa.reset_coordinates()
    time.sleep(2)
    fresa.consulta_posicion()
    fresa.probe_z()
    fresa.reset_coordinates()
    fresa.avanzar(fresa.avance_x, fresa.avance_y)
    fresa.probe_z()
    fresa.close_grbl()


main()
