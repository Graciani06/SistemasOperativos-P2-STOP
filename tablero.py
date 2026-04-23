import threading
import time

class TableroJuego:
    def __init__(self):
        # Recurso compartido: categorías
        self.categorias = {"Marca": "", "Comida": "", "Lugar": "", "Animal": ""}
        self.letra_actual = ""
        self.puntuaciones = {}
        
        # Semáforos (Mutex) para exclusión mutua (semafors2.pdf)
        self.semaforos = {cat: threading.Semaphore(1) for cat in self.categorias}

    def escribir_en_categoria(self, nombre_jugador, categoria, palabra):
        if nombre_jugador not in self.puntuaciones:
            self.puntuaciones[nombre_jugador] = 0

        # WAIT (P) - Bloqueamos la categoría
        self.semaforos[categoria].acquire()
        exito = False
        
        if self.categorias[categoria] == "":
            time.sleep(5) # Simulación de tiempo de escritura (Sección Crítica)
            self.categorias[categoria] = palabra
            self.puntuaciones[nombre_jugador] += 1
            exito = True
        
        # SIGNAL (V) - Liberamos
        self.semaforos[categoria].release()
        return exito