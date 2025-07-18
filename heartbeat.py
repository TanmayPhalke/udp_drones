import socket, json, time

DRONE_ID = "DRONE_001"
GCS_IP = "100.113.114.176"
PORT = 6060

while True:
    packet = {
        "drone_id": DRONE_ID,
        "battery": 88,      # You can later connect to MAVLink
        "gps_fix": True,
        "timestamp": time.time()
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(json.dumps(packet).encode(), (GCS_IP, PORT))
    time.sleep(2)