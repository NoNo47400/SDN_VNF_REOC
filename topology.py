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
    switch_app = net.addSwitch('s1')
    switch_srv = net.addSwitch('s2')
    switch_gi = net.addSwitch('s3')  #### REVOIR REGLE SDN CAR PAS LE MEME NUMERO DE SWITCH
    switch_gf = net.addSwitch('s4')
    switch_gf1_dev = net.addSwitch('s5')
    switch_gf2_dev = net.addSwitch('s6')
    switch_gf3_dev = net.addSwitch('s7')


    # Ajout des conteneurs Docker pour les gateways et le datacenter
    app1 = net.addDocker('app1', ip='10.0.0.101/24', dimage='app1-image', mac='10:00:00:00:00:00', dcmd='node application.js --remote_ip "10.0.0.100" --remote_port 8080 --device_name "app1" --send_period 5000')
    app2 = net.addDocker('app2', ip='10.0.0.102/24', dimage='app2-image', mac='20:00:00:00:00:00', dcmd='node application.js --remote_ip "10.0.0.100" --remote_port 8080 --device_name "app2" --send_period 5000')
    app3 = net.addDocker('app3', ip='10.0.0.103/24', dimage='app3-image', mac='30:00:00:00:00:00', dcmd='node application.js --remote_ip "10.0.0.100" --remote_port 8080 --device_name "app3" --send_period 5000')

    server = net.addDocker('service', ip='10.0.0.100/24', dimage='server-image', mac='01:00:00:00:00:00', dcmd='node server.js --local_ip "0.0.0.0" --local_port 8080 --local_name "srv"')

    gatewayIntermediaire = net.addDocker('gI', ip='10.0.0.1/24', dimage='gateway_intermediaire-image', mac='00:00:00:00:00:01', dcmd='node gateway.js --local_ip "0.0.0.0" --local_port 8181 --local_name "gwi" --remote_ip "10.0.0.100" --remote_port 8080 --remote_name "srv"')
    
    # PLUTOT METTRE ADRESSE A CHAQUE LIEN QUE CHAQUE MACHINE
    # il manque le serveur aussi
    gatewayFinal1 = net.addDocker('gF1', ip='10.0.0.10/24', dimage='gateway_final1-image', mac='00:00:00:00:10:00', dcmd='node gateway.js --local_ip "0.0.0.0" --local_port 8282 --local_name "gwf1" --remote_ip "10.0.0.1" --remote_port 8181 --remote_name "gwi"')
    dev1_gF1 = net.addDocker('dev1_gF1', ip='10.0.0.11/24', dimage='dev1_gf1-image', mac='00:00:00:00:11:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device1_gf1" --remote_ip "10.0.0.10" --remote_port 8282 --remote_name "gwf1" --send_period 3000')
    dev2_gF1 = net.addDocker('dev2_gF1', ip='10.0.0.12/24', dimage='dev2_gf1-image', mac='00:00:00:00:12:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device2_gf1" --remote_ip "10.0.0.10" --remote_port 8282 --remote_name "gwf1" --send_period 3000')
    dev3_gF1 = net.addDocker('dev3_gF1', ip='10.0.0.13/24', dimage='dev3_gf1-image', mac='00:00:00:00:13:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device3_gf1" --remote_ip "10.0.0.10" --remote_port 8282 --remote_name "gwf1" --send_period 3000')

    gatewayFinal2 = net.addDocker('gF2', ip='10.0.0.20/24', dimage='gateway_final2-image', mac='00:00:00:00:20:00', dcmd='node gateway.js --local_ip "0.0.0.0" --local_port 8282 --local_name "gwf2" --remote_ip "10.0.0.1" --remote_port 8181 --remote_name "gwi"')
    dev1_gF2 = net.addDocker('dev1_gF2', ip='10.0.0.21/24', dimage='dev1_gf2-image', mac='00:00:00:00:21:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device1_gf2" --remote_ip "10.0.0.20" --remote_port 8282 --remote_name "gwf2" --send_period 3000')
    dev2_gF2 = net.addDocker('dev2_gF2', ip='10.0.0.22/24', dimage='dev2_gf2-image', mac='00:00:00:00:22:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device2_gf2" --remote_ip "10.0.0.20" --remote_port 8282 --remote_name "gwf2" --send_period 3000')
    dev3_gF2 = net.addDocker('dev3_gF2', ip='10.0.0.23/24', dimage='dev3_gf2-image', mac='00:00:00:00:23:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device3_gf2" --remote_ip "10.0.0.20" --remote_port 8282 --remote_name "gwf2" --send_period 3000')

    gatewayFinal3 = net.addDocker('gF3', ip='10.0.0.30/24', dimage='gateway_final3-image', mac='00:00:00:00:30:00', dcmd='node gateway.js --local_ip "0.0.0.0" --local_port 8282 --local_name "gwf3" --remote_ip "10.0.0.1" --remote_port 8181 --remote_name "gwi"')
    dev1_gF3 = net.addDocker('dev1_gF3', ip='10.0.0.31/24', dimage='dev1_gf3-image', mac='00:00:00:00:31:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device1_gf3" --remote_ip "10.0.0.30" --remote_port 8282 --remote_name "gwf3" --send_period 3000')
    dev2_gF3 = net.addDocker('dev2_gF3', ip='10.0.0.32/24', dimage='dev2_gf3-image', mac='00:00:00:00:32:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device2_gf3" --remote_ip "10.0.0.30" --remote_port 8282 --remote_name "gwf3" --send_period 3000')
    dev3_gF3 = net.addDocker('dev3_gF3', ip='10.0.0.33/24', dimage='dev3_gf3-image', mac='00:00:00:00:33:00', dcmd='node device.js --local_ip "0.0.0.0" --local_port 9001 --local_name "device3_gf3" --remote_ip "10.0.0.30" --remote_port 8282 --remote_name "gwf3" --send_period 3000')

    # Création des liens
    net.addLink(app1, switch_app)
    net.addLink(app2, switch_app)
    net.addLink(app3, switch_app)
    net.addLink(switch_app, switch_srv)
    net.addLink(switch_srv, server)
    net.addLink(switch_srv, switch_gi)
    net.addLink(switch_gi, gatewayIntermediaire)
    net.addLink(switch_gi, dc1)
    net.addLink(switch_gi, switch_gf)
    net.addLink(switch_gf, gatewayFinal1)
    net.addLink(switch_gf, gatewayFinal2)
    net.addLink(switch_gf, gatewayFinal3)
    net.addLink(switch_gf, switch_gf1_dev)
    net.addLink(switch_gf, switch_gf2_dev)
    net.addLink(switch_gf, switch_gf3_dev)
    net.addLink(switch_gf1_dev, gatewayFinal1)
    net.addLink(switch_gf1_dev, dev1_gF1)
    net.addLink(switch_gf1_dev, dev2_gF1)
    net.addLink(switch_gf1_dev, dev3_gF1)
    net.addLink(switch_gf2_dev, gatewayFinal2)
    net.addLink(switch_gf2_dev, dev1_gF2)
    net.addLink(switch_gf2_dev, dev2_gF2)
    net.addLink(switch_gf2_dev, dev3_gF2)
    net.addLink(switch_gf3_dev, gatewayFinal3)
    net.addLink(switch_gf3_dev, dev1_gF3)
    net.addLink(switch_gf3_dev, dev2_gF3)
    net.addLink(switch_gf3_dev, dev3_gF3)

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
