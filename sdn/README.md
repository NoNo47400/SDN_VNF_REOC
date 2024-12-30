# Fichiers SDN

Ce dossier contient un ensemble de 2 fichiers Python. Chacun a pour objectif de démarrer une VNF et de rediriger le trafic réseau en fonction. Voici une description détaillée de chaque fichier et de son rôle :

## 1. **VNF Monitoring**
- **Objectif** : 
  - Créer et démarrer la VNF de monitoring.
  - Rediriger les trames à destination de la gateway intermédiaire vers cette VNF.  
  - **Utilité** : Permet de calculer le bitrate pour chaque gateway finale.

## 2. **VNF Gateway Intermédiaire**
- **Objectif** : 
  - Créer et démarrer la VNF pour la gateway intermédiaire.
  - Rediriger les trames en provenance de la gateway finale 1, initialement à destination de la gateway intermédiaire, vers cette nouvelle VNF.  
  - **Utilité** : Réduit la charge de la gateway intermédiaire finale, qui n’aura plus à traiter les demandes provenant de la gateway finale 1.

## Comment lancer les vnfs

Il est crucial de démarrer les VNF dans cet ordre spécifique afin de garantir que le VNF de monitoring soit associé à l’interface eth1 du switch du datacenter, et que la gateway intermédiaire soit reliée à eth2. Cet ordre a une importance majeure pour la configuration correcte des règles SDN.

Pour lancer la vnf de monitoring, lancez simplement:
```bash
sudo python3 launch_vnf_monitoring.py
```

Pour lancer la gateway intermediaire vnf, lancez simplement la commande suivante en précisant le dscp (le dscp est égal au numéro de la zone ex: zone1: dscp=1):
```bash
sudo python3 launch_vnf_gi.py <dscp> 
```

Il est conseillé de lancer la topologie avant de lancer les vnfs (voir ../README.md)