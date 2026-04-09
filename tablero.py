import threading
import time

class TableroJuego:
    def __init__(self):
        # 1. Nuestro Recurso Compartido
        self.categorias = {
            "Marca": "",
            "Comida": "",
            "Lugar": "",
            "Animal": ""
        }
        
        # 2. Nuestros Semáforos (Mutex inicializados a 1)
        self.semaforos = {
            "Marca": threading.Semaphore(1),
            "Comida": threading.Semaphore(1),
            "Lugar": threading.Semaphore(1),
            "Animal": threading.Semaphore(1)
        }

    def escribir_en_categoria(self, nombre_jugador, categoria, palabra):
        print("[" + nombre_jugador + "] Intentando escribir en la categoria: " + categoria)
        
        # -------------------------------------------------------------
        # WAIT (P(s), Down)
        # Si la categoría está libre, pasa. Si está ocupada, se bloquea.
        # -------------------------------------------------------------
        self.semaforos[categoria].acquire()
        
        # --- INICIO DE LA SECCIÓN CRÍTICA ---
        print("[" + nombre_jugador + "] ha bloqueado la categoria. Escribiendo...")
        
        # Bloqueamos durante 5 segundos como pide el enunciado
        time.sleep(5) 
        
        # Escribimos en el recurso compartido
        self.categorias[categoria] = palabra
        print("[" + nombre_jugador + "] ha escrito: " + palabra)
        # --- FIN DE LA SECCIÓN CRÍTICA ---
            
        # -------------------------------------------------------------
        # SIGNAL (V(s), Up)
        # Libera el semáforo y despierta a otros hilos.
        # -------------------------------------------------------------
        self.semaforos[categoria].release()
        
        print("[" + nombre_jugador + "] ha liberado la categoria: " + categoria)


# --- PRUEBA LOCAL (Sin sockets todavía) ---
if __name__ == "__main__":
    tablero = TableroJuego()

    # Simulamos dos funciones que ejecutarán dos hilos distintos
    def jugador1():
        tablero.escribir_en_categoria("Jugador 1", "Animal", "Perro")

    def jugador2():
        tablero.escribir_en_categoria("Jugador 2", "Animal", "Pato")

    # Creamos dos hilos apuntando a la misma categoría al mismo tiempo
    h1 = threading.Thread(target=jugador1)
    h2 = threading.Thread(target=jugador2)

    # ¡GO! Arrancamos los hilos a la vez
    h1.start()
    h2.start()

    # Esperamos a que terminen (como en la pag 6 de hilos.pdf)
    h1.join()
    h2.join()
    
    print("\nEstado final del tablero:")
    print(tablero.categorias)




# --- PRUEBA LOCAL (Sin sockets todavía) ---
if __name__ == "__main__":
    tablero = TableroJuego()

    # Simulamos dos funciones que ejecutarán dos hilos distintos
    def jugador1():
        tablero.escribir_en_categoria("Jugador 1", "Animal", "Perro")

    def jugador2():
        tablero.escribir_en_categoria("Jugador 2", "Animal", "Pato")

    # Creamos dos hilos apuntando a la misma categoría al mismo tiempo
    h1 = threading.Thread(target=jugador1)
    h2 = threading.Thread(target=jugador2)

    # ¡GO! Arrancamos los hilos a la vez
    h1.start()
    h2.start()

    h1.join()
    h2.join()
    
    print("\nEstado final del recurso compartido:")
    print(tablero.categorias)