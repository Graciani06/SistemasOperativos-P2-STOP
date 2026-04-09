import socket

def main():
    # 1. Creamos nuestro propio "Buzón" usando Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Conectamos nuestro buzón con el del servidor (destino)
    print("Conectando al servidor de STOP!...")
    s.connect(('127.0.0.1', 65432))
    
    # 3. SEND (pasoDeMensajes.pdf pág 3)
    # Pedimos al usuario que escriba por teclado usando input()
    mensaje = input("Escribe una palabra para la categoria Animal: ")
    
    print("Enviando mensaje: " + mensaje)
    s.send(mensaje.encode('utf-8'))
    
    # 4. RECEIVE BLOQUEANTE (pasoDeMensajes.pdf pág 4)
    # Ahora el cliente hace un receive y se queda bloqueado esperando
    # a que el servidor le conteste que ha recibido el mensaje.
    respuesta = s.recv(1024)
    
    # Decodificamos los bytes recibidos a texto y lo imprimimos
    print("El servidor me ha contestado:", respuesta.decode('utf-8'))
    
    # 5. Cerramos la comunicación
    s.close()
    print("Conexión cerrada.")

if __name__ == '__main__':
    main()