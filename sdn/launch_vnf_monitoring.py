import requests
import json

def create_vnf_monitoring():
    # On créé le vnf de monitoring et on récupère son adresse mac
    url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitoring"
    headers = {'Content-Type': 'application/json'}
    data = {
        "image": "vnf_monitoring-image",
        "network": "(id=monitoring,ip=10.0.0.200/24)"
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

def redirect_frames_gf_to_vnf(mac_address):
    # On ajoute une règle dans le switch S3 pour rediriger toutes les requetes en direction de la gateway intermediaire vers la vnf de monitoring 
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,
        "priority": 11111,
        "match": {
            "in_port": 4,
                "nw_dst": "10.0.0.1", 
                "dl_type": 2048
            },
        "actions": [         
            {"type": "SET_FIELD", "field": "ipv4_dst", "value": "10.0.0.200"},
            {"type": "SET_FIELD", "field": "eth_dst", "value": mac_address},
            {"type": "OUTPUT", "port": 3}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Déviation des trames ajoutée avec succès.")
    else:
        print(f"Erreur lors de la déviation des trames : {response.status_code}")

def redirect_frames_vnf_to_gf(ip_addr):
    # On ajoute une règle dans le switch S3 pour modifier l'adresse source de la réponse et être invisible aux yeux des gateways finales
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,
        "priority": 11111,
        "match": {
            "in_port": 3,
                "nw_dst": ip_addr, 
                "dl_type": 2048
            },
        "actions": [         
            {"type": "SET_FIELD", "field": "ipv4_src", "value": "10.0.0.1"},
            {"type": "SET_FIELD", "field": "eth_src", "value": "00:00:00:00:00:01"},
            {"type": "OUTPUT", "port": 4}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Déviation des trames ajoutée avec succès.")
    else:
        print(f"Erreur lors de la déviation des trames : {response.status_code}")

def get_sdn_flows():
    # Affiche les règles dans le switch S3 afin de voir que tout a bien été ajouté
    url = "http://localhost:8080/stats/flow/3"
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

def main():
    mac_address = create_vnf_monitoring()
    if mac_address:
        redirect_frames_gf_to_vnf(mac_address)
        redirect_frames_vnf_to_gf("10.0.0.10")
        redirect_frames_vnf_to_gf("10.0.0.20")
        redirect_frames_vnf_to_gf("10.0.0.30")
        get_sdn_flows()

if __name__ == "__main__":
    main()