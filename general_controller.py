from flask import Flask, jsonify, request
import time
import json
import requests

#voir API REST pour vim-emu
#voir comment parler au sdn controller


app = Flask(__name__)

# On redigrige tous les paquets à destination de gwi, à la destination du vnf
def modify_route_gf_to_vnf():
    # URL de l'API REST
    url = "http://localhost:8080/stats/flowentry/modify"

    # Les données JSON à envoyer
    data = {
        "dpid": 1,
        "cookie": 1,
        "cookie_mask": 1,
        "table_id": 0,
        "idle_timeout": 30,
        "hard_timeout": 30,
        "priority": 11111,
        "flags": 1,
        "match": {
            "nw_dst": "10.0.0.1" # adresse du gwi
        },
        "actions": [
            {
                "nw_dst": "10.0.0.200", # adresse du vnf
            }
        ]
    }
    # Envoi de la requête POST
    response = requests.post(url, json=data)

    # Gestion de la réponse
    if response.status_code == 200:
        print("Flow entry successfully modified!")
        print("Response:", response.json())  # Affiche la réponse du serveur
    else:
        print("Failed to modify flow entry.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")



def modify_route_vnf_to_gf():
    # URL de l'API REST
    url = "http://localhost:8080/stats/flowentry/modify"

    # Les données JSON à envoyer
    data = {
        "dpid": 1,
        "cookie": 1,
        "cookie_mask": 1,
        "table_id": 0,
        "idle_timeout": 30,
        "hard_timeout": 30,
        "priority": 11111,
        "flags": 1,
        "match": {
            "nw_src": "10.0.0.200" # adresse du vnf
            "nw_dst": {"10.0.0.10", "10.0.0.20", "10.0.0.30"} # adresses des gf
        },
        "actions": [
            {
                "nw_src": "10.0.0.1", # adresse du gwi
            }
        ]
    # Envoi de la requête POST
    response = requests.post(url, json=data)

    # Gestion de la réponse
    if response.status_code == 200:
        print("Flow entry successfully modified!")
        print("Response:", response.json())  # Affiche la réponse du serveur
    else:
        print("Failed to modify flow entry.")
        print(f"Status Code: {response.status_code}, Response: {response.text}")
}


# Pour créer la VNF, ATTENTION, mettre la bonne adresse IP
@app.route('/new_vnf', methods=['GET'])
def create_vnf():
    url = "http://127.0.0.1:5001/restapi/compute/cvim1/new_vnf"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "image": "ubuntu:trusty",
        "network": "(id=input,ip=10.0.0.1/24),(id=output,ip=20.0.0.1/24)"
    }

    try:
        # Envoyer la requête PUT à l'API cible
        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            response_sdn = modify_route_gf_to_vnf()
            if response_sdn.status_code == 200:
                response_sdn = modify_route_vnf_to_gf()
                if response_sdn.status_code == 200:
                    return jsonify({"status": "success", "message": "VNF created successfully! and Redirection is good!"}), 200
                else:
                    return jsonify({
                        "status": "failure",
                        "message": "Failed to redirect with SDN vnf to gf",
                        "details": response.text
                    }), response.status_code
            else:
                return jsonify({
                    "status": "failure",
                    "message": "Failed to redirect with SDN gf to vnf",
                    "details": response.text
                }), response.status_code
        else:
            return jsonify({
                "status": "failure",
                "message": "Failed to create VNF.",
                "details": response.text
            }), response.status_code

    except requests.exceptions.RequestException as e:
        # En cas d'erreur réseau ou autre exception
        return jsonify({
            "status": "failure",
            "message": "An error occurred while communicating with the API.",
            "error": str(e)
        }), 500

## Pour ajouter redirection, il faut trouver un moyen de, après etre passé par la vnf, rediriger tout le signal soit vers la gwi soit vers la gwi2 que l'on va créer 
## tout ça dépendamment de l'adresse du gf source que l'on a plus vu que c'est celle de la vnf qui apparait maintenant

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1234, debug=True)