import requests
import json
import argparse

def create_vnf_gi():
    # On créé le vnf gateway intermediaire et on récupère son adresse mac
    url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_gI"
    headers = {'Content-Type': 'application/json'}
    data = {
        "image": "gateway_intermediaire_vnf-image",
        "network": "(id=gwi,ip=10.0.0.2/24)"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            response_json = response.json()
            mac_address = response_json['network'][0]['mac']
            print(f"Adresse MAC récupérée : {mac_address}")
            return mac_address
        except KeyError:
            print("Erreur : l'adresse MAC n'a pas été trouvée dans la réponse.")
    else:
        print(f"Erreur dans la création du VNF : {response.status_code}")
    return None

def modify_request_vnf_to_new_gi(dscp, mac_dst):
    # On ajoute une règle dans le switch présent dans le datacenter pour rediriger le traffic de la zone x en sortie du vnf de monitoring vers notre gateway vnf 
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 1001,
        "priority": 1111, 
        "match": {
            "in_port": 2,
                "nw_src": "10.0.0.200", 
                "nw_dst": "10.0.0.1",
                "ip_dscp": dscp, # tos = dscp<<2
                "dl_type": 2048                
            },
        "actions": [
            {"type": "SET_FIELD", "field": "ipv4_dst", "value": "10.0.0.2"},
            {"type": "SET_FIELD", "field": "eth_dst", "value": mac_dst},
            {"type": "OUTPUT", "port": 3}  
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Modification des trames de réponse ajoutée avec succès.")
    else:
        print(f"Erreur lors de la modification des trames : {response.status_code}")

def modify_request_new_gi_to_vnf():
    # On ajoute une règle dans le switch présent dans le datacenter pour modifier l'adresse source afin que le vnf de monitoring n'y voit que du feu 
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 1001,
        "priority": 1111, 
        "match": {
            "in_port": 3,
                "nw_src": "10.0.0.2", 
                "nw_dst": "10.0.0.200",
                "dl_type": 2048                
            },
        "actions": [
            {"type": "SET_FIELD", "field": "ipv4_src", "value": "10.0.0.1"},
            {"type": "SET_FIELD", "field": "eth_src", "value": "00:00:00:00:00:01"},
            {"type": "OUTPUT", "port": 2}  
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Modification des trames de réponse ajoutée avec succès.")
    else:
        print(f"Erreur lors de la modification des trames : {response.status_code}")

def get_sdn_flows():
    # Affiche les règles dans le switch du data center afin de voir que tout a bien été ajouté
    url = "http://localhost:8080/stats/flow/1001"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            flows = response.json()
            print("Règles SDN actuelles :")
            print(json.dumps(flows, indent=2))
        except ValueError:
            print("Erreur : la réponse n'est pas au format JSON.")
    else:
        print(f"Erreur lors de la récupération des flux SDN : {response.status_code}")

def main(dscp):
    mac_address = create_vnf_gi()
    if mac_address:
        modify_request_vnf_to_new_gi(dscp, mac_address)
        modify_request_new_gi_to_vnf()
        get_sdn_flows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de gestion des VNFs avec des règles SDN.")
    parser.add_argument("dscp", type=int, help="Valeur DSCP pour les règles SDN.")
    args = parser.parse_args()
    main(args.dscp)
