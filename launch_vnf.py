import requests
import json

def create_vnf_monitoring():
    """Crée un VNF de monitoring et retourne son adresse MAC."""
    url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitoring"
    headers = {'Content-Type': 'application/json'}
    data = {
        "image": "vnf_monitoring-image",
        "network": "(id=input,ip=10.0.0.200/24)"
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
    """Ajoute une règle sur S2 pour rediriger les trames originaire du port eth4 vers le VNF de monitoring sur le port eth3."""
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,
        "priority": 1111,
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


def add_request_vnf_to_gi(tos, ip, mac):
    """Ajoute une règle sur S2 pour rediriger les trames les trames de réponse du VNF originaire du port eth4 vers les gf sur le port eth3."""
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,
        "priority": 1111,
        "match": {
            "in_port": 3,
                "nw_src": "10.0.0.200", 
                "nw_dst": "10.0.0.1",
                "ip_dscp": tos, # tos = dscp<<2
                "dl_type": 2048                
            },
        "actions": [
            {"type": "SET_FIELD", "field": "ipv4_src", "value": ip},
            {"type": "SET_FIELD", "field": "eth_src", "value": mac},
            {"type": "OUTPUT", "port": 2}
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Modification des trames de réponse ajoutée avec succès.")
    else:
        print(f"Erreur lors de la modification des trames : {response.status_code}")

def get_sdn_flows():
    """Récupère et affiche les règles SDN associées au DPID 3."""
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

# Programme principal
def main():
    mac_address = create_vnf_monitoring()
    if mac_address:
        redirect_frames_gf_to_vnf(mac_address)
        # Envoyé vers une adresse random pour savoir d'où vient de base le paquet
        add_request_vnf_to_gi(1, "10.0.0.10", "00:00:00:00:10:00")
        add_request_vnf_to_gi(2, "10.0.0.20", "00:00:00:00:20:00")
        add_request_vnf_to_gi(4, "10.0.0.30", "00:00:00:00:30:00")
        get_sdn_flows()

if __name__ == "__main__":
    main()