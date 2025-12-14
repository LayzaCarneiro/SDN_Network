from mininet.topo import Topo

CITIES = {
    1: "Seattle",
    2: "Chicago",
    3: "NewYork",
    4: "LosAngeles",
    5: "Denver",
    6: "WashingtonDC",
    7: "Sunnyvale",
    8: "Houston",
    9: "Atlanta"
}

class Internet2Topo(Topo):
    def build(self):

        # Criando switches
        switches = {}
        for i in range(1, 10):
            switches[i] = self.addSwitch(f's{i}-{CITIES[i]}')

        # Criando hosts (1 por switch)
        for i in range(1, 10):
            host = self.addHost(f'h{i}-{CITIES[i]}')
            self.addLink(host, switches[i])

        # Links entre switches (topologia Internet2)
        self.addLink(switches[1], switches[2])
        self.addLink(switches[2], switches[3])

        self.addLink(switches[1], switches[4])
        self.addLink(switches[2], switches[5])
        self.addLink(switches[3], switches[6])

        self.addLink(switches[4], switches[5])
        self.addLink(switches[5], switches[6])

        self.addLink(switches[4], switches[7])
        self.addLink(switches[6], switches[9])

        self.addLink(switches[7], switches[8])
        self.addLink(switches[8], switches[9])