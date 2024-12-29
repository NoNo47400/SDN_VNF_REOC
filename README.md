# Projet cobinant SDN et VNF

Le but était d'implémenter un réseau virtuel et de le monitorer et agir sur celui-ci même après son déploiement via des outils comme [VIM-EMU](https://github.com/containernet/vim-emu/wiki/APIs) pour l'émulation de fonctions réseau et [RYU](https://ryu.readthedocs.io/en/latest/app/ofctl_rest.html) comme contrôleur SDN.     

Vous pourrez retrouver la toplogie dans le fichier `toplogie.py`. Celle-ci simule une application IoT avec trois zones avec chacunes trois devices. Trois applications on accès aux données de ces devices en passant par un service.

## Comment lancer la topologie

Pour démarrer la topologie, lancez simplement:
```bash
sudo python3 topology.py
```

Il est conseillé de créer les images dockers (voir docker/README.md) avant de lancer la topologie.

## Structure du projet


├── docker/                      # Dossier qui contient tous les dockerfile                       
│   ├── application.Dockerfile                 
│   ├── application.js                                   
│   ├── create_docker.py                              
│   ├── device.Dockerfile                         
│   ├── device.js                       
│   ├── gateway_final.Dockerfile                        
│   ├── gateway_intermediaire_vnf.Dockerfile                     
│   ├── gateway_intermediaire.Dockerfile                    
│   ├── gateway.js                         
│   ├── README.md                          
│   ├── server.Dockerfile                        
│   ├── server.js                     
│   ├── vnf_monitoring.Dockerfile                            
│   ├── vnf_monitoring.py                              
├── sdn/                         # Dossier qui contient les launchers des vnfs                        
│   ├── launch_vnf_gi.py                          
│   ├── launch_vnf_monitoring.py                          
├── README.md                       
└── topology.py                  # Toplogie de l'infrastructure réseau simlulé                     