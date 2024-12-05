from flask import Flask, jsonify, request
import time
import json
import requests

app = Flask(__name__)
local_ip = "0.0.0.0"
local_port = 5000
# Recopier infos de la gateway intermediaire pour se faire passer pour elle
packet_count = {
    "192.168.1.1": 0,
    "192.168.2.1": 0,
    "192.168.3.1": 0
}
bitrate = {
    "192.168.1.1": 0,
    "192.168.2.1": 0,
    "192.168.3.1": 0
}
start_time = time.time()

def increment_packet_count(addr):
    if addr in packet_count:
        packet_count[addr] += 1

# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateways/register', methods=['POST'])
def gateways_register():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(request.url, json=request.json)
    return resp
    
# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/devices/register', methods=['POST'])
def devices_register():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(request.url, json=request.json)
    return resp

# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/device/<dev>/data', methods=['POST'])
def device_data(dev):
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(request.url, json=request.json)
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateways', methods=['GET'])
def get_gateways():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(request.url)
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateway/<gw>', methods=['GET'])
def get_gateway(gw):
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(request.url)
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/ping', methods=['GET'])
def ping():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(request.url)
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/health', methods=['GET'])
def health():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(request.url)
    return resp

# Pour calculer le nombre de bytes en un temps x -> possibilité d'avoir le débit
def calculate_throughput():
    global bitrate, packet_count, start_time
    elapsed_time = time.time() - start_time
    for ip in packet_count:
        bitrate[ip] = packet_count[ip] / elapsed_time
        packet_count[ip]=0
    # Je remet à time.time() le start time comme ça j'ai un bitrate calculé sur les 100 dernières millisecondes
    start_time = time.time()

# Pour accéder aux infos sur le debit REST
@app.route('/bitrate', methods=['GET'])
def get_throughput():
    global bitrate
    return jsonify({"bitrate_gf1": bitrate[0], "bitrate_gf2": bitrate[1], "bitrate_gf2": bitrate[2]})

# Fonction principale
def main():
    while True:
        calculate_throughput()
        time.sleep(100)


if __name__ == "__main__":
    # Démarre le REST dans un autre thread
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host=local_ip, port=local_port))
    flask_thread.start()

    main()