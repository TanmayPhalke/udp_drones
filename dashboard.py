from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import socket
import time
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

drones = {}  # { drone_id: {"ip": ..., "port": ..., "video_port": ..., "telemetry": {...}} }

@app.route('/')
def home():
    return render_template('dashboard.html', drones=drones)

@app.route('/command', methods=['POST'])
def send_command():
    data = request.json
    drone_ids = data['drone_ids']
    command = data['command']
    for drone_id in drone_ids:
        ip = drones[drone_id]['ip']
        port = drones[drone_id]['port']
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(command.encode(), (ip, port))
    return jsonify({"status": "sent"})

@app.route('/launch_mission', methods=['POST'])
def launch_mission():
    drone_id = request.json['drone_id']
    try:
        subprocess.Popen(["/usr/bin/missionplanner", "--connect", f"udp:127.0.0.1:{14550 + int(drone_id)}"])
        return jsonify({"status": "Mission Planner launched"})
    except Exception as e:
        return jsonify({"status": f"Failed: {str(e)}"}), 500

def udp_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 6060))  # Drone telemetry port
    while True:
        msg, addr = s.recvfrom(1024)
        ip = addr[0]
        data = msg.decode()
        parts = data.split(',')  # drone_id,x,y,battery
        if len(parts) != 4:
            continue
        drone_id, x, y, battery = parts
        drones[drone_id] = {
            "ip": ip,
            "port": 7070,
            "video_port": str(8000 + int(drone_id)),
            "telemetry": {
                "x": x,
                "y": y,
                "battery": battery
            }
        }
        socketio.emit('drone_update', {"drone_id": drone_id, "telemetry": drones[drone_id]['telemetry']})

@socketio.on('connect')
def client_connected():
    emit('init', drones)

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
