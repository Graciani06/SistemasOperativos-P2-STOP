import socket
import threading
import random
import tablero

def atender_jugador(conexion, direccion, tablero_compartido, clientes_conectados):
    # Recibimos el nombre (Primer mensaje del protocolo)
    try:
        nombre = conexion.recv(1024).decode('utf-8').strip()
        clientes_conectados[conexion] = nombre
        
        cats = ", ".join(tablero_compartido.categorias.keys())
        bienvenida = f"\nBienvenido {nombre}. Categorias: {cats}. Esperando 'GO!'...\n"
        conexion.send(bienvenida.encode('utf-8'))

        while True:
            datos = conexion.recv(1024)
            if not datos: break
            msg = datos.decode('utf-8').strip()

            if msg.upper() == "GO!":
                letra = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                tablero_compartido.letra_actual = letra
                for c in tablero_compartido.categorias: tablero_compartido.categorias[c] = ""
                
                anuncio = f"\n¡NUEVA PARTIDA! Letra: {letra}\n"
                for c in clientes_conectados: c.send(anuncio.encode('utf-8'))
            
            elif "," in msg:
                cat, palabra = [x.strip() for x in msg.split(",")]
                if cat in tablero_compartido.categorias and palabra[0].upper() == tablero_compartido.letra_actual:
                    if tablero_compartido.escribir_en_categoria(nombre, cat, palabra):
                        # 1. Broadcast del acierto
                        aviso = f"\n{nombre} escribio {palabra} en {cat}.\nTablero: {tablero_compartido.categorias}\n"
                        for c in clientes_conectados: c.send(aviso.encode('utf-8'))
                        
                        # 2. NUEVO: Comprobar si el tablero se ha completado
                        lleno = all(valor != "" for valor in tablero_compartido.categorias.values())
                        
                        if lleno:
                            # Calculamos ganador
                            max_puntos = max(tablero_compartido.puntuaciones.values())
                            ganadores = [n for n, p in tablero_compartido.puntuaciones.items() if p == max_puntos]
                            
                            resultado = f"\n--- PARTIDA TERMINADA ---\nPuntos: {tablero_compartido.puntuaciones}"
                            resultado += f"\nGANADOR: {', '.join(ganadores)}!\n"
                            
                            for c in clientes_conectados:
                                c.send(resultado.encode('utf-8'))
                                # El PDF dice "el socket se libera", podemos cerrar aquí o esperar a que salgan
                    else:
                        conexion.send(f"ERROR: {cat} ya esta ocupada.\n".encode('utf-8'))
                else:
                    conexion.send("ERROR: Letra o categoria incorrecta.\n".encode('utf-8'))
    except: pass
    finally:
        if conexion in clientes_conectados: del clientes_conectados[conexion]
        conexion.close()

def iniciar_partida(puerto):
    # Esta función se ejecuta en un PROCESO separado (multiprocessing)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', puerto))
    s.listen(10)
    
    mi_tablero = tablero.TableroJuego()
    dict_clientes = {} # Memoria compartida entre HILOS de este PROCESO
    
    print(f"Partida iniciada en puerto {puerto}")
    while True:
        conn, addr = s.accept()
        # Creamos HILO bajo demanda (hilos.pdf)
        threading.Thread(target=atender_jugador, args=(conn, addr, mi_tablero, dict_clientes)).start()