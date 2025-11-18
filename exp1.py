#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

# Router Configuration
class LinuxRouter( Node ):
    
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

# Network Topology class
class NetworkTopo( Topo ):

    def build( self, **_opts ):

        router1 = self.addNode( 'r1', cls=LinuxRouter, ip='10.0.1.1/24' )
        router2 = self.addNode( 'r2', cls=LinuxRouter, ip='10.0.1.2/24' )

        

        self.addLink( router1, router2, intfName1='r1-eth1',intfName2='r2-eth0',params1={ 'ip' : '10.0.1.1/24' },
                      params2={ 'ip' : '10.0.1.2/24' } )  

        h1 = self.addHost( 'h1', ip='10.0.0.1/24',defaultRoute='via 10.0.0.3' )
        h2 = self.addHost( 'h2', ip='10.0.3.2/24',defaultRoute='via 10.0.3.4' )
        h3 = self.addHost( 'h3', ip='10.0.2.2/24',defaultRoute='via 10.0.2.1' )

        self.addLink( h1, router1 ,intfName2='r1-eth0',params1={ 'ip' : '10.0.0.1/24' },
                      params2={ 'ip' : '10.0.0.3/24' } )

        self.addLink( h2, router1 ,intfName2='r1-eth2',params1={ 'ip' : '10.0.3.2/24' },
                      params2={ 'ip' : '10.0.3.4/24' } )  

        self.addLink( h3, router2 ,intfName2='r2-eth1',params1={ 'ip' : '10.0.2.2/24' },
                      params2={ 'ip' : '10.0.2.1/24' } )          



def run():
    # Initialising Network Topology Class object
    topo = NetworkTopo()
    net = Mininet( topo=topo,
                   waitConnected=True ) 
    
    #Starting the network
    net.start()


    # Routing Rules for routers
    net['r1'].cmd('ip route replace 10.0.2.0/24 via 10.0.1.2')
    net['r2'].cmd('ip route replace 10.0.0.0/24 via 10.0.1.1')
    net['r2'].cmd('ip route replace 10.0.3.0/24 via 10.0.1.1')

    
    with open('result1.txt', 'w') as f:
    
        # pings tests for outputs
        tests = [
            ('h1 -> h3 ', net['h1'], 'ping -c 1 10.0.2.2'),
            ('h2 -> h3 ', net['h2'], 'ping -c 1 10.0.2.2'),
            ('h3 -> h1 ', net['h3'], 'ping -c 1 10.0.0.1'),
            ('h3 -> h2 ', net['h3'], 'ping -c 1 10.0.3.2'),
        ]

        # parsing the tests and writing output to results1.txt
        for label, host, cmd in tests:
            f.write('\n=== ' + label + ' ===\n')
            f.write(host.cmd(cmd))

    # network stop
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
