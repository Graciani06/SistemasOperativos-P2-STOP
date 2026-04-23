from bottle import route, run, default_app
import multiprocessing
import servidor
import socket

puertos_activos = []

def obtener_puerto_libre():
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
    puertos_activos.append(puerto)
    return {"status": "success", "partida_id": puerto, "mensaje": f"Conectate al puerto {puerto}"}

@route('/stop/list')
def listar_partidas():
    return {"partidas_activas": puertos_activos}

# NUEVO: Gunicorn necesita este objeto 'app' para funcionar en el servidor Linux
app = default_app()

if __name__ == '__main__':
    # Esto SOLO se ejecutará en tu Windows local para hacer pruebas
    run(host='0.0.0.0', port=8080)