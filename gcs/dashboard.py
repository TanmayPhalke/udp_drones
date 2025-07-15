from flask import Flask, jsonify
import threading, time, socket, json

app = Flask(__name__)
drones = {}

def udp_listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", 5050))
    while True:
        try:
            data, _ = s.recvfrom(1024)
            drone = json.loads(data.decode())
            drones[drone["drone_id"]] = {
                "battery": drone["battery"],
                "gps_fix": drone["gps_fix"],
                "last_seen": time.time()
            }
        except: pass

@app.route("/")
def home():
    now = time.time()
    view = {}
    for d, info in drones.items():
        age = now - info["last_seen"]
        status = "🟢 Online" if age < 5 else "🔴 Offline"
        view[d] = {
            "battery": info["battery"],
            "gps": "✅" if info["gps_fix"] else "❌",
            "last_seen": f"{int(age)} sec ago",
            "status": status
        }
    return jsonify(view)

if __name__ == "__main__":
    threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)
