import socket
import threading
import tablero
import random

def atender_jugador(conexion, direccion, tablero_compartido, clientes_conectados):
    print("Nuevo jugador conectado desde:", direccion)
    nombre_jugador = "Jugador-" + str(direccion[1])
    
    # 1. Guardamos al jugador en nuestro Diccionario compartido
    # La clave es la conexión, el valor es su nombre
    clientes_conectados[conexion] = nombre_jugador
    
    # --- MENSAJE DE BIENVENIDA INTELIGENTE ---
    if tablero_compartido.letra_actual == "":
        bienvenida = "\nBienvenido. No hay partida en curso. Escribe 'GO!' para empezar.\n"
    else:
        bienvenida = "\nBienvenido. Partida en curso con la letra: " + tablero_compartido.letra_actual + "\nEscribe 'Categoria,Palabra' para jugar.\n"
    conexion.send(bienvenida.encode('utf-8'))
    
    while True:
        datos = conexion.recv(1024) 
        if not datos:
            break
            
        mensaje = datos.decode('utf-8').strip()
        
        # 2. EXTRAEMOS LA INFORMACIÓN DE LOS JUGADORES
        # Sacamos todos los nombres del diccionario y los unimos con comas
        nombres_activos = ", ".join(clientes_conectados.values())
        total_jugadores = str(len(clientes_conectados))
        
        # Creamos una cabecera que se enviará en cada actualización
        info_jugadores = "\n👥 [Jugadores activos (" + total_jugadores + "): " + nombres_activos + "]"
        
        # Tolerancia a errores: Aceptamos "GO!" y "GO"
        if mensaje == "GO!" or mensaje == "GO":
            abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letra = random.choice(abecedario)
            
            tablero_compartido.letra_actual = letra
            for cat in tablero_compartido.categorias:
                tablero_compartido.categorias[cat] = ""

            # Añadimos la cabecera de jugadores al anuncio
            anuncio = info_jugadores + "\n¡NUEVA PARTIDA! Letra elegida: " + letra + "\nEl tablero se ha vaciado.\n"
            
            # Para enviar a todos, iteramos sobre las claves (las conexiones) del diccionario
            for c in clientes_conectados.keys():
                c.send(anuncio.encode('utf-8'))
                    
        else:
            partes = mensaje.split(",")
            if len(partes) == 2:
                categoria = partes[0].strip()
                palabra = partes[1].strip()
                
                if categoria in tablero_compartido.categorias:
                    if palabra[0].upper() == tablero_compartido.letra_actual:
                        
                        tablero_compartido.escribir_en_categoria(nombre_jugador, categoria, palabra)
                        
                        # Añadimos la cabecera de jugadores a la actualización del tablero
                        aviso = info_jugadores + "\n" + nombre_jugador + " escribio " + palabra + " en " + categoria + "\nTablero: " + str(tablero_compartido.categorias) + "\n"
                        for c in clientes_conectados.keys():
                            c.send(aviso.encode('utf-8'))
                        
                        lleno = True
                        for v in tablero_compartido.categorias.values():
                            if v == "": lleno = False
                        
                        # ... (dentro de comprobar si está lleno) ...
                        if lleno:
                            # 1. Calculamos la puntuación máxima
                            max_puntos = max(tablero_compartido.puntuaciones.values())
                            
                            # 2. Buscamos quién o quiénes tienen esa puntuación (por si hay empate)
                            ganadores = []
                            for nombre, puntos in tablero_compartido.puntuaciones.items():
                                if puntos == max_puntos:
                                    ganadores.append(nombre)
                            
                            # 3. Preparamos el mensaje final
                            resultado = "\n--- PARTIDA TERMINADA ---"
                            resultado += "\nPuntuaciones: " + str(tablero_compartido.puntuaciones)
                            
                            if len(ganadores) > 1:
                                resultado += "\n¡EMPATE entre: " + ", ".join(ganadores) + "!"
                            else:
                                resultado += "\n¡GANADOR: " + ganadores[0] + "!"
                            
                            for c in clientes_conectados.keys():
                                c.send(resultado.encode('utf-8'))
                    else:
                        error = "ERROR: La palabra debe empezar por " + tablero_compartido.letra_actual + "\n"
                        conexion.send(error.encode('utf-8'))
                else:
                    conexion.send("Categoria inexistente.\n".encode('utf-8'))
            else:
                conexion.send("Formato: Categoria,Palabra\n".encode('utf-8'))
        
    # 3. Cuando un jugador se va, lo borramos del diccionario
    del clientes_conectados[conexion]
    conexion.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 65432))
    s.listen(5)
    mi_tablero = tablero.TableroJuego()
    
    # NUEVO: Usamos un diccionario {} en vez de una lista []
    dict_clientes = {}
    
    print("Servidor iniciado...")
    while True:
        conexion, direccion = s.accept()
        # Pasamos el diccionario a los hilos para que compartan esta memoria
        hilo = threading.Thread(target=atender_jugador, args=(conexion, direccion, mi_tablero, dict_clientes))
        hilo.start()

if __name__ == '__main__':
    main()