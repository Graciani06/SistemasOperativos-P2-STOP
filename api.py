from bottle import route, run, default_app
import multiprocessing
import servidor
import random

@route('/stop/new')
def nueva_partida():
    # Asignamos un puerto aleatorio para la partida 
    puerto = random.randint(8000, 9000)
    
    p = multiprocessing.Process(target=servidor.iniciar_partida, args=(puerto,))
    p.start()
    
    return {"status": "success", "partida_id": puerto, "mensaje": f"Conectate al puerto {puerto}"}

@route('/stop/<puerto>')
def unirse_partida(puerto):
    return {"status": "success", "mensaje": f"Usa la terminal para unirte al puerto {puerto}"}

app = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)