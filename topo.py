#!/usr/bin/python

"""
Simplified Internet2 Topology Emulation using Canonical Names (sX, hX).

Note:
This topology is a simplified abstraction of the Internet2 backbone.
Exact geographical distances and node degrees were adapted to ensure
feasibility within the Mininet environment while preserving structural
and functional characteristics for SDN performance evaluation.

This script manually defines a custom topology mimicking the structure of the 
Internet2 research network backbone, using 10 numerical switches (s1-s10) as nodes. 
One host (h1-h10) is explicitly attached to every switch node.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink

class Internet2Topo( Topo ):
    """
    Simplified Internet2 Topology: 10 Numerical Switches (s1-s10) connected in a mesh-like structure.
    One host is manually attached to each switch.
    
    Conceptual Mapping (Expanded):
    s1: CHI (Chicago)    | s6: SEA (Seattle)
    s2: NYC (New York)   | s7: DEN (Denver)
    s3: ATL (Atlanta)    | s8: MIA (Miami)
    s4: DAL (Dallas)     | s9: SJO (San Jose)
    s5: LAX (Los Angeles)| s10: WAS (Washington, D.C.)
    """

    def build( self ):
        """
        Build the topology:
        1. Add switches
        2. Add hosts
        3. Connect hosts to switches
        4. Create backbone links with realistic delay and bandwidth
        """

        # ------------------------------------------------------------------
        # 1. Add Switches (canonical names are recommended by Mininet)
        # ------------------------------------------------------------------
        info('*** Adding switches (s1–s10)\n')
        
        s1 = self.addSwitch('s1')   # CHI
        s2 = self.addSwitch('s2')   # NYC
        s3 = self.addSwitch('s3')   # ATL
        s4 = self.addSwitch('s4')   # DAL
        s5 = self.addSwitch('s5')   # LAX
        s6 = self.addSwitch('s6')   # SEA
        s7 = self.addSwitch('s7')   # DEN
        s8 = self.addSwitch('s8')   # MIA
        s9 = self.addSwitch('s9')   # SJO
        s10 = self.addSwitch('s10') # WAS

        # ------------------------------------------------------------------
        # 2. Add Hosts (one host per switch)
        # ------------------------------------------------------------------
        info('*** Adding hosts (h1–h10)\n')

        h1 = self.addHost( 'h1', ip='10.0.0.1/24' )
        h2 = self.addHost( 'h2', ip='10.0.0.2/24' )
        h3 = self.addHost( 'h3', ip='10.0.0.3/24' )
        h4 = self.addHost( 'h4', ip='10.0.0.4/24' )
        h5 = self.addHost( 'h5', ip='10.0.0.5/24' )
        h6 = self.addHost( 'h6', ip='10.0.0.6/24' )
        h7 = self.addHost( 'h7', ip='10.0.0.7/24' )
        h8 = self.addHost( 'h8', ip='10.0.0.8/24' )
        h9 = self.addHost( 'h9', ip='10.0.0.9/24' )
        h10 = self.addHost( 'h10', ip='10.0.0.10/24' )

        # ------------------------------------------------------------------
        # 3. Host-to-Switch Access Links
        # ------------------------------------------------------------------
        info('*** Adding host-to-switch access links\n')

        self.addLink( h1, s1 )
        self.addLink( h2, s2 )
        self.addLink( h3, s3 )
        self.addLink( h4, s4 )
        self.addLink( h5, s5 )
        self.addLink( h6, s6 )
        self.addLink( h7, s7 )
        self.addLink( h8, s8 )
        self.addLink( h9, s9 )
        self.addLink( h10, s10 )

        # ------------------------------------------------------------------
        # 4. Switch-to-Switch Backbone Links
        # TCLink is used to emulate realistic WAN conditions
        # ------------------------------------------------------------------
        info('*** Adding inter-switch backbone links\n')
        
        # s1 acts as a logical central node, but the topology has side links
        self.addLink(s1, s2, delay='8ms',  bw=1000)   # CHI <-> NYC
        self.addLink(s2, s3, delay='6ms',  bw=1000)   # NYC <-> ATL
        self.addLink(s3, s4, delay='12ms', bw=1000)   # ATL <-> DAL
        self.addLink(s4, s5, delay='18ms', bw=1000)   # DAL <-> LAX
        self.addLink(s5, s6, delay='28ms', bw=1000)   # LAX <-> SEA
        self.addLink(s6, s7, delay='15ms', bw=1000)   # SEA <-> DEN
        self.addLink(s7, s8, delay='20ms', bw=1000)   # DEN <-> MIA
        self.addLink(s8, s9, delay='35ms', bw=1000)   # MIA <-> SJO
        self.addLink(s9, s10, delay='12ms', bw=1000)  # SJO <-> WAS

        
def runInternet2Topo():
    """
    Instantiate the topology, connect it to a remote SDN controller,
    and start the Mininet CLI.
    """

    # Set Mininet logging level
    setLogLevel('info')

    # --------------------------------------------------------------
    # Configure Remote SDN Controller
    # The controller is assumed to be running locally (Ryu)
    # Default OpenFlow port: 6653
    # --------------------------------------------------------------
    info('*** Configuring remote SDN controller (127.0.0.1:6653)\n')

    remote_controller = RemoteController(
        name='c0',
        ip='127.0.0.1',
        port=6653
    )

    # Create topology instance
    topo = Internet2Topo()

    # Initialize Mininet
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        controller=remote_controller,
        link=TCLink
    )

    # Start the network
    net.start()

    # Open Mininet CLI
    info('*** Starting Mininet CLI (type "exit" to stop the network)\n')
    CLI(net)

    # Stop the network after CLI exits
    net.stop()

if __name__ == '__main__':
    # Entry point of the script
    runInternet2Topo()