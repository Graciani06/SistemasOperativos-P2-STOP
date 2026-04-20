def __init__(self):
        # ... (tus categorías y semáforos) ...
        self.categorias = {"Marca": "", "Comida": "", "Lugar": "", "Animal": ""}
        self.letra_actual = ""
        
        # NUEVO: Diccionario para llevar la cuenta de puntos de cada nombre
        self.puntuaciones = {}
        
        # ... (tus semáforos) ...

    def escribir_en_categoria(self, nombre_jugador, categoria, palabra):
        # Nos aseguramos de que el jugador esté en el diccionario de puntos
        if nombre_jugador not in self.puntuaciones:
            self.puntuaciones[nombre_jugador] = 0

        self.semaforos[categoria].acquire()
        
        # SECCIÓN CRÍTICA
        if self.categorias[categoria] == "":
            time.sleep(5) 
            self.categorias[categoria] = palabra
            # NUEVO: Sumamos un punto al jugador que ha ganado la posición
            self.puntuaciones[nombre_jugador] += 1
            print("[" + nombre_jugador + "] +1 punto por " + categoria)
        else:
            print("[" + nombre_jugador + "] llegó tarde.")
            
        self.semaforos[categoria].release()