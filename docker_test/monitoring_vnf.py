from flask import Flask, jsonify, request
import time
import requests
from threading import Lock

app = Flask(__name__)

local_ip = "0.0.0.0"
local_port = 8181  # même port que le gwi pour éviter de modifier depuis SDN
ip_gwi = "10.0.0.1"

packet_count = {
    "10.0.0.10": 0,
    "10.0.0.20": 0,
    "10.0.0.30": 0
}
bitrate = {
    "10.0.0.10": 0,
    "10.0.0.20": 0,
    "10.0.0.30": 0
}
addr = {
    "10.0.0.10": "10.0.0.251",
    "10.0.0.20": "10.0.0.252",
    "10.0.0.30": "10.0.0.253"
}
port = {
    "10.0.0.10": 2001,
    "10.0.0.20": 2002,
    "10.0.0.30": 2003
}

E_OK              = 200
E_CREATED         = 201
E_FORBIDDEN       = 403
E_NOT_FOUND       = 404
E_ALREADY_EXIST   = 500

packet_count_lock = Lock()
bitrate_lock = Lock()

start_time = time.time()

def increment_packet_count(addr):
    global packet_count
    with packet_count_lock:
        if addr in packet_count:
            packet_count[addr] += 1

@app.route('/gateways/register', methods=['POST'])
def gateways_register():

    try:
        increment_packet_count(request.remote_addr)
        ##### Voir comment recup ip source
        #resp = requests.post(f"http://{addr[request.remote_addr]}:{local_port}/gateways/register", json=request)
        resp = requests.post(f"http://{ip_gwi}:{local_port}/gateways/register", json=request.json)
        #resp = requests.post(f"http://{ip_gwi}:{port[request.remote_addr]}/gateways/register", json=request.json)
        print(f"request: {request.json}")
        return "", E_CREATED
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /gateways/register: {e}")
        return "", E_ALREADY_EXIST

@app.route('/devices/register', methods=['POST'])
def devices_register():
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.post(f"http://{addr[request.remote_addr]}:{local_port}/devices/register", json=request)
        resp = requests.post(f"http://{ip_gwi}:{local_port}/devices/register", json=request.json)
        #resp = requests.post(f"http://{ip_gwi}:{port[request.remote_addr]}/devices/register", json=request.json)
        print(f"request: {request.json}")
        return "", E_OK
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /devices/register: {e}")

@app.route('/device/<dev>/data', methods=['POST'])
def device_data(dev):
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.post(f"http://{addr[request.remote_addr]}:{local_port}/device/{dev}/data", json=request)
        resp = requests.post(f"http://{ip_gwi}:{local_port}/device/{dev}/data", json=request.json)
        #resp = requests.post(f"http://{ip_gwi}:{port[request.remote_addr]}/device/{dev}/data", json=request.json)
        print(f"request: {request.json}")
        return "", E_OK
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /device/{dev}/data: {e}")

@app.route('/gateways', methods=['GET'])
def get_gateways():
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.get(f"http://{addr[request.remote_addr]}:{local_port}/gateways")
        resp = requests.get(f"http://{ip_gwi}:{local_port}/gateways")
        #resp = requests.get(f"http://{ip_gwi}:{port[request.remote_addr]}/gateways")
        print(f"resp: {resp.json()}")
        return resp.json()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /gateways: {e}")

@app.route('/gateway/<gw>', methods=['GET'])
def get_gateway(gw):
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.get(f"http://{addr[request.remote_addr]}:{local_port}/gateway/{gw}")
        resp = requests.get(f"http://{ip_gwi}:{local_port}/gateway/{gw}")
        #resp = requests.get(f"http://{ip_gwi}:{port[request.remote_addr]}/gateway/{gw}")
        print(f"resp: {resp.json()}")
        return resp.json(), E_OK
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /gateway/{gw}: {e}")
        return "", E_NOT_FOUND

@app.route('/ping', methods=['GET'])
def ping():
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.get(f"http://{addr[request.remote_addr]}:{local_port}/ping")
        resp = requests.get(f"http://{ip_gwi}:{local_port}/ping")
        #resp = requests.get(f"http://{ip_gwi}:{port[request.remote_addr]}/ping")
        return "", E_OK
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /ping: {e}")

@app.route('/health', methods=['GET'])
def health():
    try:
        increment_packet_count(request.remote_addr)
        #resp = requests.get(f"http://{addr[request.remote_addr]}:{local_port}/health")
        resp = requests.get(f"http://{ip_gwi}:{local_port}/health")
        #resp = requests.get(f"http://{ip_gwi}:{port[request.remote_addr]}/health")
        print(f"resp: {resp.json()}")
        return "", E_OK
    except requests.RequestException as e:
        print(f"[ERROR] Failed to process /health: {e}")

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


# CHanger addr ip par celle mise dans le launch + ne pas attendre reponse car il y en aura surement pas vu que le paquet est modifié