from flask import Flask, jsonify, request
import time
from threading import Lock
import socket
import http.client
import json

app = Flask(__name__)

local_ip = "0.0.0.0"
local_port = 8181  # même port que le gwi pour éviter de modifier depuis SDN
ip_gwi = "10.0.0.1"

packet_count = {}

bitrate = {}

# Mappage des tos en fonction des ips
tos_mapping = {
    "10.0.0.10": 4,
    "10.0.0.20": 8,
    "10.0.0.30": 16
}

packet_count_lock = Lock()
bitrate_lock = Lock()

start_time = time.time()

class TOSAdapter(http.client.HTTPConnection):
    def __init__(self, host, port, tos, timeout=None):
        super().__init__(host, port, timeout=timeout)
        self.tos = tos

    def connect(self):
        # On précise le tos avant de démarrer la connexion
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, self.tos)
        self.sock.connect((self.host, self.port))

def send_with_tos(method, url, payload, client_ip):
    tos = tos_mapping.get(client_ip, 0)  
    # On créé la connexion tcp nous même 
    conn = TOSAdapter(ip_gwi, local_port, tos)
    try:
        if method.upper() == "GET":
            conn.request("GET", url)
        elif method.upper() == "POST":
            if payload:
                json_payload = json.dumps(payload)
                headers = {'Content-Type': 'application/json'}
                conn.request("POST", url, json_payload, headers)
            else:
                conn.request("POST", url)
        response = conn.getresponse()
        data = response.read() 
        conn.close() 
        return data  # On retourne la réponse
    except Exception as e:
        print(f"[ERROR] Request failed for {client_ip}: {e}")
        return None  

@app.route('/gateways/register', methods=['POST'])
def gateways_register():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateways/register"
    # On passe par notre propre connexion pour envoyer la requete http afin de placer notre tos
    response_data = send_with_tos("POST", url, request.json, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/devices/register', methods=['POST'])
def devices_register():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/devices/register"
    response_data = send_with_tos("POST", url, request.json, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/device/<dev>/data', methods=['POST'])
def device_data(dev):
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/device/{dev}/data"
    response_data = send_with_tos("POST", url, request.json, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/gateways', methods=['GET'])
def get_gateways():
    client_ip = request.remote_addr
    print(f'adresse : {client_ip}')
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateways"
    response_data = send_with_tos("GET", url, None, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/gateway/<gw>', methods=['GET'])
def get_gateway(gw):
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateway/{gw}"
    response_data = send_with_tos("GET", url, None, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/ping', methods=['GET'])
def ping():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/ping"
    response_data = send_with_tos("GET", url, None, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

@app.route('/health', methods=['GET'])
def health():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/health"
    response_data = send_with_tos("GET", url, None, client_ip)
    if response_data:
        return response_data, 201
    else:
        return jsonify({"error": "Request failed"}), 500

def increment_packet_count(addr):
    global packet_count
    with packet_count_lock:
        if addr not in packet_count:
            packet_count[addr] = 0  # Initialise l'adresse avec un compteur à 0 si elle n'existe pas
        packet_count[addr] += 1
    with bitrate_lock:
        if addr not in bitrate:
            bitrate[addr] = 0  # Initialise le bitrate si nécessaire


def calculate_bitrate():
    global bitrate, packet_count, start_time
    try:
        elapsed_time = time.time() - start_time
        with packet_count_lock, bitrate_lock:
            for ip in packet_count:
                bitrate[ip] = packet_count[ip] / elapsed_time if elapsed_time > 0 else 0
                packet_count[ip] = 0
            start_time = time.time()
    except Exception as e:
        print(f"[ERROR] Error calculating bitrate: {e}")

@app.route('/bitrate', methods=['GET'])
def get_throughput():
    global bitrate
    try:
        with bitrate_lock:
            return jsonify(bitrate)
    except Exception as e:
        print(f"[ERROR] Error retrieving bitrate: {e}")
        return "", 500

def main():
    try:
        while True:
            calculate_bitrate()
            time.sleep(5)
    except KeyboardInterrupt:
        print("[INFO] Stopping the application.")
    except Exception as e:
        print(f"[ERROR] Error in main loop: {e}")

if __name__ == "__main__":
    from threading import Thread
    try:
        flask_thread = Thread(target=lambda: app.run(host=local_ip, port=local_port))
        flask_thread.start()
        main()
    except Exception as e:
        print(f"[CRITICAL] Critical error in main application: {e}")
