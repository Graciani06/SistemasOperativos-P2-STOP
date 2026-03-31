import socket
import threading  # Visto en hilos.pdf (pág 6)

def atender_jugador(conexion, direccion):
    """
    Función que ejecutará cada hilo de forma independiente.
    Equivale a la función 'ejecutar(c)' de la página 6 de hilos.pdf
    """
    print("Nuevo jugador conectado desde:", direccion)
    
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
        print("Jugador", direccion, "dice:", mensaje)
        
        # SEND (pasoDeMensajes.pdf pág 3)
        # Enviamos una respuesta al cliente
        respuesta = "Servidor recibió tu mensaje: " + mensaje
        conexion.send(respuesta.encode('utf-8'))
        
    conexion.close()
    print("Jugador desconectado:", direccion)

def main():
    # 1. Creamos el "Buzón" (pasoDeMensajes.pdf pág 5) usando Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 65432))
    s.listen(5) # Permite encolar hasta 5 peticiones de conexión simultáneas
    
    print("Servidor STOP! iniciado y esperando jugadores...")
    
    # 2. Bucle infinito del hilo principal (receptor de peticiones)
    while True:
        # El hilo principal se bloquea aquí esperando a que alguien se conecte
        conexion, direccion = s.accept()
        
        # DISEÑO BAJO DEMANDA (hilos.pdf pág 2)
        # "Al llegar una petición crea un proceso/hilo para atender dicha petición"
        hilo = threading.Thread(target=atender_jugador, args=(conexion, direccion))
        hilo.start()
        
        # print equivalente al de hilos.pdf para ver que el hilo principal sigue libre
        print("Hilo principal libre. Hilos activos actualmente:", threading.active_count())

if __name__ == '__main__':
    main()