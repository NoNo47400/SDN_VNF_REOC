import requests
import json

def create_vnf_gi():
    """Crée un VNF de monitoring et retourne son adresse MAC."""
    url = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_gI"
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


def modify_request_vnf_to_new_gi(tos, ip, mac, mac_dst):
    """Ajoute une règle sur S2 pour rediriger les trames les trames de réponse du VNF originaire du port eth4 vers les gf sur le port eth3."""
    url = "http://localhost:8080/stats/flowentry/add"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3e9,
        "priority": 1111, 
        "match": {
            "in_port": 2,
                "nw_src": "10.0.0.200", 
                "nw_dst": "10.0.0.1",
                "ip_dscp": tos, # tos = dscp<<2
                "dl_type": 2048                
            },
        "actions": [
            {"type": "SET_FIELD", "field": "ipv4_src", "value": ip},
            {"type": "SET_FIELD", "field": "eth_src", "value": mac},
            {"type": "SET_FIELD", "field": "ipv4_dst", "value": "10.0.0.2"},
            {"type": "SET_FIELD", "field": "eth_dst", "value": mac_dst},
            {"type": "OUTPUT", "port": 3}  # ça marche pas ça me saoule, juste parce que les deux vnfs sont sur le meme port
            #{"type": "OUTPUT", "port": 4}  # j'ai donc essayé d'envoyer sur un port différent en espérant que le messag me revienne mais non
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("Modification des trames de réponse ajoutée avec succès.")
    else:
        print(f"Erreur lors de la modification des trames : {response.status_code}")

def delete_request_vnf_to_gi(tos, ip):
    """Supprime la règle sur S2 pour rediriger les trames de réponse du VNF originaire du port eth4 vers les GF sur le port eth3."""
    url = "http://localhost:8080/stats/flowentry/delete"
    headers = {'Content-Type': 'application/json'}
    data = {
        "dpid": 3,  # Identifiant du switch cible
        "priority": 1111,  # La priorité doit être la même que celle utilisée dans add_request_vnf_to_new_gi
        "match": {
            "nw_src": "10.0.0.200",  # Adresse source du VNF (à adapter si nécessaire)
            "nw_dst": ip,  # Adresse de destination du trafic
            "ip_dscp": tos,  # DSCP utilisé, ici c’est tos = dscp<<2
            "dl_type": 2048  # Type de trame Ethernet (IPv4)
        }
    }
    
    # Effectuer la requête DELETE pour supprimer la règle
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("Règle supprimée avec succès.")
    else:
        print(f"Erreur lors de la suppression de la règle : {response.status_code}")

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
        modify_request_vnf_to_new_gi(1, "10.0.0.10", "00:00:00:00:10:00", mac_address)
        get_sdn_flows()


if __name__ == "__main__":
    main()