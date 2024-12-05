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
    gatewayIntermediaire = net.addDocker('gI', dimage='gateway_intermediaire_image')
    
    app = net.addDocker('app', dimage='app_web_image')
    
    gatewayFinal1 = net.addDocker('gF1', dimage='gateway_final1_image')
    dev1_gF1 = net.addDocker('dev1_gF1', dimage='dev1_gF1_image')
    dev2_gF1 = net.addDocker('dev2_gF1', dimage='dev2_gF1_image')
    dev3_gF1 = net.addDocker('dev3_gF1', dimage='dev3_gF1_image')
    
    gatewayFinal2 = net.addDocker('gF2', dimage='gateway_final2_image')
    dev1_gF2 = net.addDocker('dev1_gF2', dimage='dev1_gF2_image')
    dev2_gF2 = net.addDocker('dev2_gF2', dimage='dev2_gF2_image')
    dev3_gF2 = net.addDocker('dev3_gF2', dimage='dev3_gF2_image')

    gatewayFinal3 = net.addDocker('gF3', dimage='gateway_final3_image')
    dev1_gF3 = net.addDocker('dev1_gF3', dimage='dev1_gF3_image')
    dev2_gF3 = net.addDocker('dev2_gF3', dimage='dev2_gF3_image')
    dev3_gF3 = net.addDocker('dev3_gF3', dimage='dev3_gF3_image')

    # Création des liens
    net.addLink(app, switch1)
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
