# Fichiers GUI

Ce dossier contient les trois fichiers nécessaires pour faire tourner l'interface graphique.              

L'interface permet de récupérer les logs de certains dockers ainsi que le bitrate calculé par la vnf de monitoring.       
De plus, il est aussi possible de lancer la vnf de monitoring ainsi que la vnf gateway intermediaire en précisant la zone que l'on souhaite rediriger.       

## Démarrer l'application

Pensez à bien démarrer la topologie avant.      

Pour démarrer l'application il suffit de lancer la commande suivante et de vous taper dans une page web en dehors de la machine virtuelle http://localhost:1234/:     
```bash
python3 app.py
```