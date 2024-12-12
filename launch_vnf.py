import requests
import json

# Première requête - PUT
url_1 = "http://127.0.0.1:5001/restapi/compute/dc1/vnf_monitoring"
headers_1 = {'Content-Type': 'application/json'}
data_1 = {
    "image": "vnf_monitoring-image",
    "network": "(id=input,ip=10.0.0.200/24)"
}
response_1 = requests.put(url_1, headers=headers_1, data=json.dumps(data_1))

# Affichage du résultat de la première requête
if response_1.status_code == 200:
    try:
        response_json = response_1.json()
        mac_address = response_json['network'][0]['mac']
        print(f"Adresse MAC récupérée : {mac_address}")
    except KeyError:
        print("Erreur : l'adresse MAC n'a pas été trouvée dans la réponse.")
else:
    print(f"Erreur dans la première requête : {response_1.status_code}")

# Deuxième requête - POST
url_2 = "http://localhost:8080/stats/flowentry/add"
headers_2 = {'Content-Type': 'application/json'}
data_2 = {
    "dpid": 1,
    "priority": 11111,
    "match": {"nw_dst": "10.0.0.2", "dl_type": 2048},
    "actions": [{"type": "SET_FIELD", "field": "ipv4_dst", "value": "10.0.0.200"}, 
                {"type": "SET_FIELD", "field": "eth_dst", "value": "00:10:00:00:00:00"}
    ]
}
response_2 = requests.post(url_2, headers=headers_2, data=json.dumps(data_2))

# Vérification si la réponse est au format JSON avant de l'afficher
if response_2.status_code == 200:
    print("Deuxième requête réussie.")
    try:
        print(response_2.json())  # Affiche la réponse si elle est au format JSON
    except ValueError:
        print("La réponse de la deuxième requête n'est pas au format JSON.")
        print(response_2.text)  # Affiche le texte brut de la réponse
else:
    print(f"Erreur dans la deuxième requête : {response_2.status_code}")

# Vérification que la règle a bien été ajoutée avec une requête GET
url_get_flow = "http://localhost:8080/stats/flow/1"
response_get_flow = requests.get(url_get_flow)

if response_get_flow.status_code == 200:
    flow_data = response_get_flow.json()
    if flow_data:
        print("Règle ajoutée avec succès :")
        print(json.dumps(flow_data, indent=2))
    else:
        print("Aucune règle trouvée pour le dpid 1.")
else:
    print(f"Erreur lors de la récupération des flux : {response_get_flow.status_code}")

# Troisième requête - POST
data_3 = {
    "dpid": 1,
    "priority": 11111,
    "match": {"nw_src": "10.0.0.200", "nw_dst": "10.0.0.20", "dl_type": 2048},
    "actions": [{"type": "SET_FIELD", "field": "ipv4_src", "value": "10.0.0.1"},
                {"type": "SET_FIELD", "field": "eth_src", "value": "00:00:00:00:00:01"}
    ]
}
response_3 = requests.post(url_2, headers=headers_2, data=json.dumps(data_3))

# Vérification si la réponse est au format JSON avant de l'afficher
if response_3.status_code == 200:
    print("Troisième requête réussie.")
    try:
        print(response_3.json())  # Affiche la réponse si elle est au format JSON
    except ValueError:
        print("La réponse de la troisième requête n'est pas au format JSON.")
        print(response_3.text)  # Affiche le texte brut de la réponse
else:
    print(f"Erreur dans la troisième requête : {response_3.status_code}")

# Vérification que la deuxième règle a bien été ajoutée avec une requête GET
response_get_flow_2 = requests.get(url_get_flow)

if response_get_flow_2.status_code == 200:
    flow_data_2 = response_get_flow_2.json()
    if flow_data_2:
        print("Règles SDN ajoutée avec succès :")
        print(json.dumps(flow_data_2, indent=2))
    else:
        print("Aucune règle trouvée pour le dpid 1.")
else:
    print(f"Erreur lors de la récupération des flux : {response_get_flow_2.status_code}")
