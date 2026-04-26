import socket
import threading
import os 

def recibir_mensajes(s):
    while True:
        data = s.recv(2048).decode('utf-8')
        
        if not data: 
            print("\n[Desconectado del servidor]")
            os._exit(0) 
            
        print(data)

def main():
    while True:
        ip = input("IP del servidor: ").strip()
        partes = ip.split('.')
        
        es_valida = True 
        if len(partes) == 4:
            for p in partes:
                if not p.isdigit():
                    es_valida = False
        else:
            es_valida = False
            
        if es_valida:
            break 
        else:
            print("Formato incorrecto. Ejemplo: 192.168.1.10")
    
    puerto = int(input("Puerto de la partida: "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))
    
    nombre = input("Introduce tu nombre: ")
    s.send(nombre.encode('utf-8'))
    
    hilo = threading.Thread(target=recibir_mensajes, args=(s,), daemon=True)
    hilo.start()
    
    print("Para jugar escribe 'Categoria, Palabra'. Para salir pon 'SALIR'.")
    
    while True:
        msg = input()
        if msg.upper() == "SALIR": 
            break
        
        s.send(msg.encode('utf-8'))
        
    #Cuando salimos del bucle (escribiendo SALIR), cerramos la conexion
    s.close()

if __name__ == "__main__":
    main()