import socket
import threading
import random
import os
import tablero
import time

def reloj_inactividad(limite, estado, clientes):
    while True:
        time.sleep(1) 
        
        if estado['iniciada']:
            inactividad = time.time() - estado['ultimo_tiempo']
            
            print(f"Tiempo inactivo: {int(inactividad)}s / {limite}s", flush=True)
            
            if inactividad > limite:
                print("Limite de tiempo alcanzqdo", flush=True)
                aviso = "\nPartida cerrada por inactividad.\n"
                
                # Avisamos a todos y cerramos sus conexiones
                for c in list(clientes.keys()):
                    c.send(aviso.encode('utf-8'))
                    c.close()
                
                os._exit(0)

def atender_jugador(conexion, direccion, tablero, clientes, estado):
    nombre = conexion.recv(1024).decode('utf-8').strip()
    clientes[conexion] = nombre
    
    cats = ", ".join(tablero.categorias.keys())
    bienvenida = f"\nHola {nombre}. Las categorias son estas: {cats}. Escribe 'GO!' para empezar.\n"
    conexion.send(bienvenida.encode('utf-8'))

    # Bucle  del jugador
    while True:
        datos = conexion.recv(1024)
        
        # Si el cliente se desconecta, recv devuelve vacio y rompemos el bucle
        if not datos: 
            break 
        
        msg = datos.decode('utf-8').strip()

        if msg != "":
            estado['ultimo_tiempo'] = time.time()

        # Solo iniciamos si no ha empezado ya
        if msg.upper() == "GO!" and not estado['iniciada']:
            estado['iniciada'] = True
            estado['ultimo_tiempo'] = time.time()
            
            letra = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            tablero.letra_actual = letra
            
            for c in tablero.categorias: 
                tablero.categorias[c] = ""
            
            anuncio = f"\n[NUEVA PARTIDA] Letra elegida: {letra}. Suerte a todos:)\n"
            for c in clientes: 
                c.send(anuncio.encode('utf-8'))
        
        elif "," in msg:
            partes = msg.split(",")
            if len(partes) >= 2:
                cat = partes[0].strip()
                palabra = partes[1].strip()
                
                if cat in tablero.categorias and palabra[0].upper() == tablero.letra_actual:
                    if tablero.escribir_en_categoria(nombre, cat, palabra):
                        aviso = f"\n{nombre} ha completado {cat} con '{palabra}'.\nEstado actual: {tablero.categorias}\n"
                        for c in clientes: 
                            c.send(aviso.encode('utf-8'))
                        
                        # Si no quedan categorias vacias, la partida acaba
                        if all(valor != "" for valor in tablero.categorias.values()):
                            os._exit(0) 
                            
    # Si llegamos hasta aquies por que el bucle while se ha roto
    # porque el jugador se ha ido. Procedemos a limpiar:
    if conexion in clientes:
        del clientes[conexion]
    conexion.close()

def iniciar_partida(puerto):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', puerto))
    s.listen(10)
    
    juego = tablero.TableroJuego()
    clientes_conectados = {} 
    estado_partida = {'iniciada': False, 'ultimo_tiempo': time.time()}

    hilo_reloj = threading.Thread(target=reloj_inactividad, args=(30, estado_partida, clientes_conectados), daemon=True)
    hilo_reloj.start()

    print(f"Servidor escuchando en puerto {puerto}", flush=True)
    
    while True:
        conn, addr = s.accept()
        hilo_jugador = threading.Thread(target=atender_jugador, args=(conn, addr, juego, clientes_conectados, estado_partida))
        hilo_jugador.start()