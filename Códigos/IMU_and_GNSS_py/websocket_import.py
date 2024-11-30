import websocket
import json
from xyz_to_ned import xyztoned

accel_data = None
gyro_data = None
mag_data = None

def on_message(ws, message):
    global accel_data, gyro_data, mag_data, i

    bruto = json.loads(message)

    if bruto["type"] == "android.sensor.accelerometer":
        accel_data = bruto["values"]

    if bruto["type"] == "android.sensor.gyroscope":
        gyro_data = bruto["values"]

    if bruto["type"] == "android.sensor.magnetic_field":
        mag_data = bruto["values"]

    if accel_data is not None and gyro_data is not None and mag_data is not None:

        time = bruto["timestamp"]        
        xyztoned(accel_data, gyro_data, mag_data, time)

        accel_data = None
        gyro_data = None
        mag_data = None

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")
    

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
 
 
connect('ws://192.168.1.13:8080/sensors/connect?types=["android.sensor.accelerometer","android.sensor.gyroscope","android.sensor.magnetic_field"]]') 
