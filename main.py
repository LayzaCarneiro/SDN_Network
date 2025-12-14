from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

from internet2_topology import Internet2Topo

def main():
    setLogLevel('info')

    topo = Internet2Topo()

    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=None,   # sem controlador por enquanto
        autoSetMacs=True,
        autoStaticArp=True
    )

    net.start()

    print("\n*** Testando conectividade")
    net.pingAll()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()
