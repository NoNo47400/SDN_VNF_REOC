from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.node import Docker

def create_topology():
    # Création du réseau
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Ajout du contrôleur SDN (Ryu)
    controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Ajout des switches SDN
    switchA = net.addSwitch('sA')
    switchB = net.addSwitch('sB')
    switchC = net.addSwitch('sC')

    # Ajout des conteneurs Docker pour les gateways et le datacenter
    gatewayIntermediaire = net.addDocker('gI', dimage='gateway_intermediaire_image')
    gatewayFinal1 = net.addDocker('gF1', dimage='gateway_final1_image')
    gatewayFinal2 = net.addDocker('gF2', dimage='gateway_final2_image')
    gatewayFinal3 = net.addDocker('gF3', dimage='gateway_final3_image')
    datacenter = net.addDocker('dc', dimage='datacenter_image')

    # Création des liens
    net.addLink(switchA, switchB)
    net.addLink(switchB, gatewayIntermediaire)
    net.addLink(switchB, datacenter)
    net.addLink(switchB, switchC)
    net.addLink(switchC, gatewayFinal1)
    net.addLink(switchC, gatewayFinal2)
    net.addLink(switchC, gatewayFinal3)

    # Démarrage du réseau
    net.start()

    # Configuration des routes (si nécessaire)
    # Exemple: gatewayIntermediaire.cmd('route add default gw 10.0.0.1')

    # Lancement du CLI pour interagir avec le réseau
    net.interact()

    # Arrêt du réseau
    net.stop()

def main():
    create_topology()

if __name__ == '__main__':
    main()
