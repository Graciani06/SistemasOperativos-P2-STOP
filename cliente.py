import socket
import threading  # Aplicamos la teoría de hilos.pdf (pág 6) al cliente

def escuchar_servidor(conexion):
    """
    Este hilo independiente se dedica ÚNICAMENTE a hacer el Receive bloqueante.
    Así recibimos los avisos de otros jugadores en tiempo real
    sin que nuestro teclado nos bloquee.
    """
    while True:
        try:
            # RECEIVE BLOQUEANTE
            respuesta = conexion.recv(2048)
            if not respuesta:
                print("\nEl servidor ha cerrado la conexión.")
                break
            
            # Imprimimos lo que nos diga el servidor
            print(respuesta.decode('utf-8'))
        except:
            # Si hay un error (ej: cerramos el cliente), salimos del bucle
            break

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print("Conectando al servidor de STOP!...")
    s.connect(('127.0.0.1', 65432))
    
    # 1. CREAMOS EL HILO RECEPTOR
    # Arrancamos un hilo secundario que se quede escuchando
    hilo_escucha = threading.Thread(target=escuchar_servidor, args=(s,))
    # Lo marcamos como "daemon" para que muera automáticamente si cerramos el programa principal
    hilo_escucha.daemon = True 
    hilo_escucha.start()
    
    # 2. BUCLE DEL HILO PRINCIPAL (EMISOR)
    
    
    while True:
        # El programa principal se queda bloqueado aquí esperando tu teclado
        mensaje = input()
        
        if mensaje.upper() == "SALIR":
            break
            
        # SEND
        s.send(mensaje.encode('utf-8'))
        
    s.close()
    print("Te has desconectado del juego.")

if __name__ == '__main__':
    main()