import requests
import json

def create_vnf_gi():
    """Crée un VNF de monitoring et retourne son adresse MAC."""
    url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_gi"
    headers = {'Content-Type': 'application/json'}
    data = {
        "image": "gateway_intermediaire_vnf-image",
        "network": "(id=input,ip=10.0.0.2/24)"
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


def modify_request_vnf_to_new_gi(ip_dst, nw_ip_src, nw_mac_src, mac_dst):
    """Ajoute une règle sur S2 pour rediriger les trames les trames de réponse du VNF originaire du port eth4 vers les gf sur le port eth3."""
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,
        "priority": 1111,  # Plus prioritaire que celle créé avec le vnf de monitoring pour l'écraser (pas besoin de la supprimer)
        "match": {
            "in_port": 3,
                "nw_dst": ip_dst,  
                "dl_type": 2048
            },
        "actions": [
            {"type": "SET_FIELD", "field": "ipv4_src", "value": nw_ip_src},
            {"type": "SET_FIELD", "field": "eth_src", "value": nw_mac_src},
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
    mac_address = create_vnf_gi()
    if mac_address:
        modify_request_vnf_to_new_gi("10.0.0.251", "10.0.0.10", "00:00:00:00:10:00", mac_address)
        get_sdn_flows()

if __name__ == "__main__":
    main()