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


def main():
    fresa = milling_grbl()
    fresa.wake_up_grbl()        # Iniciar comunicacion
    fresa.probe_z()             # Probar altura
    print("aca1")
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    print("aca2")
    fresa.reset_coordinates()   # Reseteo X0 Y0 Z0
    print("aca3")
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    print("aca4")
    fresa.z_pos_error = fresa.z_pos  # Asigna offset de error grbl: issue G92
    print("aca5")
    fresa.update_posicion()     # Consulta y actualiza el registro posicion
    print("aca6")

    input("Verificar si Z es igual a 0")
    for i in range(fresa.x_cant):
        for j in range(fresa.x_cant):
            fresa.avanzar(fresa.x_inf_izq + fresa.avance_x * j,
                          fresa.y_inf_izq + fresa.avance_y * i,
                          200)
            fresa.probe_z()
            fresa.update_posicion()
            print(fresa.posiciones_now)

    fresa.avanzar(0.0, 0.0, 100)
    fresa.wait_clean_buffer()
    fresa.update_posicion()
    fresa.close_grbl()


main()
