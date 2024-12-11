from flask import Flask, jsonify, request
import time
import json
import requests

app = Flask(__name__)

# Il faut que le general controller s'adresse à nous via l'adresse IP exterieur du docker
# Il faut que ce monitoring vnf envoie les infos vers la gwi
# Les paquets qui vont être reçu ici sont modifié avant par le SDN controller afin que les paquets qui ont à la base dest_ip = gwi_ip et dest_port = gwi_port deviennent dest_ip = monitoring_vnf_ip et dest_port = monitoring_vnf_port
local_ip = "10.0.0.200"
local_port = 8181  # même port que le gwi pour pas avoir à modifier depuis sdn

gwi_ip = "10.0.0.1"

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
start_time = time.time()

def increment_packet_count(addr):
    if addr in packet_count:
        packet_count[addr] += 1

# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateways/register', methods=['POST'])
def gateways_register():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(gwi_ip + "/gateways/register", json=request.json)
    return resp
    
# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/devices/register', methods=['POST'])
def devices_register():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(gwi_ip + "/devices/register", json=request.json)
    return resp

# J'intercepte le POST à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/device/<dev>/data', methods=['POST'])
def device_data(dev):
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.post(gwi_ip + "/device/<dev>/data", json=request.json)
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateways', methods=['GET'])
def get_gateways():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(gwi_ip + "/gateways")
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/gateway/<gw>', methods=['GET'])
def get_gateway(gw):
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(gwi_ip + "/gateway/<gw>")
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/ping', methods=['GET'])
def ping():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(gwi_ip + "/ping")
    return resp

# J'intercepte le GET à direction de gwi et ajoute au compteur que j'ai vu une trame passé, puis je transmet la donnée recu pour rester invisible au yeux du gwi et du gwf
@app.route('/health', methods=['GET'])
def health():
    global packet_count
    increment_packet_count(request.remote_addr)
    resp = requests.get(gwi_ip + "/health")
    return resp

# Pour calculer le nombre de bytes en un temps x -> possibilité d'avoir le débit
def calculate_bitrate():
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
    return jsonify(bitrate)

# Fonction principale
def main():
    while True:
        calculate_bitrate()
        time.sleep(100)


if __name__ == "__main__":
    # Démarre le REST dans un autre thread
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host=local_ip, port=local_port))
    flask_thread.start()

    main()