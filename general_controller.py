import requests

# TOUT FAUX
# Voir ça https://github.com/containernet/vim-emu/wiki/APIs

# A faire
VIM = "http://<VIM_IP>:<VIM_PORT>"
SDN_CONTROLLER = "http://<SDN_CONTROLLER_IP>:<SDN_CONTROLLER_PORT>"
VNF_MONITORING = "http://<VNF_MONITORING_IP>:<VNF_MONITORING_PORT>"

# Fonction pour créer un VNF
def create_vnf(vnf_type):
    response = requests.post(f"{VIM}/vnf/create", json={"type": vnf_type})
    return response.json()

# Fonction pour rediriger le trafic
def redirect_traffic(source, destination, source_ip=None):
    data = {"source": source, "destination": destination}
    if source_ip:
        data["source_ip"] = source_ip
    response = requests.post(f"{SDN_CONTROLLER}/traffic/redirect", json=data)
    return response.json()

# Fonction pour obtenir les données de trafic du VNF Monitoring
def get_traffic_data():
    response = requests.get(f"{VNF_MONITORING}/traffic/data")
    return response.json()

# Créer un VNF pour le monitoring
vnf_monitoring = create_vnf("monitoring")
print(f"Created VNF Monitoring: {vnf_monitoring}")

# Rediriger le trafic vers le VNF Monitoring
redirect_traffic("Gateway_Intermediaire", vnf_monitoring["id"])
print("Traffic redirected to VNF Monitoring")

# Rediriger le trafic du VNF Monitoring vers la Gateway Intermédiaire
redirect_traffic(vnf_monitoring["id"], "Gateway_Intermediaire")
print("Traffic redirected from VNF Monitoring to Gateway Intermediaire")

# Obtenir les données de trafic du VNF Monitoring
traffic_data = get_traffic_data()
print(f"Traffic data: {traffic_data}")

# Créer un VNF pour la Gateway Intermédiaire 2
vnf_gateway = create_vnf("gateway")
print(f"Created VNF Gateway Intermediaire 2: {vnf_gateway}")

# Trouver la source avec le trafic le plus élevé
max_source = max(traffic_data, key=lambda x: x['traffic'])
print(f"Source with highest traffic: {max_source}")

# Rediriger le trafic de la Gateway Intermédiaire vers la Gateway Intermédiaire 2 pour la source avec le trafic le plus élevé
redirect_traffic("Gateway_Intermediaire", vnf_gateway["id"], source_ip=max_source["source"])
print("Traffic redirected from Gateway Intermediaire to Gateway Intermediaire 2")

# Rediriger le trafic de la Gateway Intermédiaire 2 vers l'application
redirect_traffic(vnf_gateway["id"], "application")
print("Traffic redirected from Gateway Intermediaire 2 to application")