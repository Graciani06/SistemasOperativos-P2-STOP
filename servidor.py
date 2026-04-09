import socket
import threading  # Visto en hilos.pdf (pág 6)
import tablero    # Importamos el archivo con el recurso compartido y semáforos

def atender_jugador(conexion, direccion, tablero_compartido):
    """
    Función que ejecutará cada hilo de forma independiente.
    Equivale a la función 'ejecutar(c)' de la página 6 de hilos.pdf.
    """
    print("Nuevo jugador conectado desde:", direccion)
    
    # Le asignaremos un nombre genérico basado en su puerto para identificarlo
    nombre_jugador = "Jugador-" + str(direccion[1])
    
    # Bucle para que el servidor siga escuchando a este jugador en concreto
    while True:
        # RECEIVE BLOQUEANTE (pasoDeMensajes.pdf pág 4)
        # Este hilo se bloquea aquí hasta que este jugador envíe algo.
        # Como es un hilo independiente, el servidor principal NO se bloquea.
        datos = conexion.recv(1024) 
        
        # Si recv devuelve vacío, significa que el cliente se ha desconectado
        if not datos:
            break
            
        mensaje = datos.decode('utf-8')
        print(nombre_jugador + " dice: " + mensaje)
        
        # INTERACCIÓN CON EL RECURSO COMPARTIDO (sincronizacion.pdf)
        # Simulamos que el jugador intenta escribir en "Animal" lo recibido
        tablero_compartido.escribir_en_categoria(nombre_jugador, "Animal", mensaje)
        
        # SEND (pasoDeMensajes.pdf pág 3)
        # Enviamos el estado actual del tablero al jugador para que lo vea
        respuesta = "Tablero actualizado: " + str(tablero_compartido.categorias)
        conexion.send(respuesta.encode('utf-8'))
        
    conexion.close()
    print("Jugador desconectado:", direccion)

def main():
    # 1. Creamos el "Buzón" (pasoDeMensajes.pdf pág 5) usando Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Anclamos el buzón a nuestra IP y puerto para que los clientes nos encuentren
    s.bind(('127.0.0.1', 65432))
    s.listen(5) # Permite encolar hasta 5 peticiones de conexión simultáneas
    
    # 2. CREAMOS EL RECURSO COMPARTIDO
    # Se crea una sola vez antes del bucle infinito (hilos.pdf pág 7 - compartir memoria)
    mi_tablero = tablero.TableroJuego()
    
    print("Servidor STOP! iniciado y esperando jugadores...")
    
    # 3. Bucle infinito del hilo principal (receptor de peticiones)
    while True:
        # El hilo principal se bloquea aquí esperando a que alguien se conecte
        conexion, direccion = s.accept()
        
        # DISEÑO BAJO DEMANDA (hilos.pdf pág 2)
        # "Al llegar una petición crea un proceso/hilo para atender dicha petición"
        # Le pasamos el 'mi_tablero' como argumento al nuevo hilo para compartir la memoria
        hilo = threading.Thread(target=atender_jugador, args=(conexion, direccion, mi_tablero))
        hilo.start()
        
        # Print equivalente al de hilos.pdf para ver que el hilo principal sigue libre
        print("Hilo principal libre. Hilos activos actualmente: " + str(threading.active_count()))

if __name__ == '__main__':
    main()