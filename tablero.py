import threading
import time

class TableroJuego:
    def __init__(self):
        self.categorias = {"Marca": "", "Comida": "", "Lugar": "", "Animal": ""}
        self.letra_actual = ""
        self.puntuaciones = {}
        
        #Usamos un semaforo binario para proteger cada categoria por separado
        self.semaforos = {
            "Marca": threading.Semaphore(1),
            "Comida": threading.Semaphore(1),
            "Lugar": threading.Semaphore(1),
            "Animal": threading.Semaphore(1)
        }

    def escribir_en_categoria(self, nombre_jugador, categoria, palabra):
        if nombre_jugador not in self.puntuaciones:
            self.puntuaciones[nombre_jugador] = 0

        #Lo bloqueamos
        self.semaforos[categoria].acquire()
        exito = False
        
        #SECCION CRITICA 
        if self.categorias[categoria] == "":
            time.sleep(2) 
            self.categorias[categoria] = palabra
            self.puntuaciones[nombre_jugador] += 1
            exito = True
        # -----------------------
            
        # Liberamos (signal)
        self.semaforos[categoria].release()
            
        return exito