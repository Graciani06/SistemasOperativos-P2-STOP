import socket
import threading

def escuchar(s):
    while True:
        try:
            data = s.recv(2048).decode('utf-8')
            if not data: break
            print(data)
        except: break

def main():
    ip = "127.0.0.1"
    puerto = int(input("Introduce el puerto de la partida (ej: 8000): "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))
    
    nombre = input("Tu nombre: ")
    s.send(nombre.encode('utf-8'))
    
    threading.Thread(target=escuchar, args=(s,), daemon=True).start()
    
    print("Escribe 'GO!. 'SALIR' para irte.")
    while True:
        msg = input()
        if msg.upper() == "SALIR": break
        s.send(msg.encode('utf-8'))
    s.close()

if __name__ == "__main__":
    main()