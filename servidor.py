import socket
import threading
import tablero
import random  # NUEVO: Para generar la letra aleatoria

def atender_jugador(conexion, direccion, tablero_compartido, clientes_conectados):
    print("Nuevo jugador conectado desde:", direccion)
    nombre_jugador = "Jugador-" + str(direccion[1])
    
    while True:
        datos = conexion.recv(1024) 
        if not datos:
            break
            
        mensaje = datos.decode('utf-8').strip()
        print(nombre_jugador + " dice: " + mensaje)
        
        if mensaje == "GO!":
            abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letra = random.choice(abecedario)
            
            anuncio = "\n¡EL JUEGO COMIENZA! Letra elegida: " + letra + "\nTablero: " + str(tablero_compartido.categorias) + "\n"
            print("Generando letra " + letra + " y avisando a todos...")
            
            # BROADCAST DE INICIO
            for cliente in clientes_conectados:
                cliente.send(anuncio.encode('utf-8'))
                    
        else:
            # LÓGICA DE JUEGO NORMAL
            partes = mensaje.split(",")
            
            if len(partes) == 2:
                categoria = partes[0].strip()
                palabra = partes[1].strip()
                
                if categoria in tablero_compartido.categorias:
                    
                    # ENTRAMOS A LA SECCIÓN CRÍTICA
                    tablero_compartido.escribir_en_categoria(nombre_jugador, categoria, palabra)
                    
                    # BROADCAST DE ACTUALIZACIÓN
                    aviso = "\n" + nombre_jugador + " ha escrito en " + categoria + "\nTablero: " + str(tablero_compartido.categorias) + "\n"
                    for cliente in clientes_conectados:
                        cliente.send(aviso.encode('utf-8'))
                    
                    # --- NUEVO: COMPROBAR FIN DE PARTIDA ---
                    # Comprobamos si queda algún valor vacío ("") en el diccionario
                    tablero_lleno = True
                    for valor in tablero_compartido.categorias.values():
                        if valor == "":
                            tablero_lleno = False
                    
                    # Si ya no hay vacíos, el juego ha terminado
                    if tablero_lleno:
                        fin_msg = "\n¡EL TABLERO ESTÁ COMPLETO! Fin de la partida.\n"
                        print("Partida terminada. Tablero lleno.")
                        for cliente in clientes_conectados:
                            cliente.send(fin_msg.encode('utf-8'))
                            
                        # Aquí, idealmente, se podría reiniciar el tablero para una nueva partida:
                        # tablero_compartido.categorias = {"Marca": "", "Comida": "", "Lugar": "", "Animal": ""}
                        
                else:
                    error = "Categoria no valida. Las categorias son: Marca, Comida, Lugar, Animal\n"
                    conexion.send(error.encode('utf-8'))
            else:
                error = "Formato incorrecto. Debes usar la coma: Categoria,Palabra\n"
                conexion.send(error.encode('utf-8'))
        
    clientes_conectados.remove(conexion)
    conexion.close()
    print("Jugador desconectado:", direccion)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 65432))
    s.listen(5)
    
    mi_tablero = tablero.TableroJuego()
    
    # NUEVO: Lista compartida en memoria principal para guardar los sockets
    lista_clientes = []
    
    print("Servidor STOP! iniciado y esperando jugadores...")
    
    while True:
        conexion, direccion = s.accept()
        
        # NUEVO: Guardamos el socket del nuevo jugador en la lista
        lista_clientes.append(conexion)
        
        # NUEVO: Pasamos la lista_clientes al hilo también
        hilo = threading.Thread(target=atender_jugador, args=(conexion, direccion, mi_tablero, lista_clientes))
        hilo.start()
        
        print("Hilo principal libre. Hilos activos actualmente: " + str(threading.active_count()))

if __name__ == '__main__':
    main()