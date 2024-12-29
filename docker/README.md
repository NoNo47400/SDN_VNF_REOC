# Fichiers Docker

Ce dossier contient un ensemble de 7 fichiers Docker, chacun destiné à des composants spécifiques. Voici une description détaillée de chaque fichier et de son rôle :

## 1. **Application**
- **Objectif** : Télécharger toutes les dépendances nécessaires pour exécuter le fichier `application.js`.
- **Commande de lancement** : Spécifiée dans le fichier `topologie.py`.

## 2. **Device**
- **Objectif** : Télécharger toutes les dépendances nécessaires pour exécuter le fichier `device.js`.
- **Commande de lancement** : Spécifiée dans le fichier `topologie.py`.

## 3. **Server**
- **Objectif** : Télécharger toutes les dépendances nécessaires pour exécuter le fichier `server.js`.
- **Commande de lancement** : Spécifiée dans le fichier `topologie.py`.

## 4. **Gateway intermédiaire**
- **Objectif** : Télécharger toutes les dépendances nécessaires pour exécuter le fichier `gateway.js`.
- **Commande de lancement** : Spécifiée dans le fichier `topologie.py`.

## 5. **Gateway finale**
- **Objectif** : Similaire à la gateway intermédiaire, mais avec un port exposé différent.
- **Commande de lancement** : Spécifiée dans le fichier `topologie.py`.

## 6. **Gateway intermédiaire VNF**
- **Objectif** : Télécharger toutes les dépendances pour exécuter le fichier `gateway.js`.
- **Particularité** : La commande d'exécution est directement définie dans le `Dockerfile`.  
  Ce choix s'explique par le fait que ce conteneur est démarré via une API REST qui ne permet pas de définir les paramètres comme dans `topologie.py`.

## 7. **VNF Monitoring**
- **Objectif** : Télécharger toutes les dépendances pour exécuter le fichier Python `vnf_monitoring.py`.
- **Langage** : Contrairement aux autres composants, celui-ci est écrit en Python.
- **Fonction principale** :
  - Simuler le comportement d'une gateway intermédiaire.
  - Transiter de manière transparente les messages en provenance des gateways finales.
  - Ajouter un paramètre **TOS** à ces messages.  
    Ce paramètre **TOS**, combiné avec une règle SDN, permet d'identifier la provenance originale des messages.

## Créer les images dockers

Pour créer les images dockers il suffit de lancer le fichier `create_dockers.py` via la commande suivante:   
```bash
sudo python3 create_dockers.py
```