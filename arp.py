import subprocess

def get_mac_addresses(network):
    # Exécute la commande arp-scan pour scanner le réseau spécifié
    command = f"sudo arp-scan --interface=eth0 {network}"
    
    # Exécution du processus et capture de la sortie
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Vérifie si la commande a réussi
    if result.returncode == 0:
        # Filtre les adresses MAC et retourne les résultats
        mac_addresses = []
        for line in result.stdout.splitlines():
            # Vérifie si l'interface eth0 est présente dans la ligne et extrait l'adresse MAC
            if "eth0" in line:
                columns = line.split()
                if len(columns) > 1:  # Assure qu'il y a assez de colonnes pour récupérer l'adresse MAC
                    mac_addresses.append(columns[1])  # Adresse MAC est dans la 2e colonne
        return mac_addresses
    else:
        print("Erreur lors du scan du réseau.")
        return []

# Réseau à scanner
network = "10.0.0.0/24"
mac_addresses = get_mac_addresses(network)

# Affiche les adresses MAC récupérées
if mac_addresses:
    print("Adresses MAC trouvées sur le réseau :")
    for mac in mac_addresses:
        print(mac)
else:
    print("Aucune adresse MAC trouvée.")