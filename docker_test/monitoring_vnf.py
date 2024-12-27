from flask import Flask, jsonify, request
import time
import requests
from requests.adapters import HTTPAdapter
from threading import Lock
import socket
from threading import Thread


app = Flask(__name__)

local_ip = "0.0.0.0"
local_port = 8181  # même port que le gwi pour éviter de modifier depuis SDN
ip_gwi = "10.0.0.1"

packet_count = {
    "10.0.0.10": 0,
    "10.0.0.20": 0,
    "10.0.0.30": 0
}

bitrate = {}

# Mapping des TOS par IP
tos_mapping = {
    "10.0.0.10": 4,
    "10.0.0.20": 8,
    "10.0.0.30": 16
}

packet_count_lock = Lock()
bitrate_lock = Lock()

start_time = time.time()

class TOSAdapter(HTTPAdapter):
    """Adapter pour envoyer des requêtes avec un TOS spécifique."""
    def __init__(self, tos_value, *args, **kwargs):
        self.tos_value = tos_value
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        class TOSConnectionPool(requests.packages.urllib3.poolmanager.PoolManager):
            def _new_conn(self):
                conn = super()._new_conn()
                conn.sock.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, self.tos_value)
                return conn
        self.poolmanager = TOSConnectionPool(*args, **kwargs)


#def send_with_tos(req_type, url, json_data, client_ip):
def send_with_tos(url, json_data, client_ip):
    """Envoie une requête avec un TOS spécifique."""
    tos = tos_mapping.get(client_ip, 0)  # Par défaut 0
    session = requests.Session()
    adapter = TOSAdapter(tos_value=tos)
    session.mount("http://", adapter)
    try:
        session.post(url, json=json_data, timeout=1)
        # if req_type == "POST":
        #     session.post(url, json=json_data, timeout=1)  # Timeout court pour ne pas attendre de réponse.
        # elif req_type == "GET":
        #     session.get(url, timeout=1)  # Timeout court pour ne pas attendre de réponse.
    except Exception as e:
        print(f"[ERROR] Requête échouée pour {client_ip} avec TOS {tos}: {e}")


@app.route('/gateways/register', methods=['POST'])
def gateways_register():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateways/register"
    #send_with_tos("POST", url, request.json, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip} avec data {request.json}")
    return "", 201

@app.route('/devices/register', methods=['POST'])
def devices_register():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/devices/register"
    # send_with_tos("POST", url, request.json, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip} avec data {request.json}")
    return "", 201

@app.route('/device/<dev>/data', methods=['POST'])
def device_data(dev):
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/device/{dev}/data"
    # send_with_tos("POST", url, request.json, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip} avec data {request.json}")
    return "", 201

@app.route('/gateways', methods=['GET'])
def get_gateways():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateways"
    # send_with_tos("GET", url, None, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip}")
    return "", 201

@app.route('/gateway/<gw>', methods=['GET'])
def get_gateway(gw):
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/gateway/{gw}"
    # send_with_tos("GET", url, None, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip}")
    return "", 201

@app.route('/ping', methods=['GET'])
def ping():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/ping"
    # send_with_tos("GET", url, None, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip}")
    return "", 201

@app.route('/health', methods=['GET'])
def health():
    client_ip = request.remote_addr
    increment_packet_count(client_ip)
    url = f"http://{ip_gwi}:{local_port}/health"
    # send_with_tos("GET", url, None, client_ip)
    send_with_tos(url, request.json, client_ip)
    print(f"[INFO] Requête envoyée pour {client_ip}")
    return "", 201

def increment_packet_count(addr):
    global packet_count, bitrate
    with packet_count_lock:
        if addr not in packet_count:
            packet_count[addr] = 0  # Initialise le compteur
        packet_count[addr] += 1
    with bitrate_lock:
        if addr not in bitrate:
            bitrate[addr] = 0  # Initialise le débit si nécessaire


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
    try:
        flask_thread = Thread(target=lambda: app.run(host=local_ip, port=local_port))
        flask_thread.start()
        main()
    except Exception as e:
        print(f"[CRITICAL] Critical error in main application: {e}")


# CHanger addr ip par celle mise dans le launch + ne pas attendre reponse car il y en aura surement pas vu que le paquet est modifié