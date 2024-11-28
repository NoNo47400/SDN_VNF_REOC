from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink

def create_topology():
    # Création du réseau
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    # Ajout du contrôleur SDN (Ryu)
    controller = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    # Ajout des switches SDN
    switchA = net.addSwitch('sA')
    switchB = net.addSwitch('sB')
    switchC = net.addSwitch('sC')

    # Ajout des gateways
    gatewayIntermediaire = net.addHost('gI', ip='10.0.0.1/24')
    gatewayFinal1 = net.addHost('gF1', ip='10.0.0.2/24')
    gatewayFinal2 = net.addHost('gF2', ip='10.0.0.3/24')
    gatewayFinal3 = net.addHost('gF3', ip='10.0.0.4/24')

    # Ajout du datacenter
    datacenter = net.addHost('dc', ip='10.0.0.5/24')

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
