import serial
import time
# Listar dispositivos en terminal:
# ls /dev/ttyAC*
# Instancia de objeto serial
ard_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)


class milling_grbl():
    """ Definición de la clase milling:
        tupla puntos_extremos
          [x_inf_izq, y_inf_izq, x_sup_der, y_sup_der, x_cant, y cant]
    """
    x_pos, y_pos, z_pos = 0, 0, 0
    x_inf_izq, y_inf_izq = 0, 0
    x_sup_der, y_sup_der = 0, 0
    x_cant, y_cant = 0, 0
    total_medidas = 0
    avance_x, avance_y = 0, 0
    posiciones_now, z_pos_error = 0, 0
    z_max_depth, z_secure_depth = -1, 1

    def __init__(self):
        self.x_inf_izq = float(input("X inferior izq: "))
        self.y_inf_izq = float(input("Y inferior izq: "))
        self.x_sup_der = float(input("X superior izq: "))
        self.y_sup_der = float(input("Y superior izq: "))
        self.x_cant    = int(input("X cantidad puntos: "))
        self.y_cant    = int(input("Y cantidad puntos: "))

        # puntos_extremos = [0, 0, 24.03, 8.77, 3, 2]  # Para patron de prueba
        # puntos_extremos = [0, 0, 10, 10, 2, 2]       # Para prueba rapida
        # self.x_inf_izq, self.y_inf_izq = puntos_extremos[0], puntos_extremos[1]
        # self.x_sup_der, self.y_sup_der = puntos_extremos[2], puntos_extremos[3]
        # self.x_cant, self.y_cant = puntos_extremos[4], puntos_extremos[5]

        self.total_medidas = self.x_cant * self.y_cant
        self.avance_x = (self.x_sup_der - self.x_inf_izq) / self.x_cant
        self.avance_y = (self.y_sup_der - self.y_inf_izq) / self.y_cant

        tupla_posiciones = (self.x_inf_izq, self.y_inf_izq,
                            self.x_sup_der, self.y_sup_der)
        print("Posiciones: " + str(tupla_posiciones))
        print("Avance X: " + str(self.avance_x))
        print("Avance Y: " + str(self.avance_y))

    def update_posicion(self):
        time.sleep(0.1)
        # print("\nupdate_posicion")
        gcode_to_send = "?" + "\r\n"
        ard_serial.write(bytes(gcode_to_send, encoding="ascii"))
        i = 1
        while True:
            grbl_says = str(ard_serial.readline())
            i += 1
            # print(i)
            if i > 5:
                """ Si va a error (Ov:100,100,100), aplica recursividad para
                resetear las coordenadas y volver a leer la posición.
                Puede ocasionar una falla si se da el error cuando la posicion
                sea distinta de 0,0,0. De todas formas, lo que falla es el WCO
                y no el MPos que contiene las coordenadas de posicion relativas
                al WCO """
                self.reset_coordinates()
                self.update_posicion()
                break
            # if grbl_says != "b''":  # Muestra mensajes con contenido
            #    print("Grbl says: " + grbl_says)
            # Encuentra WCO, parsea y sale
            if grbl_says.find("MPos") > (-1):   # Para consulta
                # if grbl_says.find("PRB") > (-1):  # Para zonda
                print("Grbl says: " + grbl_says)
                var_aux_a = str(grbl_says)
                indice_first_WCO = var_aux_a.find("MPos:") + len("MPos:")
                indice_second_WCO = var_aux_a.find("|", indice_first_WCO)
                var_aux_a = var_aux_a[indice_first_WCO:indice_second_WCO]
                var_aux_a = var_aux_a.split(",")
                # En este punto hay una tupla con los elementos para:
                # x_pos, y_pos, z_pos
                self.x_pos = float(var_aux_a[0])
                self.y_pos = float(var_aux_a[1])
                self.z_pos = float(var_aux_a[2])
                self.posiciones_now = [self.x_pos, self.y_pos, self.z_pos]
                # print("Posicion grbl: " + str(self.posiciones_now) +
                #      str(self.z_pos_error))
                # La correción de z, funciona si el valor de z es negativo o
                # positivo. Probado!
                self.z_pos = float(var_aux_a[2]) - self.z_pos_error
                self.posiciones_now = [self.x_pos, self.y_pos, self.z_pos]
                print("Posicion fix: " + str(self.posiciones_now))
                self.wait_clean_buffer()
                break

    def probe_z(self):
        # print("\nprobe_z")
        # 1er elemento: gcode. 2do elemento: Código que espera
        gcodes = [["$X", "ok"], ["G91", "ok"], ["G1 Z0.2 F100", "ok"],
                  ["G38.2 Z-10 F50", "PRB"], ["G38.5 Z01 F1", "PRB"],
                  ["G38.2 Z-10 F1", "PRB"], ["G38.5 Z01 F1", "PRB"],
                  ["G04 P0.1", "ok"],  # Pausa en seg
                  ["M2", "ok"], ["G90", "ok"]
                  ]
        for i in range(len(gcodes)):
            self.send_to_grbl(gcodes[i])
        self.wait_clean_buffer()

    def avanzar(self, X_avance, Y_avance, velocidad):
        # print("\navanzar")
        # 1er elemento: gcode. 2do elemento: Código que espera
        gcodes = [["$X", "ok"], ["G90", "ok"], ["G1 Z1 F50", "ok"],
                  ["G1 X" + str(X_avance) + "Y" + str(Y_avance) +
                   "F" + str(velocidad), "ok"],
                  ["M2", "ok"]
                  ]
        for i in range(len(gcodes)):
            self.send_to_grbl(gcodes[i])
        self.wait_clean_buffer()

    def reset_coordinates(self):
        # print("\nreset_coordinates")
        gcodes = [["$X", "ok"], ["G92 X0.0 Y0.0", "ok"],
                  ["G92 Z0.0", "ok"]]
        for i in range(len(gcodes)):
            self.send_to_grbl(gcodes[i])
        self.wait_clean_buffer()

    def send_to_grbl(self, code_to_send):
        # print("\nsend_to_grbl")
        # Recibe un array con dos elementos:
        # Elem 0: Gcode, Elem 1: Tipo de mensaje de retorno
        print(code_to_send[0])
        code_to_send[0] = code_to_send[0] + "\r\n"
        ard_serial.write(bytes(code_to_send[0], encoding="ascii"))
        while True:
            grbl_says = str(ard_serial.readline())
            # if grbl_says != "b''":   # Mostrar mensajes con contenido
            #    print(grbl_says)
            # Cuando encuentre el código esperado en el mensaje salir
            if grbl_says.find("ok") > (-1):
                # print("Grbl_says: " + grbl_says)
                self.wait_clean_buffer()
                break
            if grbl_says.find("PRB") > (-1):
                print("Grbl_says: " + grbl_says)
                self.wait_clean_buffer()
                break

    def wait_clean_buffer(self):
        # print("\nwait_clean_buffer")
        # Verificar que la linea esté desocupada
        while True:
            grbl_says = str(ard_serial.readline())
            # if grbl_says != "b''":                 # Mensajes no vacíos
            #    print("Grbl says: " + grbl_says)
            if grbl_says.find("b''") > (-1):     # Hay mensaje vacío (timeout)
                break                           # Salir del while

    def wake_up_grbl(self):
        # print("\nwake_up_grbl")
        bytes_to_send = b'\r\n\r\n'
        ard_serial.write(bytes_to_send)
        time.sleep(2)            # Wait for grbl to initialize
        ard_serial.flushInput()  # Flush startup text in serial input

    def close_grbl(self):
        # print("\nclose_grbl")
        ard_serial.close()
        return 1
