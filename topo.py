#!/usr/bin/python

"""
Simplified Internet2 Topology Emulation using Canonical Names (sX, hX).

This script manually defines a custom topology mimicking the structure of the 
Internet2 research network backbone, using 6 numerical switches (s1-s6) as nodes. 
One host (h1-h6) is explicitly attached to every switch node.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSSwitch, RemoteController, OVSKernelSwitch
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
        # --- 1. Add Switches (Canonical s1 to s10) ---
        info( 'Adding 10 Canonical Switches (s1-s10)...\n' )
        
        # Central Hub (s1: CHI)
        s1 = self.addSwitch( 's1' ) 
        
        # East Coast (s2: NYC, s3: ATL)
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )

        # South/West (s4: DAL, s5: LAX, s6: SEA)
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )

        s7 = self.addSwitch( 's7' ) # DEN
        s8 = self.addSwitch( 's8' ) # MIA
        s9 = self.addSwitch( 's9' ) # SJO
        s10 = self.addSwitch( 's10' ) # WAS

        # --- 2. Add Hosts (One Host per Switch, h1 to h10) ---
        info( 'Adding 10 Hosts (h1-h10)...\n' )
        # Using hX for host names and sequential IPs (10.0.0.1 to 10.0.0.6)

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

        # --- 3. Add Links (Connections) ---

        # Hosts <-> Switches Connections (Access Links)
        info( 'Adding Host-Switch Access Links...\n' )
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

        # Switches <-> Switches Connections (Backbone Links - based on Internet2 structure)
        info( 'Adding Inter-Switch Backbone Links (Mesh-like)...\n' )
        
        # Central Hub (s1) connections
        self.addLink( s1, s2, delay='10ms', bw=1000 ) # CHI <-> NYC
        self.addLink( s2, s3, delay='5ms', bw=1000 ) # CHI <-> ATL
        self.addLink( s3, s4, delay='20ms', bw=1000 ) # CHI <-> DAL
        
        # West and South connections
        self.addLink( s4, s5, delay='15ms', bw=1000 ) # DAL <-> LAX
        self.addLink( s5, s6, delay='25ms', bw=1000 ) # LAX <-> SEA

        self.addLink( s6, s7, delay='10ms', bw=1000 ) # LAX <-> SEA
        self.addLink( s7, s8, delay='10ms', bw=1000 ) # LAX <-> SEA
        self.addLink( s8, s9, delay='10ms', bw=1000 ) # LAX <-> SEA
        self.addLink( s9, s10, delay='10ms', bw=1000 ) # LAX <-> SEA

        
def runInternet2Topo():
    """Creates the network and starts the Mininet CLI."""
    
    # Set the logging level
    setLogLevel( 'info' )

    # --- 1. Configurar o Controlador Remoto (C0) ---
    # Assumimos que o controlador está rodando em 127.0.0.1 (localhost) na porta 6653 (padrão OpenFlow)
    info( '*** Configurando Controlador Remoto (127.0.0.1:6653)...\n' )
    remote_controller = RemoteController( 
        'c0', 
        ip='127.0.0.1', 
        port=6653 
    )

    # Create the topology
    topo = Internet2Topo()

    # Initialize the network using the defined topology.
    # OVSSwitch works reliably with canonical names (sX).
    net = Mininet( topo=topo, 
                   switch=OVSKernelSwitch, 
                   controller=remote_controller,
                   link=TCLink
                     )

    # Start the network
    net.start()

    # Open the Command Line Interface (CLI) for interaction
    info( '*** Opening Mininet CLI. Type "exit" to quit.\n' )
    CLI( net )

    # Stop the network when the CLI is closed
    net.stop()

if __name__ == '__main__':
    # This ensures the runInternet2Topo() function is executed when the script is called
    runInternet2Topo()