import websocket
import json
import numpy as np
import threading
import sys
from time import sleep
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Filtro de Kalman para estimar a aceleração linear

dt = 1.0  # Intervalo de tempo (segundos)

# Matrizes do modelo
A = np.array([[1, dt], [0, 1]])  # Matriz de transição de estado (modelo de movimento)
B = np.array([[0.5 * dt**2], [dt]])  # Matriz de controle (não usada neste caso)
H = np.array([[1, 0]])  # Matriz de observação (observamos diretamente a aceleração)
Q = np.array([[1e-5, 0], [0, 1e-5]])  # Ruído do processo (baixo)
R = np.array([[1]])  # Ruído da medição (assumido como alto, devido ao ruído no sensor)
P = np.eye(2)  # Covariância inicial do erro
x = np.array([[0], [0]])  # Estado inicial (aceleração e velocidade)

# Variáveis globais para armazenar a posição estimada
x_pos = 0
y_pos = 0
z_pos = 0

# Função do filtro de Kalman
def kalman_filter(z):
    global x, P
    # Predição
    x_pred = np.dot(A, x)  # Predição do estado
    P_pred = np.dot(np.dot(A, P), A.T) + Q  # Predição da covariância

    # Atualização (medição)
    y = z - np.dot(H, x_pred)  # Inovação (erro de medição)
    S = np.dot(np.dot(H, P_pred), H.T) + R  # Covariância de inovação
    K = np.dot(np.dot(P_pred, H.T), np.linalg.inv(S))  # Ganho de Kalman

    # Atualização do estado
    x = x_pred + np.dot(K, y)

    # Atualização da covariância
    P = np.dot(np.eye(2) - np.dot(K, H), P_pred)

    return x[0, 0], x[1, 0]  # Retorna a aceleração estimada e a velocidade estimada

# Funções de WebSocket para GPS
closed = False

def on_message(ws, message):
    data = json.loads(message)
    lat, long, alti, time = data["latitude"], data["longitude"], data["altitude"], data["time"]
    lastKnownLocation = data["lastKnowLocation"]
    print(f"({lat},{long}, {alti}, {time}) response to getLastKnownLocation = {lastKnownLocation}")
    
    # Atualiza a posição GPS
    global x_pos, y_pos, z_pos
    x_pos, y_pos, z_pos = lat, long, alti

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    global closed
    closed = True
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")
    thread = threading.Thread(target=send_requests, args=(ws,))
    thread.start()

def send_requests(ws):
    while True:
        if not closed:
            ws.send("getLastKnownLocation")
            sleep(1)  # 1 second sleep
        else:
            sys.exit()  # stop this thread    

def connect_gps(url):
    ws = websocket.WebSocketApp(url,
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ws.run_forever()

# Funções de WebSocket para Acelerômetro
def on_message_accel(ws, message):
    global x_pos, y_pos, z_pos
    data = json.loads(message)
    x_accel, y_accel, z_accel = data['values'][0], data['values'][1], data['values'][2]
    
    # Aplica o filtro de Kalman para estimar a aceleração
    accel_estimada, velocidade_estimada = kalman_filter(z_accel)
    
    # Estima a posição com base na aceleração
    x_pos += velocidade_estimada * dt
    y_pos += velocidade_estimada * dt
    z_pos += accel_estimada * dt  # Pode ajustar isso conforme o modelo de movimento real
    
    print(f"Posição estimada: ({x_pos:.2f}, {y_pos:.2f}, {z_pos:.2f})")

def on_error_accel(ws, error):
    print("error occurred ", error)
    
def on_close_accel(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open_accel(ws):
    print("connected to accelerometer")

def connect_accel(url):
    ws = websocket.WebSocketApp(url,
                                 on_open=on_open_accel,
                                 on_message=on_message_accel,
                                 on_error=on_error_accel,
                                 on_close=on_close_accel)
    ws.run_forever()

# Função para plotar a posição 3D dinamicamente
def plot_position():
    global x_pos, y_pos, z_pos
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('Altitude')
    
    while True:
        ax.scatter(x_pos, y_pos, z_pos, color='r')
        ax.set_xlim([x_pos-1, x_pos+1])
        ax.set_ylim([y_pos-1, y_pos+1])
        ax.set_zlim([z_pos-1, z_pos+1])
        plt.pause(0.1)  # Atualiza a cada 0.1 segundo
        plt.draw()

# Conectar aos WebSockets e plotar a posição
def main():
    gps_url = "ws://192.168.1.10:8080/gps"
    accel_url = "ws://192.168.1.10:8080/sensor/connect?type=android.sensor.accelerometer"
    
    # Cria threads para conexões de WebSocket
    threading.Thread(target=connect_gps, args=(gps_url,)).start()
    threading.Thread(target=connect_accel, args=(accel_url,)).start()
    
    # Inicia o gráfico
    plot_position()

if __name__ == "__main__":
    main()
