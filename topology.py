import logging                                                              
from mininet.log import setLogLevel                                         
from emuvim.dcemulator.net import DCNetwork                                 
from emuvim.api.rest.rest_api_endpoint import RestApiEndpoint               
from emuvim.api.openstack.openstack_api_endpoint import OpenstackApiEndpoint

logging.basicConfig(level=logging.INFO)
setLogLevel('info')  # set Mininet loglevel
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.base').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.compute').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.keystone').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.nova').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.neutron').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.heat.parser').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.glance').setLevel(logging.DEBUG)
logging.getLogger('api.openstack.helper').setLevel(logging.DEBUG)

def create_topology():
    # Création du réseau avec Containernet
    net = DCNetwork(monitor=False, enable_learning=True)

    dc1 = net.addDatacenter("dc1")
    # add OpenStack-like APIs to the emulated DC
    api1 = OpenstackApiEndpoint("0.0.0.0", 6001)
    api1.connect_datacenter(dc1)
    api1.start()
    api1.connect_dc_network(net)
    # add the command line interface endpoint to the emulated DC (REST API)
    rapi1 = RestApiEndpoint("0.0.0.0", 5001)
    rapi1.connectDCNetwork(net)
    rapi1.connectDatacenter(dc1)
    rapi1.start()

    # On va communiquer avec le VIM via l'API REST pour faire nos demandes de créations de container tout ça
    # On va aussi communiquer avec le SDN controller qui est automatiquement créé par mininet il faut trouver comment lui parler
    # Notre script tournera à l'exterieur comme le VIM et le SDN afin de faire nos requetes
    # Le datacenter c'est pour que le vim puisse créer des VNF et les gérer

    # Ajout des switches SDN
    switch1 = net.addSwitch('s1')
    switch2 = net.addSwitch('s2')
    switch3 = net.addSwitch('s3')

    # Ajout des conteneurs Docker pour les gateways et le datacenter
    gatewayIntermediaire = net.addDocker('gI', ip='10.0.0.1/24', dimage='gateway_intermediaire-image')
    
    app1 = net.addDocker('app1', ip='10.0.0.101/24', dimage='app1-image')
    app2 = net.addDocker('app2', ip='10.0.0.102/24', dimage='app2-image')
    app3 = net.addDocker('app3', ip='10.0.0.103/24', dimage='app3-image')

    server = net.addDocker('service', ip='10.0.0.100/24', dimage='server-image')
    
    # PLUTOT METTRE ADRESSE A CHAQUE LIEN QUE CHAQUE MACHINE
    # il manque le serveur aussi
    gatewayFinal1 = net.addDocker('gF1', ip='10.0.0.10/24', dimage='gateway_final1-image')
    dev1_gF1 = net.addDocker('dev1_gF1', ip='10.0.0.11/24', dimage='dev1_gf1-image')
    dev2_gF1 = net.addDocker('dev2_gF1', ip='10.0.0.12/24', dimage='dev2_gf1-image')
    dev3_gF1 = net.addDocker('dev3_gF1', ip='10.0.0.13/24', dimage='dev3_gf1-image')

    gatewayFinal2 = net.addDocker('gF2', ip='10.0.0.20/24', dimage='gateway_final2-image')
    dev1_gF2 = net.addDocker('dev1_gF2', ip='10.0.0.21/24', dimage='dev1_gf2-image')
    dev2_gF2 = net.addDocker('dev2_gF2', ip='10.0.0.22/24', dimage='dev2_gf2-image')
    dev3_gF2 = net.addDocker('dev3_gF2', ip='10.0.0.23/24', dimage='dev3_gf2-image')

    gatewayFinal3 = net.addDocker('gF3', ip='10.0.0.30/24', dimage='gateway_finale3-image')
    dev1_gF3 = net.addDocker('dev1_gF3', ip='10.0.0.31/24', dimage='dev1_gf3-image')
    dev2_gF3 = net.addDocker('dev2_gF3', ip='10.0.0.32/24', dimage='dev2_gf3-image')
    dev3_gF3 = net.addDocker('dev3_gF3', ip='10.0.0.33/24', dimage='dev3_gf3-image')

    # Création des liens
    net.addLink(app1, server)
    net.addLink(app2, server)
    net.addLink(app3, server)
    net.addLink(server, switch1)
    net.addLink(switch1, switch2)
    net.addLink(switch2, gatewayIntermediaire)
    net.addLink(switch2, dc1)
    net.addLink(switch2, switch3)
    net.addLink(switch3, gatewayFinal1)
    net.addLink(switch3, gatewayFinal2)
    net.addLink(switch3, gatewayFinal3)
    net.addLink(gatewayFinal1, dev1_gF1)
    net.addLink(gatewayFinal1, dev2_gF1)
    net.addLink(gatewayFinal1, dev3_gF1)
    net.addLink(gatewayFinal2, dev1_gF2)
    net.addLink(gatewayFinal2, dev2_gF2)
    net.addLink(gatewayFinal2, dev3_gF2)
    net.addLink(gatewayFinal3, dev1_gF3)
    net.addLink(gatewayFinal3, dev2_gF3)
    net.addLink(gatewayFinal3, dev3_gF3)

    # Modification des adresses IP si besoin
    #gatewayFinal1.cmd('ifconfig dev1-eth0 10.0.0.1/24 up')

    # Démarrage du réseau
    net.start()

    # Configuration des routes (si nécessaire)
    # Exemple: gatewayIntermediaire.cmd('route add default gw 10.0.0.1')

    # Lancement du CLI pour interagir avec le réseau
    net.CLI()

    # Arrêt du réseau
    net.stop()

def main():
    create_topology()

if __name__ == '__main__':
    main()
