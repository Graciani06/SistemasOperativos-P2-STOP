from bottle import route, run, default_app
import multiprocessing
import servidor
import socket

try:
    multiprocessing.set_start_method('spawn')
except RuntimeError:
    pass

def obtener_puerto_libre():
    #lE pedimos al Sistema Operativo que nos de un puerto libre
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    puerto = s.getsockname()[1]
    s.close()
    return puerto

@route('/stop/new')
def nueva_partida():
    puerto = obtener_puerto_libre()
    
    p = multiprocessing.Process(target=servidor.iniciar_partida, args=(puerto,))
    p.start()
    
    return {"status": "success", "partida_id": puerto, "mensaje": f"Conectate al puerto {puerto}"}

@route('/stop/<puerto>')
def unirse_partida(puerto):
    return {"status": "success", "mensaje": f"Usa la terminal para unirte al puerto {puerto}"}

app = default_app()

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)