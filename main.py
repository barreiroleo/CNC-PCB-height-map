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

from milling_machine import milling_grbl
# import pdb
# pdb.set_trace()
# Declaraciones de salida de texto
mapFile = open('/home/leonardo/Escritorio/pyMapFile.map', 'w')
logFile = open('outputFiles/logFile.txt', 'w')
# para escribir: f.write()
# para cerrar: f.close()


def initialize_high():
    fresa.probe_z()             # Probar altura
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    fresa.reset_coordinates()   # Reseteo X0 Y0 Z0
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    fresa.z_pos_error = fresa.z_pos  # Asigna offset de error grbl: issue G92
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    # z_question = input("Z es igual a 0: (Y / N)")
    z_question = 'y'
    if z_question == 'n':
        initialize_high()
    if z_question == 'y':
        return


def main():
    # Encabezado de fichero de mappeo
    mapFile.write(str(fresa.x_inf_izq) + ';' + str(fresa.y_inf_izq) + ';' +
                  str(fresa.x_sup_der) + ';' + str(fresa.y_sup_der) + "\n")
    mapFile.write(str(fresa.x_cant) + ';' + str(fresa.y_cant) + ';' +
                  str(fresa.z_max_depth) + ';' + str(fresa.z_secure_depth) + "\n")
    mapFile.write("0;20;20" + "\n")  # Valores de interpolación soft Candle
    fresa.wake_up_grbl()        # Iniciar comunicacion

    initialize_high()

    meassurements_y = []
    for i in range(fresa.y_cant):
        meassurements_x = []
        for j in range(fresa.x_cant):
            fresa.avanzar(fresa.x_inf_izq + fresa.avance_x * j,
                          fresa.y_inf_izq + fresa.avance_y * i, 200)
            fresa.probe_z()
            fresa.update_posicion()
            meassurements_x.append(fresa.z_pos)
            # line_to_log = (str(fresa.x_pos) + ";" + str(fresa.y_pos) +
            #                  ";" + str(fresa.z_pos))
            # mapFile.write(line_to_log + "\n")
            print(fresa.posiciones_now)
        meassurements_y.append(meassurements_x)
    print("Finish mapping")
    print(meassurements_y)
    # meassurements_y.reverse()  # Ordena las mediciones respecto al eje Y. No hace falta para Candle
    for i in range(len(meassurements_y)):
        for j in range(len(meassurements_y[i])):
            mapFile.write(str(meassurements_y[i][j]))
            if j < (len(meassurements_y[i])-1):
                mapFile.write(";")
        mapFile.write("\n")

    fresa.avanzar(0.0, 0.0, 200)
    fresa.wait_clean_buffer()
    fresa.update_posicion()
    fresa.close_grbl()


fresa = milling_grbl()
main()
