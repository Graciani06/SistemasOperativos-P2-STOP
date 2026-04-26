import urllib.request
import time

def prueba_estres(num_partidas):
    print(f"Iniciando prueba de estrés: Creando {num_partidas} partidas simultáneas...")
    exitos = 0
    
    # Uso mi ip de azure actual, hay que cambiarla cada vez que inicie si cambia
    ip_azure = "158.158.34.25" 
    url = f"http://{ip_azure}:8080/stop/new"

    for i in range(num_partidas):
        try:
            # Hacemos una petición HTTP a la API
            respuesta = urllib.request.urlopen(url, timeout=3)
            datos = respuesta.read().decode('utf-8')
            print(f"[{i+1}] Partida creada con éxito: {datos}")
            exitos += 1
        except Exception as e:
            print(f"[{i+1}] Error al crear partida: {e}")
        
        time.sleep(0.1)

    print(f"\n--- RESUMEN ---")
    print(f"Partidas solicitadas: {num_partidas}")
    print(f"Partidas creadas exitosamente: {exitos}")

if __name__ == "__main__":
    prueba_estres(50)